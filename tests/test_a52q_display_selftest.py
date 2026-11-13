"""Display nodes must be hardware-bound and require intact kernel evidence."""
import copy
import hashlib
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch
import zlib
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import adt
import a52q_display_selftest as display
from a52q_payload import validate_payload
from test_a52q_payload import fixture


class KernelDisplayTests(unittest.TestCase):
    def setUp(self):
        self.config = {'reg': [0x9c000000, 0x9e4000], 'geometry': [1080, 2400, 4320],
            'start_register': 0xae0101c, 'nonce': 81, 'scope': 'test fixture, not hardware proof',
            'guards': [dict(address=0xae0101c + 4 * i, value=0) for i in range(13)]}

    def frame(self, phase=0x30, nonce=81, detail=0):
        body = f'{nonce:016x}/{phase:02x}/{detail:08x}'.encode()
        return b'A52D1 ' + body + f' {zlib.crc32(body):08x}\n'.encode()

    def test_completion_needs_all_phases_and_no_error(self):
        complete = b''.join(self.frame(p) for p in (0x10, 0x20, 0x30))
        result = display.decode_kernel_console(complete * 2, self.config)
        self.assertTrue(result['kernel_refresh_completed'])
        self.assertEqual(result['stages']['0x30']['valid_copies'], 2)
        self.assertFalse(result['visible_output_verified'])
        self.assertIsNone(result['panel_refresh_hz'])
        for failed in (self.frame(), complete + self.frame(0xe4), complete.replace(b'00000051', b'00000052'),
                       complete.replace(b'/30/', b'/31/')):
            self.assertFalse(display.decode_kernel_console(failed, self.config)['kernel_refresh_completed'])
        with self.assertRaisesRegex(ValueError, 'disagree'):
            display.decode_kernel_console(complete + self.frame(detail=1), self.config)

    def test_reject_bad_mapping_geometry_or_registers(self):
        variants = [dict(reg=[0x9c000004, 0x9e4000]), dict(reg=[0x9c000000, 0x1000]),
            dict(reg=[0xffffc000, 0x8000]), dict(geometry=[1080, 2400, 4096]),
            dict(geometry=[0xffffffff, 2400, 4320]), dict(nonce=0), dict(start_register=0xdeadbeef)]
        for changed in variants:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                display.adt_node(dict(self.config, **changed))
        for address in (self.config['guards'][0]['address'], 0xae01021, 0x9c000000):
            bad = copy.deepcopy(self.config)
            bad['guards'][1]['address'] = address
            with self.assertRaises(ValueError): display.adt_node(bad)

    def test_cannot_promote_failed_shim_refresh(self):
        with patch.object(display, 'display_result', return_value={'controller_start_consumed': False}):
            with self.assertRaisesRegex(ValueError, 'successful'):
                display.configuration(None, None, {}, b'')

    def test_hardware_binding_and_tampered_adt(self):
        data, manifest = fixture()
        offset, size = struct.unpack_from('<2Q', data, 0x20)
        tree, _ = adt.parse(data[offset:offset + size])
        tree.children.append(display.adt_node(self.config))
        encoded = adt.serialize(tree)
        data[offset:] = encoded
        struct.pack_into('<Q', data, 0x28, len(encoded))
        manifest['display_selftest'] = copy.deepcopy(self.config)
        manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
        with self.assertRaisesRegex(ValueError, 'hardware-bound'): validate_payload(data, manifest)
        manifest['environment'] = 'SM-A525F/DS hardware candidate'
        validate_payload(data, manifest)
        manifest['display_selftest']['guards'][1]['value'] = 1
        with self.assertRaisesRegex(ValueError, 'differs'): validate_payload(data, manifest)


if __name__ == '__main__':
    unittest.main()
