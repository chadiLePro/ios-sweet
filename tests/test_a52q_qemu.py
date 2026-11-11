"""Validate emulator evidence decoding; actual execution is a separate QEMU step."""
from pathlib import Path
import struct
import sys
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from qemu_a52q_diag import FIELDS, MAGIC, decode_record, decode_ramlog, linux_load_address
from a52q_diag_log import TEXT_FIELDS, decode_checked_console


class DiagnosticDecodingTests(unittest.TestCase):
    def test_record_preserves_64_bit_addresses(self):
        values = dict.fromkeys(FIELDS, 0)
        values.update(magic=MAGIC, version=1, stage=2, image=0x100800000)
        raw = struct.pack('<' + 'Q' * len(FIELDS), *(values[k] for k in FIELDS))
        self.assertEqual(decode_record(raw)['image'], 0x100800000)

    def test_record_rejects_truncation_and_unknown_version(self):
        with self.assertRaises(ValueError):
            decode_record(b'')
        raw = struct.pack('<' + 'Q' * len(FIELDS), MAGIC, 99, *([0] * (len(FIELDS) - 2)))
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


class CheckedConsoleTests(unittest.TestCase):
    def copy(self, index, changes=None, omit=None):
        values = dict.fromkeys(TEXT_FIELDS, 0)
        values.update(stage=2, current_el=4, cntfrq=19200000)
        values.update(changes or {})
        body = ''.join(f'{k}=0x{values[k]:016x}\n' for k in TEXT_FIELDS if k != omit).encode()
        return (f'A52QDIAG v2 copy={index}\n'.encode() + body +
                f'crc32=0x{zlib.crc32(body):016x}\nA52QDIAG END\n'.encode())

    def test_three_intact_copies(self):
        result = decode_checked_console(b''.join(self.copy(i) for i in range(3)))
        self.assertEqual(result['valid_copies'], [0, 1, 2])
        self.assertEqual(result['fields']['cntfrq'], 19200000)

    def test_rejects_corrupted_copy_and_preserves_intact_ones(self):
        damaged = self.copy(0).replace(b'current_el=0x0000000000000004', b'current_el=0x0000000000000008')
        result = decode_checked_console(damaged + self.copy(1) + self.copy(2))
        self.assertEqual(result['valid_copies'], [1, 2])
        self.assertEqual(result['fields']['current_el'], 4)

    def test_all_damaged_copies_are_rejected(self):
        damaged = b''.join(self.copy(i) for i in range(3)).replace(b'current_el=', b'currEnt_el=')
        with self.assertRaises(ValueError):
            decode_checked_console(damaged)

    def test_intact_copies_must_agree(self):
        with self.assertRaises(ValueError):
            decode_checked_console(self.copy(0) + self.copy(1, {'current_el': 8}))

    def test_resynchronizes_after_truncated_copy(self):
        result = decode_checked_console(self.copy(0)[:30] + self.copy(1))
        self.assertEqual(result['valid_copies'], [1])

    def test_valid_crc_does_not_allow_missing_fields(self):
        with self.assertRaises(ValueError):
            decode_checked_console(self.copy(0, omit='current_el'))

    def test_rejects_duplicate_copy_identifiers(self):
        with self.assertRaises(ValueError):
            decode_checked_console(self.copy(0) * 2)


if __name__ == '__main__':
    unittest.main()
