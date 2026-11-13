/* Opt-in mapping/refresh diagnostic. No panel, clock, reset or DSI commands.
 * Absence of /a52q-display-selftest means no MMIO reads or framebuffer writes.
 * This is not the IOMobileFramebuffer ABI or a claim of periodic VSync.
 */
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <sys/param.h>
#include <sys/systm.h>
#include <kern/clock.h>
#include <mach/mach_time.h>
#include <machine/machine_routines.h>
#include <vm/pmap.h>
#include <pexpert/device_tree.h>
#include <libkern/libkern.h>
#include "a52q_display_pattern.h"

extern vm_offset_t ml_io_map(vm_offset_t phys_addr, vm_size_t size);

struct a52d_guard { uint64_t address; uint32_t value, reserved; };
_Static_assert(sizeof(struct a52d_guard) == 16, "display ADT guard ABI");

static int a52d_property(DTEntry node, const char *name, void *out, unsigned length)
{
    const void *bytes;
    unsigned size;
    if (SecureDTGetProperty(node, name, &bytes, &size) != kSuccess || size != length) return 0;
    memcpy(out, bytes, length);
    return 1;
}

static void a52d_report(uint64_t nonce, unsigned phase, unsigned detail)
{
    char body[48];
    int length = snprintf(body, sizeof(body), "%016llx/%02x/%08x", nonce, phase, detail);
    if (length <= 0 || (unsigned)length >= sizeof(body)) return;
    uint32_t crc = 0xffffffffU;
    for (int i = 0; i < length; i++) {
        crc ^= (uint8_t)body[i];
        for (unsigned bit = 0; bit < 8; bit++) crc = (crc >> 1) ^ (0xedb88320U & (0U - (crc & 1)));
    }
    for (unsigned i = 0; i < 5; i++) printf("A52D1 %s %08x\n", body, crc ^ 0xffffffffU);
}

void a52q_display_selftest(void);
void a52q_display_selftest(void)
{
    DTEntry node, chosen;
    if (SecureDTLookupEntry(NULL, "/a52q-display-selftest", &node) != kSuccess) return;
    uint64_t nonce = 0, reg[2], start, ram_base, ram_size;
    uint32_t geometry[3];
    struct a52d_guard guards[13];
    if (!a52d_property(node, "nonce", &nonce, sizeof(nonce)) || !nonce) return;
    if (!a52d_property(node, "reg", reg, sizeof(reg)) ||
        !a52d_property(node, "geometry", geometry, sizeof(geometry)) ||
        !a52d_property(node, "start-register", &start, sizeof(start)) ||
        !a52d_property(node, "guards", guards, sizeof(guards)) ||
        SecureDTLookupEntry(NULL, "/chosen", &chosen) != kSuccess ||
        !a52d_property(chosen, "dram-base", &ram_base, sizeof(ram_base)) ||
        !a52d_property(chosen, "dram-size", &ram_size, sizeof(ram_size)) ||
        reg[0] & PAGE_MASK || reg[1] & PAGE_MASK || !reg[1] || reg[1] > (64U << 20) ||
        reg[0] < 0x80000000ULL || reg[0] > 0x100000000ULL - reg[1] ||
        geometry[0] < 3 || geometry[0] > 4096 || geometry[1] < 2 || geometry[1] > 4096 ||
        geometry[2] != (uint64_t)geometry[0] * 4 || (uint64_t)geometry[2] * geometry[1] > reg[1] ||
        ram_base + ram_size < ram_base ||
        (reg[0] < ram_base + ram_size && ram_base < reg[0] + reg[1])) {
        a52d_report(nonce, 0xe0, 0); return;
    }
    unsigned start_index = 13;
    for (unsigned i = 0; i < 13; i++) {
        if (!guards[i].address || guards[i].address >= 0x80000000ULL ||
            guards[i].address & 3 || guards[i].reserved) {
            a52d_report(nonce, 0xe0, i + 1); return;
        }
        for (unsigned j = 0; j < i; j++) if (guards[i].address == guards[j].address) {
            a52d_report(nonce, 0xe0, i + 1); return;
        }
        if (guards[i].address == start && guards[i].value == 0) start_index = i;
    }
    if (start_index == 13) { a52d_report(nonce, 0xe0, 14); return; }
    printf("A52Q display selftest: guarded kernel mapping\n");
    volatile uint32_t *registers[13];
    for (unsigned i = 0; i < 13; i++) {
        /* ml_io_map uses VM_WIMG_IO. Do not create a cached RAM alias. */
        registers[i] = (volatile uint32_t *)ml_io_map((vm_offset_t)guards[i].address, 4);
        if (!registers[i]) { a52d_report(nonce, 0xe1, i); return; }
        if (*registers[i] != guards[i].value) { a52d_report(nonce, 0xe2, i); return; }
    }
    /* io_map's permanent submap is only 8 MiB in this XNU. The DT splash
     * reservation is larger; allocate its VA in kernel_map with the existing
     * unmappable API, retaining VM_WIMG_IO and the same physical bounds.
     * Keep this mapping for the boot lifetime; no cached aliases are created. */
    volatile uint32_t *pixels = (volatile uint32_t *)ml_io_map_unmappable(
        (vm_offset_t)reg[0], (vm_size_t)reg[1], VM_WIMG_IO);
    if (!pixels) { a52d_report(nonce, 0xe1, 13); return; }
    a52d_report(nonce, 0x10, 0);
    if (!a52q_display_pattern(pixels, geometry[0], geometry[1], geometry[2], reg[1])) {
        a52d_report(nonce, 0xe3, 0); return;
    }
    __asm__ volatile("dsb sy" ::: "memory");
    a52d_report(nonce, 0x20, 0);
    uint64_t deadline;
    nanoseconds_to_deadline(100 * NSEC_PER_MSEC, &deadline);
    *registers[start_index] = 1;
    __asm__ volatile("dsb sy" ::: "memory");
    while (*registers[start_index] & 1) {
        if (mach_absolute_time() >= deadline) { a52d_report(nonce, 0xe4, 0); return; }
    }
    a52d_report(nonce, 0x30, 0);
}
#endif
