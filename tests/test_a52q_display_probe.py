"""Display experiments must reject unsupported state before generating writes."""
import copy
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import a52q_display_probe as probe


class DisplayProbeTests(unittest.TestCase):
    def setUp(self):
        values = {'ctl0.ctl_top': 1 << 17, 'ctl0.ctl_start': 0,
                  'ctl0.ctl_intf_active': 2, 'ctl1.ctl_intf_active': 0, 'ctl2.ctl_intf_active': 0,
                  'dsi.dsi_ctrl': 501, 'dsi.dsi_status': 5,
                  'sspp0.sspp_src_size': 2400 << 16 | 1080,
                  'sspp0.sspp_src0_addr': 0x9c000000, 'sspp0.sspp_src_ystride0': 4320,
                  'sspp0.sspp_src_format': 0x237ff, 'sspp0.sspp_src_unpack_pattern': 0x03020001,
                  'sspp0.sspp_src_op_mode': 0x80000000}
        self.rows = [dict(label=k, value=v, address=0xae00000 + i * 4) for i, (k, v) in enumerate(values.items())]
        self.expected = {'registers': [{k: v for k, v in r.items() if k != 'value'} for r in self.rows],
                         'live_dtb_sha256': 'fixture'}
        self.captured = dict(copy.deepcopy(self.expected), capture_id=13)
        self.region = (0x9c000000, 0x9e4000)

    def config(self):
        sources, evidence = MagicMock(), MagicMock()
        node = SimpleNamespace(parent=SimpleNamespace(path='/reserved-memory'), name='cont_splash_region@9c000000')
        digest = SimpleNamespace(hexdigest=lambda: '11d3f62b2547f877ee96300884a19db6f1b88874c84c30682a9e4c6bc20a2243')
        with patch.object(probe.hashlib, 'sha256', return_value=digest), \
             patch.object(probe, 'layout', return_value=self.expected), \
             patch.object(probe, 'decode', return_value={'completed_reads': len(self.rows), 'registers': self.rows}), \
             patch.object(probe, 'Fdt', return_value=SimpleNamespace(nodes={'x': node})), \
             patch.object(probe, 'regs', return_value=[self.region]):
            return probe.configuration(evidence, sources, {'handoff_probe': self.captured}, b'crc fixture')

    def test_reserved_linear_handoff(self):
        config = self.config()
        self.assertEqual(config['base'], 0x9c000000)
        self.assertEqual(config['stride'], 4320)
        self.assertEqual(len(config['guards']), 13)
        self.assertIn('A52Q_DISPLAY_START_REGISTER', probe.header(config))

    def test_no_scanout_outside_reservation(self):
        self.region = (0x9c000000, 0x1000)
        with self.assertRaisesRegex(ValueError, 'reserved splash'):
            self.config()

    def test_reject_video_compressed_or_changed_stride(self):
        for label, value in [('dsi.dsi_ctrl', 503), ('sspp0.sspp_src_format', 0x400237ff),
                             ('sspp0.sspp_src_ystride0', 4096), ('ctl0.ctl_start', 1)]:
            with self.subTest(label=label):
                row = next(r for r in self.rows if r['label'] == label)
                old = row['value']
                row['value'] = value
                with self.assertRaises(ValueError):
                    self.config()
                row['value'] = old

    def test_reject_capture_layout_change(self):
        self.captured['live_dtb_sha256'] = 'other firmware'
        with self.assertRaisesRegex(ValueError, 'does not match'):
            self.config()


if __name__ == '__main__':
    unittest.main()
