"""Measured local boot namespace; no Apple IMG4, signature or secure-boot trust."""
import hashlib
import json
import re

SCOPE = 'local development namespace only; unsealed, unauthenticated; not Apple IMG4 or secure-boot trust'


def document_bytes(document):
    return json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def measurement(kernel_sha256, root_sha256, live_dtb_sha256):
    values = (kernel_sha256, root_sha256, live_dtb_sha256)
    if any(type(value) is not str or not re.fullmatch('[0-9a-f]{64}', value) for value in values):
        raise ValueError('local boot manifest requires measured SHA256 inputs')
    document = dict(format='a52q-local-boot-manifest-v1', target='samsung,a52q',
        trust='local-development-unsealed', kernel_sha256=kernel_sha256,
        root_sha256=root_sha256, live_dtb_sha256=live_dtb_sha256)
    return dict(document=document, sha384=hashlib.sha384(document_bytes(document)).hexdigest(), scope=SCOPE)


def chosen_properties(record):
    document = record['document']
    if record != measurement(document['kernel_sha256'], document['root_sha256'], document['live_dtb_sha256']):
        raise ValueError('local boot manifest content or measurement differs')
    return {'boot-manifest-hash': bytes.fromhex(record['sha384']),
            'a52q-local-boot-manifest': document_bytes(document)}


def verify_chosen(chosen, record, kernel_sha256, root_sha256, live_dtb_sha256, development):
    names = ('boot-manifest-hash', 'a52q-local-boot-manifest')
    actual = [(name, value) for name, flags, value in chosen.props if name in names]
    if record is None:
        if actual: raise ValueError('boot manifest properties must be explicitly declared')
        return
    if not development:
        raise ValueError('local boot manifest requires explicit full-root development mode')
    expected = measurement(kernel_sha256, root_sha256, live_dtb_sha256)
    if record != expected or len(actual) != 2 or dict(actual) != chosen_properties(expected):
        raise ValueError('boot manifest properties differ from measured kernel/root/board evidence')
