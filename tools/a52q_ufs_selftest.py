"""Bind the opt-in kernel UFS test to successful physical shim read evidence."""
import hashlib
import os
import re
import zlib
from a52q_handoff import decode
from fdt_evidence import Fdt, physical_regs
from mkadt import node, u32, u64


def configuration(evidence, build, console):
    checked = decode(console, build['handoff_probe'])
    baseline = build['ufs_read']
    expected = {'last_lba': baseline['expected_last_lba'], 'block_bytes': baseline['expected_block_size'],
                'data_crc32': baseline['expected_read_crc32'], 'failure': 0,
                'ocs': 0, 'response_header': 0x21000000}
    if (checked.get('stage') != 0xb3 or checked.get('esr') != 0 or checked.get('ufs_read') != expected or
            checked.get('ufs_nop') != {'ocs': 0, 'response_header': 0x20000000, 'doorbell': 0}):
        raise ValueError('kernel UFS test needs a CRC-checked physical capacity/block read success')
    raw = (evidence / 'live.dtb').read_bytes()
    if hashlib.sha256(raw).hexdigest() != baseline['live_dtb_sha256']:
        raise ValueError('UFS proof belongs to another device tree')
    tree = Fdt(raw)
    hosts = [n for n in tree.nodes.values() if n.enabled() and 'qcom,ufshc' in n.strings('compatible')]
    if len(hosts) != 1:
        raise ValueError('need one live UFS host')
    host = hosts[0]
    names, spans = host.strings('reg-names'), physical_regs(host)
    if names.count('ufs_mem') != 1 or len(names) != len(spans):
        raise ValueError('ambiguous UFS physical registers')
    return {'reg': list(spans[names.index('ufs_mem')]), 'nonce': int.from_bytes(os.urandom(8), 'little'),
            'last_lba': expected['last_lba'], 'block_bytes': expected['block_bytes'],
            'read_lba': baseline['read_lba'], 'read_crc32': expected['data_crc32'],
            'physical_read_console_sha256': hashlib.sha256(console).hexdigest(),
            'scope': 'kernel-only NOP/capacity/one RECOVERY block; no disk registration or writes'}


def adt_node(config):
    return node('a52q-ufs-selftest', [('reg', u64(*config['reg'])), ('nonce', u64(config['nonce']))] +
                [(name.replace('_', '-'), u32(config[name])) for name in
                 ('last_lba', 'block_bytes', 'read_lba', 'read_crc32')])


def decode_kernel_console(data, config):
    stages = {}
    pattern = rb'A52K1 ([0-9a-f]{16}/[0-9a-f]{2}(?:/[0-9a-f]{8}){5}) ([0-9a-f]{8})\r*\n'
    for match in re.finditer(pattern, data):
        if zlib.crc32(match[1]) != int(match[2], 16):
            continue
        nonce, phase, *values = [int(v, 16) for v in match[1].split(b'/')]
        if nonce != config['nonce']:
            continue
        if phase in stages and stages[phase]['values'] != values:
            raise ValueError('CRC-valid kernel UFS records disagree')
        stages.setdefault(phase, {'values': values, 'copies': 0})['copies'] += 1
    expected = [0, config['last_lba'], config['block_bytes'], config['read_crc32'], 0x21000000]
    success = 0x20 in stages and stages[0x20]['values'] == expected and not any(s >= 0xe0 for s in stages)
    return {'scope': 'kernel UFS selftest only; not Apple userland or a mounted disk',
            'nonce': config['nonce'], 'success': success,
            'stages': {hex(k): dict(zip(('ocs', 'last_lba', 'block_bytes', 'data_crc32', 'response_header'), v['values']),
                                  valid_copies=v['copies']) for k, v in stages.items()}}
