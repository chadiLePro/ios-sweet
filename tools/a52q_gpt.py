"""Audit captured GPT metadata against Linux partition bounds; no device access.

All offsets come from CRC-checked primary/backup tables. This tool neither
selects a filesystem nor writes a partition, and reports no device GUIDs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib


def header(data, block, disk_blocks, current):
    if len(data) != block or data[:8] != b'EFI PART':
        raise ValueError('invalid GPT header block')
    revision, size, crc, reserved = struct.unpack_from('<4I', data, 8)
    if revision != 0x10000 or not 92 <= size <= block or reserved:
        raise ValueError('unsupported GPT header')
    check = bytearray(data[:size]); struct.pack_into('<I', check, 16, 0)
    if zlib.crc32(check) != crc:
        raise ValueError('GPT header CRC mismatch')
    here, other, first, last = struct.unpack_from('<4Q', data, 24)
    entries, count, width, array_crc = struct.unpack_from('<Q3I', data, 72)
    if (here != current or other != (disk_blocks - 1 if current == 1 else 1) or
            not 2 <= first <= last < disk_blocks - 1 or not 1 <= count <= 512 or
            not 128 <= width <= 1024 or width & (width - 1) or count * width > 65536):
        raise ValueError('invalid GPT geometry')
    blocks = (count * width + block - 1) // block
    if not ((current == 1 and 2 <= entries and entries + blocks <= first) or
            (current == disk_blocks - 1 and last < entries and entries + blocks <= current)):
        raise ValueError('GPT entry array overlaps usable space')
    return {'first': first, 'last': last, 'count': count, 'width': width,
            'array_crc': array_crc, 'guid': data[56:72]}


def audit(primary, backup, entries, backup_entries, block, disk_bytes, sysfs):
    if not 512 <= block <= 65536 or block & (block - 1) or disk_bytes % block:
        raise ValueError('invalid logical block size/capacity')
    a = header(primary, block, disk_bytes // block, 1)
    b = header(backup, block, disk_bytes // block, disk_bytes // block - 1)
    if a != b or entries != backup_entries:
        raise ValueError('primary and backup GPT disagree')
    if len(entries) != a['count'] * a['width'] or zlib.crc32(entries) != a['array_crc']:
        raise ValueError('GPT entry-array CRC/length mismatch')
    result, seen_names = [], set()
    for index in range(a['count']):
        entry = entries[index * a['width']:(index + 1) * a['width']]
        if entry[:16] == bytes(16): continue
        first, last = struct.unpack_from('<2Q', entry, 32)
        name = entry[56:128].decode('utf-16le').split('\0', 1)[0]
        if not a['first'] <= first <= last <= a['last'] or not name or name in seen_names:
            raise ValueError('invalid/ambiguous GPT partition')
        seen_names.add(name)
        sectors = (first * (block // 512), (last - first + 1) * (block // 512))
        if sysfs.get(index + 1) != sectors:
            raise ValueError('GPT partition differs from live sysfs bounds')
        result.append({'index': index + 1, 'name': name, 'first_lba': first,
            'block_count': last - first + 1, 'offset_bytes': first * block,
            'bytes': (last - first + 1) * block})
    if len(sysfs) != len(result):
        raise ValueError('live partition count differs from GPT')
    ordered = sorted(result, key=lambda p: p['first_lba'])
    if any(p['first_lba'] + p['block_count'] > q['first_lba'] for p, q in zip(ordered, ordered[1:])):
        raise ValueError('overlapping GPT partitions')
    return {'block_bytes': block, 'disk_bytes': disk_bytes, 'partitions': result,
            'scope': 'CRC-checked GPT/sysfs bounds only; no filesystem or write authorization'}


def from_capture(directory):
    capture = json.loads((directory / 'capture.json').read_text())
    data = {}
    for name in ('primary-header.bin', 'backup-header.bin', 'primary-entries.bin', 'backup-entries.bin'):
        raw = (directory / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != capture['files'][name]:
            raise ValueError('GPT capture hash mismatch')
        data[name] = raw
    rows = [tuple(map(int, row.split())) for row in capture['sysfs']]
    if any(len(row) != 3 for row in rows) or len({row[0] for row in rows}) != len(rows):
        raise ValueError('ambiguous sysfs evidence')
    return audit(data['primary-header.bin'], data['backup-header.bin'], data['primary-entries.bin'],
        data['backup-entries.bin'], capture['block_bytes'], capture['disk_bytes'],
        {row[0]: (row[1], row[2]) for row in rows})


def diagnostic_boot_tail(report, root_bytes, packed_boot_end):
    """Plan a small diagnostic filesystem in BOOT padding; writes nothing.

    This is a new software layout, not a captured firmware address. A future
    packager/partition driver must independently check and implement it before
    any trial; current images and kernels do not consume this plan.
    """
    block = report['block_bytes']
    candidates = [p for p in report['partitions'] if p['name'] == 'boot']
    if (block != 4096 or len(candidates) != 1 or candidates[0]['index'] != 19 or
            candidates[0]['bytes'] != 96 << 20 or not 8 << 20 <= root_bytes <= 32 << 20 or
            root_bytes % block or packed_boot_end <= 0):
        raise ValueError('unsupported A52 diagnostic BOOT layout')
    boot = candidates[0]
    offset = boot['bytes'] - root_bytes
    if packed_boot_end > offset:
        raise ValueError('diagnostic filesystem overlaps packed BOOT content/trailer')
    return {'partition': 'BOOT only', 'offset_in_boot_bytes': offset,
            'first_lba': boot['first_lba'] + offset // block, 'block_count': root_bytes // block,
            'bytes': root_bytes, 'scope': 'software layout proposal only; no image or partition modified'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture', type=Path)
    args = parser.parse_args()
    try: print(json.dumps(from_capture(args.capture), indent=2))
    except (ValueError, KeyError, OSError) as error: parser.exit(1, f'GPT audit rejected: {error}\n')
