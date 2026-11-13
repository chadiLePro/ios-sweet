/* CPU-only BGRA diagnostic. No MMIO, allocation, panel modes or clocks. */
#ifndef A52Q_DISPLAY_PATTERN_H
#define A52Q_DISPLAY_PATTERN_H
#include <stdint.h>

static inline int a52q_display_pattern(volatile uint32_t *pixels, uint32_t width,
    uint32_t height, uint32_t stride, uint64_t available)
{
    if (!pixels || width < 3 || height < 2 || width > 4096 || height > 4096 ||
        stride % 4 || (uint64_t)width * 4 > stride ||
        (uint64_t)(height - 1) * stride + (uint64_t)width * 4 > available)
        return 0;
    unsigned border = width / 64;
    if (!border) border = 1;
    for (unsigned y = 0; y < height; y++) {
        volatile uint32_t *row = pixels + (uint64_t)y * (stride / 4);
        for (unsigned x = 0; x < width; x++) {
            unsigned band = (uint64_t)x * 3 / width;
            uint32_t color = band == 0 ? 0xffff0000U : band == 1 ? 0xff00ff00U : 0xff0000ffU;
            if (x < border || width - x <= border || y < border || height - y <= border)
                color = 0xffffffffU;
            row[x] = color;
        }
    }
    return 1;
}
#endif
