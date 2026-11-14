"""Compile the actual C allowlist body; XNU ABI/page validation is separate."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class ExecPolicyTests(unittest.TestCase):
    def test_exact_policy_rejects_unknown_changed_entitled_and_wrong_root(self):
        root = Path(__file__).resolve().parents[1]
        compiler = shutil.which('gcc')
        if os.name == 'nt' and Path('C:/winlibs/mingw64/bin/gcc.exe').exists():
            compiler = 'C:/winlibs/mingw64/bin/gcc.exe'
        if not compiler: self.skipTest('native C compiler unavailable')
        source = (root / 'xnu/a52q/a52q_amfi.c').read_text()
        begin = source.index('static int a52q_cache_pin_index(')
        end = source.index('\nstatic kern_return_t a52q_bool(', begin)
        function = source[begin:end]
        report = json.loads((root / 'xnu/a52q/ios16-20H392-cache-pins.json').read_text())
        pins = [bytes.fromhex(d['cdhash']) for f in report['files'] for d in f['code_directories']]
        entries = ',\n'.join('{' + ','.join(str(b) for b in pin) + '}' for pin in pins)
        prefix = r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef int kern_return_t;
#define CS_CDHASH_LEN 20
#define CS_ADHOC 2
#define CS_VALID 1
#define MNT_RDONLY 1
#define MNT_ROOTFS 0x4000
#define VREG 1
#define KERN_SUCCESS 0
#define KERN_DENIED 53
#define printf(...) ((void)0)
struct cs_blob {
 uint32_t csb_flags;
 uint8_t csb_cdhash[20];
 void *csb_entitlements, *csb_entitlements_blob, *csb_der_entitlements_blob;
};
struct fake_mount { uint64_t flags; };
typedef struct fake_mount *mount_t;
struct fake_vnode { mount_t mount; int type; struct cs_blob *blob; };
typedef struct fake_vnode *vnode_t;
static mount_t vnode_mount(vnode_t vp) { return vp->mount; }
static uint64_t vfs_flags(mount_t mp) { return mp->flags; }
static int vnode_vtype(vnode_t vp) { return vp->type; }
static struct cs_blob *csvnode_get_blob(vnode_t vp, long offset) { assert(offset == 0); return vp->blob; }
static int full_root;
int a52q_ufs_root_named(const char *name) { return full_root && !strcmp(name, "a52ios0"); }
'''
        body = r'''
int main(void) {
 static const uint8_t expected[][20] = {EXPECTED};
 struct cs_blob blob = {0};
 full_root = 1;
 assert(a52q_without_monitor(NULL, NULL) == KERN_DENIED);
 assert(a52q_without_monitor(NULL, &blob) == KERN_DENIED);
 for (unsigned i=0; i<sizeof(expected)/sizeof(expected[0]); i++) {
  memset(&blob, 0, sizeof(blob)); memcpy(blob.csb_cdhash, expected[i], 20);
  full_root=1;
  assert(a52q_without_monitor(NULL, &blob) == KERN_SUCCESS);
  for (unsigned byte=0; byte<20; byte++) {
   blob.csb_cdhash[byte]^=1;
   assert(a52q_without_monitor(NULL, &blob) == KERN_DENIED);
   blob.csb_cdhash[byte]^=1;
  }
  full_root=0;
  assert(a52q_without_monitor(NULL, &blob) == KERN_DENIED);
  full_root=1;
  assert(a52q_without_monitor((void*)1, &blob) == KERN_DENIED);
  blob.csb_entitlements=(void*)1;
  assert(a52q_without_monitor(NULL, &blob) == KERN_DENIED);
  blob.csb_entitlements=NULL; blob.csb_entitlements_blob=(void*)1;
  assert(a52q_without_monitor(NULL, &blob) == KERN_DENIED);
  blob.csb_entitlements_blob=NULL; blob.csb_der_entitlements_blob=(void*)1;
  assert(a52q_without_monitor(NULL, &blob) == KERN_DENIED);
  blob.csb_der_entitlements_blob=NULL;
  struct fake_mount ro = {MNT_RDONLY | MNT_ROOTFS}, other = {MNT_RDONLY | MNT_ROOTFS};
  struct fake_vnode root = {&ro, 2, NULL}, cache = {&ro, VREG, &blob};
  assert(!a52q_cache_root_mapping_allowed(&cache, &root)); /* CS_VALID missing */
  blob.csb_flags=CS_VALID;
  assert(a52q_cache_root_mapping_allowed(&cache, &root));
  for (unsigned byte=0; byte<20; byte++) {
   blob.csb_cdhash[byte]^=1;
   assert(!a52q_cache_root_mapping_allowed(&cache, &root));
   blob.csb_cdhash[byte]^=1;
  }
  full_root=0; assert(!a52q_cache_root_mapping_allowed(&cache, &root)); full_root=1;
  cache.mount=&other; assert(!a52q_cache_root_mapping_allowed(&cache, &root)); cache.mount=&ro;
  ro.flags=MNT_ROOTFS; assert(!a52q_cache_root_mapping_allowed(&cache, &root));
  ro.flags=MNT_RDONLY; assert(!a52q_cache_root_mapping_allowed(&cache, &root));
  ro.flags=MNT_RDONLY | MNT_ROOTFS;
  cache.type=2; assert(!a52q_cache_root_mapping_allowed(&cache, &root)); cache.type=VREG;
  cache.blob=NULL; assert(!a52q_cache_root_mapping_allowed(&cache, &root)); cache.blob=&blob;
  blob.csb_entitlements_blob=(void*)1; assert(!a52q_cache_root_mapping_allowed(&cache, &root));
  blob.csb_entitlements_blob=NULL;
  assert(!a52q_cache_root_mapping_allowed(NULL, &root));
  assert(!a52q_cache_root_mapping_allowed(&cache, NULL));
 }
 puts("PASS: exact kernel policy, all 44 cache pins and 880 changed hashes");
 return 0;
}
'''.replace('EXPECTED', entries)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'policy.c'; path.write_text(prefix + function + body)
            executable = Path(directory) / ('policy.exe' if os.name == 'nt' else 'policy')
            subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', str(path), '-o', str(executable)],
                           check=True, capture_output=True)
            result = subprocess.run([str(executable)], check=True, capture_output=True, text=True)
            self.assertIn('880 changed hashes', result.stdout)


if __name__ == '__main__': unittest.main()
