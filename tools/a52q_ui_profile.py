"""Evidence-bound opt-in development UI profile; no device writes or UI claim."""
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import zlib
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
    if 'text_console' in config and config['text_console'] is not True:
        raise ValueError('invalid opt-in bitmap console declaration')
    if 'display_scale' in config and (type(config['display_scale']) is not int or config['display_scale'] != 3):
        raise ValueError('invalid logical display scale')
    if 'abort_reason' in config and config['abort_reason'] is not True:
        raise ValueError('invalid opt-in abort-reason probe')
    if 'var_write_development' in config and (config['var_write_development'] is not True or not config.get('var_plan')):
        raise ValueError('development var writes need an explicit persistent var plan')


def configuration(build,console,kernel_sha256,root_sha256):
    cfg=build.get('embedded_payload',{}).get('display_selftest')
    if not cfg or not decode_kernel_console(console,cfg)['kernel_refresh_completed']:
        raise ValueError('need the exact CRC-confirmed XNU display refresh proof')
    result=dict(cfg,nonce=int.from_bytes(os.urandom(8),'little') or 1,
                kernel_sha256=kernel_sha256,root_sha256=root_sha256,
                physical_kernel_console_sha256=hashlib.sha256(console).hexdigest(),
                software_vsync_us=16667,physical_panel_hz=None,display_scale=3,
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


def decode_console(data,config):
    """Only guarded-adapter evidence; never infer framework or visible UI success."""
    validate_config(config)
    records={}
    for m in re.finditer(rb'A52G1 ([0-9a-f]{16}/[0-9a-f]{2}/[0-9a-f]{8}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(m[1])!=int(m[2],16):continue
        nonce,phase,count=[int(v,16) for v in m[1].split(b'/')]
        if nonce!=config['nonce']:continue
        if phase not in (0x10,0x30,0xe0,0xe1) or (phase==0x10 and count) or (phase==0x30 and not 1<=count<=3):
            raise ValueError('invalid CRC-valid UI adapter record')
        row=records.setdefault((phase,count),dict(phase=phase,frames=count,valid_copies=0))
        row['valid_copies']+=1
    failures={}
    for m in re.finditer(rb'A52G2 ([0-9a-f]{16}/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{8}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(m[1])!=int(m[2],16):continue
        nonce,reason,index,value=[int(v,16) for v in m[1].split(b'/')]
        if nonce!=config['nonce']:continue
        if (reason not in (1,2,3,4,5,6,7) or
            (reason in (1,4,7) and (index!=0xff or value)) or
            (reason in (2,3) and index>=len(config['guards'])) or
            (reason==2 and value) or
            (reason==5 and (index!=6 or value!=5)) or
            (reason==6 and (index!=1 or not value&1))):
            raise ValueError('invalid CRC-valid UI rejection detail')
        row=failures.setdefault((reason,index,value),dict(
            reason={1:'profile',2:'register-map',3:'register-value',4:'frame-map',5:'dsi-busy-timeout',6:'start-completion-timeout'}[reason],
            register_index=index if index<13 else None,observed=value,valid_copies=0))
        if reason==3:
            row['expected']=config['guards'][index]['value']
            if value==row['expected']:raise ValueError('non-mismatching UI guard rejection')
        row['valid_copies']+=1
    rows=list(records.values())
    return dict(records=rows,rejections=list(failures.values()),adapter_prepared=any(r['phase']==0x10 for r in rows),
        guarded_submit_observed=any(r['phase']==0x30 for r in rows),
        error_record_observed=any(r['phase']>=0xe0 for r in rows),
        physical_visible_ui_verified=False,physical_panel_hz=None,
        scope='CRC-valid software adapter records only; not service startup, sustained Hz or a visible lock screen')
