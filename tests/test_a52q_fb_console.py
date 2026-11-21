"""Native execution of the real bounded console, ownership and font renderer."""
from pathlib import Path
import os,shutil,subprocess,sys,tempfile,unittest
R=Path(__file__).resolve().parents[1]

class BitmapConsoleTests(unittest.TestCase):
    def test_pstore_body_is_unchanged_and_mirror_follows_write(self):
        sys.path.insert(0,str(R/'xnu/a52q'));import text_console
        original=(R/'xnu/a52q/a52q_early.c').read_text();new=text_console.early(original)
        a=original.index('static void byte(');b=original.index('void sweet_early_putc')
        self.assertIn(original[a:b],new)
        self.assertIn('byte(c);\n    a52q_fb_console_putc(c);\n    busy = 0;',new)
        self.assertIn('va_end(copy);\n    string("\\n");\n    a52q_fb_console_panic();',new)
        with self.assertRaises(ValueError):text_console.early(new)

    def test_real_console_bounds_scroll_backpressure_and_handoff(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native C compiler unavailable')
        body='\n'.join(l for l in (R/'xnu/a52q/a52q_fb_console.c').read_text().splitlines() if not l.startswith('#include'))
        harness=r'''
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include "a52q_ui_profile.h"
#include "a52q_fb_console.h"
#include "a52q_text_grid.h"
#define ARM64_BOARD_CONFIG_A52Q 1
#define NSEC_PER_MSEC 1000000ULL
unsigned char iso_font[256*16];
static uint32_t *pixels;static int flag=1,mapped=1,flushes,quiet_flushes;
static uint64_t ticks;
static int PE_parse_boot_argn(const char *name,void *v,size_t n) {
 assert(!strcmp(name,"a52q_text_console") && n==sizeof(int));memcpy(v,&flag,n);return 1;
}
uintptr_t a52q_ui_pixels(void){return mapped ? (uintptr_t)pixels : 0;}
int a52q_ui_flush(void){++flushes;return 1;}
int a52q_ui_flush_quiet(void){++flushes;++quiet_flushes;return 1;}
static uint64_t mach_absolute_time(void){return ticks;}
static void nanoseconds_to_deadline(uint64_t span,uint64_t *v){*v=ticks+span;}
static int test_print(const char *fmt,...) {
 char b[256];va_list a;va_start(a,fmt);int n=vsnprintf(b,sizeof(b),fmt,a);va_end(a);
 assert(n>=0 && n<(int)sizeof(b));for(int i=0;i<n;i++)a52q_fb_console_putc(b[i]);return n;
}
#define printf test_print
'''
        checks=r'''
static void reset(void) {
 a52text_head=a52text_count=0;a52text_queue_busy=a52text_draw_busy=a52text_state=0;
 a52text_deadline=0;flag=mapped=1;flushes=quiet_flushes=0;ticks=0;
}
int main(void) {
 unsigned char *allocation=malloc(A52Q_UI_BYTES+8);assert(allocation);
 memset(allocation,0xa5,A52Q_UI_BYTES+8);pixels=(uint32_t *)(allocation+4);
 iso_font['A'*16]=1;
 struct a52text_grid grid;a52text_init(&grid);
 assert(!a52text_draw(pixels,100,iso_font,&grid));
 assert(!a52text_draw((uint32_t *)(allocation+1),A52Q_UI_BYTES,iso_font,&grid));
 for(unsigned i=0;i<5000;i++){a52text_put(&grid,'X');a52text_put(&grid,'\n');}
 assert(grid.row==A52TEXT_ROWS-1 && grid.col==0);
 a52text_init(&grid);a52text_put(&grid,'A');a52text_put(&grid,'\b');assert(grid.cells[0][0]==' ');
 a52text_put(&grid,27);a52text_put(&grid,'[');a52text_put(&grid,'3');a52text_put(&grid,'1');a52text_put(&grid,'m');
 a52text_put(&grid,'A');assert(grid.cells[0][0]=='A' && grid.col==1);
 reset();flag=0;a52q_fb_console_start();assert(!flushes && allocation[4]==0xa5);
 reset();mapped=0;a52q_fb_console_start();a52q_fb_console_tick(1);assert(!flushes);
 reset();a52text_queue_busy=1;a52q_fb_console_putc('X');assert(!a52text_count);a52text_queue_busy=0;
 a52q_fb_console_putc('A');a52q_fb_console_start();assert(flushes==1);
 assert(pixels[16]==0xffffffffU && pixels[17]==0xffffffffU && pixels[18]==0xff000000U);
 assert(pixels[1080+16]==0xffffffffU && pixels[2160+16]==0xff000000U);
 assert(pixels[32*1080]==0xffffffffU); /* queued early A, first body row */
 for(unsigned i=0;i<4;i++)assert(allocation[i]==0xa5);
 for(uint64_t i=4+1080ULL*2400*4;i<A52Q_UI_BYTES+8;i++)assert(allocation[i]==0xa5);
 for(unsigned i=0;i<A52TEXT_QUEUE+1000;i++)a52q_fb_console_putc('A');
 assert(a52text_count==A52TEXT_QUEUE);a52q_fb_console_panic();assert(!a52text_count && flushes==2 && quiet_flushes==1);
 a52text_draw_busy=1;a52q_fb_console_panic();assert(flushes==2);
 assert(!a52q_fb_console_handoff());a52text_draw_busy=0;assert(a52q_fb_console_handoff());
 uint32_t before=pixels[0];a52q_fb_console_putc('Z');a52q_fb_console_tick(1);a52q_fb_console_panic();
 assert(!a52text_count && flushes==2 && pixels[0]==before);
 free(allocation);return 0;
}
'''
        # Raw C strings need actual control-character escapes, not literal backslashes.
        checks=checks.replace("'\\\\n'","'\\n'").replace("'\\\\b'","'\\b'")
        with tempfile.TemporaryDirectory() as d:
            c=Path(d)/'console.c';c.write_text(harness+body+checks);exe=Path(d)/('console.exe' if os.name=='nt' else 'console')
            p=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-I',str(R/'xnu/a52q'),str(c),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            p=subprocess.run([str(exe)],capture_output=True,text=True,timeout=20);self.assertEqual(p.returncode,0,p.stderr)

if __name__=='__main__':unittest.main()
