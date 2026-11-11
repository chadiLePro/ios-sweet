"""Planner safety checks use synthetic ranges, never private phone dumps."""
import unittest

from test_a52q_evidence import dtb, CELLS
from fdt_evidence import Fdt, Node
from a52q_memory import plan, check_placement, iomem_ranges, subtract, LIMIT


def evidence():
    tree = Fdt(dtb())
    tree.nodes['/reserved-memory/dynamic'].props['alloc-ranges'] = CELLS(0, 0, 0, 0xffffffff)
    # Synthetic Samsung-shaped reservation at the start of the high bank.
    tree.nodes['/reserved-memory/test@110000000'].props['reg'] = CELLS(1, 0, 0, 0x5900000)
    return tree


IOMEM = '100000000-10fffffff : System RAM\n'


class MemoryPlanningTests(unittest.TestCase):
    def test_excludes_samsung_shaped_debug_reservation(self):
        report = plan(evidence(), IOMEM)
        self.assertEqual(report['candidates'], [{'base': '0x105900000', 'size': '0xa700000',
                                                'end_exclusive': '0x110000000'}])
        with self.assertRaises(ValueError):
            check_placement(report, 0x100000000, 0x4000)
        self.assertFalse(check_placement(report, 0x105900000, 0x4000)['hardware_access_validated'])

    def test_dynamic_window_entirely_excluded_not_only_size(self):
        tree = evidence()
        tree.nodes['/reserved-memory/dynamic'].props['alloc-ranges'] = CELLS(1, 0, 0, 0x10000000)
        self.assertEqual(plan(tree, IOMEM)['candidates'], [])

    def test_unbounded_dynamic_reservation_blocks_plan(self):
        with self.assertRaisesRegex(ValueError, 'bounded alloc-ranges'):
            plan(Fdt(dtb()), IOMEM)

    def test_dynamic_size_and_window_validation(self):
        for key, value in [('alloc-ranges', b'x'), ('size', CELLS(0, 0)),
                           ('size', CELLS(1, 0))]:
            with self.subTest(key=key, value=value):
                tree = evidence()
                tree.nodes['/reserved-memory/dynamic'].props[key] = value
                with self.assertRaises(ValueError):
                    plan(tree, IOMEM)

    def test_iomem_children_memreserve_and_live_exclusions(self):
        tree = evidence()
        tree.reservations = [(0x108000000, 0x1000000)]
        report = plan(tree, IOMEM + '  106000000-106ffffff : Kernel code\n',
                      [(0x10a000000, 0x1000000)])
        for base in (0x106000000, 0x108000000, 0x10a000000):
            with self.assertRaises(ValueError):
                check_placement(report, base, 0x4000)
        # Entire placement must fit one candidate, not bridge the excluded code.
        with self.assertRaises(ValueError):
            check_placement(report, 0x105900000, 0x2000000)

    def test_iomem_redacted_and_malformed_rejected(self):
        for text in ('00000000-00000000 : System RAM', 'garbage',
                     '2000-1000 : System RAM', '0-fffffffffffffffff : System RAM',
                     '1000-2000 : reserved'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                iomem_ranges(text)

    def test_intersection_and_alignment(self):
        report = plan(evidence(), '105900001-10ffffffd : System RAM\n')
        self.assertEqual(report['candidates'][0]['base'], '0x105904000')
        self.assertEqual(report['candidates'][0]['end_exclusive'], '0x10fffc000')
        with self.assertRaises(ValueError):
            check_placement(report, 0x105904001, 0x4000)
        with self.assertRaises(ValueError):
            plan(evidence(), '80000000-ffffffff : System RAM')

    def test_reserved_translation_rejected(self):
        tree = evidence()
        tree.nodes['/reserved-memory'].props['ranges'] = CELLS(1, 2, 3, 4)
        with self.assertRaisesRegex(ValueError, 'translation'):
            plan(tree, IOMEM)

    def test_missing_reservations_and_overlapping_banks_rejected(self):
        tree = evidence()
        del tree.nodes['/reserved-memory']
        with self.assertRaisesRegex(ValueError, 'reserved-memory'):
            plan(tree, IOMEM)
        tree = evidence()
        root = tree.nodes['/']
        root.children.append(Node('memory@duplicate', root, {
            'device_type': b'memory\0', 'reg': CELLS(1, 0, 0, 0x100000)}))
        with self.assertRaisesRegex(ValueError, 'overlapping'):
            plan(tree, IOMEM)

    def test_multiple_windows_excluded_and_static_reg_takes_precedence(self):
        tree = evidence()
        dynamic = tree.nodes['/reserved-memory/dynamic']
        dynamic.props['alloc-ranges'] = CELLS(1, 0x6000000, 0, 0x1000000,
                                             1, 0xa000000, 0, 0x1000000)
        report = plan(tree, IOMEM)
        for base in (0x106000000, 0x10a000000):
            with self.assertRaises(ValueError):
                check_placement(report, base, 0x4000)
        dynamic.props['reg'] = CELLS(1, 0xc000000, 0, 0x1000000)
        report = plan(tree, IOMEM)
        self.assertTrue(check_placement(report, 0x106000000, 0x4000)['fits_snapshot_candidates'])
        with self.assertRaises(ValueError):
            check_placement(report, 0x10c000000, 0x4000)

    def test_interval_overflow_and_edges(self):
        ram, occupied = iomem_ranges('ffffffffffffc000-ffffffffffffffff : System RAM')
        self.assertEqual(ram, [(LIMIT - 0x4000, LIMIT)])
        self.assertEqual(occupied, [])
        self.assertEqual(subtract([(0, 10)], [(3, 5), (5, 7)]), [(0, 3), (7, 10)])
        with self.assertRaises(ValueError):
            plan(evidence(), IOMEM, [(LIMIT - 1, 2)])


if __name__ == '__main__':
    unittest.main()
