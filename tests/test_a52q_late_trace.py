"""Execute the actual late pstore writer, bounds, CRC and IOKit observers."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'xnu/a52q'))
import graphics_trace
import text_console
sys.path.insert(0,str(R/'tools'))
from a52q_ui_late_trace import decode


class LateTraceTests(unittest.TestCase):
    def compile_run(self,source,cpp=False):
        compiler=('C:/winlibs/mingw64/bin/g++.exe' if cpp else 'C:/winlibs/mingw64/bin/gcc.exe') if os.name=='nt' else shutil.which('c++' if cpp else 'cc')
        if not compiler:self.skipTest('native compiler unavailable')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/('test.cpp' if cpp else 'test.c');path.write_text(source)
            exe=Path(directory)/('test.exe' if os.name=='nt' else 'test')
            args=[compiler,'-std=c++14' if cpp else '-std=c11','-Wall','-Wextra','-Werror']
            if cpp and os.name=='nt':args+=['-static']
            result=subprocess.run([*args,str(path),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            result=subprocess.run([str(exe)],capture_output=True,timeout=20)
            self.assertEqual(result.returncode,0,result.stderr)
            return result.stdout

    def test_fixed_slots_preserve_header_prefix_canaries_and_drop_when_busy(self):
        source=r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#define A52Q_RAMLOG_SIZE 0x40000U
static uint8_t memory[A52Q_RAMLOG_SIZE+32],copy[A52Q_RAMLOG_SIZE+32];
static volatile uint8_t *console=memory+16;
static unsigned position;
static int busy;
'''+text_console.LATE.replace('__asm__ volatile("dsb sy" ::: "memory");','__atomic_thread_fence(__ATOMIC_SEQ_CST);')+r'''
int main(void) {
 memset(memory,0xa5,sizeof(memory));memcpy(copy,memory,sizeof(copy));
 const char line[]="A52OBS1 aaaaaaaaaaaaaaaa/00000001/00/tick owner=1 06253313\n";
 unsigned length=(unsigned)strlen(line);
 a52q_early_critical(line,length,0);assert(!memcmp(copy,memory,sizeof(copy)));
 position=A52Q_RAMLOG_SIZE-12;busy=1;a52q_early_critical(line,length,0);
 assert(!memcmp(copy,memory,sizeof(copy)));busy=0;
 a52q_early_critical(line,length,0);assert(!memcmp(copy,memory,sizeof(copy)) && !busy);
 uint32_t *header=(uint32_t *)(memory+16);
 header[0]=0x43474244;header[1]=header[2]=position;memcpy(copy,memory,sizeof(copy));
 a52q_early_critical(NULL,length,0);a52q_early_critical(line,0,0);
 a52q_early_critical(line,241,0);a52q_early_critical(line,length,8);
 assert(!memcmp(copy,memory,sizeof(copy)));
 for(unsigned slot=0;slot<8;slot++) {
  a52q_early_critical(line,length,slot);assert(!busy && position==A52Q_RAMLOG_SIZE-12);
  assert(!memcmp(memory,copy,16+A52Q_RAMLOG_SIZE-4096));
  assert(!memcmp(memory+16+A52Q_RAMLOG_SIZE,copy+16+A52Q_RAMLOG_SIZE,16));
  const uint8_t *out=memory+16+A52Q_RAMLOG_SIZE-4096+slot*512;
  for(unsigned i=0;i<3;i++)assert(!memcmp(out+i*length,line,length));
 }
 char longline[240];memset(longline,'Z',sizeof(longline));
 a52q_early_critical(longline,240,7);
 assert(!memcmp(memory+16+A52Q_RAMLOG_SIZE-512,longline,240));
 assert(!memcmp(memory+16+A52Q_RAMLOG_SIZE-272,longline,240));
 assert(memory[16+A52Q_RAMLOG_SIZE-32]=='\n');
 return 0;
}
'''
        self.compile_run(source)

    def test_crc_nonce_schema_and_conflicting_sequence(self):
        body=b'1111111111111111/00000001/00/tick state=1 owner=1'
        def frame(b):return b'A52OBS1 '+b+b' %08x\n'%zlib.crc32(b)
        line=frame(body)
        self.assertEqual(decode(line*3)['records'][0]['valid_copies'],3)
        self.assertEqual(decode(line,0x2222222222222222)['records'],[])
        self.assertEqual(decode(line.replace(b'owner=1',b'owner=2'))['records'],[])
        with self.assertRaises(ValueError):decode(frame(body.replace(b'/00/',b'/09/')))
        with self.assertRaises(ValueError):decode(line+frame(body.replace(b'owner=1',b'owner=2')))

    def test_iokit_helpers_only_observe_graphics_processes_and_known_open_classes(self):
        source=r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define ARM64_BOARD_CONFIG_A52Q 1
typedef unsigned kern_return_t;typedef unsigned IOReturn;
struct OSObject {virtual ~OSObject() {} };
struct OSString:OSObject {const char *value;explicit OSString(const char *v):value(v){} const char *getCStringNoCopy(){return value;}};
struct OSDictionary {OSObject *value;OSObject *getObject(const char *key){return !strcmp(key,"IOProviderClass") ? value : nullptr;}};
struct Meta {const char *name;const char *getClassName(){return name;}};
struct IOService:OSObject {Meta meta;explicit IOService(const char *name):meta{name}{} Meta *getMetaClass(){return &meta;}};
#define OSDynamicCast(type,obj) dynamic_cast<type *>(obj)
static const char *process="SpringBoard";static unsigned observations,lastslot;static char latest[240];
static void proc_selfname(char *name,unsigned n){snprintf(name,n,"%s",process);}
static int proc_selfpid(void){return 26;}
static void a52q_ui_observe(unsigned slot,const char *payload){observations++;lastslot=slot;snprintf(latest,sizeof(latest),"%s",payload);}
'''
        source+='\n'.join(line for line in graphics_trace.HELPER.splitlines() if not line.startswith('#include'))
        source+=r'''
int main(void) {
 IOService fb("AppleCLCD"),surface("IOCoreSurfaceRoot"),other("AppleKeyStore");
 OSString name("IOMobileFramebuffer");OSDictionary dict{&name};
 a52q_graphics_match(&dict,0,"AppleCLCD","match");assert(observations==1 && lastslot==1);
 a52q_graphics_open(&fb,0,0,0xe00002c1,true);assert(observations==2 && lastslot==3);
 assert(strstr(latest,"rpc=00000000 io=e00002c1 valid=1"));
 a52q_graphics_open(&surface,2,0xe00002c7,0,false);assert(observations==3 && lastslot==4);
 assert(strstr(latest,"valid=0"));a52q_graphics_next(&surface);assert(observations==4 && lastslot==2);
 a52q_graphics_open(&other,0,0,0,true);assert(observations==4);
 a52q_graphics_next(nullptr);assert(observations==4);
 process="other";a52q_graphics_match(&dict,0,"none","match");a52q_graphics_open(&fb,0,0,0,true);
 a52q_graphics_next(&surface);assert(observations==4);
 process="backboardd";a52q_graphics_open(&fb,0,0,0,true);assert(observations==5 && lastslot==3);
 return 0;
}
'''
        self.compile_run(source,cpp=True)

    def test_transform_keeps_all_original_return_values_and_iterator_consumption(self):
        source=graphics_trace.ANCHOR+'\n'+r'''
is_io_iterator_next() {
        *object = obj;
}
/* Routine io_iterator_reset */
        *existing = IOUserIterator::withIterator(found);
        kr = kIOReturnSuccess;
        kr = *service ? kIOReturnSuccess : kIOReturnNotFound;
is_io_service_open_extended() {
        return kIOReturnBadArgument;
        return kIOReturnBadArgument;
        return kIOReturnNotPermitted;
        return kIOReturnUnsupported;
#if 0
        return kIOReturnMessageTooLarge;
#endif
        return err;
}
/* Routine io_service_close */
'''.replace('        ','\t\t')
        changed=graphics_trace.iokit(source)
        self.assertEqual(re.findall(r'return ([^;]+);',changed[len(graphics_trace.HELPER):]),re.findall(r'return ([^;]+);',source))
        self.assertEqual(changed.count('a52q_graphics_open(service,'),5)
        stripped=re.sub(r'#if defined\(ARM64_BOARD_CONFIG_A52Q\)\n.*?\n#endif\n','',changed,flags=re.S)
        self.assertEqual([line.strip() for line in stripped.splitlines() if line.strip()],
            [line.strip() for line in source.splitlines() if line.strip()])
        self.assertNotIn('getNextObject()',changed);self.assertNotIn('->reset()',changed)
        with self.assertRaises(ValueError):graphics_trace.iokit(changed)
        with self.assertRaises(ValueError):graphics_trace.iokit(source.replace('return err;','return other;'))


if __name__=='__main__':unittest.main()
