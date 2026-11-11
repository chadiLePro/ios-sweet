"""Synthetic inputs only: real device trees and partition dumps stay private."""
from pathlib import Path
import struct
import sys
import unittest
import gzip
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from android_boot_evidence import inspect, kernel_contract
from fdt_evidence import Fdt, describe, simplefb
from a52q_ramoops import configuration
from package_a52q_diag import verify_overlay

U32 = lambda n: struct.pack('>I', n)
CELLS = lambda *v: struct.pack('>' + 'I' * len(v), *v)


def dtb(framebuffer=False, reserve=True, fmt=b'x8r8g8b8\0', ramoops=False):
    strings = bytearray()
    code = bytearray()

    def begin(name):
        code.extend(U32(1) + name.encode() + b'\0')
        code.extend(bytes(-len(code) % 4))

    def prop(name, value):
        n = len(strings)
        strings.extend(name.encode() + b'\0')
        code.extend(U32(3) + U32(len(value)) + U32(n) + value)
        code.extend(bytes(-len(code) % 4))

    def end():
        code.extend(U32(2))

    begin('')
    prop('#address-cells', U32(2))
    prop('#size-cells', U32(2))
    prop('model', b'Synthetic A52Q fixture\0')
    prop('qcom,board-id', CELLS(34, 6))
    begin('memory@100000000')
    prop('device_type', b'memory\0')
    prop('reg', CELLS(1, 0, 0, 0x10000000))
    end()
    begin('reserved-memory')
    prop('#address-cells', U32(2))
    prop('#size-cells', U32(2))
    prop('ranges', b'')
    if reserve:
        begin('test@110000000')
        prop('reg', CELLS(1, 0x10000000, 0, 0x100000))
        if ramoops:
            prop('compatible', b'ramoops\0')
            for k in ('record', 'console', 'ftrace', 'pmsg'):
                prop(k + '-size', U32(0x40000))
        end()
    begin('dynamic')
    prop('size', CELLS(0, 0x1000))
    end()
    end()
    if framebuffer:
        begin('framebuffer@110000000')
        prop('compatible', b'simple-framebuffer\0')
        prop('reg', CELLS(1, 0x10000000, 0, 0x100000))
        prop('width', U32(64))
        prop('height', U32(64))
        prop('stride', U32(256))
        prop('format', fmt)
        end()
    end()
    code.extend(U32(9))
    # Empty memreserve list at 40; structure begins at 56.
    off = 56
    s = off + len(code)
    h = struct.pack('>10I', 0xd00dfeed, s + len(strings), off, s, 40, 17, 16,
                    0, len(strings), len(code))
    return bytearray(h + bytes(16) + code + strings)


def boot(version=2, gap=False):
    data = bytearray(4096 * 7)
    data[:8] = b'ANDROID!'
    struct.pack_into('<10I', data, 8, 16, 0x8000, 8, 0x2000000, 0, 0,
                     0x1e00000, 4096, version, 0)
    if version >= 1:
        # Deliberate page gap: DTBO is not necessarily immediately after ramdisk.
        struct.pack_into('<IQI', data, 1632, 4, 4096 * (4 if gap else 3),
                         1660 if version == 2 else 1648)
    if version == 2:
        struct.pack_into('<IQ', data, 1648, 4, 0x1f00000)
    return data


class BootTests(unittest.TestCase):
    def test_v0(self):
        self.assertEqual(inspect(boot(0))['header_version'], 0)

    def test_v2_offsets_and_recovery_gap(self):
        info = inspect(boot(gap=True))
        self.assertEqual(info['sections']['recovery_dtbo']['offset'], 16384)
        self.assertEqual(info['sections']['dtb']['offset'], 20480)

    def test_rejects_invalid_page(self):
        b = boot()
        struct.pack_into('<I', b, 36, 0)
        with self.assertRaises(ValueError):
            inspect(b)

    def test_rejects_truncation(self):
        with self.assertRaises(ValueError):
            inspect(boot()[:5000])

    def test_rejects_overlapping_recovery(self):
        b = boot()
        struct.pack_into('<Q', b, 1636, 4096)
        with self.assertRaises(ValueError):
            inspect(b)

    def test_rejects_v3(self):
        b = boot()
        struct.pack_into('<I', b, 40, 3)
        with self.assertRaises(ValueError):
            inspect(b)

    def test_gzip_image_contract(self):
        raw = bytearray(64)
        raw[56:60] = b'ARM\x64'
        struct.pack_into('<QQQ', raw, 8, 0x80000, 4096, 10)
        kernel = gzip.compress(raw)
        b = boot()
        struct.pack_into('<I', b, 8, len(kernel))
        b[4096:4096 + len(kernel)] = kernel
        self.assertEqual(kernel_contract(b)['text_offset'], 0x80000)

    def test_rejects_non_gzip_template(self):
        with self.assertRaises(ValueError):
            kernel_contract(boot())


