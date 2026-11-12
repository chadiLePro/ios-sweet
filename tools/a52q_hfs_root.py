"""Container checks for a small, QEMU-only HFS+ root experiment.

Layout: Apple OSS hfs-627.100.6/core/hfs_format.h, pinned by patch 0026.
This checks volume geometry and clean-unmount flags; it is not a filesystem
checker. The image producer must separately run fsck.hfsplus after unmounting.
It deliberately supplies no Samsung storage or physical-memory placement.
"""
import struct

MAX_BYTES = 32 << 20


def validate_hfs_test_root(data):
    if not 8 << 20 <= len(data) <= MAX_BYTES or len(data) % 16384:
        raise ValueError('HFS test root must be 8..32 MiB and 16 KiB aligned')
    header = data[1024:1536]
    signature, version, attributes, _, journal = struct.unpack_from('>HHIII', header)
    if (signature, version) not in ((0x482b, 4), (0x4858, 5)):
        raise ValueError('need a raw HFS+/HFSX volume, not a wrapper or partition image')
    if not attributes & (1 << 8) or attributes & ((1 << 11) | (1 << 14)):
        raise ValueError('HFS test root is not cleanly unmounted')
    block, total, free = struct.unpack_from('>III', header, 40)
    if (not 512 <= block <= 65536 or block & (block - 1) or
            total * block != len(data) or free > total or journal >= total):
        raise ValueError('invalid HFS test volume geometry')
    alt = data[-1024:-512]
    if alt[:4] != header[:4] or alt[40:48] != header[40:48]:
        raise ValueError('HFS alternate volume header geometry differs')
    for offset in range(112, 512, 80):
        logical, _, blocks = struct.unpack_from('>QII', header, offset)
        if blocks > total or logical > blocks * block:
            raise ValueError('HFS metadata fork exceeds volume')
        allocated = 0
        for position in range(offset + 16, offset + 80, 8):
            start, count = struct.unpack_from('>II', header, position)
            if start + count > total or (not count and start):
                raise ValueError('HFS metadata extent exceeds volume')
            allocated += count
        if allocated > blocks:
            raise ValueError('HFS metadata extents exceed fork allocation')
    return {'signature': hex(signature), 'version': version, 'block_size': block,
            'total_blocks': total, 'bytes': len(data), 'journaled': bool(attributes & (1 << 13)),
            'scope': 'volume geometry only; not a substitute for fsck or a boot test'}
