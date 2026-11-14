"""Audit the exact shared-cache files used by the validated full-root master.

Run against a read-only mounted image or the checksum-identical native staging
tree. Uses bounded streaming/mmap, never modifies files, and verifies every
CodeDirectory page hash. CMS presence is reported, not authenticated.
"""
import argparse
import hashlib
import json
import mmap
from pathlib import Path
import stat
import struct
from a52q_userland_audit import signature

PREFIX = 'System/Library/Caches/com.apple.dyld/'


def audit_file(path, expected_sha256):
    before = path.stat()
    if not stat.S_ISREG(before.st_mode) or not 512 <= before.st_size <= 4 << 30:
        raise ValueError('cache must be a regular bounded file')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1 << 20): digest.update(block)
        if digest.hexdigest() != expected_sha256:
            raise ValueError(f'{path.name}: original file checksum differs')
        with mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
            if data[:16] != b'dyld_v1   arm64\0':
                raise ValueError('need the audited plain arm64 cache format')
            offset, size = struct.unpack_from('<QQ', data, 40)
            if offset == size == 0 and path.name.endswith('.symbols'):
                result = dict(directories=[], entitlement_keys=[], cms_present=False,
                              scope='unmapped symbols sidecar; no executable pin')
            else:
                if size == 0: size = len(data) - offset
                if offset < 512 or not 12 <= size <= 32 << 20 or offset + size > len(data):
                    raise ValueError('invalid bounded cache signature geometry')
                result = signature(data, offset, size)
                if not result['directories'] or result['entitlement_keys'] or result.get('der_entitlements_present'):
                    raise ValueError('cache pin requires signed entitlement-free cache data')
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('cache changed during verification')
    return dict(name=path.name, bytes=before.st_size, sha256=digest.hexdigest(), **result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('cache-dir', 'checksums', 'master-report', 'out'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.out.exists(): raise ValueError('output exists')
        master = json.loads(args.master_report.read_text())
        if (master.get('hfs_fsck_passed') is not True or master.get('readonly_fsck_passed') is not True or
                master.get('core_checksums_passed') != 47):
            raise ValueError('need the completed full-root validation report')
        expected = {}
        for line in args.checksums.read_text().splitlines():
            digest, name = line.split(None, 1)
            if name.startswith(PREFIX):
                name = name[len(PREFIX):]
                if '/' in name or name in expected: raise ValueError('ambiguous cache checksum list')
                expected[name] = digest
        if len(expected) != 44: raise ValueError('need all 44 original 20H392 cache files')
        files = []
        for name, digest in expected.items():
            files.append(audit_file(args.cache_dir / name, digest))
            print('Verified cache', name, flush=True)
        pins = sorted({d['cdhash'] for f in files for d in f['directories']})
        result = dict(master_sha256=master['sha256'], files=files, cdhashes=pins,
            original_cache_file_checksums_passed=len(files), executable_page_hashes_checked=True,
            entitlements_granted=False,
            scope='exact original cache bytes and CodeDirectory hashes; no Apple CMS trust or runtime claim')
        with args.out.open('x') as stream: json.dump(result, stream, indent=2)
        print(f'PASS: {len(files)} original cache files, {len(pins)} CodeDirectory pins')
    except (OSError, ValueError, KeyError, struct.error) as error:
        parser.exit(1, f'Cache audit rejected: {error}\n')


if __name__ == '__main__': main()
