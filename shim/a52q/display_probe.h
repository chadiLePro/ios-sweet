/* Included only by the explicit evidence-bound display experiment. */
#include "display-config.h"
static void display_probe(void)
{
    for (unsigned i = 0; i < sizeof(display_guard_indices) / sizeof(display_guard_indices[0]); i++) {
        unsigned index = display_guard_indices[i];
        if (index >= handoff_done || handoff_values[index] != display_guard_values[i]) {
            publish(0xea); /* Handoff changed: no display writes. */
            return;
        }
    }
    publish(0x90);
    /* MMU and data cache were checked disabled before the MMIO snapshot. */
    for (unsigned y = 0; y < 96; y++) {
        volatile uint32_t *row = (volatile uint32_t *)(A52Q_DISPLAY_BASE + y * A52Q_DISPLAY_STRIDE);
        for (unsigned x = 0; x < 160; x++) {
            uint32_t color = x < 53 ? 0xffff0000U : x < 106 ? 0xff00ff00U : 0xff0000ffU;
            if (!x || x == 159 || !y || y == 95)
                color = 0xffffffffU;
            row[x] = color;
        }
    }
    __asm__ volatile("dsb sy" ::: "memory");
    publish(0x91);
    *(volatile uint32_t *)A52Q_DISPLAY_START_REGISTER = 1;
    __asm__ volatile("dsb sy" ::: "memory");
    publish(0x92);
    uint64_t begin = READ_REG("cntpct_el0"), freq = READ_REG("cntfrq_el0");
    if (!freq) {
        publish(0xeb);
        return;
    }
    while (*(volatile const uint32_t *)A52Q_DISPLAY_START_REGISTER & 1) {
        if (READ_REG("cntpct_el0") - begin > freq / 10) {
            publish(0xe9); /* Bounded 100ms wait; no further writes/retries. */
            return;
        }
    }
    publish(0x93); /* Start consumed; visible output still needs observation. */
}
