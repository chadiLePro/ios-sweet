#include <assert.h>
#include <stdint.h>
#include <string.h>
#include "../shim/a52q/ufs_nop_protocol.h"
int main(void)
{
    uint32_t list[256];
    memset(list, 0, sizeof(list));
    ufs_nop_descriptor(list, 0x106001000ULL);
    assert(list[0] == 0x11000000U); /* native UFS type, NO DATA direction */
    assert(list[1] == 0 && list[2] == 15 && list[3] == 0);
    assert(list[4] == 0x06001000U && list[5] == 1); /* Preserve >4GiB address. */
    assert((list[6] & 0xffff) * 4 == 1024);
    assert((list[6] >> 16) * 4 == 1024);
    assert((list[7] & 0xffff) == 0); /* No PRDT/data transfer. */
    assert((list[7] >> 16) * 4 == 2048);
    for (unsigned i = 8; i < 256; i++) assert(list[i] == 0);
    return 0;
}
