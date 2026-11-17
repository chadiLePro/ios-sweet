"""Compile the real data read strategy and reject root/extent/write escapes."""
import os,shutil,subprocess,tempfile,unittest,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class DataProxyTests(unittest.TestCase):
    def test_actual_read_strategy_and_window_bounds(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        s=(R/'xnu/a52q/a52q_data_proxy.c').read_text();a=s.index('static void a52v_strategy(');b=s.index('static int a52v_ioctl(',a)
        prefix=r"""
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include "a52q_ufs_bounds.h"
#include "a52q_var_bounds.h"
#define A52V_BYTES (4ULL<<30)
#define DEV_BSIZE 512
#define B_READ 1
#define UIO_READ 1
#define UIO_SYSSPACE 1
#define minor(d) (d)
typedef char *caddr_t;
typedef int64_t daddr64_t;
#define off_t test_off_t
typedef int64_t off_t;
struct testbuf {uint32_t count,resid;int64_t block;int flags,error,done;char *data;};
typedef struct testbuf *buf_t;
static int a52v_ready=1,a52v_source=1,kernproc=0,calls,get_error,read_error,bad_residual;
static uint64_t a52v_start=(uint64_t)7360000*4096,last_offset;
static uint32_t buf_count(buf_t b){return b->count;}
static daddr64_t buf_blkno(buf_t b){return b->block;}
static void buf_setresid(buf_t b,int n){b->resid=(uint32_t)n;}
static int buf_flags(buf_t b){return b->flags;}
static int buf_device(buf_t b){(void)b;return 0;}
static int buf_map(buf_t b,caddr_t *p){*p=b->data;return 0;}
static void buf_unmap(buf_t b){(void)b;}
static int vnode_get(int n){assert(n==1);return get_error;}
static void vnode_put(int n){assert(n==1);}
static int vfs_context_kernel(void){return 1;}
static int vfs_context_ucred(int c){return c;}
static void buf_seterror(buf_t b,int e){b->error=e;}
static void buf_biodone(buf_t b){b->done=1;}
static int vn_rdwr(int op,int vp,char *p,int len,int64_t off,int seg,int flags,int cred,int *resid,int proc){
 assert(op==UIO_READ && vp==1 && seg==UIO_SYSSPACE && !flags && cred==1 && proc==0);
 assert((uint64_t)off>=a52v_start && (uint64_t)off-a52v_start<=A52V_BYTES-(unsigned)len);
 ++calls;last_offset=(uint64_t)off;memset(p,0x52,(size_t)len);
 *resid=bad_residual ? len+1 : read_error ? len/2 : 0;return read_error;
}
"""
        checks=r"""
int main(void){
 uint64_t root[]={3165696,27911647,3165696,4194304},var[]={3165696,27911647,7360000,1048576};
 assert(a52q_var_window_valid(root,var));
 for(unsigned i=0;i<4;i++){var[i]++;assert(!a52q_var_window_valid(root,var));var[i]--;}
 uint64_t old=root[0];root[0]=UINT64_MAX;assert(!a52q_var_window_valid(root,var));root[0]=old;
 char memory[1026];memset(memory,0xa5,sizeof(memory));
 struct testbuf b={512,0,0,B_READ,0,0,memory+1};
 a52v_strategy(&b);assert(!b.error && !b.resid && b.done && calls==1 && last_offset==a52v_start);
 assert((unsigned char)memory[0]==0xa5 && (unsigned char)memory[513]==0xa5);
 b=(struct testbuf){512,0,A52V_BYTES/512-1,B_READ,0,0,memory+1};a52v_strategy(&b);
 assert(!b.error && !b.resid && last_offset==a52v_start+A52V_BYTES-512);
 int before=calls;
 for(unsigned mode=0;mode<4;mode++){
  b=(struct testbuf){512,0,0,B_READ,0,0,memory+1};
  if(mode==0)b.flags=0;if(mode==1)b.block=-1;if(mode==2)b.block=A52V_BYTES/512;
  if(mode==3){b.block=A52V_BYTES/512-1;b.count=1024;}
  a52v_strategy(&b);assert(b.error && b.resid==b.count && calls==before);
 }
 b=(struct testbuf){512,0,0,B_READ,0,0,memory+1};read_error=EIO;a52v_strategy(&b);
 assert(b.error==EIO && b.resid==256);
 b=(struct testbuf){512,0,0,B_READ,0,0,memory+1};read_error=0;bad_residual=1;a52v_strategy(&b);
 assert(b.error==EIO && b.resid==512);
 b=(struct testbuf){512,0,0,B_READ,0,0,memory+1};bad_residual=0;get_error=EIO;before=calls;a52v_strategy(&b);
 assert(b.error==EIO && b.resid==512 && calls==before);
 return 0;
}
"""
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'proxy.c';p.write_text(prefix+s[a:b]+checks);exe=Path(d)/('proxy.exe' if os.name=='nt' else 'proxy')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-Wno-misleading-indentation','-I',str(R/'xnu/a52q'),str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True,text=True);self.assertEqual(v.returncode,0,v.stderr)

    def test_optional_fstab_preserves_original_root_wire(self):
        import ast
        sys.path.insert(0,str(R/'xnu/a52q'));import data_fstab
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        module=ast.parse((R/'tests/test_a52q_bootfs.py').read_text());values={}
        for item in ast.walk(module):
            if isinstance(item,ast.Assign) and isinstance(item.value,ast.Constant) and isinstance(item.value.value,str):
                for target in item.targets:
                    if isinstance(target,ast.Name):values[target.id]=item.value.value
        harness=values['harness'];checks=values['checks']
        harness=harness.replace('static int output(', 'static int var_enabled;\nstatic int output(')
        harness=harness.replace('    req->oldidx += len;','    size_t start=var_enabled ? req->oldidx : 0;\n    req->oldidx += len;')
        harness=harness.replace('if (req->oldlen < len)','if (start>req->oldlen || len>req->oldlen-start)')
        harness=harness.replace('memcpy(req->oldptr,buf,len)','memcpy((char *)req->oldptr+start,buf,len)')
        raw=(R/'xnu/a52q/a52q_bootfs.c').read_text();changed=data_fstab.transform(raw)
        with self.assertRaises(ValueError):data_fstab.transform(changed)
        body='\n'.join(l for l in changed.splitlines() if not l.startswith('#include'))
        proxy=(R/'xnu/a52q/a52q_data_proxy.c').read_text()
        wire=proxy[proxy.index('struct a52v_wire {'):proxy.index('_Static_assert(sizeof(struct a52v_wire)')]
        actual=proxy[proxy.index('int a52q_data_fstab(struct sysctl_req *req);'):proxy.rindex('#endif')]
        fake=r"""
typedef int DTEntry;
#define kSuccess 0
static int a52v_ready=1,a52v_init_lock;
static int SecureDTLookupEntry(void *parent,const char *path,DTEntry *node) {
 assert(!parent && !strcmp(path,"/a52q-ufs-var"));*node=1;return var_enabled ? kSuccess : -1;
}
static void lck_mtx_lock(int *lock){assert(lock==&a52v_init_lock);}
static void lck_mtx_unlock(int *lock){assert(lock==&a52v_init_lock);}
static int a52v_init(DTEntry node){(void)node;assert(!"ready proxy must not reopen device");return 0;}
"""+wire+actual
        extra=r"""
    mounted.flags=3;strcpy(mounted.stat.f_fstypename,"hfs");
    req.oldidx=0;assert(a52q_sysctl_edt_fstab(&req)==0);
    var_enabled=1;unsigned char both[472];struct sysctl_req paired={NULL,both,sizeof(both),0};
    assert(a52q_sysctl_edt_fstab(&paired)==0 && paired.oldidx==472);
    assert(!memcmp(both,bytes,236));assert(!strcmp((char *)both+236,"/dev/a52var0"));
    assert(!strcmp((char *)both+236+32,"/private/var"));
    int32_t rootpass,varpass;
    memcpy(&rootpass,both+0xe4,4);memcpy(&varpass,both+236+0xe4,4);
    assert(rootpass==1 && varpass==2);
    /* Target mount.c: if (passno && fs->fs_passno != passno) continue.
     * Regression: pass 0 is selected by neither mount -P 1 nor mount -P 2. */
    for(int phase=1;phase<=2;phase++) {
        assert((rootpass==phase)==(phase==1));
        assert((varpass==phase)==(phase==2));
        assert(0!=phase);
    }
    paired.oldidx=0;paired.oldlen=236;assert(a52q_sysctl_edt_fstab(&paired)==ENOMEM);
"""
        checks=checks.replace('    return 0;',extra+'    return 0;')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fstab.c';p.write_text(harness+body+fake+checks);exe=Path(d)/('fstab.exe' if os.name=='nt' else 'fstab')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror',str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True,text=True);self.assertEqual(v.returncode,0,v.stderr)

if __name__=='__main__':unittest.main()
