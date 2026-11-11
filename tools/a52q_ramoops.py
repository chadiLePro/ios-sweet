"""Derive an optional diagnostic console from DT AND running recovery evidence.

Layout follows fs/pstore/{ram.c,ram_core.c} in the pinned Samsung downstream
source. No address is supplied by the profile or borrowed from sweet.
"""
import gzip
import hashlib
from fdt_evidence import Fdt, regs


def configuration(evidence):
    data = (evidence / 'live.dtb').read_bytes()
    dt = Fdt(data)
    if 'a52q' not in ' '.join(dt.nodes['/'].strings('model')).lower():
        raise ValueError('ramoops output requires A52Q live DT identity')
    params = {}
    for line in (evidence / 'ramoops-parameters.txt').read_text().splitlines():
        k, v = line.split('=', 1)
        if k in params:
            raise ValueError('duplicate ramoops parameter')
        params[k] = int(v, 0)
    config = gzip.decompress((evidence / 'kernel-config.gz').read_bytes()).decode()
    for option in ('CONFIG_PSTORE=y', 'CONFIG_PSTORE_RAM=y', 'CONFIG_PSTORE_CONSOLE=y'):
        if option not in config.splitlines():
            raise ValueError(f'recovery missing {option}')
    nodes = [n for n in dt.nodes.values() if n.enabled() and 'ramoops' in n.strings('compatible')]
    if len(nodes) != 1:
        raise ValueError('need one enabled ramoops node')
    n = nodes[0]
    if (n.parent.path != '/reserved-memory' or n.parent.props.get('ranges') != b'' or
            len(regs(n)) != 1):
        raise ValueError('ramoops must be a physical /reserved-memory range')
    base, size = regs(n)[0]
    if size & (size - 1):
        raise ValueError('ramoops memory size would require kernel rounding')
    if params['mem_address'] != base or params['mem_size'] != size:
        raise ValueError('runtime ramoops range disagrees with DT')
    sizes = {}
    for key in ('record', 'console', 'ftrace', 'pmsg'):
        value = n.cell(key + '-size', 0)
        if params[key + '_size'] != value or (value and value & (value - 1)):
            raise ValueError(f'ramoops {key} size mismatch or unsupported rounding')
        sizes[key] = value
    if (params['ecc'] or n.cell('ecc-size', 0) or params['mem_type'] or
            n.cell('mem-type', 0)):
        raise ValueError('only no-ECC, default recovery ramoops mapping is implemented')
    dump = size - sizes['console'] - sizes['ftrace'] - sizes['pmsg']
    if (sizes['record'] <= 0 or dump <= 0 or dump % sizes['record'] or
            not 4096 <= sizes['console'] <= 1 << 20 or base % 4):
        raise ValueError('unsupported ramoops partition layout')
    # ram.c allocates dump records first, then console, ftrace, pmsg.
    return {'base': base + dump, 'size': sizes['console'],
            'live_dtb_sha256': hashlib.sha256(data).hexdigest(),
            'status': 'candidate output; reset survival and TWRP retrieval NOT tested'}
