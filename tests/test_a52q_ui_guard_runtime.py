"""Execute the real optional adapter with synthetic DT/MMIO and clock APIs."""
import os,shutil,subprocess,tempfile,unittest,zlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class UIGuardRuntimeTests(unittest.TestCase):
    def test_absence_guard_rejection_submit_and_timeout_without_reset(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native C compiler unavailable')
        source=(R/'xnu/a52q/a52q_ui_bridge.c').read_text()
        source='\n'.join(l for l in source.splitlines() if not l.startswith('#include'))
        source=source.replace('__asm__ volatile("dsb sy" ::: "memory");','harness_barrier();')
        self.assertEqual(source.count('harness_barrier();'),2)
        prefix=r"""
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include "a52q_ui_profile.h"
#include "a52q_ui_bridge.h"
#define ARM64_BOARD_CONFIG_A52Q 1
#define kSuccess 0
#define VM_WIMG_WCOMB 3
#define NSEC_PER_MSEC 1000000ULL
typedef uintptr_t vm_offset_t;
typedef size_t vm_size_t;
typedef int DTEntry;
static int flag=1,other=0,reg_maps,frame_maps,consume=1;
static uint32_t regs[13],geometry[3]={1080,2400,4320};
static uint64_t region[2]={A52Q_UI_PHYS,A52Q_UI_BYTES},nonce=81,ram_base=0x106000000ULL,ram_size=0xff00000;
static uint64_t start_address;
static struct a52q_ui_guard guards[13];
static unsigned char *frame;
static uint64_t ticks;
static int test_snprintf(char *p,size_t n,const char *fmt,...) {
 va_list a;va_start(a,fmt);int v=vsnprintf(p,n,fmt,a);va_end(a);return v;
}
#define snprintf test_snprintf
static int PE_parse_boot_argn(const char *n,void *p,size_t bytes) {
 assert(!strcmp(n,"a52q_ui") && bytes==sizeof(int));memcpy(p,&flag,bytes);return 1;
}
static int SecureDTLookupEntry(void *unused,const char *name,DTEntry *out) {
 assert(!unused);
 if (!strcmp(name,"/a52q-ui-bridge")){*out=1;return 0;}
 if (!strcmp(name,"/chosen")){*out=2;return 0;}
 if (!strcmp(name,"/a52q-display-selftest"))return other ? 0 : -1;
 return -1;
}
static int SecureDTGetProperty(DTEntry node,const char *name,const void **p,unsigned *size) {
 assert(node==1 || node==2);
 if(!strcmp(name,"reg")){*p=region;*size=sizeof(region);}
 else if(!strcmp(name,"geometry")){*p=geometry;*size=sizeof(geometry);}
 else if(!strcmp(name,"guards")){*p=guards;*size=sizeof(guards);}
 else if(!strcmp(name,"nonce")){*p=&nonce;*size=sizeof(nonce);}
 else if(!strcmp(name,"start-register")){*p=&start_address;*size=sizeof(start_address);}
 else if(!strcmp(name,"dram-base")){*p=&ram_base;*size=sizeof(ram_base);}
 else if(!strcmp(name,"dram-size")){*p=&ram_size;*size=sizeof(ram_size);}
 else return -1;
 return 0;
}
vm_offset_t ml_io_map(vm_offset_t address,vm_size_t bytes) {
 assert(bytes==4);
 for(unsigned i=0;i<13;i++)if(address==a52q_ui_expected[i].address){++reg_maps;return(uintptr_t)&regs[i];}
 assert(!"unapproved MMIO map");return 0;
}
vm_offset_t ml_io_map_unmappable(vm_offset_t address,vm_size_t bytes,unsigned flags) {
 assert(address==A52Q_UI_PHYS && bytes==A52Q_UI_BYTES && flags==VM_WIMG_WCOMB);
 ++frame_maps;return(uintptr_t)frame;
}
static void harness_barrier(void) {
 for(unsigned i=0;i<13;i++)if(i!=1)assert(regs[i]==a52q_ui_expected[i].value);
}
static void nanoseconds_to_deadline(uint64_t span,uint64_t *out){*out=ticks+span;}
static uint64_t mach_absolute_time(void){
 ticks+=consume ? 1 : 101000000;
 if(consume)regs[1]=0;
 return ticks;
}
"""
        checks=r"""
static void reset(void) {
 memcpy(guards,a52q_ui_expected,sizeof(guards));
 for(unsigned i=0;i<13;i++)regs[i]=guards[i].value;
 geometry[0]=1080;geometry[1]=2400;geometry[2]=4320;
 start_address=guards[1].address;flag=1;other=0;reg_maps=frame_maps=0;ticks=0;consume=1;
 a52ui_state=0;a52ui_busy=0;a52ui_frame=NULL;a52ui_frames=0;
}
int main(void){
 frame=malloc(A52Q_UI_BYTES);assert(frame);memset(frame,0xa5,A52Q_UI_BYTES);
 uint64_t physical=1;uint32_t width=1,height=1,stride=1;
 reset();flag=0;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(!reg_maps && !frame_maps);
 reset();other=1;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(!reg_maps && !frame_maps);
 reset();geometry[2]+=4;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(!reg_maps && !frame_maps);
 reset();regs[6]^=1;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(reg_maps==7 && !frame_maps);
 reset();assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));
 assert(reg_maps==13 && frame_maps==1 && physical==A52Q_UI_PHYS && width==1080 && height==2400 && stride==4320);
 assert(frame[0]==0xa5 && frame[A52Q_UI_BYTES-1]==0xa5);
 assert(a52q_ui_physical_allowed(physical,width,height,stride));
 assert(!a52q_ui_physical_allowed(physical+4096,width,height,stride));
 assert(a52q_ui_flush() && a52ui_frames==1 && regs[1]==0);
 consume=0;assert(!a52q_ui_flush() && regs[1]==1 && !a52q_ui_pixels());
 int state=a52ui_state;assert(!a52q_ui_flush() && a52ui_state==state);
 free(frame);return 0;
}
"""
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'guard.c';p.write_text(prefix+source+checks);exe=Path(d)/('guard.exe' if os.name=='nt' else 'guard')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-I',str(R/'xnu/a52q'),str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True);self.assertEqual(v.returncode,0,v.stderr.decode(errors='replace'))
            rows=re.findall(rb'A52G1 ([0-9a-f/]+) ([0-9a-f]{8})',v.stdout)
            self.assertTrue(rows)
            self.assertTrue(all(zlib.crc32(body)==int(crc,16) for body,crc in rows))
            self.assertTrue(any(b'/30/' in body for body,crc in rows))

if __name__=='__main__':unittest.main()
