"""Evidence-bound XNU framebuffer mapping test, not an iOS display driver."""
import hashlib
import os
import re
import struct
import zlib
from a52q_display_probe import configuration as display_configuration, result as display_result
from mkadt import node, u32, u64


def validate_config(config):
    base, size = config['reg']
    width, height, stride = config['geometry']
    if (base % 16384 or size % 16384 or size <= 0 or size > 64 << 20 or
            not 0x80000000 <= base < base + size <= 1 << 32 or
            not 3 <= width <= 4096 or not 2 <= height <= 4096 or
            stride != width * 4 or stride * height > size or
            not 0 < config['nonce'] < 1 << 64):
        raise ValueError('invalid display reservation/geometry/nonce')
    guards = config['guards']
    addresses = [g['address'] for g in guards]
    if (len(guards) != 13 or len(set(addresses)) != len(addresses) or
            any(a % 4 or not 0 < a < 0x80000000 for a in addresses) or
            any(not 0 <= g['value'] <= 0xffffffff for g in guards) or
            not any(g['address'] == config['start_register'] and g['value'] == 0 for g in guards)):
        raise ValueError('invalid display register guards/start')


def configuration(evidence, sources, build, console):
    if not display_result(build, console)['controller_start_consumed']:
        raise ValueError('kernel display test needs a successful CRC-bound physical refresh')
    checked = display_configuration(evidence, sources, build, console)
    config = {'reg': [checked['base'], checked['buffer_bytes']],
              'geometry': [checked['width'], checked['height'], checked['stride']],
              'start_register': checked['start_register'],
              'guards': [dict(address=build['handoff_probe']['registers'][g['index']]['address'],
                              value=g['value']) for g in checked['guards']],
              'nonce': int.from_bytes(os.urandom(8), 'little') or 1,
              'live_dtb_sha256': checked['live_dtb_sha256'],
              'physical_refresh_console_sha256': hashlib.sha256(console).hexdigest(),
              'scope': 'one XNU CPU blit and command-mode START; no Apple framebuffer ABI or measured panel Hz'}
    validate_config(config)
    return config


def adt_node(config):
    validate_config(config)
    return node('a52q-display-selftest', [('reg', u64(*config['reg'])),
        ('geometry', u32(*config['geometry'])), ('nonce', u64(config['nonce'])),
        ('start-register', u64(config['start_register'])),
        ('guards', b''.join(struct.pack('<QII', g['address'], g['value'], 0) for g in config['guards']))])


def decode_kernel_console(data, config):
    validate_config(config)
    stages = {}
    for match in re.finditer(rb'A52D1 ([0-9a-f]{16}/[0-9a-f]{2}/[0-9a-f]{8}) ([0-9a-f]{8})\r*\n', data):
        if zlib.crc32(match[1]) != int(match[2], 16):
            continue
        nonce, phase, detail = [int(v, 16) for v in match[1].split(b'/')]
        if nonce != config['nonce']:
            continue
        if phase in stages and stages[phase]['detail'] != detail:
            raise ValueError('CRC-valid kernel display records disagree')
        stages.setdefault(phase, {'detail': detail, 'valid_copies': 0})['valid_copies'] += 1
    return {'scope': config['scope'], 'nonce': config['nonce'],
            'kernel_refresh_completed': (all(p in stages and stages[p]['detail'] == 0 for p in (0x10, 0x20, 0x30))
                                         and not any(p >= 0xe0 for p in stages)),
            'visible_output_verified': False, 'panel_refresh_hz': None,
            'stages': {hex(k): v for k, v in stages.items()}}
