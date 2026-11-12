/* A52 UFS kernel selftest: no disk registration, write CDB, clocks or reset.
 * Enabled ONLY by the evidence-bound /a52q-ufs-selftest ADT node. Uses the exact
 * packet helpers validated by the independent physical shim experiment.
 * The shim's DMA address contains the loaded kernel now: allocate NEW wired,
 * contiguous kernel RAM and maintain its caches explicitly instead.
 */
#include <sys/param.h>
#include <sys/systm.h>
#include <sys/errno.h>
#include <kern/clock.h>
#include <mach/mach_time.h>
#include <machine/machine_routines.h>
#include <arm/caches_internal.h>
#include <vm/pmap.h>
#include <vm/vm_kern.h>
#include <pexpert/pexpert.h>
#include <pexpert/device_tree.h>
#include <libkern/libkern.h>

#include "a52q_ufs_nop_protocol.h"
#include "a52q_ufs_read_protocol.h"

extern ppnum_t pmap_find_phys(pmap_t pmap, addr64_t va);
extern vm_offset_t ml_io_map(vm_offset_t phys_addr, vm_size_t size);

enum { A52_UFS_CAP = 0, A52_UFS_VER = 8, A52_UFS_AHIT = 0x18,
    A52_UFS_HCS = 0x30, A52_UFS_HCE = 0x34, A52_UFS_BA = 0x50,
    A52_UFS_BAH = 0x54, A52_UFS_DBR = 0x58, A52_UFS_RSR = 0x60 };
enum { A52_UFS_POOL = 16384, A52_UFS_CMD = 4096, A52_UFS_DATA = 8192 };
static struct {
    vm_offset_t regs, dma;
    uint64_t pa, nonce;
    uint32_t last, block, crc, ocs, response;
} a52u;

static uint32_t a52u_read(unsigned offset)
{
    return *(volatile uint32_t *)(a52u.regs + offset);
}
static void a52u_write(unsigned offset, uint32_t value)
{
    *(volatile uint32_t *)(a52u.regs + offset) = value;
    __asm__ volatile("dsb sy" ::: "memory");
}
static int a52u_wait(unsigned offset, uint32_t mask, uint32_t value)
{
    uint64_t deadline;
    nanoseconds_to_deadline(NSEC_PER_SEC, &deadline);
    while ((a52u_read(offset) & mask) != value) {
        if (mach_absolute_time() >= deadline) return ETIMEDOUT;
    }
    return 0;
}
static int a52u_property(DTEntry node, const char *name, void *out, unsigned length)
{
    const void *bytes;
    unsigned size;
    if (SecureDTGetProperty(node, name, &bytes, &size) != kSuccess || size != length) return 0;
    memcpy(out, bytes, length);
    return 1;
}
static void a52u_report(unsigned phase)
{
    char body[112];
    int length = snprintf(body, sizeof(body), "%016llx/%02x/%08x/%08x/%08x/%08x/%08x",
        a52u.nonce, phase, a52u.ocs, a52u.last, a52u.block, a52u.crc, a52u.response);
    if (length <= 0 || (unsigned)length >= sizeof(body)) return;
    uint32_t crc = ufs_data_crc32((const uint8_t *)body, (unsigned)length);
    for (unsigned i = 0; i < 5; i++) printf("A52K1 %s %08x\n", body, crc);
}
static int a52u_transfer(unsigned opcode, uint32_t lba, unsigned bytes)
{
    if (a52u_read(A52_UFS_DBR) || a52u_read(A52_UFS_RSR) != 1 ||
        a52u_read(A52_UFS_HCE) != 1 || (a52u_read(A52_UFS_HCS) & 15) != 15) return EBUSY;
    volatile uint32_t *list = (volatile uint32_t *)a52u.dma;
    volatile uint8_t *request = (volatile uint8_t *)(a52u.dma + A52_UFS_CMD);
    bzero((void *)a52u.dma, A52_UFS_POOL);
    memset((void *)(a52u.dma + A52_UFS_DATA), 0xa5, 4096);
    if (!opcode) {
        ufs_nop_descriptor(list, a52u.pa + A52_UFS_CMD);
    } else if (!ufs_read_packet(list, request,
            (volatile uint32_t *)(a52u.dma + A52_UFS_CMD + 2048),
            a52u.pa + A52_UFS_CMD, a52u.pa + A52_UFS_DATA, opcode, lba, bytes)) {
        return EINVAL;
    }
    /* Clean/invalidate before device access; no CPU accesses to the pool until
     * completion. A second flush then invalidates device-written response/data. */
    flush_dcache64(a52u.pa, A52_UFS_POOL, TRUE);
    __asm__ volatile("dsb sy" ::: "memory");
    uint32_t old_lo = a52u_read(A52_UFS_BA), old_hi = a52u_read(A52_UFS_BAH);
    a52u_write(A52_UFS_RSR, 0);
    if (a52u_wait(A52_UFS_RSR, 1, 0)) return ETIMEDOUT;
    a52u_write(A52_UFS_BA, (uint32_t)a52u.pa);
    a52u_write(A52_UFS_BAH, (uint32_t)(a52u.pa >> 32));
    a52u_write(A52_UFS_RSR, 1);
    if (a52u_read(A52_UFS_BA) != (uint32_t)a52u.pa ||
        a52u_read(A52_UFS_BAH) != (uint32_t)(a52u.pa >> 32) ||
        a52u_wait(A52_UFS_RSR, 1, 1)) return EIO;
    a52u_write(A52_UFS_DBR, 1);
    if (a52u_wait(A52_UFS_DBR, 1, 0)) {
        /* Pool is permanently allocated: never free/reuse an in-flight DMA
         * target. No retries or reset; physical recovery is required. */
        return ETIMEDOUT;
    }
    flush_dcache64(a52u.pa, A52_UFS_POOL, TRUE);
    __asm__ volatile("dsb sy" ::: "memory");
    volatile const uint8_t *rsp = request + 1024;
    a52u.ocs = list[2] & 15;
    a52u.response = ufs_be32(rsp);
    int valid = (rsp[0] & 0x3f) == (opcode ? 0x21 : 0x20) && rsp[3] == 0 &&
        rsp[6] == 0 && rsp[7] == 0;
    a52u_write(A52_UFS_RSR, 0);
    if (a52u_wait(A52_UFS_RSR, 1, 0)) return ETIMEDOUT;
    a52u_write(A52_UFS_BA, old_lo);
    a52u_write(A52_UFS_BAH, old_hi);
    a52u_write(A52_UFS_RSR, 1);
    if (a52u_read(A52_UFS_BA) != old_lo || a52u_read(A52_UFS_BAH) != old_hi ||
        a52u_wait(A52_UFS_RSR, 1, 1)) return EIO;
    return a52u.ocs || !valid ? EIO : 0;
}

