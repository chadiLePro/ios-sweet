#!/usr/bin/env python3
"""Run the A52 loader with an explicitly QEMU-only payload; capture XNU RAM logs.

QEMU virt, 4 GiB emulated RAM, TCG, no disks/network/USB passthrough. This does
not emulate Samsung hardware. Entry, panic and userland are distinct results.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import time
import zlib
from qemu_a52q_diag import Qmp, decode_ramlog, decode_record


def entry_copies(data):
    count = 0
    for match in re.finditer(rb'(A52QXNU ENTRY v1\n)crc32=([0-9a-f]{8})\nA52QXNU END\n', data):
        count += zlib.crc32(match[1]) == int(match[2], 16)
    return count


def run(build, out, qemu, seconds=25, expected_loader_stage=None):
    metadata = json.loads((build / 'build.json').read_text())
    payload = metadata.get('embedded_payload', {})
    if payload.get('environment') != 'QEMU virt ONLY; never flash':
        raise ValueError('requires an explicitly QEMU-only payload, with emulated GIC/timer values')
    image = (build / 'diag-core.Image').resolve()
    if hashlib.sha256(image.read_bytes()).hexdigest() != metadata['image_sha256']:
        raise ValueError('Image hash mismatch')
    out.mkdir(parents=True, exist_ok=False)
    symbols = {w[2]: int(w[0], 16) for l in (build / 'symbols.txt').read_text().splitlines()
               if len(w := l.split()) == 3}
    # QEMU arm64 Linux boot: Image text_offset is copied from the Samsung
    # template (0x80000), so the generic boot stub places it at RAM_BASE+offset.
    import struct
    load = 0x40000000 + struct.unpack_from('<Q', image.read_bytes(), 8)[0]
    if load < 0x40001000:
        load += 0x200000
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
    args = [qemu, '-M', 'virt,gic-version=3,virtualization=off', '-accel', 'tcg',
            '-cpu', 'cortex-a76', '-m', '4096', '-smp', '1', '-nodefaults', '-display', 'none',
            '-serial', 'null', '-monitor', 'none', '-nic', 'none', '-no-reboot', '-S',
            '-kernel', str(image), '-qmp', f'tcp:127.0.0.1:{port},server=on,wait=off',
            '-d', 'int,guest_errors', '-D', str((out / 'qemu.log').resolve())]
    (out / 'invocation.json').write_text(json.dumps(args, indent=2) + '\n')
    report = {'scope': 'QEMU virt only; no Samsung boot or hardware claim', 'status': 'unknown',
              'image_sha256': metadata['image_sha256'], 'payload': payload,
              'qemu': subprocess.check_output([qemu, '--version'], text=True).splitlines()[0]}
    process, qmp = None, None
    try:
        with (out / 'stderr.txt').open('wb') as err:
            process = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=err, creationflags=0x08000000 if os.name == 'nt' else 0)
            qmp = Qmp(port, process)
            qmp.call('cont')
            # Each run is bounded. Polling lets loader-only tests finish promptly.
            deadline = time.monotonic() + seconds
            while time.monotonic() < deadline:
                time.sleep(0.5)
                qmp.call('stop')
                record = decode_record(qmp.dump(load + symbols['a52q_diagnostic'],
                    metadata['diagnostic_record_bytes'], out / 'record.bin'))
                if expected_loader_stage is not None and record['stage'] == expected_loader_stage:
                    break
                if record['stage'] >= 0xe0:
                    break
                trace = out / 'qemu.log'
                if trace.exists() and trace.stat().st_size > 8 << 20:
                    break  # Capture the first fault, not hundreds of MiB of recursive exceptions.
                qmp.call('cont')
            qmp.call('stop')
            log = metadata['output']
            raw = qmp.dump(log['base'], log['size'], out / 'ramoops.bin')
            try:
                console = decode_ramlog(raw)
            except (ValueError, UnicodeError):
                console = raw[12:].rstrip(b'\0').decode('ascii', errors='replace')
            (out / 'console.txt').write_text(console, encoding='utf-8')
            (out / 'registers.txt').write_text(qmp.monitor('info registers'))
            report['loader_record'] = decode_record(qmp.dump(load + symbols['a52q_diagnostic'],
                metadata['diagnostic_record_bytes'], out / 'record.bin'))
            report['crc_valid_entry_copies'] = entry_copies(raw)
            if 'A52QXNU PANIC:' in console or 'panic(cpu ' in console:
                report['status'] = 'XNU panic observed'
            elif 'A52QXNU stage=' in console:
                report['status'] = 'XNU C bootstrap observed'
            elif report['crc_valid_entry_copies']:
                report['status'] = 'XNU assembly entry verified; C bootstrap not demonstrated'
            elif expected_loader_stage == report['loader_record']['stage']:
                report['status'] = 'expected loader stage reached; not an XNU boot'
            else:
                report['status'] = 'no XNU entry demonstrated'
            qmp.call('quit')
            process.wait(timeout=5)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        report['error'] = str(exc)
    finally:
        if qmp:
            qmp.close()
        if process and process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--qemu', default='qemu-system-aarch64')
    p.add_argument('--seconds', type=int, default=25)
    p.add_argument('--expect-loader-stage', type=lambda v: int(v, 0))
    a = p.parse_args()
    result = run(a.build, a.out, a.qemu, a.seconds, a.expect_loader_stage)
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if 'error' in result or result['status'] == 'no XNU entry demonstrated' else 0)
