"""Compile the actual sysctl body with VFS/output API fixtures; no kernel claim."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class BootFilesystemTests(unittest.TestCase):
    def test_readonly_mounted_root_and_measured_wire_contract(self):
        root = Path(__file__).resolve().parents[1]
        compiler = 'C:/winlibs/mingw64/bin/gcc.exe' if Path('C:/winlibs/mingw64/bin/gcc.exe').exists() else shutil.which('cc')
        if not compiler: self.skipTest('native C compiler unavailable')
        body = '\n'.join(line for line in (root/'xnu/a52q/a52q_bootfs.c').read_text().splitlines()
                         if not line.startswith('#include'))
        harness = r'''
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <assert.h>
#define dev_t test_dev_t
typedef int dev_t;
struct vfsstatfs { char f_fstypename[16]; };
struct mount { unsigned flags; struct vfsstatfs stat; };
typedef struct mount *mount_t;
typedef struct vnode { mount_t mp; } *vnode_t;
struct sysctl_req { void *newptr, *oldptr; size_t oldlen, oldidx; };
#define SYSCTL_HANDLER_ARGS (struct sysctl_req *req)
#define SYSCTL_DECL(...)
#define SYSCTL_NODE(...)
#define SYSCTL_PROC(...)
#define MNT_RDONLY 1
#define MNT_ROOTFS 2
static struct mount mounted = {3, {"hfs"}};
static struct vnode node = {&mounted};
vnode_t rootvnode = &node;
dev_t rootdev = 42;
static int full_root = 1, device_error = 0;
static mount_t vnode_mount(vnode_t vp) { return vp->mp; }
static unsigned vfs_flags(mount_t mp) { return mp->flags; }
static struct vfsstatfs *vfs_statfs(mount_t mp) { return &mp->stat; }
static int a52q_ufs_root_named(const char *name) { return full_root && !strcmp(name,"a52ios0"); }
static int a52q_ufs_rootdev(dev_t *dev) { *dev=42; return device_error; }
static int output(struct sysctl_req *req, const void *buf, size_t len) {
    req->oldidx += len;
    if (!req->oldptr) return 0;
    if (req->oldlen < len) return ENOMEM;
    memcpy(req->oldptr,buf,len); return 0;
}
#define SYSCTL_OUT output
'''
        checks = r'''
int main(void) {
    struct sysctl_req query = {0};
    assert(a52q_sysctl_edt_fstab(&query)==0 && query.oldidx==236);
    unsigned char bytes[236]; memset(bytes,0xa5,sizeof(bytes));
    struct sysctl_req req = {NULL,bytes,sizeof(bytes),0};
    assert(a52q_sysctl_edt_fstab(&req)==0 && req.oldidx==sizeof(bytes));
    assert(!strcmp((char*)bytes,"/dev/a52ios0"));
    assert(!strcmp((char*)bytes+0x20,"/"));
    assert(!strcmp((char*)bytes+0x60,"hfs"));
    assert(!strcmp((char*)bytes+0x80,"ro"));
    assert(!strcmp((char*)bytes+0xc0,"ro"));
    int32_t frequency,pass;memcpy(&frequency,bytes+0xe0,4);memcpy(&pass,bytes+0xe4,4);
    assert(frequency==0 && pass==1);
    for (unsigned i=0xe8;i<236;i++) assert(bytes[i]==0);
    req.oldlen=235;assert(a52q_sysctl_edt_fstab(&req)==ENOMEM);req.oldlen=236;
    req.newptr=bytes;assert(a52q_sysctl_edt_fstab(&req)==EPERM);req.newptr=NULL;
    full_root=0;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);full_root=1;
    device_error=ENXIO;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);device_error=0;
    rootdev=43;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);rootdev=42;
    rootvnode=NULL;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);rootvnode=&node;
    node.mp=NULL;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);node.mp=&mounted;
    mounted.flags=MNT_ROOTFS;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);
    mounted.flags=MNT_RDONLY;assert(a52q_sysctl_edt_fstab(&req)==ENOENT);mounted.flags=3;
    strcpy(mounted.stat.f_fstypename,"mockfs");assert(a52q_sysctl_edt_fstab(&req)==ENOENT);
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'bootfs.c'; binary = Path(directory)/'bootfs.exe'
            source.write_text(harness + body + checks)
            subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', str(source), '-o', str(binary)], check=True, capture_output=True)
            subprocess.run([str(binary)], check=True, capture_output=True)
