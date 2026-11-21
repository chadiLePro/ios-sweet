"""CRC-protected saved user registers; no inference of successful service startup."""
import argparse,json,re,zlib
from pathlib import Path

def decode(data):
    records={}
    for m in re.finditer(rb'A52CR1 ([^\r\n]{1,239}) ([0-9a-f]{8})\r?\n',data):
        if zlib.crc32(m[1])!=int(m[2],16):continue
        fields=m[1].decode('ascii').split('/')
        if (len(fields)!=8 or not re.fullmatch(r'[1-9][0-9]*',fields[0]) or
            fields[1] not in ('SpringBoard','logd','mediaserverd') or
            any(not re.fullmatch(r'[0-9a-f]{16}',v) for v in fields[2:])):
            raise ValueError('invalid CRC-valid crash register record')
        row=records.setdefault(m[1],dict(pid=int(fields[0]),process=fields[1],
            **{k:int(v,16) for k,v in zip(('slide','main_header','pc','lr','sp','fp'),fields[2:])},valid_copies=0))
        row['valid_copies']+=1
    return dict(records=list(records.values()),scope='saved registers with CRC integrity; symbolicate against measured binaries, not a service success claim')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('console',type=Path);a=p.parse_args()
    print(json.dumps(decode(a.console.read_bytes()),indent=2))
