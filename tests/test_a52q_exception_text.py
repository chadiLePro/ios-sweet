import os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'xnu/a52q'));import failure_reason
sys.path.insert(0,str(R/'tools'));from a52q_exception_trace import decode


class ExceptionTextTests(unittest.TestCase):
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
            self.assertEqual(decode(v.stdout.replace(b'parameter',b'parameteX'))['records'][-1]['rank'],2)
