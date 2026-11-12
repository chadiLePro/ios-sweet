"""Kernel test output must be capture-bound; hardware nodes cannot enter QEMU."""
from pathlib import Path
import hashlib
import struct
import sys
import unittest
import zlib
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import adt
from a52q_ufs_selftest import adt_node, decode_kernel_console
from a52q_payload import validate_payload
from test_a52q_payload import fixture


class KernelUfsTests(unittest.TestCase):
    config = {'reg': [0x1d84000, 0x3000], 'nonce': 81, 'last_lba': 0x12345678,
              'block_bytes': 4096, 'read_lba': 123888, 'read_crc32': 0xabcdef12}

    def frame(self, phase=0x20, nonce=81, crc=0xabcdef12):
        body = f'{nonce:016x}/{phase:02x}/00000000/12345678/00001000/{crc:08x}/21000000'.encode()
        return b'A52K1 ' + body + f' {zlib.crc32(body):08x}\r\n'.encode()

    def test_success_and_integrity(self):
        result = decode_kernel_console(self.frame() * 2, self.config)
        self.assertTrue(result['success'])
        self.assertEqual(result['stages']['0x20']['valid_copies'], 2)
        self.assertFalse(decode_kernel_console(self.frame().replace(b'abcdef12', b'abcdef13'), self.config)['success'])
        self.assertFalse(decode_kernel_console(self.frame(nonce=82), self.config)['success'])
        self.assertFalse(decode_kernel_console(self.frame(crc=0), self.config)['success'])

    def test_error_and_conflicting_records(self):
        self.assertFalse(decode_kernel_console(self.frame() + self.frame(phase=0xe7), self.config)['success'])
        with self.assertRaisesRegex(ValueError, 'disagree'):
            decode_kernel_console(self.frame() + self.frame(crc=0), self.config)

    def test_disk_requires_both_transfer_and_bsd_path_proof(self):
        self.assertFalse(decode_kernel_console(self.frame(), self.config)['readonly_disk_verified'])
        self.assertFalse(decode_kernel_console(self.frame(phase=0x30), self.config)['readonly_disk_verified'])
        self.assertTrue(decode_kernel_console(self.frame() + self.frame(phase=0x30), self.config)['readonly_disk_verified'])
        self.assertFalse(decode_kernel_console(self.frame() + self.frame(phase=0x30) +
            self.frame(phase=0xe8), self.config)['readonly_disk_verified'])

    def test_hardware_binding_and_adt_tamper(self):
        data, manifest = fixture()
        offset, size = struct.unpack_from('<2Q', data, 0x20)
        tree, _ = adt.parse(data[offset:offset + size])
        tree.children.append(adt_node(self.config))
        encoded = adt.serialize(tree)
        data[offset:] = encoded
        struct.pack_into('<Q', data, 0x28, len(encoded))
        manifest['ufs_selftest'] = dict(self.config)
        manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
        with self.assertRaisesRegex(ValueError, 'hardware-bound'):
            validate_payload(data, manifest)
        manifest['environment'] = 'SM-A525F/DS hardware candidate'
        validate_payload(data, manifest)
        manifest['ufs_selftest']['read_crc32'] ^= 1
        with self.assertRaisesRegex(ValueError, 'differs'):
            validate_payload(data, manifest)
