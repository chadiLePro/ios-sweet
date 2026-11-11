/* Early single-core XNU RAM console. The physical backing is reserved ramoops.
 * Exact 16 KiB pages are mapped Device-nGnRnE; surrounding carveouts stay absent.
 * Before final TTBR0 removal arm_vm_init reuses this L3 at a reserved kernel VA.
 * No framebuffer, UART, UFS or persistent storage is accessed.
 */
#include <arm64/sweet_early.h>
#include <kern/misc_protos.h>
#include <stdint.h>

#if defined(A52Q)
uint64_t a52q_console_l3[2048] __attribute__((aligned(16384)));
static volatile uint8_t *console = (volatile uint8_t *)(uintptr_t)A52Q_RAMLOG_BASE;
static int busy, panicking;
static uint32_t position;

static void byte(char c)
{
    /* A bounded nonwrapping Linux persistent_ram_buffer; preserve old bytes
     * only until first output, then publish each appended byte in order. */
    volatile uint32_t *h = (volatile uint32_t *)console;
    if (!position) {
        /* Preserve the CRC-protected assembly entry copies when C starts.
         * Only accept a bounded nonwrapping header, never arbitrary offsets. */
        if (h[0] == 0x43474244 && h[1] == h[2] && h[2] > 0 && h[2] <= 4096) {
            position = h[2];
        } else {
            h[0] = 0;
            h[1] = h[2] = 0;
        }
    }
    if (position >= A52Q_RAMLOG_SIZE - 12)
        return;
    console[12 + position++] = (uint8_t)c;
    __asm__ volatile("dsb sy" ::: "memory");
    h[1] = h[2] = position;
    __asm__ volatile("dsb sy" ::: "memory");
    h[0] = 0x43474244;
    __asm__ volatile("dsb sy" ::: "memory");
}

void sweet_early_putc(char c)
{
    if (busy)
        return;
    busy = 1;
    byte(c);
    busy = 0;
}

static void string(const char *s)
{
    while (*s)
        sweet_early_putc(*s++);
}

static void hex(uint64_t value)
{
    static const char digits[] = "0123456789abcdef";
    for (int shift = 60; shift >= 0; shift -= 4)
        sweet_early_putc(digits[(value >> shift) & 15]);
}

void sweet_early_mark(unsigned int stage, const char *label)
{
    /* Triplicate milestone lines. Stream text is observational and is not
     * accepted by the r4 checksummed-register decoder. Keep this distinction. */
    for (unsigned copy = 0; copy < 3; copy++) {
        string("\nA52QXNU stage=0x");
        hex(stage);
        string(" sctlr=0x");
        hex(__builtin_arm_rsr64("SCTLR_EL1"));
        string(" ");
        string(label);
        string("\n");
    }
}

void sweet_early_panic(const char *fmt, va_list *args)
{
    if (panicking)
        return;
    panicking = 1;
    string("\nA52QXNU PANIC: ");
    va_list copy;
    va_copy(copy, *args);
    _doprnt(fmt, &copy, sweet_early_putc, 16);
    va_end(copy);
    string("\n");
}

void sweet_early_relocate(uint64_t base)
{
    console = (volatile uint8_t *)(uintptr_t)base;
    __asm__ volatile("dsb sy" ::: "memory");
    sweet_early_mark(9, "kernel RAM-console VA live");
}

void sweet_early_disable(void) {}
#endif
