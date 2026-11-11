#!/usr/bin/env python3
"""Execute the diagnostic Image on QEMU virt; this does NOT emulate an A52.

Uses TCG, a generic loader and fixed emulation-only load address. Tests the same
raw Image that is packaged for the phone, including its entry and RAM logger.
No disks, USB passthrough, networking or phone tools are attached to the guest.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import time
from android_boot_evidence import inspect as inspect_boot

FIELDS = ('magic version stage image image_end dtb current_el sctlr mpidr midr '
          'mmfr0 pfr0 cntfrq exception_slot esr elr far').split()
MAGIC = 0x4741494451323541
RAM_BASE, RAM_END = 0x40000000, 0xc0000000  # QEMU virt, 2 GiB; not an A52 map


def linux_load_address(image):
    offset, size = struct.unpack_from('<QQ', image, 8)
    if image[56:60] != b'ARM\x64' or not size:
        raise ValueError('need a sized Linux arm64 Image')
    # QEMU hw/arm/boot.c: BOOTLOADER_MAX_SIZE = 4 KiB.
    return RAM_BASE + offset + (0x200000 if offset < 4096 else 0)


def decode_record(data):
    if len(data) != len(FIELDS) * 8:
        raise ValueError('wrong diagnostic record size')
    record = dict(zip(FIELDS, struct.unpack('<' + 'Q' * len(FIELDS), data)))
    if record['magic'] != MAGIC or record['version'] != 1:
        raise ValueError('no supported A52Q diagnostic record')
    return record


def decode_ramlog(data):
    if len(data) < 12:
        raise ValueError('truncated RAM console')
    sig, start, size = struct.unpack_from('<III', data)
    if sig != 0x43474244 or not 0 <= start <= size <= len(data) - 12:
        raise ValueError('invalid Linux persistent_ram_buffer header')
    raw = data[12 + start:12 + size] + data[12:12 + start]
    return raw.decode('ascii')


class Qmp:
    def __init__(self, port, process):
        deadline = time.monotonic() + 15
        while True:
            try:
                self.sock = socket.create_connection(('127.0.0.1', port), timeout=2)
                break
            except OSError:
                if process.poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError('QEMU QMP did not become available; see stderr.txt')
                time.sleep(0.05)
        self.file = self.sock.makefile('rwb')
        if 'QMP' not in self.read():
            raise RuntimeError('invalid QMP greeting')
        self.call('qmp_capabilities')

    def read(self):
        line = self.file.readline()
        if not line:
            raise RuntimeError('QMP disconnected')
        return json.loads(line)

    def call(self, command, **arguments):
        self.file.write((json.dumps({'execute': command, 'arguments': arguments}) + '\n').encode())
        self.file.flush()
        while True:
            reply = self.read()
            if 'error' in reply:
                raise RuntimeError(f'QMP {command}: {reply["error"]}')
            if 'return' in reply:
                return reply['return']

    def monitor(self, command):
        return self.call('human-monitor-command', **{'command-line': command})

    def dump(self, base, size, path):
        filename = path.resolve().as_posix()
        if '"' in filename:
            raise ValueError('quote in memory-dump path')
        response = self.monitor(f'pmemsave {base:#x} {size:#x} "{filename}"')
        if response.strip():
            raise RuntimeError(f'pmemsave failed: {response}')
        data = path.read_bytes()
        if len(data) != size:
            raise ValueError('truncated QEMU memory dump')
        return data

    def close(self):
        self.file.close()
        self.sock.close()


def run(build_dir, out, qemu, cpu, load_address, fault_at_park=False, linux_entry=False,
        entry_el2=False, boot_image=None):
    out.mkdir(parents=True, exist_ok=False)
    image = (build_dir / 'diag-core.Image').resolve()
    metadata = json.loads((build_dir / 'build.json').read_text())
    image_data = image.read_bytes()
    if hashlib.sha256(image_data).hexdigest() != metadata['image_sha256']:
        raise ValueError('Image and build manifest disagree')
    if not RAM_BASE + 0x200000 <= load_address <= RAM_END - len(image_data) or load_address % 4096:
        raise ValueError('emulation load address must be page aligned and inside QEMU RAM')
    symbols = {}
    for line in (build_dir / 'symbols.txt').read_text().splitlines():
        words = line.split()
        if len(words) == 3:
            symbols[words[2]] = int(words[0], 16)
    if linux_entry:
        load_address = linux_load_address(image_data)
    if fault_at_park:
        # Deliberately corrupt a COPY, never the deliverable Image or BOOT candidate.
        patched = bytearray(image_data)
        struct.pack_into('<I', patched, symbols['park'], 0)  # UDF #0
        image = (out / 'exception-injected.Image').resolve()
        image.write_bytes(patched)
    container_hash = None
    if boot_image:
        if not linux_entry or fault_at_park:
            raise ValueError('--boot-image requires --linux-entry without fault injection')
        container = boot_image.read_bytes()
        container_hash = hashlib.sha256(container).hexdigest()
        part = inspect_boot(container)['sections']['kernel']
        compressed = container[part['offset']:part['offset'] + part['size']]
        if gzip.decompress(compressed) != image_data:
            raise ValueError('BOOT candidate kernel differs from the build being tested')
        image = (out / 'kernel-extracted-from-boot.gz').resolve()
        image.write_bytes(compressed)
    record_address = load_address + symbols['a52q_diagnostic']
    log = metadata['output'] if isinstance(metadata['output'], dict) else None
    if log and not (RAM_BASE <= log['base'] and log['base'] + log['size'] <= RAM_END):
        raise ValueError('configured output lies outside QEMU test RAM')
    if log and load_address < log['base'] + log['size'] and log['base'] < load_address + len(image_data):
        raise ValueError('emulation load address overlaps log')
    if ',' in image.as_posix():
        raise ValueError('comma in QEMU loader path is unsupported')
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
    version = subprocess.check_output([qemu, '--version'], text=True).splitlines()[0]
    args = [qemu, '-M', 'virt,gic-version=3,virtualization=' + ('on' if entry_el2 else 'off'), '-accel', 'tcg',
            '-cpu', cpu, '-m', '2048', '-smp', '1', '-nodefaults', '-display', 'none',
            '-serial', 'null', '-monitor', 'none', '-nic', 'none', '-no-reboot', '-S',
            '-qmp', f'tcp:127.0.0.1:{port},server=on,wait=off',
            '-d', 'int,guest_errors', '-D', str((out / 'qemu.log').resolve())]
    if linux_entry:
        args += ['-kernel', str(image)]
    else:
        args += ['-device', f'loader,file={image.as_posix()},addr={load_address:#x},force-raw=on,cpu-num=0']
    (out / 'invocation.json').write_text(json.dumps(args, indent=2) + '\n')
    process, qmp = None, None
    result = {'status': 'failed', 'scope': 'QEMU virt diagnostic only; no A52, Samsung loader or XNU emulation',
              'qemu': version, 'cpu': cpu, 'load_address': hex(load_address),
              'image_sha256': metadata['image_sha256'],
              'executed_image_sha256': hashlib.sha256(image.read_bytes()).hexdigest(),
              'fault_injected_into_copy': fault_at_park,
              'expected_current_el': 8 if entry_el2 else 4,
              'host_extracted_boot_container_sha256': container_hash,
              'entry': 'QEMU Linux arm64 boot stub' if linux_entry else 'QEMU generic raw loader'}
    try:
        with (out / 'stderr.txt').open('wb') as stderr:
            process = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                       stderr=stderr, creationflags=0x08000000 if os.name == 'nt' else 0)
            qmp = Qmp(port, process)
            qmp.call('cont')
            deadline = time.monotonic() + 5
            while True:
                time.sleep(0.1)
                qmp.call('stop')
                data = qmp.dump(record_address, len(FIELDS) * 8, out / 'record.bin')
                try:
                    record = decode_record(data)
                    if record['stage'] == 0xff and not fault_at_park:
                        raise RuntimeError(f'guest exception: {record}')
                    expected = 0xff if fault_at_park else 2
                    if record['stage'] != expected:
                        raise ValueError('diagnostic has not completed')
                    if fault_at_park and (record['exception_slot'] != 4 or
                                          record['elr'] != load_address + symbols['park']):
                        raise RuntimeError('fault injection did not reach the expected synchronous exception vector')
                    if (record['image'] != load_address or record['current_el'] != result['expected_current_el']
                            or record['cntfrq'] == 0):
                        raise RuntimeError('unexpected image base, exception level or timer frequency')
                    if log:
                        text = decode_ramlog(qmp.dump(log['base'], log['size'], out / 'ramoops.bin'))
                        if 'A52QDIAG v1' not in text or f'stage=0x{expected:016x}\n' not in text:
                            raise ValueError('RAM console has not completed')
                        (out / 'console.txt').write_text(text)
                    break
                except ValueError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError('no completed diagnostic record before timeout')
                    qmp.call('cont')
            (out / 'registers.txt').write_text(qmp.monitor('info registers'))
            result.update(status='passed', diagnostic=record, ramoops_checked=bool(log))
            qmp.call('quit')
            process.wait(timeout=5)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        result['error'] = str(exc)
    finally:
        if qmp:
            qmp.close()
        if process and process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--qemu', default='qemu-system-aarch64')
    p.add_argument('--cpu', default='cortex-a76')
    p.add_argument('--load-address', type=lambda x: int(x, 0), default=0x40200000)
    p.add_argument('--fault-at-park', action='store_true', help='inject UDF into a COPY to test exception capture')
    p.add_argument('--linux-entry', action='store_true', help='exercise QEMU Linux Image loading and FDT handoff')
    p.add_argument('--entry-el2', action='store_true', help='enable QEMU EL2 and test handoff without dropping privilege')
    p.add_argument('--boot-image', type=Path, help='host-extract and boot the gzip kernel from this Android image; no Samsung emulation')
    a = p.parse_args()
    try:
        result = run(a.build, a.out, a.qemu, a.cpu, a.load_address,
                     a.fault_at_park, a.linux_entry, a.entry_el2, a.boot_image)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        p.exit(1, f'QEMU test failed: {exc}\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
