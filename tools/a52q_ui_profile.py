"""Evidence-bound opt-in development UI profile; no device writes or UI claim."""
import hashlib
import json
import os
from pathlib import Path
import re
import struct
from a52q_display_selftest import validate_config as validate_display, decode_kernel_console
from mkadt import node, u32, u64, cstr

EXPECTED=json.loads((Path(__file__).resolve().parents[1]/'devices/a52q-ui-profile.json').read_text())


def validate_config(config):
    validate_display(config)
    for key in ('reg','geometry','start_register','guards','live_dtb_sha256'):
        if config.get(key)!=EXPECTED[key]:raise ValueError('UI profile differs from captured A52 splash: '+key)
    for key in ('kernel_sha256','root_sha256','physical_kernel_console_sha256'):
        if not isinstance(config.get(key),str) or not re.fullmatch('[0-9a-f]{64}',config[key]):
            raise ValueError('UI profile lacks bound kernel/root/physical proof')
    if config.get('software_vsync_us')!=16667 or config.get('physical_panel_hz') is not None:
        raise ValueError('UI profile must distinguish software cadence from physical panel Hz')


def configuration(build,console,kernel_sha256,root_sha256):
    cfg=build.get('embedded_payload',{}).get('display_selftest')
    if not cfg or not decode_kernel_console(console,cfg)['kernel_refresh_completed']:
        raise ValueError('need the exact CRC-confirmed XNU display refresh proof')
    result=dict(cfg,nonce=int.from_bytes(os.urandom(8),'little') or 1,
                kernel_sha256=kernel_sha256,root_sha256=root_sha256,
                physical_kernel_console_sha256=hashlib.sha256(console).hexdigest(),
                software_vsync_us=16667,physical_panel_hz=None,
                scope='development no-SEP and CPU surface bridge; Apple services/visible UI unverified')
    validate_config(result);return result


def adt_node(config):
    validate_config(config)
    return node('a52q-ui-bridge', [('reg',u64(*config['reg'])),
        ('geometry',u32(*config['geometry'])),('nonce',u64(config['nonce'])),
        ('start-register',u64(config['start_register'])),
        ('guards',b''.join(struct.pack('<QII',g['address'],g['value'],0) for g in config['guards']))])


def display_node():
    return node('disp0',[('device_type',cstr('display-subsystem')),
        ('compatible',cstr('a52q,display')),('canvas-width',u32(1080)),('canvas-height',u32(2400))])
