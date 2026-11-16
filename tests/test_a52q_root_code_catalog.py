"""Synthetic signed inputs; no Apple code or mounted image required."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_root_code_catalog import arm64_slice, entries, header, measure
from test_a52q_userland_audit import fixture, entitled_fixture


def catalog(data):
    row = measure(data)
    row['paths'] = ['/usr/libexec/synthetic']
    return dict(format='a52q-root-code-catalog-v1', build='20H392',
                complete_walk=True, master_sha256='01' * 32, measured_files=[row])


class RootCodeCatalogTests(unittest.TestCase):
    def test_checked_in_catalog_header_matches_audit_manifest(self):
        root = Path(__file__).resolve().parents[1] / 'xnu/a52q'
        metadata = json.loads((root / 'ios16-20H392-root-code-catalog.json').read_text())
        # apply.py and Git use LF source text; normalize checkout line endings.
        data = (root / 'a52q_root_code_catalog.h').read_text(encoding='utf-8').encode('utf-8')
        self.assertEqual(hashlib.sha256(data).hexdigest(), metadata['generated_header_sha256'])
        self.assertIn(metadata['master_sha256'].encode(), data)
        self.assertEqual(data.count(b'    {{'), metadata['code_identities'])

    def test_measures_original_pages_and_signed_slots(self):
        report = catalog(entitled_fixture())
        rows = entries(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], tuple(report['measured_files'][0]['entitlement_blobs'][str(n)]['bytes'] for n in (5, 7)))
        self.assertIn('0x', header(report))
        self.assertIn('01' * 32, header(report))

    def test_changed_code_and_metadata_reject(self):
        data = fixture(); data[1024] ^= 1
        with self.assertRaisesRegex(ValueError, 'page hash mismatch'):
            measure(data)
        data = entitled_fixture(); data[-1] ^= 1
        with self.assertRaisesRegex(ValueError, 'special-slot hash mismatch'):
            measure(data)

    def test_fat_slice_bounds_and_ambiguous_architectures(self):
        thin = bytes(fixture()); offset = 4096
        fat = struct.pack('>7I', 0xcafebabe, 1, 0x100000c, 0, offset, len(thin), 12)
        fat += bytes(offset - len(fat)) + thin
        self.assertEqual(arm64_slice(fat), thin)
        self.assertEqual(measure(fat)['slice_sha256'], measure(thin)['sha256'])
        broken = bytearray(fat); struct.pack_into('>I', broken, 16, len(fat) + 1)
        with self.assertRaisesRegex(ValueError, 'slice exceeds'):
            measure(broken)
        fat = struct.pack('>I', 0xcafebabe) + struct.pack('>I', 2) + struct.pack('>5I', 0x100000c, 0, offset, len(thin), 12) * 2
        fat += bytes(offset - len(fat)) + thin
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            measure(fat)

    def test_incomplete_empty_or_wrong_build_reject(self):
        report = catalog(fixture())
        for field, value in (('complete_walk', False), ('build', 'other'),
                             ('master_sha256', '00'), ('measured_files', [])):
            bad = copy.deepcopy(report); bad[field] = value
            with self.assertRaises(ValueError):
                entries(bad)

    def test_deduplicates_identity_and_rejects_metadata_conflict(self):
        report = catalog(entitled_fixture())
        report['measured_files'].append(copy.deepcopy(report['measured_files'][0]))
        self.assertEqual(len(entries(report)), 1)
        report['measured_files'][1]['entitlement_blobs']['5']['bytes'] += 1
        with self.assertRaisesRegex(ValueError, 'inconsistent metadata'):
            entries(report)

    def test_unverified_slots_and_pages_reject(self):
        report = catalog(entitled_fixture())
        report['measured_files'][0]['entitlement_blobs']['5']['special_slot_hashes_match'] = False
        with self.assertRaisesRegex(ValueError, 'unverified signed metadata'):
            entries(report)
        report = catalog(fixture())
        report['measured_files'][0]['directories'][0]['executable_page_hashes_match'] = False
        with self.assertRaisesRegex(ValueError, 'unverified code pages'):
            entries(report)


if __name__ == '__main__':
    unittest.main()
