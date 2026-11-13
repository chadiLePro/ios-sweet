#include <assert.h>
#include <stdint.h>
#include <string.h>
#include "../shim/a52q/display_pattern.h"

int main(void)
{
    enum { W = 96, H = 64, ROW = 100 };
    uint32_t buffer[ROW * H + 2], before[ROW * H + 2];
    for (unsigned i = 0; i < ROW * H + 2; i++) buffer[i] = 0xdeadbeef;
    memcpy(before, buffer, sizeof(buffer));
    uint64_t needed = ((H - 1) * ROW + W) * 4;
    assert(!a52q_display_pattern(buffer + 1, W, H, ROW * 4, needed - 1));
    assert(!a52q_display_pattern(buffer + 1, W, H, (W - 1) * 4, sizeof(buffer)));
    assert(!a52q_display_pattern(buffer + 1, W, H, ROW * 4 + 1, sizeof(buffer)));
    assert(!a52q_display_pattern(buffer + 1, UINT32_MAX, H, ROW * 4, UINT64_MAX));
    assert(!a52q_display_pattern(buffer + 1, W, 0, ROW * 4, sizeof(buffer)));
    assert(!a52q_display_pattern(0, W, H, ROW * 4, needed));
    assert(memcmp(buffer, before, sizeof(buffer)) == 0);
    assert(a52q_display_pattern(buffer + 1, W, H, ROW * 4, needed));
    assert(buffer[0] == 0xdeadbeef && buffer[ROW * H + 1] == 0xdeadbeef);
    for (unsigned y = 0; y < H; y++) {
        for (unsigned x = W; x < ROW; x++) assert(buffer[1 + y * ROW + x] == 0xdeadbeef);
        assert(buffer[1 + y * ROW] == 0xffffffffU);
        assert(buffer[y * ROW + W] == 0xffffffffU);
    }
    assert(buffer[1 + 32 * ROW + 10] == 0xffff0000U);
    assert(buffer[1 + 32 * ROW + 48] == 0xff00ff00U);
    assert(buffer[1 + 32 * ROW + 80] == 0xff0000ffU);
    return 0;
}
