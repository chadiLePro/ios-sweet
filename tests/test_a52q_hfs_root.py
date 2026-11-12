"""Reject unsafe HFS RAM-root geometry; these fixtures are not filesystems."""
from pathlib import Path
import struct
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_hfs_root import validate_hfs_test_root, hardware_root_proof


def fixture():
    data = bytearray(8 << 20)
    struct.pack_into('>HHIII', data, 1024, 0x4858, 5, (1 << 8) | (1 << 13), 0, 2)
    struct.pack_into('>III', data, 1064, 4096, len(data) // 4096, 0)
    data[-1024:-512] = data[1024:1536]
    return data


class HfsRootTests(unittest.TestCase):
    def test_physical_diagnostic_requires_same_kernel_and_root_qemu_boot(self):
        import copy
        report = {'scope': 'QEMU virt only; no Samsung boot or hardware claim',
            'status': 'diagnostic PID1 observed in QEMU; not Apple iOS userland',
            'diagnostic_pid1_observed': True, 'diagnostic_init_heartbeats': 7,
            'payload': {'environment': 'QEMU virt ONLY; never flash', 'kernel_sha256': 'k',
                        'hfs_test_root': {'sha256': 'r'}}}
        normalized = hardware_root_proof(report, 'k', 'r')
        self.assertEqual(hardware_root_proof(normalized, 'k', 'r'), normalized)
        for kernel, root in [('other', 'r'), ('k', 'other')]:
            with self.assertRaises(ValueError): hardware_root_proof(report, kernel, root)
        for key, value in [('error', 'timeout'), ('diagnostic_pid1_observed', False),
                           ('diagnostic_init_heartbeats', 0), ('scope', 'phone'), ('status', 'panic')]:
            bad = copy.deepcopy(report); bad[key] = value
            with self.assertRaises(ValueError): hardware_root_proof(bad, 'k', 'r')

    def test_clean_geometry(self):
        self.assertEqual(validate_hfs_test_root(fixture())['block_size'], 4096)

    def test_bad_volume_header(self):
        for offset, value in ((1024, 0), (1028, 0), (1064, 3072), (1068, 0xffffffff)):
            with self.subTest(offset=offset):
                data = fixture()
                struct.pack_into('>I', data, offset, value)
                with self.assertRaises(ValueError):
                    validate_hfs_test_root(data)

    def test_alternate_and_metadata_bounds(self):
        data = fixture()
        data[-1024] = 0
        with self.assertRaisesRegex(ValueError, 'alternate'):
            validate_hfs_test_root(data)
        data = fixture()
        struct.pack_into('>Q', data, 1024 + 112, 0xffffffffffffffff)
        with self.assertRaisesRegex(ValueError, 'fork exceeds'):
            validate_hfs_test_root(data)
        data = fixture()
        struct.pack_into('>II', data, 1024 + 128, 0xfffffffe, 2)
        with self.assertRaisesRegex(ValueError, 'extent exceeds'):
            validate_hfs_test_root(data)


if __name__ == '__main__':
    unittest.main()
