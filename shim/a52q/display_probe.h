/* Included only by the explicit evidence-bound display experiment. */
#include "display-config.h"
#include "display_pattern.h"
static void display_probe(void)
{
    for (unsigned i = 0; i < sizeof(display_guard_indices) / sizeof(display_guard_indices[0]); i++) {
        unsigned index = display_guard_indices[i];
        if (index >= handoff_done || handoff_values[index] != display_guard_values[i]) {
            publish(0xea); /* Handoff changed: no display writes. */
            return;
        }
    }
    uint64_t freq = READ_REG("cntfrq_el0");
    if (freq < 10) {
        publish(0xeb); /* Need a timebase before any pixel or MMIO write. */
        return;
    }
    publish(0x90);
    /* MMU and data cache were checked disabled before the MMIO snapshot.
     * Full captured surface: unmistakable even when the boot logo stays up. */
    if (!a52q_display_pattern((volatile uint32_t *)A52Q_DISPLAY_BASE,
            A52Q_DISPLAY_WIDTH, A52Q_DISPLAY_HEIGHT, A52Q_DISPLAY_STRIDE,
            A52Q_DISPLAY_BUFFER_BYTES)) {
        publish(0xec);
        return;
    }
    __asm__ volatile("dsb sy" ::: "memory");
    publish(0x91);
    uint64_t begin = READ_REG("cntvct_el0");
    *(volatile uint32_t *)A52Q_DISPLAY_START_REGISTER = 1;
    __asm__ volatile("dsb sy" ::: "memory");
    publish(0x92);
    while (*(volatile const uint32_t *)A52Q_DISPLAY_START_REGISTER & 1) {
        /* The virtual counter is already used by the verified A52 UFS probe.
         * Access to the physical counter depends on separate EL2 permissions. */
        if (READ_REG("cntvct_el0") - begin >= freq / 10) {
            publish(0xe9); /* Bounded 100ms wait; no further writes/retries. */
            return;
        }
    }
    publish(0x93); /* Start consumed; visible output still needs observation. */
}
