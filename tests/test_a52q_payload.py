"""Bounds/identity checks for the real loader container and minimal bootstrap ADT."""
from pathlib import Path
import sys
import struct
import hashlib
import unittest
import mkinit
import mkpayload
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import adt
from a52q_payload import make_adt, validate_payload, validate_kernel, validate_bootstrap_init, PAGE, PANIC
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


def kernel_header_fixture(table_va=0xfffffe0007004000, ctf=False):
    """Parser fixture only; contains no runnable kernel code."""
    data = bytearray(0x4000)
    text = struct.pack('<II16s4Q4I', 0x19, 72, b'__TEXT',
        0xfffffe0007004000, 0x4000, 0, 0x4000, 5, 5, 0, 0)
    names = b'\0_a52q_console_l3\0'
    sym = struct.pack('<6I', 2, 24, 0x200, 1, 0x300, len(names))
    commands = text + sym
    if ctf:
        commands += struct.pack('<II16s4Q4I', 0x19, 72, b'__CTF',
            0xfffffe0007008000, 0, 0x3ff0, 16, 1, 1, 0, 0)
    struct.pack_into('<8I', data, 0, 0xfeedfacf, 0x100000c, 0, 2, 3 if ctf else 2,
                     len(commands), 0, 0)
    data[32:32 + len(commands)] = commands
    struct.pack_into('<IBBHQ', data, 0x200, 1, 0xf, 1, 0, table_va)
    data[0x300:0x300 + len(names)] = names
    markers = b'A52QXNU stage=0x\0kernel RAM-console VA live\0'
    data[0x500:0x500 + len(markers)] = markers
    return data


def init_fixture():
    """Synthetic RET-only object to test container checks, not a runnable PID1."""
    data = bytearray(0x200)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT', 0, 4,
                          0x180, 2, 0, 0, 0x80000400, 0, 0, 0)
    segment = mkinit.segment('', 0, 4, 0x180, 4, 5, [section])
    names = b'\0_start\0'
    commands = segment + struct.pack('<6I', 2, 24, 0x190, 1, 0x1a0, len(names))
    struct.pack_into('<8I', data, 0, 0xfeedfacf, 0x100000c, 0, 1, 2, len(commands), 0, 0)
    data[32:32 + len(commands)] = commands
    struct.pack_into('<I', data, 0x180, 0xd65f03c0)
    struct.pack_into('<IBBHQ', data, 0x190, 1, 0xf, 1, 0, 0)
    data[0x1a0:0x1a0 + len(names)] = names
    return mkinit.build(data)


def ramdisk_fixture():
    data, manifest = fixture()
    virt, entry, adt_off, adt_size, end, phys, memory = struct.unpack_from('<7Q', data, 16)
    init = init_fixture()
    rd_size = (len(init) + PAGE - 1) & ~(PAGE - 1)
    tree = mkpayload.add_ramdisk_to_adt(data[adt_off:adt_off + adt_size], phys + end - virt, rd_size)
    result = bytearray(0x2a8 + 64)
    pos = len(result)
    result += struct.pack('<2I', 0xd65f03c0, 0xd503201f)
    init_pos = len(result)
    result += init
    result += bytes(-len(result) % 16)
    tree_pos = len(result)
    result += tree
    struct.pack_into('<8sII7Q', result, 0, b'SWEETXNU', 1, 2,
                     virt, entry, tree_pos, len(tree), end + rd_size, phys, memory)
    struct.pack_into('<4Q', result, 0x2a8, entry, PAGE, pos, 8)
    struct.pack_into('<4Q', result, 0x2a8 + 32, end, rd_size, init_pos, len(init))
    manifest['bootstrap_init'] = {'sha256': hashlib.sha256(init).hexdigest(), 'bytes': len(init)}
    manifest['payload_sha256'] = hashlib.sha256(result).hexdigest()
    return result, manifest


class PayloadTests(unittest.TestCase):
    def test_static_init_geometry_and_architecture(self):
        data = init_fixture()
        validate_bootstrap_init(data)
        for off, value in ((4, 7), (8, 2), (12, 1), (20, 0xffffffff)):
            bad = bytearray(data)
            struct.pack_into('<I', bad, off, value)
            with self.assertRaises(ValueError):
                validate_bootstrap_init(bad)
        with self.assertRaises(ValueError):
            validate_bootstrap_init(b'not a filesystem')

    def test_ramdisk_is_a_protected_loader_segment(self):
        data, manifest = ramdisk_fixture()
        validate_payload(data, manifest)
        manifest['bootstrap_init']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'manifest mismatch'):
            validate_payload(data, manifest)
        data, manifest = ramdisk_fixture()
        # Move the RAMDisk mapping onto the kernel: must reject even after
        # recomputing the container hash, rather than trusting its ADT property.
        off, size = struct.unpack_from('<2Q', data, 0x20)
        tree, _ = adt.parse(data[off:off + size])
        mmap = next(c for c in tree.children if c.name == 'chosen').children[0]
        mmap.props = [(n, f, struct.pack('<2Q', 0x106004000, 2 * PAGE) if n == 'RAMDisk' else v)
                      for n, f, v in mmap.props]
        data[off:off + size] = adt.serialize(tree)
        manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
        with self.assertRaisesRegex(ValueError, 'final protected loader segment'):
            validate_payload(data, manifest)

    def test_kernel_table_alignment_and_file_only_ctf(self):
        validate_kernel(kernel_header_fixture())
        validate_kernel(kernel_header_fixture(ctf=True))
        with self.assertRaisesRegex(ValueError, '16 KiB aligned'):
            validate_kernel(kernel_header_fixture(table_va=0xfffffe0007005000))

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
