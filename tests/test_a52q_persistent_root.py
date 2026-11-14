"""Full-root planning rejects RAM fallback and mismatched storage evidence."""
import copy
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import MagicMock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import adt
import a52q_persistent_root as root
from a52q_hfs_root import read_test_root
from a52q_payload import validate_payload
from a52q_ufs_selftest import adt_node as ufs_node
from test_a52q_payload import fixture as payload_fixture


class PersistentRootTests(unittest.TestCase):
    def setUp(self):
        self.ufs = dict(reg=[0x1d84000, 0x3000], nonce=81, last_lba=31077375,
            block_bytes=4096, read_lba=123888, read_crc32=0x12345678)
        self.master = dict(bytes=16 << 30, sha256='a' * 64, header_crc32=81,
                           volume=dict(bytes=16 << 30, journaled=False))
        self.report = dict(block_bytes=4096, disk_bytes=(31077375 + 1) * 4096,
            partitions=[dict(name='userdata', index=31, first_lba=3165696,
                             block_count=27911647, bytes=27911647 * 4096)])
        self.capture = MagicMock()
        header = bytearray(4096)
        struct.pack_into('<I', header, 16, 123)
        struct.pack_into('<QIII', header, 72, 2, 36, 128, 456)
        def child(name):
            item = MagicMock()
            item.read_bytes.return_value = header if name == 'primary-header.bin' else b'capture'
            return item
        self.capture.__truediv__.side_effect = child
        with patch.object(root, 'from_capture', return_value=self.report):
            self.config = root.configuration(self.capture, self.ufs, self.master, 'b' * 64)

    def test_exact_userdata_root_window(self):
        self.assertEqual(self.config['window'], [3165696, 27911647, 3165696, 4194304])
        self.assertEqual(self.config['gpt_crc32'], [123, 456])
        for key, value in [('window', [3165696, 8192, 3165696, 4194304]),
                           ('window', [3165696, 27911647, 3165697, 4194304]),
                           ('ufs_nonce', 82), ('layout_kind', 1), ('partition_index', 19),
                           ('sha256', 'x'), ('gpt_crc32', [1]), ('offset_in_partition_bytes', 4096)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                root.validate_config(dict(self.config, **{key: value}), self.ufs)
        with patch.object(root, 'from_capture', return_value=self.report):
            self.report['partitions'][0]['bytes'] = 96 << 20
            with self.assertRaisesRegex(ValueError, 'cannot contain'):
                root.configuration(self.capture, self.ufs, self.master, 'b' * 64)

    def test_full_root_is_never_read_into_diagnostic_buffer(self):
        path = MagicMock()
        path.stat.return_value.st_mode = 0o100644
        path.stat.return_value.st_size = 16 << 30
        with self.assertRaisesRegex(ValueError, '8..32 MiB'):
            read_test_root(path)
        path.open.assert_not_called()
        with self.assertRaisesRegex(ValueError, 'completed read-only fsck'):
            root.inspect_master(path, {})
        path.open.assert_not_called()

    def test_payload_needs_exact_kernel_root_name_and_no_ram_root(self):
        data, manifest = payload_fixture()
        off, size = struct.unpack_from('<2Q', data, 0x20)
        tree, _ = adt.parse(data[off:off + size])
        tree.children += [ufs_node(self.ufs), root.adt_node(self.config)]
        encoded = adt.serialize(tree); data[off:] = encoded
        struct.pack_into('<Q', data, 0x28, len(encoded))
        data[0x48:0x48 + len(b'rd=a52ios0')] = b'rd=a52ios0'
        manifest.update(ufs_selftest=self.ufs, ufs_ios_root=copy.deepcopy(self.config),
                        kernel_sha256='b' * 64, environment='SM-A525F/DS hardware candidate')
        def check():
            import hashlib
            manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
            validate_payload(data, manifest)
        check()
        manifest['kernel_sha256'] = 'c' * 64
        with self.assertRaisesRegex(ValueError, 'kernel hash'): check()
        manifest['kernel_sha256'] = 'b' * 64
        manifest['bootstrap_init'] = {'diagnostic': True}
        with self.assertRaisesRegex(ValueError, 'RAM-root fallback'): check()
        del manifest['bootstrap_init']
        data[0x48:0x2a8] = bytes(608)
        with self.assertRaisesRegex(ValueError, 'rd=a52ios0'): check()


if __name__ == '__main__':
    unittest.main()
