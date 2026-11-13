"""Derive a bounded splash-buffer refresh experiment from CRC-checked handoff.

This is a diagnostic, not a framebuffer driver. It reuses only the bootloader's
captured linear BGRA pipe, checks the same state at runtime, fills the captured
surface in the DT splash reservation, and writes CTL_START once. No flush,
address, clock, reset, IOMMU, DSI command or panel configuration is programmed.
The CTL_START operation is defined by pinned sde_hw_ctl.c:trigger_start().
"""
import hashlib
from fdt_evidence import Fdt, regs
from a52q_handoff import decode, layout


def configuration(evidence, sources, capture_build, console):
    enums = (sources / 'sde_hw_mdss.h').read_bytes()
    if hashlib.sha256(enums).hexdigest() != '11d3f62b2547f877ee96300884a19db6f1b88874c84c30682a9e4c6bc20a2243':
        raise ValueError('pinned pixel-component enum source mismatch')
    captured = capture_build['handoff_probe']
    expected = layout(evidence, sources, 'display')
    if {k: v for k, v in captured.items() if k != 'capture_id'} != expected:
        raise ValueError('display capture does not match this evidence/source table')
    snapshot = decode(console, captured)
    if snapshot['completed_reads'] != len(expected['registers']):
        raise ValueError('display MMIO capture did not complete')
    rows = {r['label']: r for r in snapshot['registers']}
    active = [i for i in range(3) if rows[f'ctl{i}.ctl_intf_active']['value']]
    if active != [0] or rows['ctl0.ctl_intf_active']['value'] != 2:
        raise ValueError('unsupported active display controller/interface')
    if rows['ctl0.ctl_top']['value'] != 1 << 17 or rows['ctl0.ctl_start']['value']:
        raise ValueError('need idle command-mode controller 0')
    # DSI_CTRL: DSI_EN bit0, VIDEO_EN bit1, CMD_EN bit2 (Samsung driver).
    if rows['dsi.dsi_ctrl']['value'] & 7 != 5:
        raise ValueError('DSI is not enabled in command mode')
    if rows['dsi.dsi_status']['value'] != 5:
        raise ValueError('unsupported DSI handoff status')
    pipe = [rows[f'sspp0.sspp_{name}'] for name in
            ('src_size', 'src0_addr', 'src_ystride0', 'src_format', 'src_unpack_pattern', 'src_op_mode')]
    size, base, stride, fmt, unpack, op = [r['value'] for r in pipe]
    width, height = size & 0xffff, size >> 16
    # setup_format(): four 8-bit components, interleaved, 4 bytes/pixel,
    # four tightly unpacked elements, linear fetch; no YUV/DX/rotation.
    # C0=G,C1=B,C2=R,C3=A in sde_hw_mdss.h; unpack 01,00,02,03 is BGRA.
    if fmt != 0x237ff or unpack != 0x03020001 or op != 0x80000000:
        raise ValueError('unsupported linear BGRA pipe format/operation')
    if not 160 <= width <= 4096 or not 96 <= height <= 4096 or stride != width * 4:
        raise ValueError('unsupported framebuffer geometry/stride')
    tree = Fdt((evidence / 'live.dtb').read_bytes())
    regions = [r for n in tree.nodes.values() if n.parent and
               n.parent.path == '/reserved-memory' and n.name.startswith('cont_splash_region@')
               for r in regs(n)]
    if len(regions) != 1:
        raise ValueError('need one DT splash reservation')
    lo, length = regions[0]
    if base % 4 or not lo <= base < base + stride * height <= lo + length:
        raise ValueError('scanout buffer exceeds reserved splash memory')
    needed = ['ctl0.ctl_top', 'ctl0.ctl_start', 'ctl0.ctl_intf_active',
              'ctl1.ctl_intf_active', 'ctl2.ctl_intf_active', 'dsi.dsi_ctrl', 'dsi.dsi_status']
    guards = [rows[label] for label in needed] + pipe
    return {'scope': 'full captured splash surface and one CTL0_START=1; experimental refresh',
            'capture_id': captured['capture_id'], 'capture_console_sha256': hashlib.sha256(console).hexdigest(),
            'live_dtb_sha256': expected['live_dtb_sha256'], 'base': base, 'width': width,
            'height': height, 'stride': stride, 'splash_region': [lo, length],
            'buffer_bytes': lo + length - base,
            'start_register': rows['ctl0.ctl_start']['address'],
            'guards': [{'index': next(i for i, r in enumerate(expected['registers']) if r['label'] == g['label']),
                        'value': g['value']} for g in guards],
            'status': 'prepared from hardware reads; refresh not verified'}


def header(config):
    return ('/* Evidence-derived diagnostic only; never a generic display map. */\n' +
            ''.join(f'#define A52Q_DISPLAY_{k.upper()} {config[k]}ULL\n' for k in
                    ('base', 'width', 'height', 'stride', 'buffer_bytes', 'start_register')) +
            'static const unsigned display_guard_indices[] = {' +
            ','.join(str(g['index']) for g in config['guards']) + '};\n' +
            'static const uint32_t display_guard_values[] = {' +
            ','.join(hex(g['value']) + 'U' for g in config['guards']) + '};\n')


def result(build, console):
    """Decode the new trial nonce, not the earlier capture used for guards."""
    if not build.get('display_test') or build.get('embedded_payload'):
        raise ValueError('need a standalone display diagnostic build')
    trial = build['handoff_probe']
    if trial.get('group') != 'display':
        raise ValueError('not a display handoff trial')
    captured = decode(console, trial)
    guards = build['display_test']['guards']
    values = {i: r['value'] for i, r in zip(sorted(captured['valid_register_copies']), captured['registers'])}
    guards_match = all(values.get(g['index']) == g['value'] for g in guards)
    consumed = (captured['complete'] and guards_match and captured['stage'] == 0x93 and
                captured['esr'] == 0 and captured['valid_stage_copies'] > 0)
    return {'scope': 'display diagnostic only; not iOS UI or measured panel VSync',
            'capture_id': captured['capture_id'], 'stage': captured['stage'], 'esr': captured['esr'],
            'valid_stage_copies': captured['valid_stage_copies'], 'guards_match': guards_match,
            'controller_start_consumed': consumed, 'visible_output_verified': False,
            'panel_refresh_hz': None, 'next': 'record human observation of full-screen RGB bars'}


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Decode a CRC-bound A52 display diagnostic; never writes a device.')
    parser.add_argument('--build', required=True, type=Path)
    parser.add_argument('--console', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(result(json.loads(args.build.read_text()), args.console.read_bytes()), indent=2))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'display result rejected: {error}\n')
