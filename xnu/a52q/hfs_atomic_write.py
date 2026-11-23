"""Narrow HFS exchange compatibility for the observed usermanagerd boot failure.

The original Redmi block stays byte-for-byte intact. A52 uses the real HFS
exchange operation only for the two observed session/persona atomic writes on
its proven writable /var device; all other rename outcomes remain unchanged.
"""
TARGET='bsd/vfs/kpi_vfs.c'
FUNCTION='errno_t\nvn_rename('
ANCHOR='''#if defined(ARM64_BOARD_CONFIG_SWEET)
			/*
			 * SWEET: HFS has no RENAME_SWAP, which Foundation's atomic'''
END='''				_err = VNOP_EXCHANGE(*fvpp, *tvpp, 0, ctx);
			}
#endif'''
HOOK='''
#if defined(ARM64_BOARD_CONFIG_A52Q)
			if (_err == ENOTSUP)
				_err = a52q_hfs_atomic_swap(fdvp,*fvpp,fcnp,tdvp,*tvpp,tcnp,flags,ctx);
#endif'''
HELPER=r'''
#if defined(ARM64_BOARD_CONFIG_A52Q)
extern int a52q_var_atomic_context(dev_t,uint64_t *);
static int a52q_atomic_name(const struct componentname *name,const char *text)
{
    size_t size=strlen(text);
    return name && name->cn_nameptr && name->cn_namelen==(int)size &&
        !memcmp(name->cn_nameptr,text,size);
}
static unsigned a52q_atomic_pair(const struct componentname *from,const struct componentname *to)
{
    if ((a52q_atomic_name(from,"usersession.kb.writing") && a52q_atomic_name(to,"usersession.kb")) ||
        (a52q_atomic_name(to,"usersession.kb.writing") && a52q_atomic_name(from,"usersession.kb"))) return 1;
    if ((a52q_atomic_name(from,"persona.kb.writing") && a52q_atomic_name(to,"persona.kb")) ||
        (a52q_atomic_name(to,"persona.kb.writing") && a52q_atomic_name(from,"persona.kb"))) return 2;
    return 0;
}
static void a52q_atomic_record(uint64_t nonce,unsigned kind,int error)
{
    static unsigned lines;
    if (__atomic_fetch_add(&lines,1U,__ATOMIC_RELAXED)>=32) return;
    char body[96];int n=snprintf(body,sizeof(body),"%016llx/%d/%u/%08x",
        (unsigned long long)nonce,proc_selfpid(),kind,(unsigned)error);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    for (unsigned i=0;i<3;i++) printf("A52A1 %s %08x\n",body,crc^0xffffffffU);
}
static int a52q_hfs_atomic_swap(vnode_t directory,vnode_t from,struct componentname *from_name,
    vnode_t target_directory,vnode_t to,struct componentname *to_name,unsigned flags,vfs_context_t ctx)
{
    char process[32],path[256];uint64_t nonce=0;
    if (flags!=VFS_RENAME_SWAP || !directory || directory!=target_directory ||
        !from || !to || from==to || !vnode_isreg(from) || !vnode_isreg(to) ||
        vnode_mount(from)!=vnode_mount(to)) return ENOTSUP;
    proc_selfname(process,sizeof(process));process[sizeof(process)-1]=0;
    if (strcmp(process,"usermanagerd")) return ENOTSUP;
    unsigned kind=a52q_atomic_pair(from_name,to_name);
    if (!kind) return ENOTSUP; /* In particular, never systembag.kb. */
    mount_t mount=vnode_mount(from);
    if (!mount || vnode_mount(directory)!=mount) return ENOTSUP;
    struct vfsstatfs *info=vfs_statfs(mount);
    if (vfs_isrdonly(mount) || !info || strcmp(info->f_fstypename,"hfs")) return ENOTSUP;
    vnode_t device=vfs_devvp(mount);
    if (!device) return ENOTSUP;
    int allowed=vnode_vtype(device)==VBLK && a52q_var_atomic_context(vnode_specrdev(device),&nonce);
    vnode_put(device);
    if (!allowed) return ENOTSUP;
    int length=sizeof(path);
    if (vn_getpath(directory,path,&length)) return ENOTSUP;
    path[sizeof(path)-1]=0;
    if (strcmp(path,"/private/var/keybags") && strcmp(path,"/var/keybags")) return ENOTSUP;
    struct vnode_attr fa,ta;
    VATTR_INIT(&fa);VATTR_WANTED(&fa,va_nlink);
    VATTR_INIT(&ta);VATTR_WANTED(&ta,va_nlink);
    int error=vnode_getattr(from,&fa,ctx);
    if (!error) error=vnode_getattr(to,&ta,ctx);
    if (!error && (!VATTR_IS_SUPPORTED(&fa,va_nlink) || !VATTR_IS_SUPPORTED(&ta,va_nlink) ||
        fa.va_nlink!=1 || ta.va_nlink!=1)) error=ENOTSUP;
    /* Retain the MAC and data-access checks used by exchangedata(2). */
#if CONFIG_MACF
    if (!error) error=mac_vnode_check_exchangedata(ctx,from,to);
#endif
    if (!error) error=vnode_authorize(from,NULL,KAUTH_VNODE_READ_DATA|KAUTH_VNODE_WRITE_DATA,ctx);
    if (!error) error=vnode_authorize(to,NULL,KAUTH_VNODE_READ_DATA|KAUTH_VNODE_WRITE_DATA,ctx);
    if (!error) error=VNOP_EXCHANGE(from,to,0,ctx);
    if (!error) {
        /* HFS swaps the catalog identities while keeping each open vnode's
         * content. Update BOTH cached names, as the exchangedata syscall does.
         * The outer rename's old-name check then avoids a second update.
         */
        vnode_update_identity(from,target_directory,to_name->cn_nameptr,to_name->cn_namelen,
            to_name->cn_hash,VNODE_UPDATE_NAME);
        vnode_update_identity(to,directory,from_name->cn_nameptr,from_name->cn_namelen,
            from_name->cn_hash,VNODE_UPDATE_NAME);
    }
    a52q_atomic_record(nonce,kind,error);return error;
}
#endif

'''


def transform(text):
    if text.count(ANCHOR)!=1 or text.count(FUNCTION)!=1 or 'a52q_hfs_atomic_swap' in text:
        raise ValueError('unexpected or already transformed HFS exchange source')
    start=text.index(ANCHOR);end=text.index(END,start)+len(END)
    text=text[:end]+HOOK+text[end:]
    return text.replace(FUNCTION,HELPER+FUNCTION,1)
