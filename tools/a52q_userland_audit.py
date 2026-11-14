"""Inspect bounded Mach-O files without modifying/signing/executing them.

Mach-O/CodeDirectory layouts: pinned XNU mach-o/loader.h and cs_blobs.h.
Reports format and hash consistency, not Apple CMS trust or runtime support.
"""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import struct


def cstring(data, offset):
    if not 0 <= offset < len(data): raise ValueError('string offset exceeds command')
    end = data.find(b'\0', offset)
    if end < 0: raise ValueError('unterminated Mach-O string')
    return data[offset:end].decode('utf-8')


def signature(data, start, size):
    blob = data[start:start + size]
    if len(blob) != size or size < 12: raise ValueError('signature exceeds file')
    magic, length, count = struct.unpack_from('>III', blob)
    if magic != 0xfade0cc0 or length > size or count > 64 or 12 + count * 8 > length:
        raise ValueError('invalid signature SuperBlob')
    result = {'directories': [], 'entitlement_keys': [], 'cms_present': False}
    for n in range(count):
        slot, offset = struct.unpack_from('>II', blob, 12 + n * 8)
        if offset < 12 + count * 8 or offset + 8 > length: raise ValueError('signature slot exceeds blob')
        tag, size = struct.unpack_from('>II', blob, offset)
        if size < 8 or offset + size > length: raise ValueError('signature subblob exceeds blob')
        item = blob[offset:offset + size]
        if slot == 5 and tag == 0xfade7171:
            result['entitlement_keys'] = sorted(plistlib.loads(item[8:]).keys())
        if slot == 7: result['der_entitlements_present'] = True
        if slot == 0x10000: result['cms_present'] = True
        if tag != 0xfade0c02: continue
        if size < 44: raise ValueError('truncated CodeDirectory')
        version, flags, hashes, identifier, special, pages, limit = struct.unpack_from('>7I', item, 8)
        hash_size, hash_type, platform, shift = item[36:40]
        algorithm = {1: 'sha1', 2: 'sha256', 3: 'sha256', 4: 'sha384'}.get(hash_type)
        if not algorithm or shift > 20 or not hash_size or hash_size > hashlib.new(algorithm).digest_size:
            raise ValueError('unsupported CodeDirectory hash geometry')
        if version >= 0x20300 and limit == 0 and size >= 64:
            limit = struct.unpack_from('>Q', item, 56)[0]
        if (limit > start or pages != (limit + (1 << shift) - 1) >> shift or
                hashes < special * hash_size or hashes + pages * hash_size > size):
            raise ValueError('CodeDirectory exceeds signed file or hash array')
        for i in range(pages):
            lo = i << shift; hi = min(limit, lo + (1 << shift))
            expected = item[hashes + i * hash_size:hashes + (i + 1) * hash_size]
            if hashlib.new(algorithm, data[lo:hi]).digest()[:hash_size] != expected:
                raise ValueError('CodeDirectory executable-page hash mismatch')
        result['directories'].append(dict(slot=slot, identifier=cstring(item, identifier),
            version=hex(version), flags=hex(flags), hash_type=hash_type, platform=platform,
            page_bytes=1 << shift, pages=pages, executable_page_hashes_match=True,
            cdhash=hashlib.new(algorithm, item).digest()[:20].hex()))
    return result


def inspect(data):
    if len(data) < 32 or len(data) > 32 << 20: raise ValueError('bounded Mach-O required')
    magic, cpu, subtype, kind, count, size, flags, _ = struct.unpack_from('<8I', data)
    if magic != 0xfeedfacf or cpu != 0x100000c or count > 1024 or size > len(data) - 32:
        raise ValueError('need a thin ARM64 Mach-O with valid commands')
    result = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), cpu=hex(cpu),
        subtype=hex(subtype), arm64e=(subtype & 0xffffff) == 2, filetype=kind,
        flags=hex(flags), dylibs=[], segments=[])
    offset = 32
    for _ in range(count):
        if offset + 8 > 32 + size: raise ValueError('truncated load command')
        cmd, length = struct.unpack_from('<II', data, offset)
        if length < 8 or length % 8 or offset + length > 32 + size:
            raise ValueError('invalid load command length')
        item = data[offset:offset + length]
        if cmd in (0xc, 0x80000018, 0x8000001f, 0x80000023):
            if length < 24: raise ValueError('truncated dylib command')
            result['dylibs'].append(cstring(item, struct.unpack_from('<I', item, 8)[0]))
        elif cmd == 0xe:
            result['dylinker'] = cstring(item, struct.unpack_from('<I', item, 8)[0])
        elif cmd == 0x32:
            result['build_platform'], result['minimum_os'], result['sdk'] = struct.unpack_from('<3I', item, 8)
        elif cmd == 0x80000028:
            result['main_entry_offset'], = struct.unpack_from('<Q', item, 8)
        elif cmd == 0x2c:
            if length != 24: raise ValueError('invalid encryption command')
            result['encryption_id'] = struct.unpack_from('<I', item, 16)[0]
        elif cmd == 0x1d:
            if length != 16: raise ValueError('invalid signature command')
            result['signature'] = signature(data, *struct.unpack_from('<II', item, 8))
        elif cmd == 0x19:
            if length < 72: raise ValueError('invalid segment command')
            va, memory, position, disk, maximum, protection = struct.unpack_from('<4Q2I', item, 24)
            if position > len(data) or disk > len(data) - position or disk > memory:
                raise ValueError('segment exceeds file or VM size')
            result['segments'].append(dict(name=cstring(item, 8), vm=hex(va),
                memory=memory, disk=disk, file_offset=position, protection=protection))
        offset += length
    if offset != 32 + size: raise ValueError('load commands do not fill header')
    result['scope'] = 'format and executable-page hashes only; no CMS authentication or execution claim'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path)
    args = parser.parse_args()
    try:
        reports = {}
        for path in args.files:
            if path.stat().st_size > 32 << 20: raise ValueError('input exceeds audit bound')
            with path.open('rb') as stream: data = stream.read((32 << 20) + 1)
            reports[str(path)] = inspect(data)
        print(json.dumps(reports, indent=2))
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f'Userland audit rejected: {error}\n')
