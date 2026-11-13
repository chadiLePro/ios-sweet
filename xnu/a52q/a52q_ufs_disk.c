/* Read-only BSD LUN0 interface, enabled only AFTER the kernel UFS proof passes.
 * Optional bounded diagnostic BOOT-tail minor; no SCSI writes or resets.
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
static uint64_t a52u_root_first, a52u_root_blocks;
static int a52u_root_ready, a52u_block_major = -1;

static int a52u_unit_ready(unsigned unit)
{
    return a52u_disk_ready && (unit == 0 || (unit == 1 && a52u_root_ready));
}
static uint64_t a52u_unit_blocks(unsigned unit)
{
    return unit == 1 ? a52u_root_blocks : (uint64_t)a52u.last + 1;
}

static int a52u_disk_open(dev_t dev, int flags, int type __unused, struct proc *p __unused)
{
    if (!a52u_unit_ready(minor(dev))) return ENXIO;
    return flags & FWRITE ? EROFS : 0;
}
static int a52u_disk_close(dev_t dev __unused, int flags __unused,
    int type __unused, struct proc *p __unused) { return 0; }
static void a52u_disk_strategy_for(buf_t bp, unsigned unit)
{
    int error = 0;
    caddr_t destination = NULL;
    uint32_t count = buf_count(bp), done = 0;
    daddr64_t block = buf_blkno(bp);
    buf_setresid(bp, count);
    if (!(buf_flags(bp) & B_READ)) { error = EROFS; goto finish; }
    if (!a52u_unit_ready(unit)) { error = ENXIO; goto finish; }
    if (block < 0 || (uint64_t)block > UINT64_MAX / DEV_BSIZE ||
        !a52q_ufs_window_range(a52u_unit_blocks(unit), (uint64_t)block * DEV_BSIZE, count)) {
        error = EINVAL; goto finish;
    }
    if (!count) goto finish;
    if (buf_map(bp, &destination)) { error = EIO; goto finish; }
    lck_mtx_lock(&a52u_disk_lock);
    while (done < count) {
        uint64_t offset = (unit == 1 ? a52u_root_first * 4096 : 0) + (uint64_t)block * DEV_BSIZE + done;
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
static void a52u_disk_strategy(buf_t bp)
{
    a52u_disk_strategy_for(bp, minor(buf_device(bp)));
}
static int a52u_disk_ioctl(dev_t dev, u_long command, caddr_t data,
    int flags __unused, struct proc *p __unused)
{
    if (!a52u_unit_ready(minor(dev))) return ENXIO;
    switch (command) {
    case DKIOCGETBLOCKSIZE: *(uint32_t *)data = DEV_BSIZE; return 0;
    case DKIOCSETBLOCKSIZE: return *(uint32_t *)data == DEV_BSIZE ? 0 : EINVAL;
    case DKIOCGETPHYSICALBLOCKSIZE: *(uint32_t *)data = 4096; return 0;
    case DKIOCGETBLOCKCOUNT: *(uint64_t *)data = a52u_unit_blocks(minor(dev)) * (4096 / DEV_BSIZE); return 0;
    case DKIOCISWRITABLE: *(uint32_t *)data = 0; return 0;
    case DKIOCGETMAXBLOCKCOUNTREAD: *(uint64_t *)data = 4096 / DEV_BSIZE; return 0;
    case DKIOCGETMAXBLOCKCOUNTWRITE: *(uint64_t *)data = 0; return 0;
    case DKIOCGETMAXSEGMENTCOUNTREAD: *(uint64_t *)data = 1; return 0;
    default: return ENOTTY;
    }
}
static int a52u_disk_size(dev_t dev)
{
    return !a52u_unit_ready(minor(dev)) ? -1 :
        (int)MIN(a52u_unit_blocks(minor(dev)) * (4096 / DEV_BSIZE), INT_MAX);
}
static int a52u_disk_read(dev_t dev, struct uio *uio, int flags __unused)
{
    if (!a52u_unit_ready(minor(dev))) return ENXIO;
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
static int a52u_root_publish(int block_major, int raw_major)
{
    DTEntry node;
    if (SecureDTLookupEntry(NULL, "/a52q-ufs-root", &node) != kSuccess) return 0;
    uint64_t window[4], nonce;
    uint32_t expected;
    if (!a52u_property(node, "window", window, sizeof(window)) ||
        !a52u_property(node, "ufs-nonce", &nonce, sizeof(nonce)) || nonce != a52u.nonce ||
        !a52u_property(node, "header-crc32", &expected, sizeof(expected)) ||
        !a52q_ufs_boot_window(a52u.last, window[0], window[1], window[2], window[3])) return EINVAL;
    /* Verify the new window through the same BSD strategy before publication. */
    static uint8_t check[4096];
    buf_t bp = buf_alloc(NULL);
    if (!bp) return ENOMEM;
    a52u_root_first = window[2]; a52u_root_blocks = window[3]; a52u_root_ready = 1;
    buf_setflags(bp, B_READ); buf_setblkno(bp, 0);
    buf_setcount(bp, sizeof(check)); buf_setdataptr(bp, (uintptr_t)check);
    a52u_disk_strategy_for(bp, 1);
    int error = buf_biowait(bp);
    uint32_t crc = ufs_data_crc32(check, sizeof(check));
    if (!error && (buf_resid(bp) || crc != expected)) error = EIO;
    buf_free(bp);
    if (error) { a52u_root_ready = 0; return error; }
    void *block = devfs_make_node(makedev(block_major, 1), DEVFS_BLOCK, UID_ROOT, GID_OPERATOR, 0440, "a52root0");
    void *raw = devfs_make_node(makedev(raw_major, 1), DEVFS_CHAR, UID_ROOT, GID_OPERATOR, 0440, "ra52root0");
    if (!block || !raw) {
        if (block) devfs_remove(block);
        if (raw) devfs_remove(raw);
        a52u_root_ready = 0; return ENXIO;
    }
    a52u_block_major = block_major;
    char body[64];
    int n = snprintf(body, sizeof(body), "%016llx/%08x/%08x/%08x", a52u.nonce,
        (uint32_t)a52u_root_first, (uint32_t)a52u_root_blocks, crc);
    if (n > 0 && (unsigned)n < sizeof(body)) for (unsigned i = 0; i < 5; i++)
        printf("A52V1 %s %08x\n", body, ufs_data_crc32((const uint8_t *)body, (unsigned)n));
    printf("A52Q UFS diagnostic root: bounded read-only BOOT tail /dev/a52root0\n");
    return 0;
}

int a52q_ufs_rootdev(dev_t *dev);
int a52q_ufs_rootdev(dev_t *dev)
{
    if (!dev || !a52u_root_ready || !a52u_disk_ready || a52u_block_major < 0) return ENXIO;
    *dev = makedev(a52u_block_major, 1);
    return 0;
}
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
    a52u_disk_strategy_for(bp, 0);
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
    printf("A52Q UFS: read-only whole LUN0 minor0 /dev/a52ufs0 /dev/ra52ufs0\n");
    return a52u_root_publish(block_major, raw_major);
}
