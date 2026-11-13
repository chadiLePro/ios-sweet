#include <assert.h>
#include <stdint.h>
#include "../xnu/a52q/a52q_ufs_bounds.h"
int main(void)
{
    uint32_t last = 31077375;
    uint64_t total = ((uint64_t)last + 1) * 4096;
    assert(a52q_ufs_range(last, total, 0));
    assert(a52q_ufs_range(last, total - 4096, 4096));
    assert(!a52q_ufs_range(last, total - 512, 1024));
    assert(!a52q_ufs_range(last, total + 1, 0));
    assert(!a52q_ufs_range(last, UINT64_MAX - 511, 1024));
    assert(a52q_ufs_range(UINT32_MAX, (uint64_t)UINT32_MAX * 4096, 4096));
    /* Logical 512-byte requests can straddle physical blocks without reading
     * a following block beyond capacity or copying bytes outside the bounce. */
    uint64_t offset = 123888ULL * 4096 + 3584;
    uint32_t remaining = 8192;
    const uint32_t chunks[] = {512, 4096, 3584};
    for (unsigned i = 0; i < 3; i++) {
        uint32_t chunk = a52q_ufs_chunk(offset, remaining);
        assert(chunk == chunks[i]);
        assert(offset % 4096 + chunk <= 4096);
        offset += chunk; remaining -= chunk;
    }
    assert(remaining == 0);
    assert(a52q_ufs_boot_window(last, 99312, 24576, 115696, 8192));
    assert(!a52q_ufs_boot_window(last, 99312, 24576, 115695, 8192));
    assert(!a52q_ufs_boot_window(last, 99312, 24576, 123888, 8192));
    assert(!a52q_ufs_boot_window(last, 99312, 24576, 99312, 24576));
    assert(!a52q_ufs_boot_window(last, UINT64_MAX - 100, 24576, 0, 8192));
    assert(!a52q_ufs_boot_window(110000, 99312, 24576, 115696, 8192));
    assert(a52q_ufs_window_range(8192, (32U << 20) - 512, 512));
    assert(!a52q_ufs_window_range(8192, (32U << 20) - 512, 1024));
    assert(!a52q_ufs_window_range(UINT64_MAX, 0, 4096));
    uint8_t response[40] = {0x21};
    assert(a52q_ufs_response_ok(response, 1));
    const unsigned rejected_fields[] = {1, 2, 3, 6, 7, 10, 11, 12, 13, 14, 15, 32, 33};
    for (unsigned i = 0; i < sizeof(rejected_fields) / sizeof(rejected_fields[0]); i++) {
        response[rejected_fields[i]] = 1;
        assert(!a52q_ufs_response_ok(response, 1));
        response[rejected_fields[i]] = 0;
    }
    response[0] = 0x20;
    assert(a52q_ufs_response_ok(response, 0));
    assert(!a52q_ufs_response_ok(response, 1));
    return 0;
}
