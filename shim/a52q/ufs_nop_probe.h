#include "ufs-nop-config.h"
#include "ufs_nop_protocol.h"
static uint32_t ufs_read(unsigned index)
{
    return *(volatile const uint32_t *)handoff_addresses[index];
}
static void ufs_write(unsigned index, uint32_t value)
{
    *(volatile uint32_t *)handoff_addresses[index] = value;
    __asm__ volatile("dsb sy" ::: "memory");
}
static int ufs_wait(unsigned index, uint32_t mask, uint32_t value)
{
    uint64_t begin = READ_REG("cntvct_el0");
    while ((ufs_read(index) & mask) != value)
        if (READ_REG("cntvct_el0") - begin > A52Q_UFS_TIMER_HZ)
            return 0;
    return 1;
}
static void ufs_nop_probe(void)
{
    uintptr_t lo = A52Q_UFS_POOL, hi = lo + A52Q_UFS_POOL_BYTES;
    uint64_t dtb = a52q_diagnostic.dtb;
    if (handoff_done != A52Q_HANDOFF_COUNT ||
        !(ufs_read(UFS_INDEX_CONTROLLER_CAPABILITIES) & (1U << 24)) ||
        ufs_read(UFS_INDEX_UFS_VERSION) != 0x210 ||
        ufs_read(UFS_INDEX_CONTROLLER_ENABLE) != 1 ||
        (ufs_read(UFS_INDEX_CONTROLLER_STATUS) & 15) != 15 ||
        ufs_read(UFS_INDEX_AUTO_HIBERNATE_IDLE_TIMER) ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL) ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP) != 1 ||
        READ_REG("cntfrq_el0") != A52Q_UFS_TIMER_HZ ||
        (lo < (uintptr_t)_end && (uintptr_t)_head < hi) ||
        (dtb > lo - (16ULL << 20) && dtb < hi + (16ULL << 20))) {
        publish(0xd0);
        return;
    }
    /* Test the virtual counter BEFORE changing controller state. */
    (void)READ_REG("cntvct_el0");
    publish(0xa0);
    volatile uint32_t *pool = (volatile uint32_t *)lo;
    for (unsigned i = 0; i < A52Q_UFS_POOL_BYTES / 4; i++)
        pool[i] = 0xa52c0000U ^ i;
    __asm__ volatile("dsb sy" ::: "memory");
    for (unsigned i = 0; i < A52Q_UFS_POOL_BYTES / 4; i++)
        if (pool[i] != (0xa52c0000U ^ i)) { publish(0xd1); return; }
    for (unsigned i = 0; i < A52Q_UFS_POOL_BYTES / 4; i++)
        pool[i] = 0;
    uint64_t command = lo + 4096;
    ufs_nop_descriptor(pool, command);
    __asm__ volatile("dsb sy" ::: "memory");
    uint32_t old_lo = ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L);
    uint32_t old_hi = ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 0);
    if (!ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 0)) {
        publish(0xd2); return;
    }
    publish(0xa1);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L, (uint32_t)lo);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H, (uint32_t)(lo >> 32));
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1);
    if (ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L) != (uint32_t)lo ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H) != (uint32_t)(lo >> 32) ||
        !ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 1)) {
        publish(0xd3); return;
    }
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL, 1);
    publish(0xa2);
    if (!ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL, 1, 0)) {
        /* No base restoration under an in-flight request; keep its RAM intact
         * until the required physical reset. Never retry/reset/init here. */
        ufs_nop_doorbell = ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL);
        publish(0xd4); return;
    }
    __asm__ volatile("dsb sy" ::: "memory");
    ufs_nop_ocs = pool[2] & 15;
    volatile const uint8_t *response = (volatile const uint8_t *)(command + 1024);
    ufs_nop_response = ((uint32_t)response[0] << 24) | ((uint32_t)response[1] << 16) |
        ((uint32_t)response[2] << 8) | response[3];
    unsigned valid = response[0] == 0x20;
    for (unsigned i = 1; i < 12; i++) valid &= response[i] == 0;
    /* An idle completed request permits restoration of the original BASE/RSR,
     * without reading or reusing any bootloader descriptor contents. */
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 0);
    if (!ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 0)) {
        publish(0xd2); return;
    }
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L, old_lo);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H, old_hi);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1);
    if (ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L) != old_lo ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H) != old_hi ||
        !ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 1)) {
        publish(0xd7); return;
    }
    publish(ufs_nop_ocs ? 0xd5 : !valid ? 0xd6 : 0xa4);
}