class FdtTests(unittest.TestCase):
    def test_preserves_high_addresses_and_dynamic_reservations(self):
        info = describe(Fdt(dtb()))
        self.assertEqual(info['memory'][0]['base'], '0x100000000')
        self.assertEqual(info['dynamic_reservations'], ['/reserved-memory/dynamic'])

    def test_no_splash_inference(self):
        with self.assertRaises(ValueError):
            simplefb(Fdt(dtb()))

    def test_valid_simplefb(self):
        self.assertEqual(simplefb(Fdt(dtb(True)))['base'], 0x110000000)

    def test_rejects_unreserved_simplefb(self):
        with self.assertRaises(ValueError):
            simplefb(Fdt(dtb(True, False)))

    def test_rejects_unknown_format(self):
        with self.assertRaises(ValueError):
            simplefb(Fdt(dtb(True, fmt=b'r5g6b5\0')))

    def test_rejects_truncation(self):
        b = dtb()
        for cut in (0, 39, 55, len(b) - 1):
            with self.subTest(cut=cut), self.assertRaises(ValueError):
                Fdt(b[:cut])

    def test_rejects_block_overlap(self):
        b = dtb()
        struct.pack_into('>I', b, 12, 56)
        with self.assertRaises(ValueError):
            Fdt(b)

    def test_rejects_bad_string_offset(self):
        b = dtb()
        # First property starts at 64, property name offset at 72.
        struct.pack_into('>I', b, 72, len(b))
        with self.assertRaises(ValueError):
            Fdt(b)

    def test_rejects_unbalanced_tree(self):
        b = dtb()
        struct.pack_into('>I', b, 56, 2)
        with self.assertRaises(ValueError):
            Fdt(b)


class RamoopsTests(unittest.TestCase):
    def setup_evidence(self, folder, **overrides):
        folder.joinpath('live.dtb').write_bytes(dtb(ramoops=True))
        values = dict(mem_address=0x110000000, mem_size=0x100000,
                      record_size=0x40000, console_size=0x40000,
                      ftrace_size=0x40000, pmsg_size=0x40000, ecc=0, mem_type=0)
        values.update(overrides)
        folder.joinpath('ramoops-parameters.txt').write_text(
            ''.join(f'{k}={v}\n' for k, v in values.items()))
        folder.joinpath('kernel-config.gz').write_bytes(gzip.compress(
            b'CONFIG_PSTORE=y\nCONFIG_PSTORE_RAM=y\nCONFIG_PSTORE_CONSOLE=y\n'))

    def test_derives_console_after_dump_records(self):
        with tempfile.TemporaryDirectory() as d:
            self.setup_evidence(Path(d))
            c = configuration(Path(d))
            self.assertEqual(c['base'], 0x110040000)
            self.assertEqual(c['size'], 0x40000)

    def test_rejects_runtime_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            self.setup_evidence(Path(d), mem_address=0x120000000)
            with self.assertRaises(ValueError):
                configuration(Path(d))

    def test_rejects_ecc_and_cacheable_memory(self):
        for field in ('ecc', 'mem_type'):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as d:
                self.setup_evidence(Path(d), **{field: 1})
                with self.assertRaises(ValueError):
                    configuration(Path(d))


class OverlayTests(unittest.TestCase):
    def table(self, copies=1):
        blob = dtb(ramoops=True)
        off = 32 + 32 * copies
        total = off + len(blob) * copies
        h = struct.pack('>8I', 0xd7b7ab1e, total, 32, 32, copies, 32, 4096, 0)
        entries = b''.join(struct.pack('>8I', len(blob), off + i * len(blob), 0, 0, 0, 0, 0, 0)
                           for i in range(copies))
        return bytearray(h + entries + blob * copies)

    def test_binds_selected_board_to_ramoops(self):
        self.assertEqual(verify_overlay(self.table(), Fdt(dtb(ramoops=True))), 0)

    def test_rejects_ambiguous_board(self):
        with self.assertRaises(ValueError):
            verify_overlay(self.table(2), Fdt(dtb(ramoops=True)))

    def test_rejects_truncated_table(self):
        with self.assertRaises(ValueError):
            verify_overlay(self.table()[:-1], Fdt(dtb(ramoops=True)))

    def test_rejects_entry_in_table_header(self):
        b = self.table()
        struct.pack_into('>I', b, 36, 0)
        with self.assertRaises(ValueError):
            verify_overlay(b, Fdt(dtb(ramoops=True)))


if __name__ == '__main__':
    unittest.main()
