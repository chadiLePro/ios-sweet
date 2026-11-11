/* A52-only embedded payload loader. No MMIO or storage. MMU and D-cache off.
 * Uses the existing SWEETXNU container ABI, with independent bounds checks.
 * Allowed RAM is generated from host evidence, never inherited from Redmi.
 */
#include <stdint.h>
#include "payload-config.h"
#include "ramoops-config.h"

#define PAGE 0x4000ULL
#define LINE 608
struct segment { uint64_t va, size, off, bytes; };
struct payload {
    char magic[8];
    uint32_t version, count;
    uint64_t virt, entry, adt_off, adt_size, kernel_end, phys, mem;
    char cmdline[LINE];
    struct segment segments[];
};
struct video { uint64_t base, display, stride, width, height, depth; };
struct boot_args {
    uint16_t revision, version;
    uint64_t virt, phys, mem, top;
    struct video video;
    uint32_t machine;
    uint64_t adt;
    uint32_t adt_size;
    char cmdline[LINE];
    uint64_t flags, actual_mem;
};
_Static_assert(__builtin_offsetof(struct payload, segments) == 0x2a8, "payload ABI");
_Static_assert(__builtin_offsetof(struct boot_args, cmdline) == 108, "boot args ABI");
_Static_assert(sizeof(struct boot_args) == 736, "boot args size");
extern unsigned char _payload_start[], _payload_end[], _head[], _end[];
extern void a52q_loader_stage(uint64_t stage);

static int span(uint64_t start, uint64_t length, uint64_t lo, uint64_t hi)
{
    return start >= lo && start <= hi && length <= hi - start;
}

static void copy(uintptr_t dst, uintptr_t src, uint64_t n)
{
    while (n >= 8 && !((dst | src) & 7)) {
        *(volatile uint64_t *)dst = *(volatile const uint64_t *)src;
        dst += 8; src += 8; n -= 8;
    }
    while (n--) *(volatile uint8_t *)dst++ = *(volatile const uint8_t *)src++;
}

static void zero(uintptr_t dst, uint64_t n)
{
    while (n && (dst & 7)) { *(volatile uint8_t *)dst++ = 0; n--; }
    while (n >= 8) { *(volatile uint64_t *)dst = 0; dst += 8; n -= 8; }
    while (n--) *(volatile uint8_t *)dst++ = 0;
}

int a52q_load_embedded(void)
{
    uint64_t el, sctlr;
    __asm__ volatile("mrs %0, CurrentEL" : "=r"(el));
    if (el != 4) return 1; /* No EL2 transition assumptions on Samsung. */
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(sctlr));
    if (sctlr & 5) return 2;
    const struct payload *p = (const struct payload *)_payload_start;
    uint64_t total = (uintptr_t)_payload_end - (uintptr_t)_payload_start;
    if (total < sizeof(*p)) return 3;
    const char magic[8] = "SWEETXNU";
    for (int i = 0; i < 8; i++) if (p->magic[i] != magic[i]) return 3;
    if (p->version != 1 || !p->count || p->count > 64 ||
        sizeof(*p) + p->count * sizeof(struct segment) > total ||
        p->phys != A52Q_PAYLOAD_BASE || p->mem != A52Q_PAYLOAD_SIZE ||
        (p->phys & 0x1ffffff) || (p->mem & (PAGE - 1)) ||
        !span(p->phys, p->mem, A52Q_PAYLOAD_BASE, A52Q_PAYLOAD_END) ||
        !span(p->adt_off, p->adt_size, 0, total) || !p->adt_size ||
        p->adt_size > 0x100000 || p->kernel_end < p->virt ||
        !span(p->kernel_end - p->virt, 0, 0, p->mem) ||
        p->cmdline[LINE - 1] != 0) return 4;
    uint64_t end = p->phys + p->mem;
    if ((p->phys < (uintptr_t)_end && (uintptr_t)_head < end) ||
        (p->phys < A52Q_RAMOOPS_BASE + A52Q_RAMOOPS_SIZE && A52Q_RAMOOPS_BASE < end)) return 5;
    int entry_ok = 0;
    uint64_t last = 0;
    for (unsigned i = 0; i < p->count; i++) {
        const struct segment *s = &p->segments[i];
        if (s->va < p->virt || (s->va & (PAGE - 1)) || s->bytes > s->size ||
            !span(s->off, s->bytes, sizeof(*p) + p->count * sizeof(*s), total) ||
            !span(s->va - p->virt, s->size, 0, p->mem) ||
            s->va < last || s->va > p->kernel_end || s->size > p->kernel_end - s->va)
            return 6;
        last = s->va + s->size;
        if (p->entry >= s->va && p->entry - s->va < s->bytes) entry_ok = 1;
    }
    uint64_t adt = p->phys + (p->kernel_end - p->virt);
    if (!entry_ok || p->adt_size > end - adt || adt + p->adt_size > end - PAGE * 2)
        return 7;
    uint64_t ba_pa = (adt + p->adt_size + PAGE - 1) & ~(PAGE - 1);
    if (!span(ba_pa, PAGE, p->phys, end)) return 7;
    a52q_loader_stage(3); /* All container and destination bounds checked. */
    volatile uint64_t *probe = (volatile uint64_t *)(uintptr_t)p->phys;
    uint64_t saved = *probe;
    *probe = 0xa52a52a52a52a52aULL;
    __asm__ volatile("dsb sy" ::: "memory");
    uint64_t observed = *probe;
    *probe = saved;
    __asm__ volatile("dsb sy" ::: "memory");
    if (observed != 0xa52a52a52a52a52aULL) return 8;
    a52q_loader_stage(4); /* Bounded first-word probe, not whole-range proof. */
    for (unsigned i = 0; i < p->count; i++) {
        const struct segment *s = &p->segments[i];
        uintptr_t dst = p->phys + s->va - p->virt;
        copy(dst, (uintptr_t)_payload_start + s->off, s->bytes);
        zero(dst + s->bytes, s->size - s->bytes);
    }
    a52q_loader_stage(5);
    copy(adt, (uintptr_t)_payload_start + p->adt_off, p->adt_size);
    zero(ba_pa, PAGE);
    volatile struct boot_args *ba = (volatile struct boot_args *)(uintptr_t)ba_pa;
    ba->revision = ba->version = 2;
    ba->virt = p->virt; ba->phys = p->phys; ba->mem = p->mem;
    ba->top = ba_pa + PAGE;
    /* No framebuffer descriptor: command-mode scanout is not established. */
    ba->adt = adt - p->phys + p->virt;
    ba->adt_size = (uint32_t)p->adt_size;
    for (unsigned i = 0; i < LINE; i++) ba->cmdline[i] = p->cmdline[i];
    ba->actual_mem = p->mem;
    a52q_loader_stage(6);
    __asm__ volatile("dsb sy; ic iallu; dsb sy; isb" ::: "memory");
    ((void (*)(uint64_t))(uintptr_t)(p->phys + p->entry - p->virt))(ba_pa);
    return 9;
}
