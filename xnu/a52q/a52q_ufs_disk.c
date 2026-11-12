/* Read-only BSD LUN0 interface, enabled only AFTER the kernel UFS proof passes.
 * No GPT assumptions, partition mapping, root selection, SCSI writes or resets.
 * Logical sectors stay 512 bytes. Each request uses the proven one-block packet
 * with a serialized bounce buffer; it is intentionally slow during bring-up.
 */
#include <sys/buf.h>
#include <sys/conf.h>
#include <sys/disk.h>
#include <sys/proc.h>
#include <sys/uio.h>
#include <miscfs/devfs/devfs.h>
#include <kern/locks.h>
#include "a52q_ufs_bounds.h"

static LCK_GRP_DECLARE(a52u_disk_group, "a52q_ufs_readonly");
static LCK_MTX_DECLARE(a52u_disk_lock, &a52u_disk_group);
static int a52u_disk_ready;

static int a52u_disk_open(dev_t dev, int flags, int type __unused, struct proc *p __unused)
{
    if (minor(dev) || !a52u_disk_ready) return ENXIO;
    return flags & FWRITE ? EROFS : 0;
}
static int a52u_disk_close(dev_t dev __unused, int flags __unused,
    int type __unused, struct proc *p __unused) { return 0; }
static void a52u_disk_strategy(buf_t bp)
{
    int error = 0;
    caddr_t destination = NULL;
    uint32_t count = buf_count(bp), done = 0;
    daddr64_t block = buf_blkno(bp);
    buf_setresid(bp, count);
    if (!(buf_flags(bp) & B_READ)) { error = EROFS; goto finish; }
    if (!a52u_disk_ready) { error = ENXIO; goto finish; }
    if (block < 0 || (uint64_t)block > UINT64_MAX / DEV_BSIZE ||
        !a52q_ufs_range(a52u.last, (uint64_t)block * DEV_BSIZE, count)) {
        error = EINVAL; goto finish;
    }
    if (!count) goto finish;
    if (buf_map(bp, &destination)) { error = EIO; goto finish; }
    lck_mtx_lock(&a52u_disk_lock);
    while (done < count) {
        uint64_t offset = (uint64_t)block * DEV_BSIZE + done;
        uint32_t want = a52q_ufs_chunk(offset, count - done);
        error = a52u_transfer(0x28, (uint32_t)(offset / 4096), 4096);
        if (error) break;
        memcpy(destination + done, (const void *)(a52u.dma + A52_UFS_DATA + offset % 4096), want);
        done += want;
        buf_setresid(bp, count - done);
    }
    lck_mtx_unlock(&a52u_disk_lock);
    buf_unmap(bp);
finish:
    if (error) buf_seterror(bp, error);
    buf_biodone(bp);
}
static int a52u_disk_ioctl(dev_t dev, u_long command, caddr_t data,
    int flags __unused, struct proc *p __unused)
{
    if (minor(dev) || !a52u_disk_ready) return ENXIO;
    switch (command) {
    case DKIOCGETBLOCKSIZE: *(uint32_t *)data = DEV_BSIZE; return 0;
    case DKIOCSETBLOCKSIZE: return *(uint32_t *)data == DEV_BSIZE ? 0 : EINVAL;
    case DKIOCGETPHYSICALBLOCKSIZE: *(uint32_t *)data = 4096; return 0;
    case DKIOCGETBLOCKCOUNT: *(uint64_t *)data = ((uint64_t)a52u.last + 1) * (4096 / DEV_BSIZE); return 0;
    case DKIOCISWRITABLE: *(uint32_t *)data = 0; return 0;
    case DKIOCGETMAXBLOCKCOUNTREAD: *(uint64_t *)data = 4096 / DEV_BSIZE; return 0;
    case DKIOCGETMAXBLOCKCOUNTWRITE: *(uint64_t *)data = 0; return 0;
    case DKIOCGETMAXSEGMENTCOUNTREAD: *(uint64_t *)data = 1; return 0;
    default: return ENOTTY;
    }
}
static int a52u_disk_size(dev_t dev)
{
    return minor(dev) || !a52u_disk_ready ? -1 :
        (int)MIN(((uint64_t)a52u.last + 1) * (4096 / DEV_BSIZE), INT_MAX);
}
static int a52u_disk_read(dev_t dev, struct uio *uio, int flags __unused)
{
    if (minor(dev) || !a52u_disk_ready) return ENXIO;
    return physio(a52u_disk_strategy, NULL, dev, B_READ, minphys, uio, DEV_BSIZE);
}
static int a52u_disk_write(dev_t dev __unused, struct uio *uio __unused,
    int flags __unused) { return EROFS; }
static const struct bdevsw a52u_bdevsw = {
    .d_open = a52u_disk_open, .d_close = a52u_disk_close, .d_strategy = a52u_disk_strategy,
    .d_ioctl = a52u_disk_ioctl, .d_dump = eno_dump, .d_psize = a52u_disk_size, .d_type = D_DISK,
};
static const struct cdevsw a52u_cdevsw = {
    .d_open = a52u_disk_open, .d_close = a52u_disk_close, .d_read = a52u_disk_read,
    .d_write = a52u_disk_write, .d_ioctl = a52u_disk_ioctl, .d_stop = eno_stop,
    .d_reset = eno_reset, .d_select = eno_select, .d_mmap = eno_mmap,
    .d_strategy = eno_strat, .d_reserved_1 = eno_getc, .d_reserved_2 = eno_putc, .d_type = D_DISK,
};
static int a52u_disk_publish(uint32_t known_lba, uint32_t expected_crc)
{
    /* Exercise the BSD buffer path before publishing any device nodes. */
    static uint8_t check[4096];
    buf_t bp = buf_alloc(NULL);
    if (!bp) return ENOMEM;
    a52u_disk_ready = 1;
    buf_setflags(bp, B_READ);
    buf_setblkno(bp, (daddr64_t)known_lba * (4096 / DEV_BSIZE));
    buf_setcount(bp, sizeof(check));
    buf_setdataptr(bp, (uintptr_t)check);
    a52u_disk_strategy(bp);
    int error = buf_biowait(bp);
    if (!error && (buf_resid(bp) || ufs_data_crc32(check, sizeof(check)) != expected_crc)) error = EIO;
    buf_free(bp);
    if (error) { a52u_disk_ready = 0; return error; }
    int block_major = bdevsw_add(-1, &a52u_bdevsw);
    if (block_major < 0) { a52u_disk_ready = 0; return ENXIO; }
    int raw_major = cdevsw_add_with_bdev(-1, &a52u_cdevsw, block_major);
    if (raw_major < 0) {
        bdevsw_remove(block_major, &a52u_bdevsw);
        a52u_disk_ready = 0; return ENXIO;
    }
    void *block_node = devfs_make_node(makedev(block_major, 0), DEVFS_BLOCK,
        UID_ROOT, GID_OPERATOR, 0440, "a52ufs0");
    void *raw_node = devfs_make_node(makedev(raw_major, 0), DEVFS_CHAR,
        UID_ROOT, GID_OPERATOR, 0440, "ra52ufs0");
    if (!block_node || !raw_node) {
        if (block_node) devfs_remove(block_node);
        if (raw_node) devfs_remove(raw_node);
        cdevsw_remove(raw_major, &a52u_cdevsw);
        bdevsw_remove(block_major, &a52u_bdevsw);
        a52u_disk_ready = 0; return ENXIO;
    }
    printf("A52Q UFS: read-only LUN0 /dev/a52ufs0 /dev/ra52ufs0; no partition/root mapping\n");
    return 0;
}
