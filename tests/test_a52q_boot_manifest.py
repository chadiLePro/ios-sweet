"""Bind the development namespace to measured inputs; reject unsupported trust."""
import copy
import hashlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import adt
from a52q_boot_manifest import measurement, document_bytes, chosen_properties, verify_chosen
from test_a52q_payload import fixture
from a52q_payload import validate_payload


class LocalBootManifestTests(unittest.TestCase):
    def test_rejects_altered_inputs_properties_and_trust_claim(self):
        inputs = ['a'*64, 'b'*64, 'c'*64]
        record = measurement(*inputs)
        self.assertEqual(len(bytes.fromhex(record['sha384'])), 48)
        chosen = adt.Node()
        chosen.props = [(name, 0, value) for name, value in chosen_properties(record).items()]
        verify_chosen(chosen, record, *inputs, True)
        for index in range(3):
            changed = inputs.copy();changed[index] = 'd'*64
            with self.assertRaises(ValueError): verify_chosen(chosen, record, *changed, True)
        with self.assertRaises(ValueError): verify_chosen(chosen, record, *inputs, False)
        with self.assertRaises(ValueError): verify_chosen(chosen, None, *inputs, True)
        for name in ('boot-manifest-hash', 'a52q-local-boot-manifest'):
            changed = copy.deepcopy(chosen)
            changed.props = [(n,f,b'changed' if n==name else v) for n,f,v in changed.props]
            with self.assertRaises(ValueError): verify_chosen(changed, record, *inputs, True)
        changed = copy.deepcopy(chosen);changed.props.append(changed.props[0])
        with self.assertRaises(ValueError): verify_chosen(changed, record, *inputs, True)
        changed = copy.deepcopy(record);changed['document']['trust'] = 'Apple secure boot'
        changed['sha384'] = hashlib.sha384(document_bytes(changed['document'])).hexdigest()
        with self.assertRaises(ValueError): chosen_properties(changed)
        for value in ('unmeasured', 'A'*64, 'a'*63, None):
            with self.assertRaises(ValueError): measurement(value, *inputs[1:])

    def test_payload_rejects_undeclared_hash_even_with_updated_container_hash(self):
        data, manifest = fixture()
        import struct
        offset, size = struct.unpack_from('<2Q', data, 0x20)
        tree, _ = adt.parse(data[offset:offset+size])
        chosen = next(node for node in tree.children if node.name=='chosen')
        chosen.props.append(('boot-manifest-hash', 0, bytes(48)))
        encoded = adt.serialize(tree)
        data[offset:offset+size] = encoded
        struct.pack_into('<Q', data, 0x28, len(encoded))
        manifest['payload_sha256'] = hashlib.sha256(data).hexdigest()
        with self.assertRaisesRegex(ValueError, 'explicitly declared'):
            validate_payload(data, manifest)
