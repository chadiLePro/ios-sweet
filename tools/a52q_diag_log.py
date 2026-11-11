#!/usr/bin/env python3
"""Validate replicated A52QDIAG v2 logs recovered from pstore. Never fixes bytes.

At least one complete CRC32-valid copy is required. Intact copies must agree.
CRC32 detects accidental corruption; this is not cryptographic attestation.
"""
import argparse
import json
from pathlib import Path
import re
import zlib

TEXT_FIELDS = ('stage image image_end dtb current_el sctlr mpidr midr mmfr0 pfr0 '
               'cntfrq ctr isar0 isar1 exception_slot esr elr far').split()


def decode_checked_console(data):
    pattern = (rb'A52QDIAG v2 copy=([0-2])\n'
               rb'((?:[a-z0-9_]+=0x[0-9a-f]{16}\n)+)'
               rb'crc32=0x([0-9a-f]{16})\nA52QDIAG END\n')
    valid = []
    for match in re.finditer(pattern, data, flags=re.MULTILINE):
        index, body, checksum = match.groups()
        if zlib.crc32(body) != int(checksum, 16):
            continue
        rows = [row.split(b'=', 1) for row in body.splitlines()]
        fields = {k.decode('ascii'): int(v, 16) for k, v in rows}
        if len(rows) != len(fields) or set(fields) != set(TEXT_FIELDS):
            continue
        valid.append((int(index), body, fields))
    if not valid:
        raise ValueError('no complete CRC32-valid v2 copy; do not trust the register values')
    if len({i for i, _, _ in valid}) != len(valid):
        raise ValueError('duplicate copy identifiers; ambiguous console record')
    if len({body for _, body, _ in valid}) != 1:
        raise ValueError('CRC-valid copies disagree; refusing ambiguous diagnostic values')
    return {'format_version': 2, 'valid_copies': [i for i, _, _ in valid],
            'integrity': 'CRC32 verified; no bytes repaired', 'fields': valid[0][2]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('console', type=Path)
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    try:
        result = decode_checked_console(a.console.read_bytes())
    except (OSError, ValueError) as exc:
        p.exit(1, f'diagnostic rejected: {exc}\n')
    text = json.dumps(result, indent=2) + '\n'
    if a.out:
        a.out.write_text(text)
    print(text, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
