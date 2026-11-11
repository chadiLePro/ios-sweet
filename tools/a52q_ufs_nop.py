"""Evidence-bound UFS NOP experiment; no SCSI or flash write operations.

An idle handoff, new CPU RAM pool and source-checked descriptors are required.
Identity DMA is an explicit hypothesis: absent DT iommus is not proof of ABL
configuration. A matching NOP IN is the experiment's evidence, not an assumption.
"""
import hashlib
from a52q_handoff import decode, layout, SOURCE_COMMIT
from a52q_payload import hardware
from fdt_evidence import Fdt

EXTRA_SOURCES = {
    'ufs.h': 'a8ccd860879844c4030c830006c6867f2b262f63873df72603332d7368bda929',
    'ufshcd.c': '7dac69a2ba47a1e9b5e53907bff68e635ab17cba3d067eb666c4ecbd41ded1cd',
}


def configuration(evidence, sources, capture_build, console, cpu_log):
    for name, expected in EXTRA_SOURCES.items():
        if hashlib.sha256((sources / name).read_bytes()).hexdigest() != expected:
            raise ValueError('UFS protocol source mismatch: ' + name)
    captured = capture_build['handoff_probe']
    table = layout(evidence, sources, 'ufs')
    if {k: v for k, v in captured.items() if k != 'capture_id'} != table:
        raise ValueError('UFS snapshot differs from current evidence')
    checked = decode(console, captured)
    if not checked['complete'] or checked.get('stage') != 0x80 or checked.get('esr') != 0:
        raise ValueError('need a complete, fault-free CRC-checked UFS snapshot')
    values = {r['label'].removeprefix('ufs.reg_'): r['value'] for r in checked['registers']}
    if (values['ufs_version'] != 0x210 or not values['controller_capabilities'] & (1 << 24) or
            values['controller_enable'] != 1 or values['controller_status'] & 15 != 15 or
            values['auto_hibernate_idle_timer'] or values['utp_transfer_req_door_bell'] or
            values['utp_transfer_req_list_run_stop'] != 1):
        raise ValueError('unsupported/non-idle UFS handoff')
    tree = Fdt((evidence / 'live.dtb').read_bytes())
    host = [n for n in tree.nodes.values() if n.enabled() and 'qcom,ufshc' in n.strings('compatible')]
    if len(host) != 1 or any('iommu' in k for k in host[0].props):
        raise ValueError('UFS DMA translation requires a separate implementation')
    parent = host[0]
    while parent is not None:
        if parent.props.get('dma-ranges', b''):
            raise ValueError('UFS DMA bus translation is not implemented')
        parent = parent.parent
    # Same conservative planner and measured CPU evidence as the demonstrated
    # XNU bootstrap. Allocate only one page; no kernel/payload is loaded here.
    base, _, frequency, _, _, dt_hash = hardware(evidence, cpu_log, 128 << 20)
    indices = {r['label'].removeprefix('ufs.reg_'): i for i, r in enumerate(table['registers'])}
    writes = ['utp_transfer_req_list_base_l', 'utp_transfer_req_list_base_h',
              'utp_transfer_req_door_bell', 'utp_transfer_req_list_run_stop']
    return {'scope': 'one UFS NOP OUT/IN; no SCSI command, PRDT, flash write or device initialization',
            'source_commit': SOURCE_COMMIT, 'protocol_sources_sha256': EXTRA_SOURCES,
            'capture_console_sha256': hashlib.sha256(console).hexdigest(),
            'live_dtb_sha256': dt_hash, 'pool_base': base, 'pool_bytes': 16384,
            'timer_hz': frequency, 'timeout_ms': 1000, 'register_indices': indices,
            'write_addresses': [table['registers'][indices[n]]['address'] for n in writes],
            'aligned_upiu_size': 1024, 'command_type': 1, 'nop_out': 0, 'nop_in': 0x20,
            'dma_translation': 'identity DMA hypothesis; not established by missing DT binding',
            'status': 'prepared; NOP exchange not yet verified'}


def header(config):
    return ('/* Source-checked protocol; physical values derived from this phone evidence. */\n' +
            f'#define A52Q_UFS_POOL {config["pool_base"]}ULL\n' +
            f'#define A52Q_UFS_POOL_BYTES {config["pool_bytes"]}U\n' +
            f'#define A52Q_UFS_TIMER_HZ {config["timer_hz"]}ULL\n' +
            ''.join(f'#define UFS_INDEX_{name.upper()} {index}U\n'
                    for name, index in config['register_indices'].items()))
