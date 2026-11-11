"""Validate emulator evidence decoding; actual execution is a separate QEMU step."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from qemu_a52q_diag import FIELDS, MAGIC, decode_record, decode_ramlog, linux_load_address


class DiagnosticDecodingTests(unittest.TestCase):
    def test_record_preserves_64_bit_addresses(self):
        values = dict.fromkeys(FIELDS, 0)
        values.update(magic=MAGIC, version=1, stage=2, image=0x100800000)
        raw = struct.pack('<' + 'Q' * len(FIELDS), *(values[k] for k in FIELDS))
        self.assertEqual(decode_record(raw)['image'], 0x100800000)

    def test_record_rejects_truncation_and_unknown_version(self):
        with self.assertRaises(ValueError):
            decode_record(b'')
        raw = struct.pack('<' + 'Q' * len(FIELDS), MAGIC, 2, *([0] * (len(FIELDS) - 2)))
        with self.assertRaises(ValueError):
            decode_record(raw)

    def test_decodes_linux_wrapped_console_order(self):
        raw = struct.pack('<III', 0x43474244, 2, 4) + b'CDAB'
        self.assertEqual(decode_ramlog(raw), 'ABCD')

    def test_ramlog_rejects_uncommitted_signature_and_out_of_bounds_indices(self):
        for sig, start, size in ((0, 0, 0), (0x43474244, 5, 4), (0x43474244, 0, 8)):
            with self.subTest(start=start, size=size), self.assertRaises(ValueError):
                decode_ramlog(struct.pack('<III', sig, start, size) + b'ABCD')

    def test_qemu_linux_placement_handles_4k_stub_boundary(self):
        for offset, expected in ((0, 0x40200000), (4096, 0x40001000), (0x80000, 0x40080000)):
            raw = bytearray(64)
            struct.pack_into('<QQ', raw, 8, offset, 4096)
            raw[56:60] = b'ARM\x64'
            with self.subTest(offset=offset):
                self.assertEqual(linux_load_address(raw), expected)

    def test_linux_placement_rejects_unsized_image(self):
        with self.assertRaises(ValueError):
            linux_load_address(bytes(64))


if __name__ == '__main__':
    unittest.main()
