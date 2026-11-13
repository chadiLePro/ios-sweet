#!/usr/bin/env python3
"""Prepare an UNSIGNED, UNTESTED BOOT candidate using captured device metadata.

Never connects to a device. No flashing, vbmeta patching, Odin package, or
claim of Samsung bootloader acceptance. Requires the pinned AOSP mkbootimg:
https://android.googlesource.com/platform/system/tools/mkbootimg/+/refs/tags/android-11.0.0_r48/mkbootimg.py
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
from android_boot_evidence import inspect, kernel_contract, template_trailer
from a52q_ramoops import configuration
from fdt_evidence import Fdt

MKBOOTIMG_SHA256 = '5579fb6bcb9e89e790a70fb9ccf3c00cf56e3e46aef74d84fcb0964887e5576e'


def verify_overlay(data, live):
    if len(data) < 32:
        raise ValueError('truncated DTBO table')
    magic, total, hs, es, count, off, _, version = struct.unpack_from('>8I', data)
    if (magic != 0xd7b7ab1e or not 32 <= total <= len(data) or hs != 32 or es != 32 or
            not 1 <= count <= 256 or off < hs or off + count * es > total or version != 0):
        raise ValueError('unsupported DTBO table')
    board = live.nodes['/'].props.get('qcom,board-id')
    live_logs = [n for n in live.nodes.values() if 'ramoops' in n.strings('compatible') and n.enabled()]
    if board is None or len(live_logs) != 1:
        raise ValueError('need live board ID and one ramoops node')
    matches = []
    for i in range(count):
        size, pos = struct.unpack_from('>II', data, off + i * es)
        if pos < off + count * es or pos + size > total:
            raise ValueError('DTBO entry outside table')
        tree = Fdt(data[pos:pos + size])
        if tree.nodes['/'].props.get('qcom,board-id') == board:
            matches.append((i, tree))
    if len(matches) != 1:
        raise ValueError('no unique DTBO match for live board ID')
    index, overlay = matches[0]
    nodes = [n for n in overlay.nodes.values() if 'ramoops' in n.strings('compatible')]
    if len(nodes) != 1:
        raise ValueError('selected overlay has no unique ramoops configuration')
    for k in ('reg', 'record-size', 'console-size', 'ftrace-size', 'pmsg-size', 'ecc-size', 'mem-type'):
        if nodes[0].props.get(k) != live_logs[0].props.get(k):
            raise ValueError(f'selected boot DTBO differs from live ramoops: {k}')
    return index


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--evidence', type=Path, required=True)
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--mkbootimg', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--ufs-diagnostic-root', type=Path, help='exact QEMU-proven HFS fixture selected by payload')
    p.add_argument('--ufs-root-gpt-capture', type=Path, help='matching captured GPT/sysfs evidence')
    a = p.parse_args()
    try:
        if a.out.exists():
            raise ValueError('refusing to overwrite existing output')
        if hashlib.sha256(a.mkbootimg.read_bytes()).hexdigest() != MKBOOTIMG_SHA256:
            raise ValueError('use the pinned, unmodified AOSP mkbootimg script')
        log = configuration(a.evidence)
        live = Fdt((a.evidence / 'live.dtb').read_bytes())
        overlay = verify_overlay((a.evidence / 'dtbo.img').read_bytes(), live)
        original = (a.evidence / 'boot.img').read_bytes()
        info = inspect(original)
        trailer = template_trailer(original, info)
        if len(original) != 100663296:
            raise ValueError('need the complete observed 96 MiB BOOT partition dump')
        contract = kernel_contract(original, info)
        if info['header_version'] != 2 or info['page_size'] != 4096 or 'dtb' not in info['sections']:
            raise ValueError('expected observed v2/4096/DTB boot template')
        if 'second' in info['sections'] or 'recovery_dtbo' in info['sections']:
            raise ValueError('BOOT template unexpectedly contains second/recovery_dtbo')
        vbmeta = (a.evidence / 'vbmeta.img').read_bytes()
        if len(vbmeta) < 256 or vbmeta[:4] != b'AVB0' or not struct.unpack_from('>I', vbmeta, 120)[0] & 2:
            raise ValueError('captured vbmeta does not already disable verification; no policy changes implemented')
        build = json.loads((a.build / 'build.json').read_text())
        payload = build.get('embedded_payload', {})
        root_config = payload.get('ufs_diagnostic_root')
        if bool(a.ufs_diagnostic_root) != bool(root_config) or bool(a.ufs_root_gpt_capture) != bool(root_config):
            raise ValueError('BOOT root requires payload configuration, exact fixture and GPT evidence together')
        if build.get('embedded_payload', {}).get('environment', '') not in ('', 'SM-A525F/DS hardware candidate'):
            raise ValueError('refusing to package an emulation/test payload for a phone')
        raw = (a.build / 'diag-core.Image').read_bytes()
        if (build['output'] != log or build['template_kernel_contract'] != contract or
                hashlib.sha256(raw).hexdigest() != build['image_sha256'] or
                raw[56:60] != b'ARM\x64' or struct.unpack_from('<Q', raw, 8)[0] != contract['text_offset']):
            raise ValueError('diagnostic build is not bound to this evidence/template')
        if root_config:
            from a52q_payload import validate_payload
            symbols = {w[2]: int(w[0], 16) for line in (a.build / 'symbols.txt').read_text().splitlines()
                       if len(w := line.split()) == 3}
            start, end = symbols['_payload_start'], symbols['_payload_end']
            if not 0 <= start < end <= len(raw):
                raise ValueError('embedded disk-root payload bounds differ from Image')
            validate_payload(raw[start:end], payload)
        # Never carry the original signed footer/hash forward after replacing a kernel.
        cmdline = (original[64:576].split(b'\0')[0] + original[608:1632].split(b'\0')[0]).decode('ascii')
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=a.out.parent) as d:
            d = Path(d)
            kernel = d / 'Image.gz'
            kernel.write_bytes(gzip.compress(raw, mtime=0))
            args = [sys.executable, str(a.mkbootimg.resolve()), '--header_version', '2',
                    '--base', '0', '--pagesize', '4096', '--kernel', str(kernel),
                    '--kernel_offset', info['kernel_addr'], '--ramdisk_offset', info['ramdisk_addr'],
                    '--tags_offset', info['tags_addr'], '--dtb_offset', info['dtb_addr'],
                    '--board', info['name'], '--cmdline', cmdline,
                    '--os_version', info['os_version'], '--os_patch_level', info['os_patch_level']]
            for name in ('ramdisk', 'dtb'):
                part = info['sections'][name]
                dest = d / name
                dest.write_bytes(original[part['offset']:part['offset'] + part['size']])
                args += ['--' + name, str(dest)]
            candidate = d / 'candidate.img'
            subprocess.run(args + ['-o', str(candidate)], check=True)
            packed = candidate.read_bytes()
            check = inspect(packed)
            kernel_section = check['sections']['kernel']
            packed_kernel = packed[kernel_section['offset']:kernel_section['offset'] + kernel_section['size']]
            if gzip.decompress(packed_kernel) != raw:
                raise ValueError('round-trip changed diagnostic kernel')
            packed_cmdline = packed[64:576].split(b'\0')[0] + packed[608:1632].split(b'\0')[0]
            if packed_cmdline != cmdline.encode('ascii'):
                raise ValueError('round-trip changed embedded command line')
            for key in ('header_version', 'page_size', 'kernel_addr', 'ramdisk_addr',
                        'tags_addr', 'dtb_addr', 'name', 'os_version_raw'):
                if check[key] != info[key]:
                    raise ValueError(f'round-trip changed header field {key}')
            for name in ('ramdisk', 'dtb'):
                if check['sections'][name]['sha256'] != info['sections'][name]['sha256']:
                    raise ValueError(f'round-trip changed {name}')
            if len(packed) > len(original) or check['avb_footer']:
                raise ValueError('invalid candidate size or stale AVB footer')
            packed += trailer
            if template_trailer(packed) != trailer:
                raise ValueError('round-trip changed Samsung trailer')
            root_plan = None
            if root_config:
                from a52q_ufs_root import validate_packaging
                root_data = a.ufs_diagnostic_root.read_bytes()
                root_plan = validate_packaging(root_config, payload['ufs_selftest'], root_data,
                                               a.ufs_root_gpt_capture, len(packed))
                offset = root_plan['offset_in_boot_bytes']
                packed += bytes(offset - len(packed)) + root_data
                if packed[offset:offset + len(root_data)] != root_data or len(packed) != len(original):
                    raise ValueError('round-trip changed diagnostic root or BOOT bounds')
            # Full partition-sized output clears old AVB metadata at the tail
            # even when a recovery writer does not erase unwritten tail blocks.
            packed += bytes(len(original) - len(packed))
            if inspect(packed)['avb_footer']:
                raise ValueError('unexpected AVB footer after padding')
            a.out.write_bytes(packed)
        report = {'status': 'PACKAGED ONLY; UNTESTED, UNSIGNED; do not flash without reviewing docs/A52Q.md',
                  'intended_partition': 'BOOT only; no device-writing command implemented',
                  'bytes': len(packed), 'sha256': hashlib.sha256(packed).hexdigest(),
                  'template_boot_sha256': info['sha256'], 'dtbo_entry': overlay,
                  'seandroid_trailer_preserved': bool(trailer),
                  'kernel_contract': contract, 'candidate_ramoops': log,
                  'remaining': ['Samsung acceptance of unsigned boot image', 'actual entry EL and CPU feature report',
                                'ramoops retention across reset', 'integrity-checked diagnostic record in TWRP']}
        if root_plan:
            report['ufs_diagnostic_root'] = dict(root_config, packed_layout=root_plan)
        a.out.with_suffix(a.out.suffix + '.json').write_text(json.dumps(report, indent=2) + '\n')
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        p.exit(1, f'packaging refused: {exc}\n')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
