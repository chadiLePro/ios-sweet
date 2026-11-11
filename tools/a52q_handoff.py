"""Evidence-bound read-only display/UFS handoff snapshots. No MMIO writes."""
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib
from fdt_evidence import Fdt, physical_regs

SOURCE_COMMIT = 'f6bbda4e5986f09e4d51ceffd1b645b2d5aa75b4'
SOURCE_HASHES = {
    'ufshci.h': '66927b6a3f6374c4c3c8c23ab1980316aeec651b1f16a880fe4df22b9483ab40',
    'sde_hw_ctl.c': '8c7a4069712c45123c86443758f1e5899de37a5a36811783cdcf2edf24fbc047',
    'sde_hw_sspp.c': 'd940eb6730b93b63e53fcaacf586e1747833ef904bb299817baed4d34e165ea2',
    'dsi_ctrl_reg.h': 'c39e23a300ee28f7f01d8d3d6f6c2d47555256d22d6f0f74366a0f9c2b732a48',
}


def layout(evidence, sources, group):
    if group not in ('display', 'ufs'):
        raise ValueError('unknown handoff group')
    raw = (evidence / 'live.dtb').read_bytes()
    tree = Fdt(raw)
    if 'a52q' not in ' '.join(tree.nodes['/'].strings('model')).lower():
        raise ValueError('not A52Q evidence')
    texts = {}
    for name, expected in SOURCE_HASHES.items():
        data = (sources / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('pinned register source mismatch: ' + name)
        texts[name] = data.decode()
    rows = []

    def node(compatible):
        nodes = [n for n in tree.nodes.values() if n.enabled() and compatible in n.strings('compatible')]
        if len(nodes) != 1:
            raise ValueError('need unique enabled ' + compatible)
        return nodes[0]

    def region(n, name):
        names, regs = n.strings('reg-names'), physical_regs(n)
        if len(names) != len(regs) or names.count(name) != 1:
            raise ValueError('ambiguous physical register region')
        return regs[names.index(name)]

    def offset(source, name):
        match = re.search(r'\b' + re.escape(name) + r'\s*(?:=\s*)?\(?\s*(0x[0-9a-fA-F]+)', texts[source])
        if not match:
            raise ValueError('register definition absent: ' + name)
        return int(match[1], 16)

    def add(label, span, off, definition):
        base, size = span
        if off < 0 or off % 4 or off + 4 > size or base % 4 or base + size > 0x80000000:
            raise ValueError('register outside evidenced peripheral range')
        rows.append({'label': label, 'address': base + off, 'definition': definition})

    if group == 'ufs':
        span = region(node('qcom,ufshc'), 'ufs_mem')
        for name in ('REG_CONTROLLER_CAPABILITIES', 'REG_UFS_VERSION',
                'REG_AUTO_HIBERNATE_IDLE_TIMER', 'REG_CONTROLLER_STATUS', 'REG_CONTROLLER_ENABLE',
                'REG_UTP_TRANSFER_REQ_LIST_BASE_L', 'REG_UTP_TRANSFER_REQ_LIST_BASE_H',
                'REG_UTP_TRANSFER_REQ_DOOR_BELL', 'REG_UTP_TRANSFER_REQ_LIST_RUN_STOP'):
            add('ufs.' + name.lower(), span, offset('ufshci.h', name), 'ufshci.h:' + name)
    else:
        mdp = node('qcom,sde-kms')
        span = region(mdp, 'mdp_phys')
        for kind, prop, source, names in (
                ('ctl', 'qcom,sde-ctl-off', 'sde_hw_ctl.c', ('CTL_TOP', 'CTL_START', 'CTL_INTF_ACTIVE')),
                ('sspp', 'qcom,sde-sspp-off', 'sde_hw_sspp.c',
                 ('SSPP_SRC_SIZE', 'SSPP_SRC0_ADDR', 'SSPP_SRC_YSTRIDE0',
                  'SSPP_SRC_FORMAT', 'SSPP_SRC_UNPACK_PATTERN', 'SSPP_SRC_OP_MODE'))):
            data = mdp.props.get(prop, b'')
            if not data or len(data) % 4 or len(data) > 32:
                raise ValueError('unsupported live display sub-block table')
            for i, sub in enumerate(struct.unpack('>' + 'I' * (len(data) // 4), data)):
                for name in names:
                    add(f'{kind}{i}.{name.lower()}', span, sub + offset(source, name), source + ':' + name)
        span = region(node('qcom,dsi-ctrl-hw-v2.4'), 'dsi_ctrl')
        for name in ('DSI_HW_VERSION', 'DSI_CTRL', 'DSI_STATUS', 'DSI_VERSION'):
            add('dsi.' + name.lower(), span, offset('dsi_ctrl_reg.h', name), 'dsi_ctrl_reg.h:' + name)
    if not 1 <= len(rows) <= 96 or len({r['address'] for r in rows}) != len(rows):
        raise ValueError('invalid or overlapping snapshot table')
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    return {'group': group, 'scope': 'read-only MMIO; no clock/reset/DMA/storage commands',
            'source_commit': SOURCE_COMMIT, 'source_sha256': SOURCE_HASHES,
            'live_dtb_sha256': hashlib.sha256(raw).hexdigest(), 'registers': rows,
            'tag': int(digest[:16], 16)}


def header(config):
    rows = config['registers']
    return (f'#define A52Q_HANDOFF_COUNT {len(rows)}U\n'
            f'#define A52Q_HANDOFF_TAG 0x{config["tag"]:016x}ULL\n'
            'static const uintptr_t handoff_addresses[A52Q_HANDOFF_COUNT] = {\n' +
            ''.join(f'    0x{r["address"]:x}ULL,\n' for r in rows) + '};\n')


def decode(data, config):
    pattern = (rb'A52QHANDOFF v1 copy=([0-2])\n'
               rb'((?:[a-z0-9_.]+=0x[0-9a-f]{16}\n)+)'
               rb'crc32=0x([0-9a-f]{16})\nA52QHANDOFF END\n')
    valid = []
    for m in re.finditer(pattern, data):
        if zlib.crc32(m[2]) != int(m[3], 16):
            continue
        pairs = [line.split(b'=') for line in m[2].splitlines()]
        fields = {k.decode(): int(v, 16) for k, v in pairs}
        n = fields.get('completed', 999)
        if n > len(config['registers']):
            continue
        expected = {'tag', 'count', 'completed', 'active'}
        expected |= {f'r{i:03d}.{s}' for i in range(n) for s in ('address', 'value')}
        if (len(pairs) != len(fields) or fields.keys() != expected or
                fields.get('tag') != config['tag'] or fields.get('count') != len(config['registers']) or
                n > len(config['registers'])):
            continue
        if any(fields[f'r{i:03d}.address'] != config['registers'][i]['address'] or
               fields[f'r{i:03d}.value'] > 0xffffffff for i in range(n)):
            continue
        valid.append((int(m[1]), m[2], fields))
    if not valid or len({v[0] for v in valid}) != len(valid) or len({v[1] for v in valid}) != 1:
        raise ValueError('no unambiguous CRC-valid handoff snapshot; do not trust values')
    fields = valid[0][2]
    return {'valid_copies': [v[0] for v in valid], 'group': config['group'],
            'complete': fields['completed'] == fields['count'],
            'active_index': fields['active'], 'registers': [
                dict(config['registers'][i], value=fields[f'r{i:03d}.value'])
                for i in range(fields['completed'])]}
