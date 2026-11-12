/* Byte-range planning over the physically verified 4 KiB READ(10) command.
 * Independent of XNU so integer limits and partial-block cases are host tested.
 */
#ifndef A52Q_UFS_BOUNDS_H
#define A52Q_UFS_BOUNDS_H
#include <stdint.h>
static inline int a52q_ufs_range(uint32_t last_lba, uint64_t offset, uint64_t count)
{
    uint64_t bytes = ((uint64_t)last_lba + 1) * 4096;
    return offset <= bytes && count <= bytes - offset;
}
static inline uint32_t a52q_ufs_chunk(uint64_t offset, uint32_t remaining)
{
    uint32_t available = 4096 - (uint32_t)(offset % 4096);
    return remaining < available ? remaining : available;
}
/* Samsung utp_cmd_rsp: residual DW3, sense length at bytes32..33. A successful
 * status alone must not turn a short/overrun DMA transfer into a complete read.
 */
static inline int a52q_ufs_response_ok(volatile const uint8_t *r, int data)
{
    return r[0] == (data ? 0x21 : 0x20) && !r[1] && !r[2] && !r[3] &&
        !r[6] && !r[7] && !r[10] && !r[11] &&
        (!data || (!r[12] && !r[13] && !r[14] && !r[15] && !r[32] && !r[33]));
}
#endif
