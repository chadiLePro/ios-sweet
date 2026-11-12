#include <assert.h>
#include <stdint.h>
#include <string.h>
#include "../shim/a52q/ufs_nop_protocol.h"
#include "../shim/a52q/ufs_read_protocol.h"
int main(void)
{
    uint32_t list[8] = {0}, prdt[4] = {0};
    uint8_t request[1024] = {0};
    assert(!ufs_read_packet(list, request, prdt, 0, 0, 0x2a, 1, 4096)); /* WRITE rejected. */
    assert(!ufs_read_packet(list, request, prdt, 0, 0, 0x25, 1, 8));
    assert(!ufs_read_packet(list, request, prdt, 0, 0, 0x28, 1, 8192));
    assert(ufs_read_packet(list, request, prdt, 0x106001000ULL, 0x106002000ULL, 0x25, 0, 8));
    assert(list[0] == 0x15000000U && (list[7] & 0xffff) == 1);
    assert(prdt[0] == 0x06002000 && prdt[1] == 1 && prdt[2] == 0 && prdt[3] == 7);
    assert(request[0] == 1 && request[1] == 0x40 && request[2] == 0 && request[3] == 0);
    assert(ufs_be32(request + 12) == 8 && request[16] == 0x25);
    memset(request, 0, sizeof(request));
    assert(ufs_read_packet(list, request, prdt, 0x106001000ULL, 0x106002000ULL, 0x28, 0x12345678, 4096));
    assert(ufs_be32(request + 12) == 4096 && ufs_be32(request + 18) == 0x12345678);
    assert(request[23] == 0 && request[24] == 1 && prdt[3] == 4095);
    assert(ufs_data_crc32((const uint8_t *)"123456789", 9) == 0xcbf43926U);
    return 0;
}
