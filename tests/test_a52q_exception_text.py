import os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'xnu/a52q'));import failure_reason
sys.path.insert(0,str(R/'tools'));from a52q_exception_trace import decode


class ExceptionTextTests(unittest.TestCase):
    def test_observer_keeps_more_specific_reason_with_same_long_prefix(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        patch=(R/'xnu/patches/0051-sweet-crash-heap-strings.patch').read_text()
        # Reconstruct the checked-in upstream helper, including context lines.
        source='\n'.join(line[1:] for line in patch.splitlines()
            if line[:1] in ('+',' ') and not line.startswith('+++'))
        source=source[source.index('static void\nsweet_crash_strings'):source.index('#endif')]
        code=failure_reason.helper(source+'\n/*\n * SWEET process sampler')
        prefix=r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_A52Q 1
#define VM_PROT_READ 1
#define VM_PROT_WRITE 2
#define VM_REGION_SUBMAP_INFO_V2_COUNT_64 1
#define KERN_SUCCESS 0
#define Z_WAITOK 0
typedef int vm_map_t;
typedef uint64_t vm_map_offset_t,vm_map_size_t,user_addr_t;
typedef unsigned natural_t,mach_msg_type_number_t;
typedef struct {int is_submap,protection,user_tag;} vm_region_submap_info_data_64_t;
typedef vm_region_submap_info_data_64_t *vm_region_submap_info_64_t;
static char heap[65536];static unsigned records;
static int enabled=1;
static vm_map_t current_map(void){return 0;}
static int PE_parse_boot_argn(const char *key,char *out,size_t size){
 assert(!strcmp(key,"a52qscan") && size>=11);strcpy(out,"backboardd");return enabled;
}
static void *kalloc_data(size_t size,int flags){(void)flags;return malloc(size);}
static void kfree_data(void *p,size_t size){(void)size;free(p);}
static int vm_map_region_recurse_64(vm_map_t map,vm_map_offset_t *addr,
 vm_map_size_t *size,natural_t *depth,vm_region_submap_info_64_t info,
 mach_msg_type_number_t *count){
 (void)map;(void)depth;(void)count;if(*addr)return 1;
 *size=sizeof(heap);info->is_submap=0;info->protection=3;info->user_tag=1;return 0;
}
static int copyin(user_addr_t addr,void *out,size_t size){
 assert(addr+size<=sizeof(heap));memcpy(out,heap+addr,size);return 0;
}
void a52q_early_critical(const char *line,unsigned length,unsigned slot){
 assert(length==strlen(line) && slot==7);++records;
}
'''
        checks=r'''
int main(void){
 const char *lead="NSInvalidArgumentException ";
 memcpy(heap,lead,strlen(lead));memset(heap+strlen(lead),'x',96-strlen(lead));
 strcpy(heap+96," generic reason");
 memcpy(heap+256,heap,96);strcpy(heap+352," nil string parameter");
 a52q_crash_strings("SpringBoard",1);assert(records==0);
 enabled=0;a52q_crash_strings("backboardd",1);assert(records==0);
 enabled=1;a52q_crash_strings("backboardd",1);assert(records==2);return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            code=code.replace('<arm64/a52q_fb_console.h>','"a52q_fb_console.h"')
            path=Path(directory)/'observer.c';path.write_text(prefix+code+checks)
            exe=Path(directory)/('observer.exe' if os.name=='nt' else 'observer')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-Wno-format',
                '-I',str(R/'xnu/a52q'),str(path),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True)
            self.assertEqual(v.returncode,0,v.stderr)
            self.assertEqual([row['rank'] for row in decode(v.stdout)['records']],[1,3])

    def test_native_filter_crc_and_bounded_record(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        prefix=r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_A52Q 1
static unsigned calls;
void a52q_early_critical(const char *line,unsigned length,unsigned slot) {
 assert(length==strlen(line) && length<240 && slot==7);++calls;
}
'''
        checks=r'''
int main(void) {
 assert(!a52q_reason_rank("ordinary heap text with spaces"));
 assert(a52q_reason_rank("NSInvalidArgumentException reason text")==1);
 assert(a52q_reason_rank("Error getting shared system container x")==2);
 assert(a52q_reason_rank("NSInvalidArgumentException nil string parameter")==3);
 a52q_reason_record(9,1,"NSInvalidArgumentException reason text");
 a52q_reason_record(9,2,"Error getting shared system container x");
 a52q_reason_record(9,3,"NSURL nil string parameter");
 assert(calls==3);return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            recorder=failure_reason.RECORDER.replace('<arm64/a52q_fb_console.h>','"a52q_fb_console.h"')
            p=Path(directory)/'reason.c';p.write_text(prefix+recorder+'\n#endif\n'+checks)
            exe=Path(directory)/('reason.exe' if os.name=='nt' else 'reason')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-I',str(R/'xnu/a52q'),str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True);self.assertEqual(v.returncode,0,v.stderr)
            rows=decode(v.stdout)['records']
            self.assertEqual([r['rank'] for r in rows],[1,2,3])
            self.assertTrue(all(r['valid_copies']==3 for r in rows))
            damaged=v.stdout.replace(b'A52EX1 ',b'\x0150EX1 ')
            self.assertEqual(decode(damaged)['records'],[])
            recovered=decode(damaged,recover_framing=True)['records']
            self.assertTrue(all(r['recovered_framing_copies']==3 for r in recovered))
            self.assertEqual(len(decode(damaged.replace(b'parameter',b'parameteX'),True)['records']),2)
            self.assertEqual(decode(v.stdout.replace(b'parameter',b'parameteX'))['records'][-1]['rank'],2)
