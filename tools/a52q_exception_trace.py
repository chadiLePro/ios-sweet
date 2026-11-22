"""Decode CRC-protected, filtered backboardd heap-text observations."""
import argparse
import json
from pathlib import Path
import re
import zlib


def decode(data):
    records={}
    for match in re.finditer(rb'A52EX1 ([^\r\n]{1,207}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(match[1])!=int(match[2],16):continue
        fields=match[1].decode('ascii').split('/',3)
        if (len(fields)!=4 or not re.fullmatch('[1-9][0-9]*',fields[0]) or
            fields[1]!='backboardd' or fields[2] not in ('1','2','3') or
            not 1<=len(fields[3])<=159 or any(not 32<=ord(c)<127 for c in fields[3])):
            raise ValueError('invalid CRC-valid exception-text record')
        row=records.setdefault(match[1],dict(pid=int(fields[0]),process=fields[1],
            rank=int(fields[2]),text=fields[3],valid_copies=0))
        row['valid_copies']+=1
    return dict(records=list(records.values()),scope='filtered heap text observed during abort; not proof of the active exception object')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('console',type=Path)
    args=parser.parse_args()
    print(json.dumps(decode(args.console.read_bytes()),indent=2))
