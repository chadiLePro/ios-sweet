#!/usr/bin/env python3
"""Inspect local A52 evidence. Does not select XNU RAM or create a boot image."""
import argparse
import hashlib
import json
from pathlib import Path
import android_boot_evidence
from fdt_evidence import Fdt, describe, simplefb


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('evidence', type=Path, help='a52q_collect.py output directory')
    p.add_argument('--out', type=Path, help='private JSON report path')
    p.add_argument('--simplefb-header', type=Path,
                   help='emit diagnostic framebuffer config only if explicit simplefb is valid')
    a = p.parse_args()
    try:
        data = (a.evidence / 'live.dtb').read_bytes()
        fdt = Fdt(data)
        result = {'live_dtb_sha256': hashlib.sha256(data).hexdigest(),
                  'fdt': describe(fdt), 'boot_images': {}, 'blockers': []}
        model = ' '.join(result['fdt']['model']).lower()
        if 'a52q' not in model:
            result['blockers'].append('live DT model does not identify A52Q; review identity')
        for name in ('boot', 'recovery'):
            path = a.evidence / (name + '.img')
            if path.exists():
                result['boot_images'][name] = android_boot_evidence.inspect(path.read_bytes())
        try:
            fb = simplefb(fdt)
            result['simplefb_description'] = fb
        except ValueError as exc:
            fb = None
            result['blockers'].append(str(exc))
        result['blockers'] += [
            'No kernel RAM interval selected; live reservations and firmware-owned ranges need review',
            'No Samsung temporary boot transport verified; no boot image is produced',
            'This snapshot report alone does not demonstrate diagnostic shim or XNU execution',
        ]
        text = json.dumps(result, indent=2) + '\n'
        if a.out:
            a.out.write_text(text, encoding='utf-8')
        else:
            print(text, end='')
        if a.simplefb_header:
            if not fb or 'a52q' not in model:
                p.exit(2, 'refusing framebuffer config: missing valid A52Q simplefb evidence\n')
            # A description is not a scanout test; this still does not package an image.
            a.simplefb_header.write_text(
                '/* From live FDT ' + result['live_dtb_sha256'] + '; scanout UNTESTED. */\n' +
                ''.join(f'#define A52Q_FB_{k.upper()} {v}UL\n' for k, v in fb.items()),
                encoding='ascii')
    except (ValueError, OSError) as exc:
        p.exit(1, f'evidence rejected: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
