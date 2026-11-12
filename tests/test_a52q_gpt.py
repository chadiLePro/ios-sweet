"""Synthetic GPT only: reject damaged or mismatching partition evidence."""
from pathlib import Path
import struct
import sys
import unittest
import zlib
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_gpt import audit, diagnostic_boot_tail


def fixture(overlap=False):
    block, blocks = 4096, 4096
    entries = bytearray(4 * 128)
    ranges = [(32, 95, 'boot'), (50 if overlap else 96, 1000, 'userdata')]
    sysfs = {}
    for index, (first, last, name) in enumerate(ranges):
        entries[index * 128:index * 128 + 16] = b'T' * 16
        struct.pack_into('<2Q', entries, index * 128 + 32, first, last)
        encoded = name.encode('utf-16le')
        entries[index * 128 + 56:index * 128 + 56 + len(encoded)] = encoded
        sysfs[index + 1] = (first * 8, (last - first + 1) * 8)
    def header(current, other, location):
        data = bytearray(block); data[:8] = b'EFI PART'
        struct.pack_into('<4I4Q', data, 8, 0x10000, 92, 0, 0, current, other, 6, 4090)
        data[56:72] = b'G' * 16
        struct.pack_into('<Q3I', data, 72, location, 4, 128, zlib.crc32(entries))
        struct.pack_into('<I', data, 16, zlib.crc32(data[:92]))
        return data
    return [header(1, blocks - 1, 2), header(blocks - 1, 1, blocks - 2),
            entries, entries.copy(), block, block * blocks, sysfs]


class GptTests(unittest.TestCase):
    def test_verified_bounds(self):
        result = audit(*fixture())
        self.assertEqual(result['partitions'][0]['offset_bytes'], 32 * 4096)
        self.assertEqual(result['partitions'][1]['block_count'], 905)

    def test_header_crc(self):
        args = fixture(); args[0][40] ^= 1
        with self.assertRaisesRegex(ValueError, 'header CRC'): audit(*args)

    def test_array_damage_and_backup_mismatch(self):
        args = fixture(); args[2][10] ^= 1; args[3][10] ^= 1
        with self.assertRaisesRegex(ValueError, 'array CRC'): audit(*args)
        args = fixture(); args[3][10] ^= 1
        with self.assertRaisesRegex(ValueError, 'disagree'): audit(*args)

    def test_sysfs_disagreement(self):
        args = fixture(); args[-1][1] = (0, 512)
        with self.assertRaisesRegex(ValueError, 'sysfs bounds'): audit(*args)

    def test_overlapping_partitions(self):
        with self.assertRaisesRegex(ValueError, 'overlapping'): audit(*fixture(overlap=True))

    def test_software_tail_layout_bounds(self):
        # Synthetic partition offset; never represents captured phone evidence.
        report = {'block_bytes': 4096, 'partitions': [
            {'name': 'boot', 'index': 19, 'first_lba': 100, 'bytes': 96 << 20}]}
        plan = diagnostic_boot_tail(report, 32 << 20, 12 << 20)
        self.assertEqual(plan['first_lba'], 100 + (64 << 20) // 4096)
        self.assertEqual(plan['block_count'], (32 << 20) // 4096)
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            diagnostic_boot_tail(report, 32 << 20, 65 << 20)

    def test_software_tail_rejects_wrong_partition_or_size(self):
        report = {'block_bytes': 4096, 'partitions': [
            {'name': 'userdata', 'index': 31, 'first_lba': 100, 'bytes': 96 << 20}]}
        with self.assertRaises(ValueError): diagnostic_boot_tail(report, 32 << 20, 12 << 20)
        report['partitions'][0].update(name='boot', index=19)
        with self.assertRaises(ValueError): diagnostic_boot_tail(report, 33 << 20, 12 << 20)
