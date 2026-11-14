"""Prepare a READ-ONLY full iOS root plan from verified regular host files.

No device access, formatting, image mutation or authorization to write. The
kernel rechecks live primary GPT CRCs and userdata bounds before publishing.
Local fsck/checksum reports are provenance, not Apple signature authentication.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import struct
import zlib
from a52q_gpt import from_capture
from a52q_hfs_root import validate_volume_headers
from mkadt import node, u32, u64

ROOT_BYTES = 16 << 30


def inspect_master(path, proof):
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size != ROOT_BYTES:
        raise ValueError('full root must be a regular 16 GiB image file')
    if (proof.get('bytes') != ROOT_BYTES or proof.get('hfs_fsck_passed') is not True or
            proof.get('readonly_fsck_passed') is not True or proof.get('readonly_fsck_pending') is not False or
            proof.get('journaled') is not False or proof.get('core_checksums_passed') != 47):
        raise ValueError('need completed read-only fsck and 47 original core/cache checksums')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        first = stream.read(4096)
        digest.update(first)
        for _ in range((ROOT_BYTES - 4096) // (1 << 20) + 1):
            data = stream.read(min(1 << 20, ROOT_BYTES - stream.tell()))
            digest.update(data)
        if stream.tell() != ROOT_BYTES or stream.read(1):
            raise ValueError('full root changed size during streaming validation')
        stream.seek(ROOT_BYTES - 1024); alt = stream.read(512)
    if digest.hexdigest() != proof.get('sha256'):
        raise ValueError('full root differs from validated master hash')
    volume = validate_volume_headers(first[1024:1536], alt, ROOT_BYTES)
    if volume['journaled']:
        raise ValueError('persistent read-only root must be non-journaled')
    return dict(sha256=digest.hexdigest(), bytes=ROOT_BYTES, header_crc32=zlib.crc32(first), volume=volume)


def validate_config(config, ufs):
    parent, parent_count, first, count = config['window']
    capacity = ufs['last_lba'] + 1
    crcs = config['gpt_crc32']
    if (config.get('layout_kind') != 2 or config.get('partition_index') != 31 or
            config.get('partition_name') != 'userdata' or ufs['block_bytes'] != 4096 or
            config['ufs_nonce'] != ufs['nonce'] or parent < 2 or parent > capacity or
            parent_count > capacity - parent or count != ROOT_BYTES // 4096 or
            count > parent_count or first != parent or config['bytes'] != ROOT_BYTES or
            config['offset_in_partition_bytes'] != 0 or config['volume']['bytes'] != ROOT_BYTES or
            config['volume']['journaled'] is not False or len(crcs) != 2 or
            any(not isinstance(v, int) or not 0 <= v <= 0xffffffff for v in crcs) or
            not 0 <= config['header_crc32'] <= 0xffffffff or
            not re.fullmatch('[0-9a-f]{64}', config['sha256']) or
            not re.fullmatch('[0-9a-f]{64}', config['kernel_sha256'])):
        raise ValueError('invalid read-only full-root userdata window')


def configuration(capture, ufs, master, kernel_hash):
    report = from_capture(capture)
    if report['block_bytes'] != 4096 or report['disk_bytes'] != (ufs['last_lba'] + 1) * 4096:
        raise ValueError('GPT and physical UFS proof capacity differ')
    matches = [p for p in report['partitions'] if p['name'] == 'userdata' and p['index'] == 31]
    if len(matches) != 1 or matches[0]['bytes'] < ROOT_BYTES:
        raise ValueError('captured userdata cannot contain full root')
    part = matches[0]; header = (capture / 'primary-header.bin').read_bytes()
    entries, count, width = struct.unpack_from('<QII', header, 72)
    if entries != 2 or not 31 <= count <= 128 or width != 128:
        raise ValueError('GPT layout not supported by runtime reader')
    result = dict(master, layout_kind=2, partition_index=31, partition_name='userdata',
        window=[part['first_lba'], part['block_count'], part['first_lba'], ROOT_BYTES // 4096],
        ufs_nonce=ufs['nonce'], offset_in_partition_bytes=0, kernel_sha256=kernel_hash,
        gpt_crc32=[struct.unpack_from('<I', header, 16)[0], struct.unpack_from('<I', header, 88)[0]],
        gpt_capture_sha256=hashlib.sha256((capture / 'capture.json').read_bytes()).hexdigest(),
        scope='host preparation only; overwrites Android userdata if installed; no Apple-userland boot claim')
    validate_config(result, ufs)
    return result


def adt_node(config):
    return node('a52q-ufs-root', [('window', u64(*config['window'])),
        ('ufs-nonce', u64(config['ufs_nonce'])), ('header-crc32', u32(config['header_crc32'])),
        ('layout-kind', u32(2)), ('gpt-crc32', u32(*config['gpt_crc32']))])


def bind_plan(plan, ufs, kernel_hash):
    """Bind an immutable storage plan to this candidate's fresh log nonce."""
    validate_config(plan, dict(ufs, nonce=plan['ufs_nonce']))
    if plan['kernel_sha256'] != kernel_hash:
        raise ValueError('full root plan kernel hash differs')
    bound = dict(plan, ufs_nonce=ufs['nonce'])
    validate_config(bound, ufs)
    return bound


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('image', 'validation', 'gpt-capture', 'ufs-payload', 'kernel', 'out'):
        parser.add_argument('--' + arg, type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.out.exists(): raise ValueError('output exists')
        ufs = json.loads(args.ufs_payload.read_text())['ufs_selftest']
        master = inspect_master(args.image, json.loads(args.validation.read_text()))
        result = configuration(args.gpt_capture, ufs, master, hashlib.sha256(args.kernel.read_bytes()).hexdigest())
        args.out.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
    except (OSError, KeyError, ValueError, struct.error) as error:
        parser.exit(1, f'Full root preparation rejected: {error}\n')


if __name__ == '__main__':
    main()
