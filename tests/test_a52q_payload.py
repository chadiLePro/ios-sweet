"""Bounds/identity checks for the real loader container and minimal bootstrap ADT."""
from pathlib import Path
import sys
import struct
import hashlib
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import adt
from a52q_payload import make_adt, validate_payload, validate_kernel, PAGE, PANIC
from qemu_a52q_xnu import entry_copies
import zlib
from fdt_evidence import Node, physical_regs


def fixture():
    """One RET instruction for QEMU loader testing. This is NOT a kernel."""
    virt, phys, total = 0xfffffff006000000, 0x106000000, 128 << 20
    va = virt + PAGE
    tree = adt.serialize(make_adt(phys, total,
        [(0x08000000, 0x10000), (0x080a0000, 0xf60000)], 62500000, 27, 0, bytes(64)))
    data = bytearray(0x2d0)
    struct.pack_into('<8sII7Q', data, 0, b'SWEETXNU', 1, 1,
                     virt, va, len(data), len(tree), va + PAGE, phys, total - PANIC)
    struct.pack_into('<4Q', data, 0x2a8, va, PAGE, 0x2c8, 8)
    struct.pack_into('<2I', data, 0x2c8, 0xd65f03c0, 0xd503201f)
    data += tree
    manifest = {'target': 'A52Q', 'phys_base': hex(phys), 'mem_size': hex(total - PANIC),
        'environment': 'QEMU virt ONLY; never flash',
        'purpose': 'RET stub loader test, NOT XNU',
        'payload_sha256': hashlib.sha256(data).hexdigest()}
    return data, manifest


class PayloadTests(unittest.TestCase):
    def test_bus_translation_mixed_cells_and_missing_ranges(self):
        cell = lambda *v: struct.pack('>' + 'I' * len(v), *v)
        root = Node('', props={'#address-cells': cell(2), '#size-cells': cell(2)})
        bus = Node('soc', root, {'#address-cells': cell(1), '#size-cells': cell(1),
                               'ranges': cell(0, 1, 0x100000, 0x1000000)})
        dev = Node('test@4000', bus, {'reg': cell(0x4000, 0x1000)})
        self.assertEqual(physical_regs(dev), [(0x100104000, 0x1000)])
        bus.props['ranges'] *= 2
        with self.assertRaises(ValueError):
            physical_regs(dev)
        del bus.props['ranges']
        with self.assertRaises(ValueError):
            physical_regs(dev)

    def test_valid_loader_fixture(self):
        data, manifest = fixture()
        validate_payload(data, manifest)

    def test_metadata_and_hash_must_match(self):
        data, manifest = fixture()
        manifest['phys_base'] = '0x100000000'
        with self.assertRaises(ValueError):
            validate_payload(data, manifest)
        data[0] ^= 1
        with self.assertRaises(ValueError):
            validate_payload(data, manifest)

    def test_segment_and_boot_data_bounds(self):
        for off, value in ((0x2a8 + 16, 0xfffffffffffffff0),
                           (0x2a8 + 24, 0x100000000), (0x2a8, 3),
                           (0x18, 0), (0x30, 0xffffffffffffffff)):
            with self.subTest(off=off, value=value):
                data, manifest = fixture()
                struct.pack_into('<Q', data, off, value)
                manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
                with self.assertRaises(ValueError):
                    validate_payload(data, manifest)

    def test_minimal_adt_has_no_storage_or_display(self):
        data, _ = fixture()
        off, size = struct.unpack_from('<2Q', data, 0x20)
        root, used = adt.parse(data[off:off + size])
        self.assertEqual(used, size)
        self.assertEqual([c.name for c in root.children], ['chosen', 'defaults', 'cpus', 'arm-io', 'pram'])
        self.assertEqual(root.children[2].children[0].prop('reg'), bytes(4))
        self.assertEqual(root.children[3].children[0].prop('virtual-timer-intid'), struct.pack('<I', 27))
        self.assertNotIn(b'sweet-ufs', data)
        self.assertNotIn(b'sweet-fbcon', data)

    def test_kernel_rejects_wrong_architecture_or_missing_identity(self):
        for data in (b'', bytes(128), struct.pack('<8I', 0xfeedfacf, 0x100000c, 2, 2, 0, 0, 0, 0)):
            with self.assertRaises(ValueError):
                validate_kernel(data)

    def test_xnu_entry_crc_rejects_corruption(self):
        body = b'A52QXNU ENTRY v1\n'
        frame = body + f'crc32={zlib.crc32(body):08x}\n'.encode() + b'A52QXNU END\n'
        self.assertEqual(entry_copies(frame * 3), 3)
        self.assertEqual(entry_copies(frame.replace(b'ENTRY', b'ENTRZ')), 0)


if __name__ == '__main__':
    unittest.main()
