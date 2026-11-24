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

    def test_static_logo_once_bounds_silent_logs_and_handoff(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native C compiler unavailable')
        body='\n'.join(l for l in (R/'xnu/a52q/a52q_fb_console.c').read_text().splitlines() if not l.startswith('#include'))
        harness=r"""
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "a52q_ui_profile.h"
#include "a52q_boot_logo.h"
#define ARM64_BOARD_CONFIG_A52Q 1
static uint32_t *pixels;static int mapped,flushes;
uintptr_t a52q_ui_pixels(void){return mapped ? (uintptr_t)pixels : 0;}
int a52q_ui_flush(void){++flushes;return 1;}
"""
        checks=r"""
int main(void) {
 unsigned char *allocation=malloc(A52Q_UI_BYTES+8);assert(allocation);
 memset(allocation,0xa5,A52Q_UI_BYTES+8);pixels=(uint32_t *)(allocation+4);
 a52q_fb_console_start();assert(!flushes);mapped=1;
 a52q_fb_console_start();assert(flushes==1 && a52q_fb_console_owner()==1);
 unsigned white=0;
 for(unsigned y=0;y<2400;y++)for(unsigned x=0;x<1080;x++) {
  uint32_t v=pixels[y*1080+x];assert(v==0xff000000U || v==0xffffffffU);
  if(v==0xffffffffU){++white;assert(x>=450 && x<630 && y>=1088 && y<1312);}
 }
 assert(white>10000 && white<40000);
 for(unsigned i=0;i<4;i++)assert(allocation[i]==0xa5);
 for(uint64_t i=4+1080ULL*2400*4;i<A52Q_UI_BYTES+8;i++)assert(allocation[i]==0xa5);
 for(unsigned i=0;i<10000;i++){a52q_fb_console_putc('X');a52q_fb_console_tick(1);}
 a52q_fb_console_panic();a52q_fb_console_start();assert(flushes==1);
 assert(a52q_fb_console_handoff() && a52q_fb_console_owner()==2);
 pixels[0]=123;a52q_fb_console_start();a52q_fb_console_panic();assert(pixels[0]==123 && flushes==1);
 free(allocation);return 0;
}
"""
        with tempfile.TemporaryDirectory() as d:
            c=Path(d)/'logo.c';c.write_text(harness+body+checks);exe=Path(d)/('logo.exe' if os.name=='nt' else 'logo')
            p=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-I',str(R/'xnu/a52q'),str(c),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            p=subprocess.run([str(exe)],capture_output=True,text=True,timeout=20);self.assertEqual(p.returncode,0,p.stderr)

if __name__=='__main__':unittest.main()
