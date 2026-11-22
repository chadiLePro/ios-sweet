import os,shutil,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'));from a52q_crash_trace import decode
sys.path.insert(0,str(R/'xnu/a52q'));import exit_trace

class CrashTraceTests(unittest.TestCase):
    def test_stack_prefix_recovery_preserves_body_crc_checks(self):
        from a52q_stack_trace import decode as stacks
        body=b'395/backboardd/34fb8000/102f70000/1f75cf198/206b5e5f8'
        checksum=b' %08x\n'%zlib.crc32(body)
        original=b'A52BT1 '+body+checksum
        damaged=b'\x0150BT1 '+body+checksum
        self.assertEqual(stacks(damaged)['records'],[])
        record=stacks(damaged,recover_framing=True)['records'][0]
        self.assertEqual(record['recovered_framing_copies'],1)
        self.assertEqual(record['pcs'],[0x1f75cf198,0x206b5e5f8])
        combined=stacks(original+damaged,recover_framing=True)['records'][0]
        self.assertEqual(combined['original_framing_copies'],1)
        self.assertEqual(combined['recovered_framing_copies'],1)
        self.assertEqual(stacks(damaged.replace(b'1f75cf198',b'1f75cf199'),True)['records'],[])

    def test_transform_accepts_original_anchor_and_keeps_redmi_call_unchanged(self):
        source=('#include <kern/thread_call.h>\n#if defined(ARM64_BOARD_CONFIG_SWEET)\n'
            '\t\tif (p == current_proc()) {\n'
            '\t\t\textern void sweet_crash_log(const char *, int, int, uint64_t, uint64_t);')
        out=exit_trace.transform(source)
        self.assertIn(source.split('\n',1)[1],out)
        self.assertEqual(out.count('a52q_crash_registers(p->p_comm, proc_getpid(p));'),1)
        self.assertNotIn('task->mach_header_vm_address',out)
        self.assertLess(out.index('a52q_crash_registers(p->p_comm'),out.index('#if defined(ARM64_BOARD_CONFIG_SWEET)'))
        with self.assertRaises(ValueError):exit_trace.transform(out)
        mach='#if defined(ARM64_BOARD_CONFIG_SWEET)\n#include <vm/vm_shared_region.h>\nold_helper();\n#endif'
        from unittest.mock import patch
        with patch.object(exit_trace.failure_reason,'helper',return_value=''):
            changed=exit_trace.exception(mach)
        self.assertIn(mach,changed);self.assertIn('task->mach_header_vm_address',changed)
        with self.assertRaises(ValueError):exit_trace.exception(changed)

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
typedef struct {int bits;} arm_saved_state_t;
typedef struct {uint64_t mach_header_vm_address;} *task_t;
typedef struct {uint64_t sr_slide;} *vm_shared_region_t;
static struct {uint64_t sr_slide;} region={0x4000};
static struct {uint64_t mach_header_vm_address;} task={0x100000000};
static arm_saved_state_t state={64};static int missing,refs;
static void a52q_crash_strings(const char *name,int pid){assert(!strcmp(name,"backboardd") && pid>0);}
static void *current_thread(void){return &state;}
static task_t current_task(void){return (task_t)&task;}
static arm_saved_state_t *find_user_regs(void *t){assert(t==&state);return missing ? NULL : &state;}
static int is_saved_state64(arm_saved_state_t *s){return s->bits==64;}
typedef uint64_t user_addr_t;
static unsigned stack_copies,copy_calls;
static int bad_copy,cycle;
static int copyin(user_addr_t address,void *out,size_t length) {
 assert(length==16 && address>=0x10100 && address-0x10000<=65536-16 && !(address&15));
 ++copy_calls;if(bad_copy)return 1;
 uint64_t *frame=out;frame[0]=cycle ? address : address+32;
 frame[1]=0x180010000ULL+copy_calls*4;return 0;
}
static unsigned tail_copies;
static void a52q_early_critical(const char *line,unsigned length,unsigned slot) {
 if(!strncmp(line,"A52BT1 ",7)){assert(length==strlen(line) && slot==7);++stack_copies;return;}
 assert(length==strlen(line) && slot==(strstr(line,"backboardd") ? 7U : 6U) && !strncmp(line,"A52CR1 ",7));++tail_copies;
}
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
 a52q_crash_registers("SpringBoard",25);assert(!refs && tail_copies==1);
 missing=1;a52q_crash_registers("SpringBoard",25);assert(!refs);missing=0;
 state.bits=32;a52q_crash_registers("SpringBoard",25);assert(!refs);state.bits=64;
 a52q_crash_registers("unrelated",25);a52q_crash_registers(NULL,25);assert(!refs);
 a52q_crash_registers("backboardd",28);assert(!refs && tail_copies==2);
 assert(stack_copies==1 && copy_calls==14);
 bad_copy=1;copy_calls=0;a52q_crash_registers("backboardd",29);
 assert(copy_calls==1 && stack_copies==2);
 bad_copy=0;cycle=1;copy_calls=0;a52q_crash_registers("backboardd",30);
 assert(copy_calls==1 && stack_copies==3);
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'trace.c';p.write_text(code);exe=Path(d)/('trace.exe' if os.name=='nt' else 'trace')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror',str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True);self.assertEqual(v.returncode,0,v.stderr)
            row=decode(v.stdout)['records'];self.assertEqual(len(row),4)
            self.assertEqual(row[0]['valid_copies'],3);self.assertEqual(row[0]['slide'],0x4000)
            self.assertEqual(row[0]['pc'],0x180004000)
            self.assertEqual(row[1]['process'],'backboardd')
            from a52q_stack_trace import decode as stacks
            stack=stacks(v.stdout)['records']
            self.assertEqual([len(row['pcs']) for row in stack],[16,2,3])
            self.assertTrue(all(row['valid_copies']==3 for row in stack))
            self.assertEqual(stacks(v.stdout.replace(b'/backboardd/',b'/backboarXd/'))['records'],[])

if __name__=='__main__':unittest.main()
