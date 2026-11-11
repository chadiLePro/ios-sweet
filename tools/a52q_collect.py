#!/usr/bin/env python3
"""Read-only ADB acquisition. Writes only host files, never mounts or flashes.

Run from TWRP: python3 tools/a52q_collect.py [--adb PATH] [--serial SERIAL]
Evidence includes private boot parameters; the default backup/ path is ignored.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from fdt_evidence import Fdt
from android_boot_evidence import inspect as inspect_boot

ROOT = Path(__file__).resolve().parents[1]
PROPS = (
    'ro.product.model', 'ro.product.device', 'ro.product.vendor.device',
    'ro.board.platform', 'ro.bootloader', 'gsm.version.baseband',
    'ro.build.display.id', 'ro.build.version.release', 'ro.build.version.incremental',
    'ro.vendor.build.fingerprint', 'ro.boot.verifiedbootstate',
    'ro.boot.flash.locked', 'ro.boot.vbmeta.device_state',
)


def acquire(adb, serial, out):
    out.mkdir(parents=True, exist_ok=False)
    prefix = [adb, '-s', serial, 'exec-out']
    manifest = {'transport': 'adb exec-out; reads only', 'files': {}, 'errors': {}}

    def capture(name, command, required=False):
        dest = out / name
        try:
            with dest.open('wb') as f:
                p = subprocess.run(prefix + ['sh', '-c', command], stdout=f,
                                   stderr=subprocess.PIPE, timeout=180)
            if p.returncode or not dest.stat().st_size:
                raise RuntimeError(p.stderr.decode(errors='replace') or 'empty output')
            data = dest.read_bytes()
            if data.startswith(b'A52Q_UNAVAILABLE'):
                raise RuntimeError(data.decode(errors='replace').strip())
            # exec-out does not reliably propagate a remote command exit code.
            # Validate binary formats rather than hashing an error as a dump.
            if name == 'live.dtb':
                Fdt(data)
            elif name in ('boot.img', 'recovery.img'):
                inspect_boot(data)
            manifest['files'][name] = {
                'bytes': dest.stat().st_size,
                'sha256': hashlib.sha256(data).hexdigest(),
            }
        except (OSError, subprocess.TimeoutExpired, RuntimeError, ValueError) as exc:
            dest.unlink(missing_ok=True)
            manifest['errors'][name] = str(exc)
            if required:
                raise RuntimeError(f'{name}: {exc}') from exc

    try:
        capture('properties.txt', '; '.join(
            f'printf "{prop}="; getprop {prop}' for prop in PROPS), required=True)
        capture('live.dtb', 'cat /sys/firmware/fdt')
        capture('live-tree.tar', 'tar -C /sys/firmware/devicetree/base -cf - .')
        for name, command in {
            'cmdline.txt': 'cat /proc/cmdline',
            'iomem.txt': 'cat /proc/iomem',
            'cpuinfo.txt': 'cat /proc/cpuinfo',
            'meminfo.txt': 'cat /proc/meminfo',
            'dmesg.txt': 'dmesg',
            'kernel-config.gz': 'cat /proc/config.gz',
            'ramoops-parameters.txt': (
                'for n in mem_address mem_size record_size console_size ftrace_size '
                'pmsg_size ecc mem_type; do printf "$n="; '
                'cat /sys/module/ramoops/parameters/$n; done'),
            'console-ramoops-0.txt': 'cat /sys/fs/pstore/console-ramoops-0',
            'drm-connector.txt': (
                'for f in /sys/class/drm/card0-DSI-1/status '
                '/sys/class/drm/card0-DSI-1/enabled /sys/class/drm/card0-DSI-1/modes; '
                'do echo "$f"; cat "$f"; done'),
            'partition-links.txt': 'ls -l /dev/block/by-name /dev/block/bootdevice/by-name',
            'framebuffer.txt': (
                'if [ ! -d /sys/class/graphics/fb0 ]; then '
                'echo A52Q_UNAVAILABLE:no_fb0; exit 1; fi; '
                'for f in /sys/class/graphics/fb0/name /sys/class/graphics/fb0/stride '
                '/sys/class/graphics/fb0/virtual_size /sys/class/graphics/fb0/bits_per_pixel '
                '/sys/class/graphics/fb0/modes; do echo "$f"; cat "$f"; done'),
        }.items():
            capture(name, command)
        # Fixed allowlist: no userdata, EFS, calibration, modem, or bootloader reads.
        for part in ('boot', 'dtbo', 'recovery', 'vbmeta'):
            capture(part + '.img',
                    f'for p in /dev/block/by-name/{part} '
                    f'/dev/block/bootdevice/by-name/{part}; do '
                    '[ -b "$p" ] && exec cat "$p"; done; '
                    'echo A52Q_UNAVAILABLE:no_partition; exit 1')
    finally:
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--adb', default='adb')
    p.add_argument('--serial', help='select one device; never saved in manifest')
    p.add_argument('--out', type=Path, default=ROOT / 'backup' / 'a52q' /
                   datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    a = p.parse_args()
    try:
        devices = subprocess.check_output([a.adb, 'devices'], text=True)
        ready = [line.split()[0] for line in devices.splitlines()[1:]
                 if len(line.split()) == 2 and line.split()[1] in ('device', 'recovery')]
        serial = a.serial or (ready[0] if len(ready) == 1 else None)
        if not serial or serial not in ready:
            p.error('connect one authorized device in TWRP, or select it with --serial')
        result = acquire(a.adb, serial, a.out)
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        p.exit(1, f'acquisition failed: {exc}\n')
    print(f'Evidence: {a.out.resolve()}')
    print(f'{len(result["files"])} files; {len(result["errors"])} unavailable (see manifest.json)')
    return 0 if 'live.dtb' in result['files'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
