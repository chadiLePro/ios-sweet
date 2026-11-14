"""Audit code-signing bytes; no Apple data or runtime compatibility assertion."""
import hashlib
import plistlib
from pathlib import Path
import struct
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_userland_audit import inspect
from relink_a52q_console import amfi_wrapper


def fixture():
    data = bytearray(4096)
    struct.pack_into('<8I', data, 0, 0xfeedfacf, 0x100000c, 0, 2, 1, 16, 0, 0)
    # A one-page file signed by one SHA256 CodeDirectory; deliberately no CMS.
    identifier = b'org.test.synthetic\0'
    cd = bytearray(44 + len(identifier) + 32)
    struct.pack_into('>9I', cd, 0, 0xfade0c02, len(cd), 0x20001, 2,
                     44 + len(identifier), 44, 0, 1, len(data))
    cd[36:40] = bytes([32, 2, 0, 12]); cd[44:44 + len(identifier)] = identifier
    struct.pack_into('<4I', data, 32, 0x1d, 16, len(data), 20 + len(cd))
    cd[-32:] = hashlib.sha256(data).digest()
    return data + struct.pack('>5I', 0xfade0cc0, 20 + len(cd), 1, 0, 20) + cd


def entitled_fixture():
    data = bytearray(4096)
    struct.pack_into('<8I', data, 0, 0xfeedfacf, 0x100000c, 0, 2, 1, 16, 0, 0)
    xml = plistlib.dumps({'org.test.synthetic': True})
    xml = struct.pack('>II', 0xfade7171, 8 + len(xml)) + xml
    der = struct.pack('>II', 0xfade7172, 13) + b'\x30\x03\x01\x01\xff'
    identifier = b'org.test.synthetic\0'; hashes = 44 + len(identifier) + 7 * 32
    cd = bytearray(hashes + 32)
    struct.pack_into('>9I', cd, 0, 0xfade0c02, len(cd), 0x20001, 2, hashes, 44, 7, 1, len(data))
    cd[36:40] = bytes([32, 2, 0, 12]); cd[44:44 + len(identifier)] = identifier
    for slot, item in ((5, xml), (7, der)):
        cd[hashes - slot * 32:hashes - (slot - 1) * 32] = hashlib.sha256(item).digest()
    total = 36 + len(cd) + len(xml) + len(der)
    struct.pack_into('<4I', data, 32, 0x1d, 16, len(data), total)
    cd[-32:] = hashlib.sha256(data).digest()
    return data + struct.pack('>9I', 0xfade0cc0, total, 3, 0, 36, 5, 36 + len(cd), 7, 36 + len(cd) + len(xml)) + cd + xml + der


class UserlandAuditTests(unittest.TestCase):
    def test_amfi_leaf_rebuild_does_not_duplicate_existing_source(self):
        old = '#if defined(ARM64_BOARD_CONFIG_SWEET)\nlegacy\n#endif\n'
        new = amfi_wrapper(old)
        self.assertEqual(amfi_wrapper(new), new)
        self.assertEqual(new.count('#include "a52q_amfi.c"'), 1)
        with self.assertRaises(ValueError): amfi_wrapper(new + new)

    def test_checks_code_pages_without_claiming_cms_authentication(self):
        data = fixture(); result = inspect(data)
        self.assertFalse(result['arm64e'])
        self.assertFalse(result['signature']['cms_present'])
        self.assertTrue(result['signature']['directories'][0]['executable_page_hashes_match'])
        data[1000] ^= 1
        with self.assertRaisesRegex(ValueError, 'page hash mismatch'): inspect(data)

    def test_checks_original_xml_and_der_special_slots(self):
        data = entitled_fixture(); result = inspect(data)['signature']
        self.assertEqual(result['entitlement_keys'], ['org.test.synthetic'])
        self.assertEqual(set(result['entitlement_blobs']), {'5', '7'})
        self.assertTrue(all(v['special_slot_hashes_match'] for v in result['entitlement_blobs'].values()))
        for slot in (5, 7):
            changed = bytearray(data)
            offset = next(struct.unpack_from('>I', changed, 4096 + 16 + i * 8)[0]
                for i in range(3) if struct.unpack_from('>I', changed, 4096 + 12 + i * 8)[0] == slot)
            changed[4096 + offset + 8] ^= 1
            with self.assertRaisesRegex(ValueError, 'special-slot hash mismatch'): inspect(changed)

    def test_rejects_malformed_signature_and_load_geometry(self):
        data = fixture(); struct.pack_into('<I', data, 36, 8)
        with self.assertRaises(ValueError): inspect(data)
        data = fixture(); struct.pack_into('>I', data, 4100, len(data) + 1)
        with self.assertRaises(ValueError): inspect(data)
        data = fixture(); struct.pack_into('>I', data, 4096 + 20 + 16, 0xffffffff)
        with self.assertRaises(ValueError): inspect(data)


if __name__ == '__main__':
    unittest.main()
