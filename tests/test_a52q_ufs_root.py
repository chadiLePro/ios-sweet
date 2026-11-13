"""Synthetic filesystem/partition fixtures: no device writes or real boot claim."""
import copy
import hashlib
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import MagicMock, patch
import zlib
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import adt
import a52q_ufs_root as root
from a52q_payload import validate_payload
from a52q_ufs_selftest import adt_node as ufs_node
from test_a52q_payload import fixture as payload_fixture
from test_a52q_hfs_root import fixture as hfs_fixture


class UfsRootTests(unittest.TestCase):
    def setUp(self):
        self.ufs = dict(reg=[0x1d84000, 0x3000], nonce=81, last_lba=31077375,
            block_bytes=4096, read_lba=123888, read_crc32=0x12345678)
        self.data = hfs_fixture()
        digest = hashlib.sha256(self.data).hexdigest()
        self.proof = {'scope': 'QEMU virt only; no Samsung boot or hardware claim',
            'status': 'diagnostic PID1 observed in QEMU; not Apple iOS userland',
            'diagnostic_pid1_observed': True, 'diagnostic_init_heartbeats': 7,
            'payload': {'environment': 'QEMU virt ONLY; never flash', 'kernel_sha256': 'kernel',
                        'hfs_test_root': {'sha256': digest}}}
        self.report = {'block_bytes': 4096, 'disk_bytes': (self.ufs['last_lba'] + 1) * 4096,
            'partitions': [dict(name='boot', index=19, first_lba=100, block_count=24576, bytes=96 << 20)]}
        self.capture = MagicMock()
        (self.capture / 'capture.json').read_bytes.return_value = b'fixture'
        with patch.object(root, 'from_capture', return_value=self.report):
            self.config = root.configuration(self.capture, self.ufs, self.data, 'kernel', self.proof)

    def test_window_and_packaging_must_agree(self):
        with patch.object(root, 'from_capture', return_value=self.report):
            plan = root.validate_packaging(self.config, self.ufs, self.data, self.capture, 16 << 20)
            self.assertEqual(plan['first_lba'], 100 + (88 << 20) // 4096)
            with self.assertRaisesRegex(ValueError, 'overlaps'):
                root.validate_packaging(self.config, self.ufs, self.data, self.capture, 89 << 20)
            changed = bytearray(self.data); changed[4096] ^= 1
            with self.assertRaisesRegex(ValueError, 'differs'):
                root.validate_packaging(self.config, self.ufs, changed, self.capture, 16 << 20)

    def test_reject_wrong_capacity_root_or_qemu_proof(self):
        for key, value in [('ufs_nonce', 82), ('bytes', 9 << 20), ('offset_in_boot_bytes', 0),
                           ('sha256', 'not-a-hash'), ('window', [100, 24576, 110, 2048]),
                           ('window', [100, 24576, 100, 24576])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                root.validate_config(dict(self.config, **{key: value}), self.ufs)
        with patch.object(root, 'from_capture', return_value=self.report):
            with self.assertRaises(ValueError):
                root.configuration(self.capture, self.ufs, self.data, 'different kernel', self.proof)
            self.report['disk_bytes'] -= 4096
            with self.assertRaisesRegex(ValueError, 'capacity'):
                root.configuration(self.capture, self.ufs, self.data, 'kernel', self.proof)

    def test_crc_is_fresh_and_not_a_mount_claim(self):
        def frame(nonce=81, crc=None):
            first, count = self.config['window'][2:]
            body = f'{nonce:016x}/{first:08x}/{count:08x}/{self.config["header_crc32"] if crc is None else crc:08x}'.encode()
            return b'A52V1 ' + body + f' {zlib.crc32(body):08x}\n'.encode()
        self.assertEqual(root.decode_kernel_console(frame() * 3, self.config)['valid_copies'], 3)
        self.assertFalse(root.decode_kernel_console(frame(82), self.config)['readonly_root_window_verified'])
        with self.assertRaisesRegex(ValueError, 'disagrees'):
            root.decode_kernel_console(frame(crc=0), self.config)

    def test_payload_binding_and_no_ram_fallback(self):
        data, manifest = payload_fixture()
        off, size = struct.unpack_from('<2Q', data, 0x20)
        tree, _ = adt.parse(data[off:off + size])
        tree.children += [ufs_node(self.ufs), root.adt_node(self.config)]
        encoded = adt.serialize(tree); data[off:] = encoded
        struct.pack_into('<Q', data, 0x28, len(encoded))
        data[0x48:0x48 + len(b'rd=a52root0')] = b'rd=a52root0'
        manifest.update(ufs_selftest=self.ufs, ufs_diagnostic_root=copy.deepcopy(self.config), kernel_sha256='kernel')
        def check():
            manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
            validate_payload(data, manifest)
        with self.assertRaisesRegex(ValueError, 'hardware-bound'): check()
        manifest['environment'] = 'SM-A525F/DS hardware candidate'
        check()
        manifest['bootstrap_init'] = {'anything': True}
        with self.assertRaisesRegex(ValueError, 'RAM-root fallback'): check()
        del manifest['bootstrap_init']
        data[0x48:0x2a8] = bytes(608)
        with self.assertRaisesRegex(ValueError, 'rd=a52root0'): check()


if __name__ == '__main__':
    unittest.main()
