"""Decode bounded late graphics observations; no service-success inference."""
import argparse
import json
from pathlib import Path
import re
import zlib


def decode(data, nonce=None):
    rows={}
    for match in re.finditer(rb'A52OBS1 ([^\r\n]{1,207}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(match[1])!=int(match[2],16):continue
        parts=match[1].decode('ascii').split('/',3)
        if (len(parts)!=4 or not re.fullmatch('[0-9a-f]{16}',parts[0]) or
            not re.fullmatch('[0-9a-f]{8}',parts[1]) or parts[2] not in ('00','01','02','03','04','05') or
            not parts[3] or any(ord(c)<32 or ord(c)>126 for c in parts[3])):
            raise ValueError('invalid CRC-valid late graphics record')
        if nonce is not None and int(parts[0],16)!=nonce:continue
        key=(parts[0],int(parts[1],16))
        row=rows.setdefault(key,dict(nonce=parts[0],sequence=key[1],slot=int(parts[2],16),payload=parts[3],valid_copies=0))
        if row['slot']!=int(parts[2],16) or row['payload']!=parts[3]:
            raise ValueError('conflicting CRC-valid late graphics record')
        row['valid_copies']+=1
    return dict(records=sorted(rows.values(),key=lambda r:(r['nonce'],r['sequence'])),
        scope='CRC-valid sampled state and latest per-slot observations; absence is not success or proof of no operation')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('console',type=Path)
    parser.add_argument('--nonce',type=lambda v:int(v,16))
    args=parser.parse_args()
    print(json.dumps(decode(args.console.read_bytes(),args.nonce),indent=2))
