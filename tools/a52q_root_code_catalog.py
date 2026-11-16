#!/usr/bin/env python3
"""Measure signed Mach-O content on a read-only master; never grant trust by path.

This verifies CodeDirectory pages/metadata, not Apple CMS authentication. Cache
containers retain their separate measured policy. No filesystem is modified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import unicodedata

from a52q_userland_audit import inspect

MAGICS = (b'\xcf\xfa\xed\xfe', b'\xca\xfe\xba\xbe', b'\xca\xfe\xba\xbf')
LIMIT = 32 << 20


def arm64_slice(data):
    if data[:4] == MAGICS[0]:
        return data
    if data[:4] not in MAGICS[1:] or len(data) < 8:
        raise ValueError('unsupported Mach-O container')
    count, = struct.unpack_from('>I', data, 4)
    wide = data[:4] == MAGICS[2]
    width = 32 if wide else 20
    if not 0 < count <= 64 or 8 + width * count > len(data):
        raise ValueError('invalid fat architecture table')
    selected = []
    for n in range(count):
        pos = 8 + n * width
        cpu, subtype = struct.unpack_from('>II', data, pos)
        start, size = struct.unpack_from('>QQ' if wide else '>II', data, pos + 8)
        if start < 8 + width * count or start > len(data) or size > len(data) - start:
            raise ValueError('fat slice exceeds file')
        if cpu == 0x100000c and subtype & 0xffffff == 0:
            selected.append(data[start:start + size])
    if len(selected) != 1:
        raise ValueError('requires exactly one plain arm64 slice')
    return selected[0]


def measure(data):
    if len(data) > LIMIT:
        raise ValueError('Mach-O exceeds bounded audit size')
    audit = inspect(arm64_slice(data))
    if audit['arm64e'] or int(audit['subtype'], 16) & 0xffffff:
        raise ValueError('plain arm64 required')
    if audit['filetype'] not in (2, 6, 7, 8):
        raise ValueError('unsupported Mach-O file type')
    if audit.get('encryption_id', 0):
        raise ValueError('encrypted Mach-O requires unsupported runtime decryption')
    sig = audit.get('signature', {})
    if not sig.get('directories'):
        raise ValueError('no standalone CodeDirectory (may be a cache-only stub)')
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                slice_sha256=audit['sha256'], filetype=audit['filetype'],
                directories=sig['directories'],
                entitlement_blobs=sig.get('entitlement_blobs', {}),
                entitlement_key_count=len(sig.get('entitlement_keys', [])))


def scan(root, master_sha256):
    root = root.resolve()
    if not os.statvfs(root).f_flag & os.ST_RDONLY:
        raise ValueError('catalog scan requires a read-only mounted master')
    files, rejected, unreadable, regular, seen = [], [], [], 0, {}
    def onerror(error):
        raise error  # A partial directory walk must never look complete.
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=onerror):
        dirs.sort()
        for name in sorted(names):
            path = Path(directory) / name
            try:
                info = path.lstat()
            except FileNotFoundError:
                # Linux HFS lookup can differ from readdir for Unicode names.
                # Try equivalent spellings without ever modifying the master.
                original = path
                for form in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    candidate = path.with_name(unicodedata.normalize(form, name))
                    try:
                        info = candidate.lstat()
                    except FileNotFoundError:
                        continue
                    path = candidate
                    break
                else:
                    unreadable.append('/' + original.relative_to(root).as_posix())
                    continue  # Unmeasured content is never added to admission.
            if not stat.S_ISREG(info.st_mode):
                continue
            regular += 1
            identity = (info.st_dev, info.st_ino)
            relative = '/' + path.relative_to(root).as_posix()
            if identity in seen:
                # Preserve aliases without rehashing hard-linked cryptex copies.
                row = seen[identity]
                if row is not None:
                    row['paths'].append(relative)
                continue
            seen[identity] = None
            with path.open('rb') as stream:
                magic = stream.read(4)
                if magic not in MAGICS:
                    continue
                if info.st_size > LIMIT:
                    rejected.append(dict(path=relative, reason='Mach-O exceeds audit bound'))
                    continue
                data = magic + stream.read(LIMIT)
            try:
                row = measure(data)
            except (ValueError, struct.error) as error:
                rejected.append(dict(path=relative, reason=str(error)))
                continue
            row['paths'] = [relative]
            files.append(row)
            seen[identity] = row
            if len(files) % 100 == 0:
                print('A52_CATALOG_PROGRESS', regular, len(files), flush=True)
    return dict(format='a52q-root-code-catalog-v1', build='20H392',
                master_sha256=master_sha256, complete_walk=True,
                regular_paths=regular, measured_files=files, rejected=rejected,
                unreadable_paths=unreadable,
                scope='signed page/slot consistency on immutable master; not CMS trust or execution')


def entries(report):
    if report.get('format') != 'a52q-root-code-catalog-v1' or report.get('build') != '20H392' or not report.get('complete_walk'):
        raise ValueError('complete 20H392 catalog required')
    digest = bytes.fromhex(report['master_sha256'])
    if len(digest) != 32:
        raise ValueError('master SHA256 required')
    pins = {}
    for row in report['measured_files']:
        slots = row['entitlement_blobs']
        for slot, blob in slots.items():
            if slot not in ('5', '7') or blob.get('special_slot_hashes_match') is not True or len(bytes.fromhex(blob['sha256'])) != 32:
                raise ValueError('unverified signed metadata')
        lengths = tuple(slots.get(str(slot), {}).get('bytes', 0) for slot in (5, 7))
        for cd in row['directories']:
            if cd['executable_page_hashes_match'] is not True:
                raise ValueError('unverified code pages')
            pin = bytes.fromhex(cd['cdhash'])
            if len(pin) != 20 or any(n < 0 or n > 1 << 20 for n in lengths):
                raise ValueError('invalid identity or signed-slot sizes')
            if pin in pins and pins[pin] != lengths:
                raise ValueError('inconsistent metadata for the same CodeDirectory')
            pins[pin] = lengths
    if not pins:
        raise ValueError('empty code catalog')
    return sorted(pins.items())


def header(report):
    rows = entries(report)
    lines = ['/* Generated by a52q_root_code_catalog.py; measured identities, not CMS trust. */',
             '#ifndef A52Q_ROOT_CODE_CATALOG_H', '#define A52Q_ROOT_CODE_CATALOG_H',
             '#define A52Q_ROOT_CODE_MASTER_SHA256 "' + report['master_sha256'] + '"',
             'struct a52q_root_code_pin { uint8_t cdhash[20]; uint32_t xml_bytes, der_bytes; };',
             'static const struct a52q_root_code_pin a52q_root_code_pins[] = {']
    for pin, sizes in rows:
        lines.append('    {{' + ','.join(f'0x{v:02x}' for v in pin) + '},' + ','.join(map(str, sizes)) + '},')
    lines += ['};', '#endif', '']
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    scan_args = sub.add_parser('scan')
    scan_args.add_argument('--root', type=Path, required=True)
    scan_args.add_argument('--master-sha256', required=True)
    emit_args = sub.add_parser('header')
    emit_args.add_argument('--catalog', type=Path, required=True)
    emit_args.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    if a.command == 'scan':
        report = scan(a.root, a.master_sha256)
        entries(report)
        print('A52_ROOT_CODE_CATALOG_JSON=' + json.dumps(report, separators=(',', ':')), flush=True)
    else:
        a.out.write_text(header(json.loads(a.catalog.read_text())), encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
