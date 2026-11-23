"""Decode real HFS exchange outcomes; never infer daemon/GUI startup from them."""
import argparse,json,re,zlib
from pathlib import Path


def decode(data,nonce):
    records={}
    for match in re.finditer(rb'A52A1 ([0-9a-f]{16}/[1-9][0-9]*/[12]/[0-9a-f]{8}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(match[1])!=int(match[2],16):continue
        identity,pid,kind,error=match[1].split(b'/')
        if int(identity,16)!=nonce:continue
        key=match[1]
        row=records.setdefault(key,dict(pid=int(pid),kind=int(kind),error=int(error,16),valid_copies=0))
        row['valid_copies']+=1
    rows=list(records.values())
    return dict(records=rows,exchange_success_observed=any(not r['error'] for r in rows),
        failure_observed=any(r['error'] for r in rows),
        scope='authorized HFS exchange helper outcomes only; not proof of persona, daemon or display startup')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('console',type=Path);parser.add_argument('--nonce',required=True,type=lambda v:int(v,0))
    args=parser.parse_args();print(json.dumps(decode(args.console.read_bytes(),args.nonce),indent=2))