void a52q_ufs_selftest(void);
void a52q_ufs_selftest(void)
{
    DTEntry node;
    if (SecureDTLookupEntry(NULL, "/a52q-ufs-selftest", &node) != kSuccess) return;
    uint64_t reg[2];
    uint32_t expected_last, expected_block, lba, expected_crc;
    if (!a52u_property(node, "reg", reg, sizeof(reg)) ||
        !a52u_property(node, "nonce", &a52u.nonce, sizeof(a52u.nonce)) ||
        !a52u_property(node, "last-lba", &expected_last, sizeof(expected_last)) ||
        !a52u_property(node, "block-bytes", &expected_block, sizeof(expected_block)) ||
        !a52u_property(node, "read-lba", &lba, sizeof(lba)) ||
        !a52u_property(node, "read-crc32", &expected_crc, sizeof(expected_crc)) ||
        reg[0] & PAGE_MASK || reg[0] >= 0x80000000ULL || reg[1] < 0x64 || reg[1] > 0x10000 ||
        expected_block != 4096 || lba >= expected_last) {
        printf("A52Q UFS selftest: invalid evidence-bound ADT\n"); return;
    }
    a52u.ocs = 15;
    a52u.regs = ml_io_map((vm_offset_t)reg[0], (vm_size_t)reg[1]);
    if (!a52u.regs || !(a52u_read(A52_UFS_CAP) & (1U << 24)) ||
        a52u_read(A52_UFS_VER) != 0x210 || a52u_read(A52_UFS_AHIT)) {
        a52u_report(0xe0); return;
    }
    if (kmem_alloc_contig(kernel_map, &a52u.dma, A52_UFS_POOL, PAGE_MASK, 0, 0,
            KMA_DATA | KMA_ZERO | KMA_PERMANENT, VM_KERN_MEMORY_IOKIT) != KERN_SUCCESS) {
        a52u_report(0xe1); return;
    }
    ppnum_t page = pmap_find_phys(kernel_pmap, (addr64_t)a52u.dma);
    if (!page) { a52u_report(0xe2); return; }
    a52u.pa = ptoa_64(page);
    printf("A52Q UFS selftest: new kernel DMA pool pa=0x%llx; no disk writes\n", a52u.pa);
    a52u_report(0x10);
    if (a52u_transfer(0, 0, 0)) { a52u_report(0xe3); return; }
    a52u_report(0x11);
    if (a52u_transfer(0x25, 0, 8)) { a52u_report(0xe4); return; }
    volatile const uint8_t *data = (volatile const uint8_t *)(a52u.dma + A52_UFS_DATA);
    a52u.last = ufs_be32(data);
    a52u.block = ufs_be32(data + 4);
    if (a52u.last != expected_last || a52u.block != expected_block) { a52u_report(0xe5); return; }
    if (a52u_transfer(0x28, lba, 4096)) { a52u_report(0xe6); return; }
    a52u.crc = ufs_data_crc32(data, 4096);
    a52u_report(a52u.crc == expected_crc ? 0x20 : 0xe7);
}
