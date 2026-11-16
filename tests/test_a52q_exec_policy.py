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
        end = source.index('\nstatic const amfi_t a52q_diagnostic_amfi', begin)
        function = source[begin:end]
        report = json.loads((root / 'xnu/a52q/ios16-20H392-cache-pins.json').read_text())
        pins = [bytes.fromhex(d['cdhash']) for f in report['files'] for d in f['code_directories']]
        entries = ',\n'.join('{' + ','.join(str(b) for b in pin) + '}' for pin in pins)
        boot_pin = json.loads((root / 'xnu/a52q/ios16-20H392-boot-task-pin.json').read_text())
        fsck_bytes = bytes.fromhex(boot_pin['directories'][0]['cdhash'])
        fips_meta = json.loads((root / 'xnu/a52q/ios16-20H392-fips-pin.json').read_text())
        fips_bytes = bytes.fromhex(fips_meta['directories'][0]['cdhash'])
        dirs_meta = json.loads((root / 'xnu/a52q/ios16-20H392-dirs-cleaner-pin.json').read_text())
        dirs_bytes = bytes.fromhex(dirs_meta['directories'][0]['cdhash'])
        loader_meta = json.loads((root / 'xnu/a52q/ios16-20H392-launchd-cache-loader-pin.json').read_text())
        loader_bytes = bytes.fromhex(loader_meta['directories'][0]['cdhash'])
        proxy_meta = json.loads((root / 'xnu/a52q/ios16-20H392-xpcproxy-pin.json').read_text())
        proxy_bytes = bytes.fromhex(proxy_meta['directories'][0]['cdhash'])
        cache_meta = json.loads((root / 'xnu/a52q/ios16-20H392-launchd-cache-pin.json').read_text())
        boot_cache_entries = ','.join('{' + ','.join(str(b) for b in bytes.fromhex(d['cdhash'])) + '}'
                                     for d in cache_meta['directories'])
        mount_meta = json.loads((root / 'xnu/a52q/ios16-20H392-mount-pin.json').read_text())
        mount_bytes = bytes.fromhex(mount_meta['directories'][0]['cdhash'])
        prefix = r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include "a52q_boot_cache_policy.h"
#include "a52q_root_code_catalog.h"
typedef int kern_return_t;
#define CS_CDHASH_LEN 20
#define CS_ADHOC 2
#define CS_VALID 1
#define CS_PLATFORM_BINARY 0x04000000
#define CS_SIGNED 0x20000000
#define MNT_RDONLY 1
#define MNT_ROOTFS 0x4000
#define VREG 1
#define KERN_SUCCESS 0
#define KERN_DENIED 53
#define KERN_NOT_FOUND 56
#define KERN_INVALID_ARGUMENT 4
#define KERN_RESOURCE_SHORTAGE 6
#define __unused __attribute__((unused))
#define printf(...) ((void)0)
typedef struct { uint32_t magic, length; } CS_GenericBlob;
struct cs_blob {
 uint32_t csb_flags;
 uint8_t csb_cdhash[20];
 struct fake_vnode *csb_vnode;
 int csb_platform_binary;
 void *csb_entitlements;
 const CS_GenericBlob *csb_entitlements_blob, *csb_der_entitlements_blob;
};
typedef struct fake_proc { uint64_t flags; struct cs_blob *blob; } *proc_t;
static uint64_t proc_getcsflags(proc_t proc) { return proc->flags; }
static struct cs_blob *csproc_get_blob(proc_t proc) { return proc->blob; }
static unsigned boolean_copies;
static int copy_failure;
static char boolean_true;
void *a52q_copy_bindfs_true(void) { boolean_copies++; return copy_failure ? NULL : &boolean_true; }
struct fake_mount { uint64_t flags; };
typedef struct fake_mount *mount_t;
struct fake_vnode { mount_t mount; int type; struct cs_blob *blob; };
typedef struct fake_vnode *vnode_t;
vnode_t rootvnode;
static vnode_t measured_cache_vnode;
static int measured_files_valid = 1;
static proc_t caller;
static proc_t current_proc(void) { return caller; }
static int a52q_boot_cache_files_verified(vnode_t required) {
 return measured_files_valid && (!required || required == measured_cache_vnode);
}
static mount_t vnode_mount(vnode_t vp) { return vp->mount; }
static uint64_t vfs_flags(mount_t mp) { return mp->flags; }
static int vnode_vtype(vnode_t vp) { return vp->type; }
static struct cs_blob *csvnode_get_blob(vnode_t vp, long offset) { assert(offset == 0); return vp->blob; }
static int xml_error, der_error, wrong_output;
static size_t xml_bytes=472, der_bytes=222;
/* Native policy harness models the kernel API return contract; the actual
   XML/DER hash algorithm is checked independently by the host auditor. */
