"""Decode checked-copy backboardd frame chains retained in the RAM console."""
import argparse
import json
from pathlib import Path
import re
import zlib


def decode(data):
    records={}
    for match in re.finditer(rb'A52BT1 ([^\r\n]{1,207}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(match[1])!=int(match[2],16):
            continue
        fields=match[1].decode('ascii').split('/')
        if (not 6<=len(fields)<=20 or fields[1]!='backboardd' or
            not re.fullmatch('[1-9][0-9]*',fields[0]) or
            any(not re.fullmatch('[0-9a-f]{1,16}',value) for value in fields[2:])):
            raise ValueError('invalid CRC-valid backboardd stack record')
        row=records.setdefault(match[1],dict(pid=int(fields[0]),process=fields[1],
            slide=int(fields[2],16),main_header=int(fields[3],16),
            pcs=[int(value,16) for value in fields[4:]],valid_copies=0))
        row['valid_copies']+=1
    return dict(records=list(records.values()),
        scope='bounded frame-pointer samples; symbolize against measured files; no complete-unwind claim')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('console',type=Path)
    args=parser.parse_args()
    print(json.dumps(decode(args.console.read_bytes()),indent=2))
