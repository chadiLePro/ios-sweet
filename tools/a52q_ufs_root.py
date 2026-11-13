"""Bound a read-only diagnostic HFS root to captured BOOT padding.

The software layout is only installed by the separately checked image packager.
No userdata/GPT writes or device access occur here.
"""
import hashlib
import re
import zlib
from a52q_gpt import from_capture, diagnostic_boot_tail
from a52q_hfs_root import validate_hfs_test_root, hardware_root_proof
from mkadt import node, u32, u64


def validate_config(config, ufs):
    first, count, root_first, root_count = config['window']
    capacity = ufs['last_lba'] + 1
    if (config['ufs_nonce'] != ufs['nonce'] or ufs['block_bytes'] != 4096 or
            first < 2 or count != (96 << 20) // 4096 or first > capacity or count > capacity - first or
            not (8 << 20) // 4096 <= root_count <= (32 << 20) // 4096 or
            root_first != first + count - root_count or config['bytes'] != root_count * 4096 or
            config['offset_in_boot_bytes'] != (count - root_count) * 4096 or
            not 0 <= config['header_crc32'] <= 0xffffffff or
            not re.fullmatch('[0-9a-f]{64}', config['sha256'])):
        raise ValueError('invalid bounded BOOT diagnostic root configuration')


def configuration(gpt_capture, ufs, data, kernel_hash, qemu_report):
    volume = validate_hfs_test_root(data)
    report = from_capture(gpt_capture)
    if report['block_bytes'] != 4096 or report['disk_bytes'] != (ufs['last_lba'] + 1) * 4096:
        raise ValueError('GPT and physical UFS proof capacity differ')
    boots = [p for p in report['partitions'] if p['name'] == 'boot' and p['index'] == 19]
    if len(boots) != 1 or boots[0]['bytes'] != 96 << 20:
        raise ValueError('need the captured 96 MiB BOOT partition')
    boot = boots[0]
    digest = hashlib.sha256(data).hexdigest()
    config = {'window': [boot['first_lba'], boot['block_count'],
                        boot['first_lba'] + boot['block_count'] - len(data) // 4096, len(data) // 4096],
              'ufs_nonce': ufs['nonce'], 'bytes': len(data), 'sha256': digest,
              'offset_in_boot_bytes': boot['bytes'] - len(data),
              'header_crc32': zlib.crc32(data[:4096]), 'volume': volume,
              'gpt_capture_sha256': hashlib.sha256((gpt_capture / 'capture.json').read_bytes()).hexdigest(),
              'qemu_boot_proof': hardware_root_proof(qemu_report, kernel_hash, digest),
              'scope': 'read-only BOOT-tail diagnostic root; own PID1, no Apple userland'}
    validate_config(config, ufs)
    return config


def adt_node(config):
    return node('a52q-ufs-root', [('window', u64(*config['window'])),
        ('ufs-nonce', u64(config['ufs_nonce'])), ('header-crc32', u32(config['header_crc32']))])


def validate_packaging(config, ufs, data, gpt_capture, packed_end):
    validate_config(config, ufs)
    validate_hfs_test_root(data)
    if len(data) != config['bytes'] or hashlib.sha256(data).hexdigest() != config['sha256']:
        raise ValueError('root image differs from payload proof')
    if hashlib.sha256((gpt_capture / 'capture.json').read_bytes()).hexdigest() != config['gpt_capture_sha256']:
        raise ValueError('GPT proof differs from payload')
    report = from_capture(gpt_capture)
    plan = diagnostic_boot_tail(report, len(data), packed_end)
    if (plan['offset_in_boot_bytes'] != config['offset_in_boot_bytes'] or
            [plan['first_lba'], plan['block_count']] != config['window'][2:]):
        raise ValueError('root window differs from validated BOOT padding')
    return plan


def decode_kernel_console(data, config):
    expected = config['window'][2:] + [config['header_crc32']]
    copies = 0
    for m in re.finditer(rb'A52V1 ([0-9a-f]{16}(?:/[0-9a-f]{8}){3}) ([0-9a-f]{8})\r*\n', data):
        if zlib.crc32(m[1]) != int(m[2], 16): continue
        nonce, *values = [int(v, 16) for v in m[1].split(b'/')]
        if nonce != config['ufs_nonce']: continue
        if values != expected: raise ValueError('CRC-valid diagnostic root window disagrees')
        copies += 1
    return {'readonly_root_window_verified': copies > 0, 'valid_copies': copies,
            'scope': 'BSD root window and first-block CRC; mount/PID1 evidence is separate'}
