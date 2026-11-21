import os,shutil,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'));from a52q_crash_trace import decode
sys.path.insert(0,str(R/'xnu/a52q'));import exit_trace

class CrashTraceTests(unittest.TestCase):
    def test_transform_accepts_original_anchor_and_keeps_redmi_call_unchanged(self):
        source=('#include <kern/thread_call.h>\n#if defined(ARM64_BOARD_CONFIG_SWEET)\n'
            '\t\tif (p == current_proc()) {\n'
            '\t\t\textern void sweet_crash_log(const char *, int, int, uint64_t, uint64_t);')
        out=exit_trace.transform(source)
        self.assertIn(source.split('\n',1)[1],out)
        self.assertEqual(out.count('a52q_crash_registers(p);'),1)
        self.assertLess(out.index('a52q_crash_registers(p);'),out.index('#if defined(ARM64_BOARD_CONFIG_SWEET)'))
        with self.assertRaises(ValueError):exit_trace.transform(out)

    def test_decoder_rejects_corruption_and_bad_schema(self):
        b=b'25/SpringBoard/'+b'/'.join([b'0000000000001000']*6)
        line=b'A52CR1 '+b+b' %08x\n'%zlib.crc32(b)
        self.assertEqual(decode(line*3)['records'][0]['valid_copies'],3)
        self.assertEqual(decode(line.replace(b'SpringBoard',b'SpringBoarX'))['records'],[])
        b=b.replace(b'SpringBoard',b'unknown')
        with self.assertRaises(ValueError):decode(b'A52CR1 '+b+b' %08x\n'%zlib.crc32(b))

    def test_actual_saved_register_helper_is_filtered_and_balances_reference(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        code=r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_A52Q 1
typedef struct {const char *p_comm;} *proc_t;
static int proc_getpid(proc_t p){(void)p;return 25;}
typedef struct {int bits;} arm_saved_state_t;
typedef struct {uint64_t mach_header_vm_address;} *task_t;
typedef struct {uint64_t sr_slide;} *vm_shared_region_t;
static struct {uint64_t sr_slide;} region={0x4000};
static struct {uint64_t mach_header_vm_address;} task={0x100000000};
static arm_saved_state_t state={64};static int missing,refs;
static void *current_thread(void){return &state;}
static task_t current_task(void){return (task_t)&task;}
static arm_saved_state_t *find_user_regs(void *t){assert(t==&state);return missing ? NULL : &state;}
static int is_saved_state64(arm_saved_state_t *s){return s->bits==64;}
static vm_shared_region_t vm_shared_region_get(task_t t){assert(t==(task_t)&task);refs++;return (vm_shared_region_t)&region;}
static void vm_shared_region_deallocate(vm_shared_region_t r){assert(r==(vm_shared_region_t)&region);refs--;}
#define get_saved_state_pc(s) ((void)(s),0x180004000ULL)
#define get_saved_state_lr(s) ((void)(s),0x180008000ULL)
#define get_saved_state_sp(s) ((void)(s),0x10000ULL)
#define get_saved_state_fp(s) ((void)(s),0x10100ULL)
'''
        code+='\n'.join(l for l in exit_trace.REGISTERS.splitlines() if not l.startswith('#include'))
        code+=r'''
int main(void){
 struct {const char *p_comm;} p={"SpringBoard"};
 a52q_crash_registers((proc_t)&p);assert(!refs);
 missing=1;a52q_crash_registers((proc_t)&p);assert(!refs);missing=0;
 state.bits=32;a52q_crash_registers((proc_t)&p);assert(!refs);state.bits=64;
 p.p_comm="unrelated";a52q_crash_registers((proc_t)&p);assert(!refs);
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'trace.c';p.write_text(code);exe=Path(d)/('trace.exe' if os.name=='nt' else 'trace')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror',str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True);self.assertEqual(v.returncode,0,v.stderr)
            row=decode(v.stdout)['records'];self.assertEqual(len(row),1)
            self.assertEqual(row[0]['valid_copies'],3);self.assertEqual(row[0]['slide'],0x4000)
            self.assertEqual(row[0]['pc'],0x180004000)

if __name__=='__main__':unittest.main()
