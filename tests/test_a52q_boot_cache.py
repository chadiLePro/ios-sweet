"""Compile the actual portable request/measurement boundary; no Apple files."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class BootCachePolicyTests(unittest.TestCase):
    def test_exact_cache_and_request_reject_mutations_and_extra_capabilities(self):
        root = Path(__file__).resolve().parents[1]
        compiler = shutil.which('gcc')
        if os.name == 'nt' and Path('C:/winlibs/mingw64/bin/gcc.exe').exists():
            compiler = 'C:/winlibs/mingw64/bin/gcc.exe'
        if not compiler: self.skipTest('native C compiler unavailable')
        metadata = json.loads((root / 'xnu/a52q/ios16-20H392-launchd-cache-pin.json').read_text())
        def array(value): return '{' + ','.join(str(b) for b in bytes.fromhex(value)) + '}'
        text = r'''
#include <assert.h>
#include <string.h>
#include "a52q_boot_cache_policy.h"
int main(void) {
 uint8_t code[32]=CODE, signature[32]=SIGNATURE;
 uint8_t hashes[][20]={HASHES};
 assert(a52q_boot_cache_measurements_match(code,CODE_BYTES,signature,SIG_BYTES));
 for(unsigned i=0;i<32;i++) {
  code[i]^=1;assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES,signature,SIG_BYTES));code[i]^=1;
  signature[i]^=1;assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES,signature,SIG_BYTES));signature[i]^=1;
 }
 assert(!a52q_boot_cache_measurements_match(NULL,CODE_BYTES,signature,SIG_BYTES));
 assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES,NULL,SIG_BYTES));
 assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES-1,signature,SIG_BYTES));
 assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES+1,signature,SIG_BYTES));
 assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES,signature,SIG_BYTES-1));
 assert(!a52q_boot_cache_measurements_match(code,CODE_BYTES,signature,SIG_BYTES+1));
 for(unsigned i=0;i<2;i++) {
  assert(a52q_boot_cache_hash_index(hashes[i],20)==(int)i);
  for(unsigned j=0;j<20;j++) {
   hashes[i][j]^=1;assert(a52q_boot_cache_hash_index(hashes[i],20)<0);hashes[i][j]^=1;
  }
 }
 assert(a52q_boot_cache_hash_index(NULL,20)<0);
 assert(a52q_boot_cache_hash_index(hashes[0],19)<0);
 assert(a52q_boot_cache_hash_index(hashes[0],21)<0);
 assert(a52q_boot_cache_request_valid(6,1,1,20,0,0,0,0));
 for(unsigned i=0;i<16;i++) if(i!=6) assert(!a52q_boot_cache_request_valid(i,1,1,20,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,0,1,20,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,2,1,20,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,0,20,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,UINT64_MAX,20,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,1,19,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,1,21,0,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,1,20,1,0,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,1,20,0,1,0,0));
 assert(!a52q_boot_cache_request_valid(6,1,1,20,0,0,1,0));
 assert(!a52q_boot_cache_request_valid(6,1,1,20,0,0,0,1));
 return 0;
}
'''.replace('CODE_BYTES', str(metadata['bytes'])).replace('SIG_BYTES', str(metadata['signature_bytes']))
        text = text.replace('CODE', array(metadata['sha256'])).replace('SIGNATURE', array(metadata['signature_sha256']))
        text = text.replace('HASHES', ','.join(array(d['cdhash']) for d in metadata['directories']))
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'boundary.c'; source.write_text(text)
            executable = Path(directory) / ('boundary.exe' if os.name == 'nt' else 'boundary')
            built = subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror',
                                    '-I', str(root / 'xnu/a52q'), str(source), '-o', str(executable)],
                                   capture_output=True, text=True)
            self.assertEqual(built.returncode, 0, built.stderr)
            subprocess.run([str(executable)], check=True, capture_output=True)


if __name__ == '__main__': unittest.main()
