/* Separate, default-OFF /var writer. Included after the unchanged BSD reader so
 * both paths share its mutex/DMA ownership. Existing raw/root devices stay RO.
 * No clocks, reset, arbitrary command API, or root-window write is introduced.
 */
#include "a52q_var_bounds.h"
#include "a52q_var_write_protocol.h"
#include "a52q_var_write_plan.h"
static uint64_t a52w_root[4],a52w_var[4];
static uint8_t a52w_bounce[4096],a52w_probe[4096];
static int a52w_ready;

static void a52w_report(unsigned phase,int error)
{
    char body[112];
    int n=snprintf(body,sizeof(body),"%016llx/%02x/%08x/%08x/%08x",
        a52u.nonce,phase,(unsigned)error,a52u.ocs,a52u.response);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    uint32_t crc=ufs_data_crc32((const uint8_t *)body,(unsigned)n);
    for (unsigned i=0;i<5;i++) printf("A52W1 %s %08x\n",body,crc);
}

/* Same verified one-slot takeover/restore sequence as the existing reader.
 * Only the packet builder and outbound-data copy differ. A failed command
 * permanently poisons the shared DMA pool, exactly like a failed READ(10).
 */
static int a52w_command_inner(int sync,uint32_t lba,const uint8_t *source)
{
    if (a52u_read(A52_UFS_DBR) || a52u_read(A52_UFS_RSR)!=1 ||
        a52u_read(A52_UFS_HCE)!=1 || (a52u_read(A52_UFS_HCS)&15)!=15) return EBUSY;
    volatile uint32_t *list=(volatile uint32_t *)a52u.dma;
    volatile uint8_t *request=(volatile uint8_t *)(a52u.dma+A52_UFS_CMD);
    bzero((void *)a52u.dma,A52_UFS_POOL);
    if (sync) a52q_var_sync_packet(list,request,a52u.pa+A52_UFS_CMD);
    else {
        memcpy((void *)(a52u.dma+A52_UFS_DATA),source,4096);
        a52q_var_write_packet(list,request,
            (volatile uint32_t *)(a52u.dma+A52_UFS_CMD+2048),
            a52u.pa+A52_UFS_CMD,a52u.pa+A52_UFS_DATA,lba);
    }
    flush_dcache64(a52u.pa,A52_UFS_POOL,TRUE);
    __asm__ volatile("dsb sy" ::: "memory");
    uint32_t old_lo=a52u_read(A52_UFS_BA),old_hi=a52u_read(A52_UFS_BAH);
    a52u_write(A52_UFS_RSR,0);
    if (a52u_wait(A52_UFS_RSR,1,0)) return ETIMEDOUT;
    a52u_write(A52_UFS_BA,(uint32_t)a52u.pa);
    a52u_write(A52_UFS_BAH,(uint32_t)(a52u.pa>>32));
    a52u_write(A52_UFS_RSR,1);
    if (a52u_read(A52_UFS_BA)!=(uint32_t)a52u.pa ||
        a52u_read(A52_UFS_BAH)!=(uint32_t)(a52u.pa>>32) ||
        a52u_wait(A52_UFS_RSR,1,1)) return EIO;
    a52u_write(A52_UFS_DBR,1);
    if (a52u_wait(A52_UFS_DBR,1,0)) return ETIMEDOUT;
    flush_dcache64(a52u.pa,A52_UFS_POOL,TRUE);
    __asm__ volatile("dsb sy" ::: "memory");
    volatile const uint8_t *response=request+1024;
    a52u.ocs=list[2]&15;a52u.response=ufs_be32(response);
    int valid=a52q_ufs_response_ok(response,1); /* SCSI response, even without data. */
    a52u_write(A52_UFS_RSR,0);
    if (a52u_wait(A52_UFS_RSR,1,0)) return ETIMEDOUT;
    a52u_write(A52_UFS_BA,old_lo);a52u_write(A52_UFS_BAH,old_hi);
    a52u_write(A52_UFS_RSR,1);
    if (a52u_read(A52_UFS_BA)!=old_lo || a52u_read(A52_UFS_BAH)!=old_hi ||
        a52u_wait(A52_UFS_RSR,1,1)) return EIO;
    return a52u.ocs || !valid ? EIO : 0;
}
static int a52w_command(int sync,uint32_t lba,const uint8_t *source)
{
    if (a52u.failed) return EIO;
    int error=a52w_command_inner(sync,lba,source);
    if (error) {a52u.failed=1;a52w_report(0xe1,error);}
    return error;
}
static int a52w_read_block(void *unused __unused,uint32_t lba,uint8_t *out)
{
    int error=a52u_transfer(0x28,lba,4096);
    if (!error) memcpy(out,(const void *)(a52u.dma+A52_UFS_DATA),4096);
    return error;
}
static int a52w_write_block(void *unused __unused,uint32_t lba,const uint8_t *source)
{
    uint32_t checked;
    if (lba<a52w_var[2] || !a52q_var_write_lba(a52w_root,a52w_var,a52u.last,
        ((uint64_t)lba-a52w_var[2])*4096,4096,&checked) || checked!=lba) return EINVAL;
    int error=a52w_command(0,lba,source);
    /* Always make completed writes durable before reporting them to HFS.
     * No FUA-capability assumption; reject failed SYNCHRONIZE CACHE responses.
     */
    return error ? error : a52w_command(1,0,NULL);
}

