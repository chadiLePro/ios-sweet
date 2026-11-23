/* Separate /var proxy over the existing /dev/ra52ufs0 reader.
 * Read-only unless the additional development-write capability/probe passes.
 * Raw/root devices remain read-only. No reset, clock or new DMA mapping.
 */
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <sys/param.h>
#include <sys/systm.h>
#include <sys/buf.h>
#include <sys/conf.h>
#include <sys/disk.h>
#include <sys/file.h>
#include <sys/vnode.h>
#include <sys/proc.h>
#include <sys/uio.h>
#include <sys/sysctl.h>
#include <kern/locks.h>
#include <kern/kalloc.h>
#include <miscfs/devfs/devfs.h>
#include <sys/proc_internal.h>
#include <pexpert/device_tree.h>
#include "a52q_ufs_bounds.h"
#include "a52q_var_bounds.h"

/* Same private prototype used by target bsd/dev/arm64/conf.c and spec_vnops.c. */
extern dev_t chrtoblk(dev_t);
extern int a52q_ufs_root_named(const char *);
extern int a52q_ufs_rootdev(dev_t *);
extern int a52q_ufs_var_enable(const uint64_t [4],uint64_t,uint32_t,int *);
extern int a52q_ufs_var_write(uint64_t,const uint8_t *,uint32_t,uint32_t *);
extern int a52q_ufs_var_sync(void);
static LCK_GRP_DECLARE(a52v_group,"a52q_var_proxy");
static LCK_MTX_DECLARE(a52v_init_lock,&a52v_group);
static vnode_t a52v_source;
static int a52v_ready;
static int a52v_writable;
static uint64_t a52v_start;
#define A52V_BYTES (4ULL<<30)
struct a52v_wire { char spec[32],file[64],vfstype[32],mntops[64],type[32]; int32_t freq,passno; uint8_t unused[4]; };
_Static_assert(sizeof(struct a52v_wire)==236,"Libinfo var table stride");
static int a52v_property(DTEntry node,const char *name,void *out,unsigned bytes)
{
    const void *p;unsigned size;
    if (SecureDTGetProperty(node,name,&p,&size)!=kSuccess || size!=bytes) return 0;
    memcpy(out,p,bytes);return 1;
}
static int a52v_open(dev_t dev,int flags,int type __unused,struct proc *p __unused)
{ return !a52v_ready || minor(dev) ? ENXIO : (flags&FWRITE) && !a52v_writable ? EROFS : 0; }
static int a52v_close(dev_t dev __unused,int flags __unused,int type __unused,struct proc *p __unused)
{ return 0; }
static void a52v_strategy(buf_t bp)
{
    uint32_t count=buf_count(bp);daddr64_t block=buf_blkno(bp);caddr_t destination=NULL;
    int error=0,residual=(int)count;buf_setresid(bp,count);
    int reading=(buf_flags(bp)&B_READ)!=0;
    if (!reading && !a52v_writable) {error=EROFS;goto out;}
    if (!a52v_ready || minor(buf_device(bp))) {error=ENXIO;goto out;}
    if (count>INT_MAX || block<0 || (uint64_t)block>UINT64_MAX/DEV_BSIZE ||
        !a52q_ufs_window_range(A52V_BYTES/4096,(uint64_t)block*DEV_BSIZE,count)) {error=EINVAL;goto out;}
    if (!count) goto out;
    if (buf_map(bp,&destination)) {error=EIO;goto out;}
    if (!reading) {
        uint32_t completed=0;
        error=a52q_ufs_var_write((uint64_t)block*DEV_BSIZE,
            (const uint8_t *)destination,count,&completed);
        if (completed>count) {error=EIO;completed=0;}
        buf_setresid(bp,count-completed);buf_unmap(bp);goto out;
    }
    error=vnode_get(a52v_source);
    if (!error) {
        error=vn_rdwr(UIO_READ,a52v_source,destination,(int)count,
            (off_t)(a52v_start+(uint64_t)block*DEV_BSIZE),UIO_SYSSPACE,0,
            vfs_context_ucred(vfs_context_kernel()),&residual,kernproc);
        vnode_put(a52v_source);
    }
    if (residual<0 || (unsigned)residual>count) {error=EIO;residual=(int)count;}
    buf_setresid(bp,residual);buf_unmap(bp);
out:
    if (error) buf_seterror(bp,error);
    buf_biodone(bp);
}
static int a52v_ioctl(dev_t dev,u_long command,caddr_t data,int flags __unused,struct proc *p __unused)
{
    if (!a52v_ready || minor(dev)) return ENXIO;
    switch (command) {
    case DKIOCGETBLOCKSIZE: *(uint32_t *)data=DEV_BSIZE;return 0;
    case DKIOCSETBLOCKSIZE: return *(uint32_t *)data==DEV_BSIZE ? 0 : EINVAL;
    case DKIOCGETPHYSICALBLOCKSIZE: *(uint32_t *)data=4096;return 0;
    case DKIOCGETBLOCKCOUNT: *(uint64_t *)data=A52V_BYTES/DEV_BSIZE;return 0;
    case DKIOCISWRITABLE: *(uint32_t *)data=a52v_writable ? 1 : 0;return 0;
    case DKIOCGETMAXBLOCKCOUNTREAD: *(uint64_t *)data=4096/DEV_BSIZE;return 0;
    case DKIOCGETMAXBLOCKCOUNTWRITE: *(uint64_t *)data=a52v_writable ? 4096/DEV_BSIZE : 0;return 0;
    case DKIOCSYNCHRONIZECACHE:return a52v_writable ? a52q_ufs_var_sync() : 0;
    default:return ENOTTY;
    }
}
static int a52v_size(dev_t dev) {return !a52v_ready || minor(dev) ? -1 : A52V_BYTES/DEV_BSIZE;}
static const struct bdevsw a52v_bdevsw={.d_open=a52v_open,.d_close=a52v_close,.d_strategy=a52v_strategy,
    .d_ioctl=a52v_ioctl,.d_dump=eno_dump,.d_psize=a52v_size,.d_type=D_DISK};

