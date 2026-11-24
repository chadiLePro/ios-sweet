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
        self.assertEqual(source.count('harness_barrier();'),3)
        source=source.replace('__asm__ volatile("mrs %0, ctr_el0" : "=r"(ctr));','ctr=4ULL<<16;')
        source=source.replace('__asm__ volatile("dc cvac, %0" :: "r"(p) : "memory");','harness_clean(p);')
        source=source.replace('__asm__ volatile("at s1e1r, %0\\n\\tisb" :: "r"(va) : "memory");','(void)va;')
        source=source.replace('__asm__ volatile("mrs %0, par_el1" : "=r"(par));','par=harness_translate(va);')
        source=source.replace('__asm__ volatile("mrs %0, mair_el1" : "=r"(mair));','mair=0x44ff;')
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
static int flag=1,other=0,reg_maps,frame_maps,consume=1,busy_clears=1,console_starts;
static uint32_t regs[13],geometry[3]={1080,2400,4320};
static uint64_t region[2]={A52Q_UI_PHYS,A52Q_UI_BYTES},nonce=81,ram_base=0x106000000ULL,ram_size=0xff00000;
static uint64_t start_address;
static struct a52q_ui_guard guards[13];
static unsigned char *frame;
static uint64_t ticks;
void a52q_fb_console_start(void){assert(frame_maps==1);++console_starts;}
static uint64_t harness_translate(uintptr_t va){return (A52Q_UI_PHYS+va-(uintptr_t)frame)&~0xfffULL;}
static unsigned cleans;static uintptr_t last_clean;
static void harness_clean(uintptr_t p) {
 assert((p&63)==0 && p>=((uintptr_t)frame&~63ULL) && p<(uintptr_t)frame+A52Q_UI_BYTES);
 if(p==((uintptr_t)frame&~63ULL))cleans=0;
 if(cleans)assert(p==last_clean+64);
 last_clean=p;++cleans;
}
static unsigned tails;
int a52q_fb_console_owner(void){return 1;}
void a52q_early_critical(const char *line,unsigned length,unsigned slot) {
 assert(length>8 && length<=240 && slot<6 && !memcmp(line,"A52OBS1 ",8));++tails;
}
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
 for(unsigned i=0;i<13;i++)if(i!=1)assert(i==6 ? (regs[i]==0 || regs[i]==5) : regs[i]==a52q_ui_expected[i].value);
}
static void nanoseconds_to_deadline(uint64_t span,uint64_t *out){*out=ticks+span;}
static uint64_t mach_absolute_time(void){
 ticks+=consume ? 1 : 101000000;
 if(consume)regs[1]=0;
 if(busy_clears)regs[6]=0;
 return ticks;
}
"""
        checks=r"""
static void reset(void) {
 memcpy(guards,a52q_ui_expected,sizeof(guards));
 for(unsigned i=0;i<13;i++)regs[i]=guards[i].value;
 regs[6]=0; /* V25's actual idle DSI_STATUS, not the older busy snapshot. */
 geometry[0]=1080;geometry[1]=2400;geometry[2]=4320;
 start_address=guards[1].address;flag=1;other=0;reg_maps=frame_maps=0;ticks=0;consume=1;busy_clears=1;
 a52ui_state=0;a52ui_busy=0;a52ui_frame=NULL;a52ui_frames=0;
 console_starts=0;
}
int main(void){
 unsigned char *allocation=malloc(A52Q_UI_BYTES+16384);frame=(unsigned char *)(((uintptr_t)allocation+16383)&~16383ULL);assert(frame);memset(frame,0xa5,A52Q_UI_BYTES);
 uint64_t physical=1;uint32_t width=1,height=1,stride=1;
 reset();flag=0;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(!reg_maps && !frame_maps);
 reset();other=1;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(!reg_maps && !frame_maps);
 reset();geometry[2]+=4;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(!reg_maps && !frame_maps);
 reset();regs[6]^=1;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(reg_maps==7 && !frame_maps);
 reset();regs[6]=0x80000000;assert(!a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(reg_maps==7 && !frame_maps);
 reset();regs[6]=5;assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));assert(regs[6]==5);
 assert(a52q_ui_flush() && regs[6]==0);
 reset();regs[6]=5;busy_clears=0;assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));
 assert(regs[6]==5 && a52q_ui_flush() && a52q_ui_flush() && a52ui_frames==2 && regs[6]==5);
 reset();assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));
 assert(reg_maps==13 && frame_maps==1 && physical==A52Q_UI_PHYS && width==1080 && height==2400 && stride==4320);
 assert(console_starts==1);
 assert(frame[0]==0xa5 && frame[A52Q_UI_BYTES-1]==0xa5);
 assert(a52q_ui_physical_allowed(physical,width,height,stride));
 assert(!a52q_ui_physical_allowed(physical+4096,width,height,stride));
 assert(a52q_ui_flush() && a52ui_frames==1 && regs[1]==0);
 assert(cleans==A52Q_UI_BYTES/64 && last_clean==(uintptr_t)frame+A52Q_UI_BYTES-64);
 assert(a52q_ui_flush_quiet() && a52ui_frames==2 && regs[1]==0);
 a52ui_heartbeat_deadline=0;
 memset(frame,0xff,A52Q_UI_BYTES);
 uint32_t *pixels=(uint32_t *)frame;pixels[0]=0xff123456U;
 a52q_ui_observe(3,"open proc=backboardd io=0");
 unsigned before_tails=tails,before_frames=a52ui_frames;
 a52q_ui_heartbeat(0);
 assert(tails==before_tails+2 && a52ui_frames==before_frames && pixels[0]==0xff123456U);
 a52q_ui_heartbeat(1);assert(tails==before_tails+2); /* rate limit */
 consume=0;assert(!a52q_ui_flush() && regs[1]==1 && !a52q_ui_pixels());
 int state=a52ui_state;assert(!a52q_ui_flush() && a52ui_state==state);
 reset();assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));
 assert(a52q_ui_flush());regs[2]^=1;assert(!a52q_ui_flush() && !a52q_ui_pixels());
 reset();assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));
 regs[6]=1;assert(!a52q_ui_flush() && !a52q_ui_pixels());
 reset();assert(a52q_ui_framebuffer(&physical,&width,&height,&stride));
 puts("QUIET-BEGIN");consume=0;assert(!a52q_ui_flush_quiet());puts("QUIET-END");
 free(allocation);return 0;
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
            details=re.findall(rb'A52G2 ([0-9a-f/]+) ([0-9a-f]{8})',v.stdout)
            self.assertTrue(all(zlib.crc32(body)==int(crc,16) for body,crc in details))
            self.assertTrue(any(b'/01/ff/00000000' in body for body,crc in details))
            self.assertTrue(any(b'/03/06/00000001' in body for body,crc in details))
            self.assertFalse(any(b'/05/' in body for body,crc in details))
            self.assertTrue(any(b'/03/02/00000003' in body for body,crc in details))
            self.assertTrue(any(b'/06/01/00000001' in body for body,crc in details))
            self.assertEqual(v.stdout.split(b'QUIET-BEGIN')[1].split(b'QUIET-END')[0].strip(),b'')
            sys_path=str(R/'tools')
            import sys
            sys.path.insert(0,sys_path)
            from a52q_ui_late_trace import decode
            late=decode(v.stdout)['records']
            self.assertTrue(any('colour=1 first=ff123456' in row['payload'] for row in late))
            self.assertTrue(any('owner=1 off=0 frames=2' in row['payload'] for row in late))

if __name__=='__main__':unittest.main()
