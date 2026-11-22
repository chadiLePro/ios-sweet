"""Decode checked-copy backboardd frame chains retained in the RAM console."""
import argparse
import json
from pathlib import Path
import re
import zlib


def decode(data, recover_framing=False):
    records={}
    pattern=(rb'(?<![0-9a-f/])([1-9][0-9]*/backboardd/[0-9a-f/]{1,207}) ([0-9a-f]{8})'
        if recover_framing else rb'A52BT1 ([^\r\n]{1,207}) ([0-9a-f]{8})\r?\n')
    for match in re.finditer(pattern,data):
        if zlib.crc32(match[1])!=int(match[2],16):
            continue
        fields=match[1].decode('ascii').split('/')
        if (len(match[1])>207 or not 6<=len(fields)<=20 or fields[1]!='backboardd' or
            not re.fullmatch('[1-9][0-9]*',fields[0]) or
            any(not re.fullmatch('[0-9a-f]{1,16}',value) for value in fields[2:])):
            raise ValueError('invalid CRC-valid backboardd stack record')
        row=records.setdefault(match[1],dict(pid=int(fields[0]),process=fields[1],
            slide=int(fields[2],16),main_header=int(fields[3],16),
            pcs=[int(value,16) for value in fields[4:]],valid_copies=0))
        row['valid_copies']+=1
        if recover_framing:
            framed=data[max(0,match.start()-7):match.start()]==b'A52BT1 '
            key='original_framing_copies' if framed else 'recovered_framing_copies'
            row[key]=row.get(key,0)+1
    return dict(records=list(records.values()),
        scope='bounded frame-pointer samples; symbolize against measured files; no complete-unwind claim')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('console',type=Path)
    parser.add_argument('--recover-framing',action='store_true',
        help='accept damaged record prefixes only when the original body CRC and schema validate')
    args=parser.parse_args()
    print(json.dumps(decode(args.console.read_bytes(),args.recover_framing),indent=2))