static int csblob_get_entitlements(struct cs_blob *blob, void **out, size_t *size) {
 *out = wrong_output ? NULL : (void*)blob->csb_entitlements_blob; *size = xml_bytes; return xml_error;
}
static int csblob_get_der_entitlements(struct cs_blob *blob, const CS_GenericBlob **out, size_t *size) {
 *out = blob->csb_der_entitlements_blob; *size = wrong_output ? 0 : der_bytes; return der_error;
}
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
  assert(!(blob.csb_flags & (CS_PLATFORM_BINARY | CS_SIGNED)) && !blob.csb_platform_binary);
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
 /* The one observed boot task gets an explicit local development class. */
 struct fake_mount ro = {MNT_RDONLY | MNT_ROOTFS}, other = {MNT_RDONLY | MNT_ROOTFS};
 struct fake_vnode root = {&ro, 2, NULL}, task = {&ro, VREG, &blob};
 static const uint8_t fsck[20] = {BOOT_TASK_EXPECTED};
 rootvnode=&root; full_root=1;
 /* The data-cache signature is not an executable/platform identity. Both
    CodeDirectories require actual RO-root file identity and measurements. */
 static const uint8_t boot_cache_pins[][20]={BOOT_CACHE_EXPECTED};
 struct fake_vnode boot_cache={&ro,VREG,&blob};measured_cache_vnode=&boot_cache;
 for(unsigned i=0;i<2;i++) {
  memset(&blob,0,sizeof(blob));memcpy(blob.csb_cdhash,boot_cache_pins[i],20);
  blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_vnode=&boot_cache;
  assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
  assert(!(blob.csb_flags&(CS_PLATFORM_BINARY|CS_SIGNED)) && !blob.csb_platform_binary);
  for(unsigned byte=0;byte<20;byte++) {
   blob.csb_cdhash[byte]^=1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_cdhash[byte]^=1;
  }
  measured_files_valid=0;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);measured_files_valid=1;
  blob.csb_vnode=&task;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_vnode=&boot_cache;
  ro.flags=MNT_ROOTFS;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);ro.flags=MNT_ROOTFS|MNT_RDONLY;
  full_root=0;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);full_root=1;
  blob.csb_flags=CS_ADHOC;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_flags=CS_ADHOC|CS_VALID;
  blob.csb_entitlements=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_entitlements=NULL;
  blob.csb_entitlements_blob=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_entitlements_blob=NULL;
  blob.csb_der_entitlements_blob=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_der_entitlements_blob=NULL;
 }
 memset(&blob,0,sizeof(blob)); memcpy(blob.csb_cdhash,fsck,20);
 blob.csb_flags=CS_VALID | CS_ADHOC; blob.csb_vnode=&task;
 assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
 assert(blob.csb_platform_binary && (blob.csb_flags & CS_PLATFORM_BINARY));
 /* XNU kern_exec copies CS_SIGNED, and csproc_get_blob requires it before
    CS_OPS_STATUS can inspect the blob's platform field (patch0036 contract). */
 unsigned process_csflags=blob.csb_flags & CS_SIGNED;
 assert(process_csflags && blob.csb_platform_binary);
 process_csflags &= ~CS_SIGNED;
 assert(!process_csflags); /* same registered platform blob is hidden */
 for (unsigned byte=0; byte<20; byte++) {
  blob.csb_flags=CS_VALID | CS_ADHOC; blob.csb_platform_binary=0;
  blob.csb_cdhash[byte]^=1;
  assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
  assert(!blob.csb_platform_binary && !(blob.csb_flags & (CS_PLATFORM_BINARY | CS_SIGNED)));
  blob.csb_cdhash[byte]^=1;
 }
 full_root=0; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); full_root=1;
 ro.flags=MNT_ROOTFS; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 ro.flags=MNT_RDONLY | MNT_ROOTFS;
 task.mount=&other; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); task.mount=&ro;
 blob.csb_entitlements_blob=(void*)1; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 blob.csb_entitlements_blob=NULL; blob.csb_flags=CS_ADHOC;
 assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 blob.csb_flags=CS_VALID | CS_ADHOC; blob.csb_vnode=NULL;
 assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 /* Mandatory FIPS task gets the same RO-root, entitlement-free admission;
    its test outcome remains the real executable's responsibility. */
 static const uint8_t fips_hash[20] = {FIPS_EXPECTED};
 memset(&blob,0,sizeof(blob));memcpy(blob.csb_cdhash,fips_hash,20);
 blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_vnode=&task;
 assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
 assert(blob.csb_platform_binary && (blob.csb_flags & (CS_SIGNED|CS_PLATFORM_BINARY))==(CS_SIGNED|CS_PLATFORM_BINARY));
 struct fake_proc fips_process={CS_VALID|CS_SIGNED,&blob};
 assert(a52q_bool_proc(&fips_process,"com.apple.private.bindfs-allow")==KERN_DENIED);
 for(unsigned byte=0;byte<20;byte++) {
  blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_platform_binary=0;
  blob.csb_cdhash[byte]^=1;
  assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
  assert(!blob.csb_platform_binary && !(blob.csb_flags&(CS_SIGNED|CS_PLATFORM_BINARY)));
  blob.csb_cdhash[byte]^=1;
 }
 full_root=0;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);full_root=1;
 ro.flags=MNT_ROOTFS;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);ro.flags=MNT_RDONLY|MNT_ROOTFS;
 task.mount=&other;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);task.mount=&ro;
 blob.csb_entitlements_blob=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_entitlements_blob=NULL;
 blob.csb_der_entitlements_blob=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_der_entitlements_blob=NULL;
 blob.csb_entitlements=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_entitlements=NULL;
 blob.csb_flags=CS_ADHOC;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_vnode=NULL;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 assert(a52q_without_monitor((void*)1,&blob)==KERN_DENIED);
 /* Exact signed helpers retain metadata; xpcproxy gets no implicit admission
    for its children, and only the cache loader can use the measured query. */
 static const uint8_t signed_tasks[][20] = {{DIRS_EXPECTED},{LOADER_EXPECTED},{PROXY_EXPECTED}};
 static const size_t signed_xml_bytes[]={256,390,573}, signed_der_bytes[]={60,152,306};
 for(unsigned task_index=0;task_index<sizeof(signed_tasks)/sizeof(signed_tasks[0]);task_index++) {
 CS_GenericBlob dirs_xml={0}, dirs_der={0};
 memset(&blob,0,sizeof(blob));memcpy(blob.csb_cdhash,signed_tasks[task_index],20);
 blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_vnode=&task;
 blob.csb_entitlements_blob=&dirs_xml;blob.csb_der_entitlements_blob=&dirs_der;
 xml_bytes=signed_xml_bytes[task_index];der_bytes=signed_der_bytes[task_index];
 assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
 assert(blob.csb_platform_binary && (blob.csb_flags&(CS_SIGNED|CS_PLATFORM_BINARY))==(CS_SIGNED|CS_PLATFORM_BINARY));
 /* Real exec omits platform bits from raw p_csflags; blob classification
    remains mandatory and independently verified by the policy. */
 struct fake_proc query_process={CS_VALID|CS_SIGNED,&blob};
 caller=&query_process;
 assert(a52q_boot_cache_client_allowed()==(task_index==1));
 assert(a52q_boot_cache_query(boot_cache_pins[1],20)==(task_index==1));
 if(task_index==1) {
  uint8_t changed_hash[20];memcpy(changed_hash,boot_cache_pins[1],20);changed_hash[0]^=1;
  assert(!a52q_boot_cache_query(changed_hash,20));
  assert(!a52q_boot_cache_query(NULL,20));assert(!a52q_boot_cache_query(boot_cache_pins[1],19));
  measured_files_valid=0;assert(!a52q_boot_cache_query(boot_cache_pins[1],20));measured_files_valid=1;
  const unsigned required_flags[]={CS_VALID,CS_SIGNED};
  for(unsigned j=0;j<2;j++) {
   query_process.flags^=required_flags[j];assert(!a52q_boot_cache_client_allowed());query_process.flags^=required_flags[j];
  }
  xml_error=1;assert(!a52q_boot_cache_client_allowed());xml_error=0;
  der_error=1;assert(!a52q_boot_cache_client_allowed());der_error=0;
  blob.csb_platform_binary=0;assert(!a52q_boot_cache_client_allowed());blob.csb_platform_binary=1;
  blob.csb_flags&=~CS_PLATFORM_BINARY;assert(!a52q_boot_cache_client_allowed());blob.csb_flags|=CS_PLATFORM_BINARY;
 }
 caller=NULL;assert(!a52q_boot_cache_client_allowed());
 struct fake_proc dirs_process={CS_VALID|CS_SIGNED,&blob};
 assert(a52q_bool_proc(&dirs_process,"com.apple.private.bindfs-allow")==KERN_DENIED);
 assert(a52q_bool_proc(&dirs_process,"com.apple.private.security.storage.tmp")==KERN_DENIED);
 assert(a52q_bool_proc(&dirs_process,"com.apple.private.amfi.can-check-trust-cache")==KERN_DENIED);
 void *dirs_object=(void*)1;
 assert(a52q_object_proc(&dirs_process,"com.apple.private.bindfs-allow",&dirs_object)==KERN_NOT_FOUND && dirs_object==NULL);
 dirs_object=(void*)1;
 assert(a52q_object_proc(&dirs_process,"com.apple.security.iokit-user-client-class",&dirs_object)==KERN_NOT_FOUND && dirs_object==NULL);
 for(unsigned byte=0;byte<20;byte++) {
  blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_platform_binary=0;
  blob.csb_cdhash[byte]^=1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
  assert(!blob.csb_platform_binary && !(blob.csb_flags&(CS_SIGNED|CS_PLATFORM_BINARY)));
  blob.csb_cdhash[byte]^=1;
 }
 xml_error=1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);xml_error=0;
 der_error=1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);der_error=0;
 wrong_output=1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);wrong_output=0;
 xml_bytes--;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);xml_bytes++;
 der_bytes--;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);der_bytes++;
 blob.csb_entitlements=(void*)1;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_entitlements=NULL;
 blob.csb_entitlements_blob=NULL;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_entitlements_blob=&dirs_xml;
 blob.csb_der_entitlements_blob=NULL;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);blob.csb_der_entitlements_blob=&dirs_der;
 full_root=0;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);full_root=1;
 ro.flags=MNT_ROOTFS;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);ro.flags=MNT_RDONLY|MNT_ROOTFS;
 task.mount=&other;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);task.mount=&ro;
 blob.csb_flags=CS_ADHOC;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_vnode=NULL;assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 blob.csb_vnode=&task;assert(a52q_without_monitor((void*)1,&blob)==KERN_DENIED);
 }
 xml_bytes=472;der_bytes=222;
 /* The observed mount task retains signed XML/DER. */
 static const uint8_t mount_hash[20] = {MOUNT_EXPECTED};
 CS_GenericBlob xml = {0}, der = {0};
 memset(&blob,0,sizeof(blob)); memcpy(blob.csb_cdhash,mount_hash,20);
 blob.csb_flags=CS_VALID | CS_ADHOC; blob.csb_vnode=&task;
 blob.csb_entitlements_blob=&xml; blob.csb_der_entitlements_blob=&der;
 assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
 assert(blob.csb_platform_binary && (blob.csb_flags & CS_SIGNED));
 for (unsigned byte=0; byte<20; byte++) {
  blob.csb_flags=CS_VALID | CS_ADHOC; blob.csb_platform_binary=0;
  blob.csb_cdhash[byte]^=1;
  assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
  assert(!blob.csb_platform_binary && !(blob.csb_flags & (CS_SIGNED | CS_PLATFORM_BINARY)));
  blob.csb_cdhash[byte]^=1;
 }
 xml_error=1; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); xml_error=0;
 der_error=1; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); der_error=0;
 wrong_output=1; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); wrong_output=0;
 blob.csb_entitlements=(void*)1; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); blob.csb_entitlements=NULL;
 assert(a52q_without_monitor((void*)1,&blob)==KERN_DENIED);
 blob.csb_entitlements_blob=NULL; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); blob.csb_entitlements_blob=&xml;
 blob.csb_der_entitlements_blob=NULL; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); blob.csb_der_entitlements_blob=&der;
 ro.flags=MNT_ROOTFS; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); ro.flags=MNT_RDONLY|MNT_ROOTFS;
 task.mount=&other; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); task.mount=&ro;
 full_root=0; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED); full_root=1;
 blob.csb_flags=0; assert(a52q_without_monitor(NULL,&blob)==KERN_DENIED);
 /* Real IOKit capability callback: only the exact admitted signed mount may
    read its verified true bindfs Boolean. No context/string/other keys. */
 blob.csb_flags=CS_VALID|CS_ADHOC;
 assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
 struct fake_proc process={CS_VALID|CS_SIGNED,&blob};
 const char *key="com.apple.private.bindfs-allow";
 void *object=(void*)1;
 assert(a52q_bool_proc(&process,key)==KERN_SUCCESS);
 assert(a52q_object_proc(&process,key,&object)==KERN_SUCCESS && object==&boolean_true && boolean_copies==1);
 assert(a52q_object_proc(&process,key,NULL)==KERN_INVALID_ARGUMENT);
 assert(a52q_bool(NULL,key)==KERN_DENIED);
 assert(a52q_string(NULL,key,"true")==KERN_DENIED);
 assert(a52q_string_proc(&process,key,"true")==KERN_DENIED);
 assert(a52q_object(NULL,key,&object)==KERN_NOT_FOUND && object==NULL);
 assert(a52q_object(NULL,key,NULL)==KERN_NOT_FOUND);
 assert(a52q_bool_proc(NULL,key)==KERN_DENIED);
 assert(a52q_bool_proc(&process,NULL)==KERN_DENIED);
 const char *unapproved[]={"com.apple.private.security.disk-device-access",
  "com.apple.private.iokit.system-nvram-allow", "com.apple.private.bindfs-allow.extra", ""};
 for(unsigned i=0;i<sizeof(unapproved)/sizeof(unapproved[0]);i++) {
  assert(a52q_bool_proc(&process,unapproved[i])==KERN_DENIED);
  object=(void*)1;
  assert(a52q_object_proc(&process,unapproved[i],&object)==KERN_NOT_FOUND && object==NULL);
 }
 for(unsigned byte=0;byte<20;byte++) {
  blob.csb_cdhash[byte]^=1;
  assert(a52q_bool_proc(&process,key)==KERN_DENIED);
  blob.csb_cdhash[byte]^=1;
 }
 unsigned flags=process.flags;
 process.flags=CS_SIGNED;assert(a52q_bool_proc(&process,key)==KERN_DENIED);
 process.flags=CS_VALID;assert(a52q_bool_proc(&process,key)==KERN_DENIED);process.flags=flags;
 process.blob=NULL;assert(a52q_bool_proc(&process,key)==KERN_DENIED);process.blob=&blob;
 flags=blob.csb_flags;
 blob.csb_flags&=~CS_VALID;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_flags=flags;
 blob.csb_flags&=~CS_SIGNED;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_flags=flags;
 blob.csb_flags&=~CS_PLATFORM_BINARY;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_flags=flags;
 blob.csb_platform_binary=0;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_platform_binary=1;
 xml_error=1;assert(a52q_bool_proc(&process,key)==KERN_DENIED);xml_error=0;
 der_error=1;assert(a52q_bool_proc(&process,key)==KERN_DENIED);der_error=0;
 wrong_output=1;assert(a52q_bool_proc(&process,key)==KERN_DENIED);wrong_output=0;
 blob.csb_entitlements_blob=NULL;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_entitlements_blob=&xml;
 blob.csb_der_entitlements_blob=NULL;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_der_entitlements_blob=&der;
 blob.csb_entitlements=(void*)1;assert(a52q_bool_proc(&process,key)==KERN_DENIED);blob.csb_entitlements=NULL;
 full_root=0;assert(a52q_bool_proc(&process,key)==KERN_DENIED);full_root=1;
 ro.flags=MNT_ROOTFS;assert(a52q_bool_proc(&process,key)==KERN_DENIED);ro.flags=MNT_RDONLY|MNT_ROOTFS;
 task.mount=&other;assert(a52q_bool_proc(&process,key)==KERN_DENIED);task.mount=&ro;
 copy_failure=1;object=(void*)1;
 assert(a52q_object_proc(&process,key,&object)==KERN_RESOURCE_SHORTAGE && object==NULL);
 copy_failure=0;
 assert(boolean_copies==2); /* no rejected query may construct an object */
 /* Every measured standalone identity must pass the actual catalog checker.
    Page and signed-slot hashing are tested by the independent image auditor. */
 static const uint8_t springboard_pin[20]={
  0xea,0x63,0x7d,0x6b,0xde,0x7a,0xc2,0xfc,0xdb,0x20,
  0xb8,0x40,0x3d,0x7f,0xdc,0x10,0xe1,0x5f,0x20,0x6e};
 unsigned springboard_checked=0;
 for(unsigned n=0;n<sizeof(a52q_root_code_pins)/sizeof(a52q_root_code_pins[0]);n++) {
  const struct a52q_root_code_pin *pin=&a52q_root_code_pins[n];
  memset(&blob,0,sizeof(blob));memcpy(blob.csb_cdhash,pin->cdhash,20);
  blob.csb_flags=CS_VALID|CS_ADHOC;blob.csb_vnode=&task;
  blob.csb_entitlements_blob=pin->xml_bytes?&xml:NULL;
  blob.csb_der_entitlements_blob=pin->der_bytes?&der:NULL;
  xml_bytes=pin->xml_bytes;der_bytes=pin->der_bytes;
  assert(a52q_verified_catalog_blob(&blob)==(int)n);
  for(unsigned byte=0;byte<20;byte++) {
   blob.csb_cdhash[byte]^=1;assert(a52q_verified_catalog_blob(&blob)<0);blob.csb_cdhash[byte]^=1;
  }
  if(pin->xml_bytes) {
   xml_error=1;assert(a52q_verified_catalog_blob(&blob)<0);xml_error=0;
   xml_bytes--;assert(a52q_verified_catalog_blob(&blob)<0);xml_bytes++;
   wrong_output=1;assert(a52q_verified_catalog_blob(&blob)<0);wrong_output=0;
  }
  if(pin->der_bytes) {
   der_error=1;assert(a52q_verified_catalog_blob(&blob)<0);der_error=0;
   der_bytes--;assert(a52q_verified_catalog_blob(&blob)<0);der_bytes++;
  }
  blob.csb_entitlements=(void*)1;assert(a52q_verified_catalog_blob(&blob)<0);blob.csb_entitlements=NULL;
  const CS_GenericBlob *saved=blob.csb_entitlements_blob;
  blob.csb_entitlements_blob=pin->xml_bytes?NULL:&xml;
  assert(a52q_verified_catalog_blob(&blob)<0);blob.csb_entitlements_blob=saved;
  saved=blob.csb_der_entitlements_blob;blob.csb_der_entitlements_blob=pin->der_bytes?NULL:&der;
  assert(a52q_verified_catalog_blob(&blob)<0);blob.csb_der_entitlements_blob=saved;
  blob.csb_flags=CS_ADHOC;assert(a52q_verified_catalog_blob(&blob)<0);blob.csb_flags=CS_VALID|CS_ADHOC;
  ro.flags=MNT_ROOTFS;assert(a52q_verified_catalog_blob(&blob)<0);ro.flags=MNT_ROOTFS|MNT_RDONLY;
  task.mount=&other;assert(a52q_verified_catalog_blob(&blob)<0);task.mount=&ro;
  task.type=0;assert(a52q_verified_catalog_blob(&blob)<0);task.type=VREG;
  full_root=0;assert(a52q_verified_catalog_blob(&blob)<0);full_root=1;
  if(!memcmp(pin->cdhash,springboard_pin,20)) {
   assert(a52q_without_monitor(NULL,&blob)==KERN_SUCCESS);
   assert(blob.csb_platform_binary && (blob.csb_flags&(CS_SIGNED|CS_PLATFORM_BINARY))==(CS_SIGNED|CS_PLATFORM_BINARY));
   assert(!(blob.csb_flags&4)); /* no manufactured get-task-allow */
   struct fake_proc ui={CS_VALID|CS_SIGNED,&blob};
   assert(a52q_bool_proc(&ui,"com.apple.private.bindfs-allow")==KERN_DENIED);
   assert(a52q_bool_proc(&ui,"com.apple.private.IOSurface.protected-access")==KERN_DENIED);
   caller=&ui;assert(!a52q_boot_cache_client_allowed());caller=NULL;
   springboard_checked++;
  }
 }
 assert(springboard_checked==1);
 puts("PASS: exact kernel policy, all 44 cache pins and 880 changed hashes");
 return 0;
}
'''.replace('PROXY_EXPECTED', ','.join(str(v) for v in proxy_bytes)).replace('BOOT_CACHE_EXPECTED', boot_cache_entries).replace('LOADER_EXPECTED', ','.join(str(v) for v in loader_bytes)).replace('DIRS_EXPECTED', ','.join(str(v) for v in dirs_bytes)).replace('FIPS_EXPECTED', ','.join(str(v) for v in fips_bytes)).replace('MOUNT_EXPECTED', ','.join(str(v) for v in mount_bytes)).replace('BOOT_TASK_EXPECTED', ','.join(str(v) for v in fsck_bytes)).replace('EXPECTED', entries)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'policy.c'; path.write_text(prefix + function + body)
            executable = Path(directory) / ('policy.exe' if os.name == 'nt' else 'policy')
            compiled = subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-I', str(root / 'xnu/a52q'), str(path), '-o', str(executable)],
                                      capture_output=True, text=True)
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            result = subprocess.run([str(executable)], check=True, capture_output=True, text=True)
            self.assertIn('880 changed hashes', result.stdout)


if __name__ == '__main__': unittest.main()
