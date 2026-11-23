import os,shutil,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'xnu/a52q'));import hfs_atomic_write as atomic
sys.path.insert(0,str(R/'tools'));from a52q_hfs_atomic_trace import decode


class HFSAtomicTests(unittest.TestCase):
    def test_transform_preserves_redmi_and_rejects_drift(self):
        original=atomic.ANCHOR+'\noriginal Redmi body\n'+atomic.END
        source=atomic.FUNCTION+'void) {\n'+original+'\n}\n'
        result=atomic.transform(source)
        self.assertIn(original,result)
        self.assertEqual(result.count(atomic.HOOK),1)
        self.assertIn(atomic.HELPER,result)
        for bad in (source+source,result,source.replace(atomic.ANCHOR,'changed')):
            with self.assertRaises(ValueError):atomic.transform(bad)

    def test_actual_helper_scope_permissions_errors_and_both_identities(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        prefix=r'''
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_A52Q 1
#define CONFIG_MACF 1
#define ENOTSUP 45
#define EACCES 13
#define EIO 5
#define VFS_RENAME_SWAP 2
#define VBLK 2
#define KAUTH_VNODE_READ_DATA 1
#define KAUTH_VNODE_WRITE_DATA 2
#define VNODE_UPDATE_NAME 1
#define dev_t test_dev_t
typedef int dev_t,vfs_context_t;
struct mount;
struct vnode {struct mount *mount;int type,device,nlink,auth_error;const char *name;};
typedef struct vnode *vnode_t;
typedef struct mount *mount_t;
struct vfsstatfs {char f_fstypename[16];};
struct mount {int readonly;struct vfsstatfs info;vnode_t device;};
struct vnode_attr {unsigned supported,va_nlink;};
struct componentname {const char *cn_nameptr;int cn_namelen;unsigned cn_hash;};
#define VATTR_INIT(v) memset((v),0,sizeof(*(v)))
#define VATTR_WANTED(v,a) ((void)(v))
#define VATTR_IS_SUPPORTED(v,a) ((v)->supported)
static struct mount mount,other;
static struct vnode from,to,dir,otherdir,dev;
static struct componentname fn,tn;
static char process[32],parent[256],newnames[2][64];
static int references,exchanges,updates,mac_error,attr_error,path_error,unsupported,exchange_error;
static void proc_selfname(char *out,int size){snprintf(out,(size_t)size,"%s",process);}
static int proc_selfpid(void){return 13;}
static int vnode_isreg(vnode_t v){return v->type==1;}
static mount_t vnode_mount(vnode_t v){return v->mount;}
static struct vfsstatfs *vfs_statfs(mount_t m){return &m->info;}
static int vfs_isrdonly(mount_t m){return m->readonly;}
static vnode_t vfs_devvp(mount_t m){if(m->device)++references;return m->device;}
static int vnode_vtype(vnode_t v){return v->type;}
static dev_t vnode_specrdev(vnode_t v){return v->device;}
static void vnode_put(vnode_t v){assert(v==&dev && references>0);--references;}
int a52q_var_atomic_context(dev_t device,uint64_t *nonce){if(device!=21)return 0;*nonce=81;return 1;}
static int vn_getpath(vnode_t d,char *out,int *size){
 assert(d==&dir && *size>=(int)strlen(parent)+1);
 if(path_error)return path_error;strcpy(out,parent);*size=(int)strlen(parent)+1;return 0;
}
static int vnode_getattr(vnode_t v,struct vnode_attr *a,int ctx){
 assert(ctx==7);if(attr_error)return attr_error;a->supported=!unsupported;a->va_nlink=(unsigned)v->nlink;return 0;
}
static int mac_vnode_check_exchangedata(int ctx,vnode_t f,vnode_t t){assert(ctx==7 && f==&from && t==&to);return mac_error;}
static int vnode_authorize(vnode_t v,void *unused,int rights,int ctx){assert(!unused && rights==3 && ctx==7);return v->auth_error;}
static int VNOP_EXCHANGE(vnode_t f,vnode_t t,int flags,int ctx){assert(f==&from && t==&to && !flags && ctx==7);++exchanges;return exchange_error;}
static void vnode_update_identity(vnode_t v,vnode_t d,const char *name,int length,unsigned hash,int flags){
 assert(d==&dir && flags==VNODE_UPDATE_NAME && (hash==123 || hash==456));
 assert(updates<2 && length<64);memcpy(newnames[updates],name,(size_t)length);newnames[updates][length]=0;
 v->name=newnames[updates++];
}
static void reset(void){
 memset(&mount,0,sizeof(mount));strcpy(mount.info.f_fstypename,"hfs");mount.device=&dev;
 from=(struct vnode){&mount,1,0,1,0,"usersession.kb.writing"};
 to=(struct vnode){&mount,1,0,1,0,"usersession.kb"};
 dir=(struct vnode){.mount=&mount};otherdir=dir;dev=(struct vnode){.type=VBLK,.device=21};
 fn=(struct componentname){"usersession.kb.writing",21,123};tn=(struct componentname){"usersession.kb",14,456};
 /* Derive lengths here; native tests also exercise non-NUL components. */
 fn.cn_namelen=(int)strlen(fn.cn_nameptr);tn.cn_namelen=(int)strlen(tn.cn_nameptr);
 strcpy(process,"usermanagerd");strcpy(parent,"/private/var/keybags");
 references=exchanges=updates=mac_error=attr_error=path_error=unsupported=exchange_error=0;
}
'''
        checks=r'''
static int run(unsigned flags){return a52q_hfs_atomic_swap(&dir,&from,&fn,&dir,&to,&tn,flags,7);}
int main(void){
 reset();const char *old=from.name;
 assert(!run(2) && exchanges==1 && updates==2 && !references);
 assert(!strcmp(from.name,"usersession.kb") && !strcmp(to.name,"usersession.kb.writing") && from.name!=old);
 reset();fn=(struct componentname){"persona.kb.writing",18,123};tn=(struct componentname){"persona.kb",10,456};
 fn.cn_namelen=(int)strlen(fn.cn_nameptr);tn.cn_namelen=(int)strlen(tn.cn_nameptr);
 assert(!run(2) && exchanges==1 && updates==2 && !references);
 for(int mode=0;mode<15;mode++){
  reset();unsigned flags=2;
  if(mode==0)strcpy(process,"SpringBoard");
  if(mode==1)flags=1;
  if(mode==2){tn.cn_nameptr="systembag.kb";tn.cn_namelen=12;}
  if(mode==3)to.mount=&other;
  if(mode==4)from.type=0;
  if(mode==5)mount.readonly=1;
  if(mode==6)strcpy(mount.info.f_fstypename,"apfs");
  if(mode==7)dev.device=22;
  if(mode==8)strcpy(parent,"/private/var/other");
  if(mode==9)from.nlink=2;
  if(mode==10)dev.type=0;
  if(mode==11)mount.device=NULL;
  if(mode==12)unsupported=1;
  if(mode==13)from.mount=to.mount=NULL;
  if(mode==14)dir.mount=&other;
  assert(run(flags)==ENOTSUP && !exchanges && !updates && !references);
 }
 reset();mac_error=EACCES;assert(run(2)==EACCES && !exchanges && !updates && !references);
 reset();from.auth_error=EACCES;assert(run(2)==EACCES && !exchanges && !updates && !references);
 reset();to.auth_error=EIO;assert(run(2)==EIO && !exchanges && !updates && !references);
 reset();attr_error=EIO;assert(run(2)==EIO && !exchanges && !updates && !references);
 reset();exchange_error=EIO;assert(run(2)==EIO && exchanges==1 && !updates && !references);
 reset();assert(a52q_hfs_atomic_swap(&dir,&from,&fn,&otherdir,&to,&tn,2,7)==ENOTSUP && !exchanges);
 reset();char raw[32];memset(raw,'X',sizeof(raw));memcpy(raw,fn.cn_nameptr,(size_t)fn.cn_namelen);fn.cn_nameptr=raw;
 assert(!run(2) && exchanges==1 && updates==2 && !references);
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'atomic.c';path.write_text(prefix+atomic.HELPER+checks)
            exe=Path(directory)/('atomic.exe' if os.name=='nt' else 'atomic')
            result=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-Wno-misleading-indentation',str(path),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            result=subprocess.run([str(exe)],capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            report=decode(result.stdout,81)
            self.assertTrue(report['exchange_success_observed'] and report['failure_observed'])
            self.assertFalse(decode(result.stdout,82)['records'])
            self.assertFalse(decode(result.stdout.replace(b'A52A1 ',b'A52AX '),81)['records'])
            damaged=result.stdout.replace(b'/00000000 ',b'/00000001 ')
            self.assertFalse(decode(damaged,81)['exchange_success_observed'])
