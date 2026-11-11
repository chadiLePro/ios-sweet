"""Reject corrupted or mismatched bootloader handoff evidence."""
import sys
from pathlib import Path
import unittest
import zlib
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_handoff import decode


def sample(value=0x12345678, address=0xae05014, completed=1, copy=0):
    body = (f'tag=0x{12:016x}\ncount=0x{1:016x}\ncompleted=0x{completed:016x}\n'
            f'active=0x{0xffffffffffffffff:016x}\n'
            f'r000.address=0x{address:016x}\nr000.value=0x{value:016x}\n').encode()
    return (f'A52QHANDOFF v1 copy={copy}\n'.encode() + body +
            f'crc32=0x{zlib.crc32(body):016x}\nA52QHANDOFF END\n'.encode())


class HandoffTests(unittest.TestCase):
    config = {'tag': 12, 'group': 'display', 'registers': [
        {'label': 'test', 'address': 0xae05014}]}

    def test_checked_snapshot_and_corrupted_copy(self):
        result = decode(sample() + sample(copy=1).replace(b'12345678', b'12345679'), self.config)
        self.assertTrue(result['complete'])
        self.assertEqual(result['valid_copies'], [0])
        self.assertEqual(result['registers'][0]['value'], 0x12345678)

    def test_disagreement_and_duplicates(self):
        for data in (sample() * 2, sample() + sample(value=4, copy=1)):
            with self.assertRaises(ValueError):
                decode(data, self.config)

    def test_bounds_and_evidence_addresses(self):
        for data in (sample(address=4), sample(completed=0xffffffffffffffff), sample(value=1 << 40)):
            with self.assertRaises(ValueError):
                decode(data, self.config)

    def test_short_records_reject_stale_capture_and_keep_intact_values(self):
        config = dict(self.config, capture_id=81)
        def frame(kind, body):
            raw = body.encode()
            return kind.encode() + b' ' + raw + f' {zlib.crc32(raw):08x}\n'.encode()
        metadata = frame('A52M2', '0000000000000051/000000000000000c/01/01/ffffffffffffffff')
        record = frame('A52R2', '0000000000000051/00/0ae05014/12345678')
        stale = frame('A52R2', '0000000000000050/00/0ae05014/00000000')
        result = decode(metadata + record + record.replace(b'12345678', b'12345679') + stale, config)
        self.assertTrue(result['complete'])
        self.assertEqual(result['registers'][0]['value'], 0x12345678)
        self.assertEqual(result['valid_register_copies'], {0: 1})
        missing = decode(metadata + stale, config)
        self.assertFalse(missing['complete'])
        self.assertEqual(missing['missing_indices'], [0])
        with self.assertRaises(ValueError):
            decode(metadata + record + frame('A52R2', '0000000000000051/00/0ae05014/00000002'), config)


if __name__ == '__main__':
    unittest.main()
