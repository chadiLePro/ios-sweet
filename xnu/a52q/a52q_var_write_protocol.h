/* Opt-in development /var only. Never an arbitrary SCSI command interface.
 * UFS DD/UPIU flags follow Linux v6.1 include/ufs/{ufshci,ufs}.h;
 * WRITE(10)/SYNCHRONIZE CACHE(10) layout follows drivers/scsi/sd.c.
 * Caller zeros the descriptor/request area before either builder.
 */
#ifndef A52Q_VAR_WRITE_PROTOCOL_H
#define A52Q_VAR_WRITE_PROTOCOL_H
#include <stdint.h>
static inline int a52q_var_write_lba(const uint64_t root[4], const uint64_t var[4],
    uint32_t last, uint64_t offset, uint64_t bytes, uint32_t *lba)
{
    if (!a52q_var_window_valid(root,var) || !lba || !bytes || bytes>4096 ||
        offset%4096 || bytes!=4096 ||
        !a52q_ufs_window_range(var[3],offset,bytes) ||
        var[2]>(uint64_t)last || var[3]>(uint64_t)last+1-var[2]) return 0;
    uint64_t block=var[2]+offset/4096;
    if (block>UINT32_MAX) return 0;
    *lba=(uint32_t)block;return 1;
}
static inline void a52q_var_write_packet(volatile uint32_t *list,
    volatile uint8_t *request, volatile uint32_t *prdt,
    uint64_t command, uint64_t data, uint32_t lba)
{
    ufs_nop_descriptor(list,command);
    list[0]|=0x02000000U; /* HOST_TO_DEVICE. */
    list[7]|=1U;
    prdt[0]=(uint32_t)data;prdt[1]=(uint32_t)(data>>32);
    prdt[2]=0;prdt[3]=4095;
    request[0]=1;request[1]=0x20; /* SCSI COMMAND, UPIU WRITE, LUN0/tag0. */
    request[14]=0x10; /* expected data length 4096, big endian. */
    request[16]=0x2a;
    request[18]=(uint8_t)(lba>>24);request[19]=(uint8_t)(lba>>16);
    request[20]=(uint8_t)(lba>>8);request[21]=(uint8_t)lba;
    request[24]=1; /* Exactly one 4096-byte logical block. */
}
static inline void a52q_var_sync_packet(volatile uint32_t *list,
    volatile uint8_t *request, uint64_t command)
{
    ufs_nop_descriptor(list,command); /* No data direction or PRDT. */
    request[0]=1;request[16]=0x35; /* SYNCHRONIZE CACHE(10), whole LUN. */
}
#endif
