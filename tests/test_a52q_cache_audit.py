"""Synthetic cache: test file provenance and code-page checks independently."""
import hashlib
import json
from pathlib import Path
import struct
import re
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_cache_audit import audit_file


def fixture():
    data = bytearray(16384); data[:16] = b'dyld_v1   arm64\0'
    identifier = b'org.test.cache\0'
    cd = bytearray(44 + len(identifier) + 32)
    struct.pack_into('>9I', cd, 0, 0xfade0c02, len(cd), 0x20001, 2,
                     44 + len(identifier), 44, 0, 1, len(data))
    cd[36:40] = bytes([32, 2, 0, 14]); cd[44:44 + len(identifier)] = identifier
    struct.pack_into('<QQ', data, 40, len(data), 20 + len(cd))
    cd[-32:] = hashlib.sha256(data).digest()
    return data + struct.pack('>5I', 0xfade0cc0, 20 + len(cd), 1, 0, 20) + cd


class CacheAuditTests(unittest.TestCase):
    def test_kernel_cache_pins_match_measured_metadata(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / 'xnu/a52q/ios16-20H392-cache-pins.json').read_text())
        self.assertEqual(report['source_file_checksums_verified'], 44)
        self.assertTrue(report['all_code_page_hashes_verified'])
        self.assertFalse(report['cms_trust_authenticated'])
        expected = [d['cdhash'] for f in report['files'] for d in f['code_directories']]
        self.assertEqual(len(expected), 44)
        source = (root / 'xnu/a52q/a52q_amfi.c').read_text()
        array = source.split('static const uint8_t cache_pins', 1)[1].split('};', 1)[0]
        raw = bytes(int(s, 16) for s in re.findall(r'0x([0-9a-f]{2})', array))
        self.assertEqual([raw[i:i + 20].hex() for i in range(0, len(raw), 20)], expected)

    def test_checksum_and_page_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'dyld_shared_cache_arm64'
            data = fixture(); path.write_bytes(data)
            digest = hashlib.sha256(data).hexdigest()
            result = audit_file(path, digest)
            self.assertTrue(result['directories'][0]['executable_page_hashes_match'])
            self.assertFalse(result['cms_present'])
            data[1000] ^= 1; path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, 'original file checksum'): audit_file(path, digest)
            with self.assertRaisesRegex(ValueError, 'page hash mismatch'):
                audit_file(path, hashlib.sha256(data).hexdigest())

    def test_rejects_signature_outside_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'dyld_shared_cache_arm64'
            data = fixture(); struct.pack_into('<Q', data, 40, len(data) + 4096)
            path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, 'signature geometry'):
                audit_file(path, hashlib.sha256(data).hexdigest())


if __name__ == '__main__': unittest.main()