static int a52v_init(DTEntry node)
{
    DTEntry root;uint64_t window[4],rw[4],nonce,root_nonce;uint32_t crc;
    dev_t device;int error;vfs_context_t ctx=vfs_context_kernel();
    if (!a52q_ufs_root_named("a52ios0") || a52q_ufs_rootdev(&device) ||
        SecureDTLookupEntry(NULL,"/a52q-ufs-root",&root)!=kSuccess ||
        !a52v_property(root,"window",rw,sizeof(rw)) ||
        !a52v_property(root,"ufs-nonce",&root_nonce,sizeof(root_nonce)) ||
        !a52v_property(node,"window",window,sizeof(window)) ||
        !a52v_property(node,"ufs-nonce",&nonce,sizeof(nonce)) || nonce!=root_nonce ||
        !a52v_property(node,"header-crc32",&crc,sizeof(crc)) ||
        !a52q_var_window_valid(rw,window)) return EINVAL;
    vnode_t source=NULL;
    error=vnode_open("/dev/ra52ufs0",FREAD,0,0,&source,ctx);
    if (error) return error;
    /* vnode_open retains both counts; keep only its open usecount. */
    if (vnode_vtype(source)!=VCHR || major(chrtoblk(vnode_specrdev(source)))!=major(device) ||
        minor(vnode_specrdev(source))!=0) {error=ENXIO;goto fail;}
    uint8_t *header=kalloc_data(4096,Z_WAITOK);
    if (!header) {error=ENOMEM;goto fail;}
    int residual=4096;
    error=vn_rdwr(UIO_READ,source,(caddr_t)header,4096,(off_t)(window[2]*4096),UIO_SYSSPACE,0,
        vfs_context_ucred(ctx),&residual,kernproc);
    uint32_t found=0xffffffffU;
    for (unsigned i=0;i<4096;i++) {
        found^=header[i];
        for (unsigned j=0;j<8;j++) found=(found>>1)^(0xedb88320U&(0U-(found&1)));
    }
    kfree_data(header,4096);
    if (error || residual || (found^0xffffffffU)!=crc) {if (!error) error=EIO;goto fail;}
    error=a52q_ufs_var_enable(window,nonce,crc,&a52v_writable);
    if (error) goto fail;
    a52v_start=window[2]*4096;a52v_source=source;
    int major_number=bdevsw_add(-1,&a52v_bdevsw);
    if (major_number<0) {error=ENXIO;goto fail;}
    a52v_ready=1;
    if (!devfs_make_node(makedev(major_number,0),DEVFS_BLOCK,UID_ROOT,GID_OPERATOR,
        a52v_writable ? 0660 : 0440,"a52var0")) {
        a52v_ready=0;bdevsw_remove(major_number,&a52v_bdevsw);error=ENXIO;goto fail;
    }
    vnode_put(source);
    printf("A52Q var proxy: verified separate 4GiB UFS %s extent; root unchanged\n",
        a52v_writable ? "development-writable" : "read-only");return 0;
fail:
    vnode_close(source,FREAD,ctx);vnode_put(source);return error;
}
int a52q_data_fstab(struct sysctl_req *req);
int a52q_data_fstab(struct sysctl_req *req)
{
    DTEntry node;if (SecureDTLookupEntry(NULL,"/a52q-ufs-var",&node)!=kSuccess) return 0;
    lck_mtx_lock(&a52v_init_lock);
    int error=a52v_ready ? 0 : a52v_init(node);
    lck_mtx_unlock(&a52v_init_lock);
    if (error) {printf("A52Q var proxy: publication rejected error=%d\n",error);return error;}
    /* iOS mount -P 2 selects NONROOT_PASSNO exactly. Zero skips BOTH phases. */
    struct a52v_wire entry={.spec="/dev/a52var0",.file="/private/var",.vfstype="hfs",.passno=2};
    entry.mntops[0]=entry.type[0]='r';
    entry.mntops[1]=entry.type[1]=a52v_writable ? 'w' : 'o';
    return SYSCTL_OUT(req,&entry,sizeof(entry));
}
#endif
