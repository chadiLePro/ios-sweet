#ifndef A52Q_VAR_BOUNDS_H
#define A52Q_VAR_BOUNDS_H
#include <stdint.h>
static inline int a52q_var_window_valid(const uint64_t root[4],const uint64_t data[4])
{
    if (!root || !data || root[0]<2 || root[0]>UINT32_MAX || root[1]>UINT32_MAX ||
        root[0]>UINT32_MAX-root[1] || root[2]!=root[0] || root[3]!=(16ULL<<30)/4096 ||
        data[0]!=root[0] || data[1]!=root[1] || data[2]!=root[0]+root[3] ||
        data[3]!=(4ULL<<30)/4096 || root[1]<root[3]+data[3]) return 0;
    return 1;
}
#endif
