"""Display experiments must reject unsupported state before generating writes."""
import copy
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
import zlib
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
        self.assertEqual(config['buffer_bytes'], self.region[1])
        self.assertEqual(len(config['guards']), 13)
        self.assertIn('A52Q_DISPLAY_START_REGISTER', probe.header(config))
        self.assertIn('A52Q_DISPLAY_WIDTH 1080ULL', probe.header(config))
        self.assertIn('A52Q_DISPLAY_HEIGHT 2400ULL', probe.header(config))

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

    def trial_result(self, stage=0x93, esr=0, value=0x12345678, nonce=81):
        def frame(kind, body):
            raw = body.encode()
            return kind.encode() + b' ' + raw + f' {zlib.crc32(raw):08x}\n'.encode()
        build = {'handoff_probe': {'capture_id': 81, 'tag': 12, 'group': 'display',
                    'registers': [{'address': 0xae05014, 'label': 'fixture'}]},
                 'display_test': {'capture_id': 80, 'guards': [{'index': 0, 'value': 0x12345678}]}}
        data = frame('A52M2', f'{nonce:016x}/000000000000000c/01/01/ffffffffffffffff')
        data += frame('A52S2', f'{nonce:016x}/{stage:08x}/{esr:016x}')
        data += frame('A52R2', f'{nonce:016x}/00/0ae05014/{value:08x}')
        return build, data

    def test_controller_completion_is_not_visible_output_or_vsync(self):
        build, data = self.trial_result()
        result = probe.result(build, data)
        self.assertTrue(result['controller_start_consumed'])
        self.assertFalse(result['visible_output_verified'])
        self.assertIsNone(result['panel_refresh_hz'])
        # Uses the trial's nonce, never the earlier handoff nonce.
        self.assertEqual(result['capture_id'], 81)

    def test_reject_stale_capture_and_never_report_timeout_or_fault_as_success(self):
        build, data = self.trial_result(nonce=80)
        with self.assertRaises(ValueError): probe.result(build, data)
        for fields in ({'stage': 0xe9}, {'esr': 1}, {'value': 0}):
            build, data = self.trial_result(**fields)
            self.assertFalse(probe.result(build, data)['controller_start_consumed'])
        build, data = self.trial_result()
        self.assertFalse(probe.result(build, data.replace(b'00000093', b'00000092'))['controller_start_consumed'])


if __name__ == '__main__':
    unittest.main()
