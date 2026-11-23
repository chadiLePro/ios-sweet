"""Decode bounded-/var writer diagnostics; no filesystem or UI success inferred."""
import argparse,json,re,zlib
from pathlib import Path


def decode(data,nonce):
    records={}
    for match in re.finditer(rb'A52W1 ([0-9a-f]{16}/[0-9a-f]{2}/[0-9a-f]{8}/[0-9a-f]{8}/[0-9a-f]{8}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(match[1])!=int(match[2],16):continue
        identity,phase,error,ocs,response=[int(part,16) for part in match[1].split(b'/')]
        if identity!=nonce:continue
        if phase not in (0x10,0xe0,0xe1) or ocs>15 or (phase==0x10 and (error or ocs or response!=0x21000000)):
            raise ValueError('invalid CRC-valid var-write record')
        key=(phase,error,ocs,response)
        row=records.setdefault(key,dict(phase=phase,error=error,ocs=ocs,response=response,valid_copies=0))
        row['valid_copies']+=1
    rows=list(records.values())
    return dict(records=rows,identical_block_probe_passed=any(r['phase']==0x10 for r in rows),
        failure_observed=any(r['phase']!=0x10 for r in rows),
        scope='write/synchronize/readback probe only; no mounted-writable filesystem, service or UI claim')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('console',type=Path);parser.add_argument('--nonce',required=True,type=lambda v:int(v,0))
    args=parser.parse_args();print(json.dumps(decode(args.console.read_bytes(),args.nonce),indent=2))
