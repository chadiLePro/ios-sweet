"""Decode bounded CRC-protected keybag diagnostics; no key material is logged."""
import argparse
import json
from pathlib import Path
import re
import zlib


def decode(data):
    records = {}
    for match in re.finditer(rb'A52KB1 ([^\r\n]{1,239}) ([0-9a-f]{8})\r?\n', data):
        body, crc = match.groups()
        if zlib.crc32(body) != int(crc, 16):
            continue
        identity = re.match(rb'(open|match)/([1-9][0-9]?) ', body)
        if not identity or not 1 <= int(identity[2]) <= 80:
            raise ValueError('invalid keybag trace sequence')
        key = (identity[1].decode(), int(identity[2]))
        if key in records and records[key]['body'] != body.decode('utf-8'):
            raise ValueError('conflicting valid keybag trace copies')
        row = records.setdefault(key, dict(kind=key[0], sequence=key[1],
                                          body=body.decode('utf-8'), valid_copies=0))
        row['valid_copies'] += 1
    return dict(records=list(records.values()),
                scope='CRC integrity of observed names/statuses; no service success or keybag compatibility claim')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('console', type=Path)
    a = p.parse_args()
    print(json.dumps(decode(a.console.read_bytes()), indent=2))