int a52q_ufs_var_enable(const uint64_t window[4],uint64_t nonce,uint32_t header_crc,int *enabled);
int a52q_ufs_var_enable(const uint64_t window[4],uint64_t nonce,uint32_t header_crc,int *enabled)
{
    DTEntry cap,root;uint64_t advertised[4],root_window[4],cap_nonce;
    uint32_t cap_crc;int opt=0;
    if (!enabled) return EINVAL;
    *enabled=0;
    if (SecureDTLookupEntry(NULL,"/a52q-var-write-development",&cap)!=kSuccess) return 0;
    if (!PE_parse_boot_argn("a52qvarwrite",&opt,sizeof(opt)) || opt!=1 ||
        !a52u_disk_ready || !a52u_root_ready || a52u_root_kind!=2 ||
        SecureDTLookupEntry(NULL,"/a52q-ufs-root",&root)!=kSuccess ||
        !a52u_property(root,"window",root_window,sizeof(root_window)) ||
        root_window[2]!=a52u_root_first || root_window[3]!=a52u_root_blocks ||
        !a52u_property(cap,"window",advertised,sizeof(advertised)) ||
        memcmp(advertised,window,sizeof(advertised)) ||
        !a52q_var_window_valid(root_window,window) ||
        !a52u_property(cap,"ufs-nonce",&cap_nonce,sizeof(cap_nonce)) ||
        cap_nonce!=nonce || nonce!=a52u.nonce ||
        !a52u_property(cap,"header-crc32",&cap_crc,sizeof(cap_crc)) ||
        cap_crc!=header_crc) return EINVAL;
    lck_mtx_lock(&a52u_disk_lock);
    memcpy(a52w_root,root_window,sizeof(a52w_root));memcpy(a52w_var,window,sizeof(a52w_var));
    uint32_t lba;int error=0;
    if (!a52q_var_write_lba(a52w_root,a52w_var,a52u.last,0,4096,&lba)) error=EINVAL;
    if (!error) error=a52w_read_block(NULL,lba,a52w_probe);
    if (!error && ufs_data_crc32(a52w_probe,4096)!=header_crc) error=EIO;
    /* First command writes back the exact read/verified bytes. No filesystem
     * writes become available until synchronize + complete readback pass.
     */
    if (!error) error=a52w_write_block(NULL,lba,a52w_probe);
    if (!error) error=a52w_read_block(NULL,lba,a52w_bounce);
    if (!error && memcmp(a52w_probe,a52w_bounce,4096)) error=EIO;
    if (!error) {a52w_ready=1;*enabled=1;}
    else {a52w_ready=0;a52u.failed=1;}
    a52w_report(error ? 0xe0 : 0x10,error);
    lck_mtx_unlock(&a52u_disk_lock);
    return error;
}
int a52q_ufs_var_write(uint64_t offset,const uint8_t *source,uint32_t bytes,uint32_t *completed);
int a52q_ufs_var_write(uint64_t offset,const uint8_t *source,uint32_t bytes,uint32_t *completed)
{
    if (!completed) return EINVAL;
    *completed=0;
    lck_mtx_lock(&a52u_disk_lock);
    int error=!a52w_ready ? EROFS : a52u.failed ? EIO :
        a52q_var_write_bytes(a52w_root,a52w_var,a52u.last,offset,source,bytes,
            a52w_bounce,a52w_read_block,a52w_write_block,NULL,completed,EINVAL);
    lck_mtx_unlock(&a52u_disk_lock);return error;
}
int a52q_ufs_var_sync(void);
int a52q_ufs_var_sync(void)
{
    lck_mtx_lock(&a52u_disk_lock);
    int error=!a52w_ready ? EROFS : a52w_command(1,0,NULL);
    lck_mtx_unlock(&a52u_disk_lock);return error;
}
