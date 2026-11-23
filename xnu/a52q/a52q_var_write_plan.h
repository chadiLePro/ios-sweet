/* Shared kernel/native-test byte writer; callbacks operate on ONE 4KiB block.
 * Whole-request range validation precedes every callback. Partial writes retain
 * surrounding bytes through read/modify/write under the caller's disk lock.
 */
#ifndef A52Q_VAR_WRITE_PLAN_H
#define A52Q_VAR_WRITE_PLAN_H
#include <stdint.h>
/* Caller supplies memcpy (libkern in XNU, string.h in native tests). */
typedef int (*a52q_var_read_fn)(void *,uint32_t,uint8_t *);
typedef int (*a52q_var_write_fn)(void *,uint32_t,const uint8_t *);
static inline int a52q_var_write_bytes(const uint64_t root[4],const uint64_t var[4],
    uint32_t last,uint64_t offset,const uint8_t *source,uint32_t bytes,
    uint8_t *bounce,a52q_var_read_fn read_block,a52q_var_write_fn write_block,
    void *context,uint32_t *completed,int invalid)
{
    if (!completed) return invalid;
    *completed=0;
    if (!a52q_var_window_valid(root,var) ||
        !a52q_ufs_window_range(var[3],offset,bytes) ||
        (!source && bytes) || !bounce || !read_block || !write_block) return invalid;
    while (*completed<bytes) {
        uint64_t position=offset+*completed,base=position&~4095ULL;
        uint32_t lba,within=(uint32_t)(position-base);
        uint32_t count=a52q_ufs_chunk(position,bytes-*completed);
        if (!a52q_var_write_lba(root,var,last,base,4096,&lba)) return invalid;
        int error;
        if (within || count!=4096) {
            error=read_block(context,lba,bounce);
            if (error) return error;
        }
        memcpy(bounce+within,source+*completed,count);
        error=write_block(context,lba,bounce);
        if (error) return error;
        *completed+=count;
    }
    return 0;
}
#endif
