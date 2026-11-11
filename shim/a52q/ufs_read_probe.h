#include "ufs-read-config.h"
#include "ufs_read_protocol.h"

static int ufs_read_submit(unsigned opcode, uint32_t lba, unsigned bytes)
{
    if (ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL) ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP) != 1 ||
        ufs_read(UFS_INDEX_CONTROLLER_ENABLE) != 1 ||
        (ufs_read(UFS_INDEX_CONTROLLER_STATUS) & 15) != 15)
        return 1;
    volatile uint32_t *pool = (volatile uint32_t *)A52Q_UFS_POOL;
    for (unsigned i = 0; i < A52Q_UFS_POOL_BYTES / 4; i++) pool[i] = 0;
    for (unsigned i = 8192 / 4; i < (8192 + 4096) / 4; i++) pool[i] = 0xa5a5a5a5U;
    uint64_t command = A52Q_UFS_POOL + 4096;
    if (!ufs_read_packet(pool, (volatile uint8_t *)command,
            (volatile uint32_t *)(command + 2048), command, A52Q_UFS_POOL + 8192,
            opcode, lba, bytes))
        return 2;
    __asm__ volatile("dsb sy" ::: "memory");
    uint32_t old_lo = ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L);
    uint32_t old_hi = ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 0);
    if (!ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 0)) return 3;
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L, (uint32_t)A52Q_UFS_POOL);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H, (uint32_t)(A52Q_UFS_POOL >> 32));
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1);
    if (ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L) != (uint32_t)A52Q_UFS_POOL ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H) != (uint32_t)(A52Q_UFS_POOL >> 32) ||
        !ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 1)) return 4;
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL, 1);
    if (!ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_DOOR_BELL, 1, 0)) return 5;
    __asm__ volatile("dsb sy" ::: "memory");
    volatile const uint8_t *rsp = (volatile const uint8_t *)(command + 1024);
    ufs_read_ocs = pool[2] & 15;
    ufs_read_response = ufs_be32(rsp);
    int valid = (rsp[0] & 0x3f) == 0x21 && rsp[3] == 0 && rsp[6] == 0 && rsp[7] == 0;
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 0);
    if (!ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 0)) return 6;
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L, old_lo);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H, old_hi);
    ufs_write(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1);
    if (ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_L) != old_lo ||
        ufs_read(UFS_INDEX_UTP_TRANSFER_REQ_LIST_BASE_H) != old_hi ||
        !ufs_wait(UFS_INDEX_UTP_TRANSFER_REQ_LIST_RUN_STOP, 1, 1)) return 7;
    return ufs_read_ocs ? 8 : !valid ? 9 : 0;
}
static void ufs_read_probe(void)
{
    /* Only continue after this boot's own fresh NOP success and list restore. */
    if (a52q_diagnostic.stage != 0xa4) return;
    publish(0xb0);
    ufs_read_failure = ufs_read_submit(0x25, 0, 8);
    if (ufs_read_failure) { publish(0xf1); return; }
    volatile const uint8_t *data = (volatile const uint8_t *)(A52Q_UFS_POOL + 8192);
    ufs_capacity_last = ufs_be32(data);
    ufs_capacity_block = ufs_be32(data + 4);
    if (ufs_capacity_last != A52Q_UFS_EXPECTED_LAST_LBA ||
        ufs_capacity_block != A52Q_UFS_EXPECTED_BLOCK_SIZE) {
        publish(0xf2); return;
    }
    publish(0xb1);
    ufs_read_failure = ufs_read_submit(0x28, A52Q_UFS_READ_LBA, 4096);
    if (ufs_read_failure) { publish(0xf3); return; }
    ufs_read_crc = ufs_data_crc32(data, 4096);
    publish(ufs_read_crc == A52Q_UFS_EXPECTED_READ_CRC32 ? 0xb3 : 0xf4);
}
