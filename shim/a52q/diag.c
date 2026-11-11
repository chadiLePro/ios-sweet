/* A52 diagnostic core, with optional bounds-checked embedded XNU handoff.
 * No board MMIO by default; optional handoff mode reads an evidenced whitelist.
 * The explicit display experiment can write splash pixels and one CTL_START.
 * Other modes have no MMIO writes, SMC, DMA, reset or storage commands. Default records into its own
 * image. Optional evidence-derived ramoops output uses reserved RAM only.
 * The default diagnostic build does not include the loader or a kernel.
 */
#include <stdint.h>

#define READ_REG(name) ({ uint64_t v; __asm__ volatile("mrs %0, " name : "=r"(v)); v; })

struct diagnostic {
    uint64_t magic, version, stage;
    uint64_t image, image_end, dtb;
    uint64_t current_el, sctlr, mpidr, midr, mmfr0, pfr0, cntfrq;
    uint64_t ctr, isar0, isar1;
    uint64_t exception_slot, esr, elr, far;
};

/* Exported symbol for a debugger / a later verified output transport. */
volatile struct diagnostic a52q_diagnostic;
extern char _head[], _end[];

#ifdef A52Q_HANDOFF
#include "handoff-config.h"
static uint32_t handoff_values[A52Q_HANDOFF_COUNT];
static unsigned handoff_done;
static uint64_t handoff_active = UINT64_MAX;
#endif

#ifdef A52Q_RAMOOPS_CONFIG
#include "ramoops-config.h"
#include "ramlog.h"

static uint32_t log_crc;
static int checksum_enabled;

static void log_char(volatile struct ramlog *r, char c)
{
    ramlog_char(r, A52Q_RAMOOPS_SIZE, c);
    if (checksum_enabled) {
        log_crc ^= (uint8_t)c;
        for (int bit = 0; bit < 8; bit++)
            log_crc = (log_crc >> 1) ^ (0xedb88320U & (0U - (log_crc & 1)));
    }
}

static void log_string(volatile struct ramlog *r, const char *s)
{
    while (*s)
        log_char(r, *s++);
}

static void log_hex(volatile struct ramlog *r, const char *key, uint64_t value)
{
    static const char hex[] = "0123456789abcdef";
    log_string(r, key);
    log_string(r, "=0x");
    for (int shift = 60; shift >= 0; shift -= 4)
        log_char(r, hex[(value >> shift) & 15]);
    log_char(r, '\n');
}

#ifdef A52Q_HANDOFF
static void handoff_hex(volatile struct ramlog *r, uint64_t value, unsigned bits)
{
    static const char hex[] = "0123456789abcdef";
    for (int shift = (int)bits - 4; shift >= 0; shift -= 4)
        log_char(r, hex[(value >> shift) & 15]);
}

static void handoff_begin(volatile struct ramlog *r, const char *kind)
{
    checksum_enabled = 0;
    log_string(r, kind);
    log_crc = 0xffffffffU;
    checksum_enabled = 1;
}

static void handoff_end(volatile struct ramlog *r)
{
    uint32_t crc = log_crc ^ 0xffffffffU;
    checksum_enabled = 0;
    log_char(r, ' ');
    handoff_hex(r, crc, 32);
    log_char(r, '\n');
}

static void log_handoff(volatile struct ramlog *r)
{
    for (unsigned copy = 0; copy < 5; copy++) {
        handoff_begin(r, "A52S2 ");
        handoff_hex(r, A52Q_CAPTURE_ID, 64); log_char(r, '/');
        handoff_hex(r, a52q_diagnostic.stage, 32); log_char(r, '/');
        handoff_hex(r, a52q_diagnostic.esr, 64);
        handoff_end(r);
        handoff_begin(r, "A52M2 ");
        handoff_hex(r, A52Q_CAPTURE_ID, 64); log_char(r, '/');
        handoff_hex(r, A52Q_HANDOFF_TAG, 64); log_char(r, '/');
        handoff_hex(r, A52Q_HANDOFF_COUNT, 8); log_char(r, '/');
        handoff_hex(r, handoff_done, 8); log_char(r, '/');
        handoff_hex(r, handoff_active, 64);
        handoff_end(r);
        for (unsigned i = 0; i < handoff_done; i++) {
            handoff_begin(r, "A52R2 ");
            handoff_hex(r, A52Q_CAPTURE_ID, 64); log_char(r, '/');
            handoff_hex(r, i, 8); log_char(r, '/');
            handoff_hex(r, handoff_addresses[i], 32); log_char(r, '/');
            handoff_hex(r, handoff_values[i], 32);
            handoff_end(r);
        }
    }
}
#endif

static void log_snapshot(void)
{
    static int active;
    if (active)
        return; /* A fault in reserved RAM output must not recursively fault. */
    uintptr_t base = A52Q_RAMOOPS_BASE, end = base + A52Q_RAMOOPS_SIZE;
    /* Even an evidence-derived output must not collide with the loaded image
     * or the incoming DTB pointer. DTB is never dereferenced in this core. */
    if ((base < (uintptr_t)_end && (uintptr_t)_head < end) ||
        (base <= a52q_diagnostic.dtb && a52q_diagnostic.dtb < end))
        return;
    active = 1;
    volatile struct ramlog *r = (volatile struct ramlog *)base;
    ramlog_begin(r);
    __asm__ volatile("dsb sy" ::: "memory");
    for (unsigned copy = 0; copy < 3; copy++) {
        checksum_enabled = 0;
        log_string(r, "A52QDIAG v2 copy=");
        log_char(r, '0' + copy);
        log_char(r, '\n');
        log_crc = 0xffffffffU;
        checksum_enabled = 1;
        log_hex(r, "stage", a52q_diagnostic.stage);
        log_hex(r, "image", a52q_diagnostic.image);
        log_hex(r, "image_end", a52q_diagnostic.image_end);
        log_hex(r, "dtb", a52q_diagnostic.dtb);
        log_hex(r, "current_el", a52q_diagnostic.current_el);
        log_hex(r, "sctlr", a52q_diagnostic.sctlr);
        log_hex(r, "mpidr", a52q_diagnostic.mpidr);
        log_hex(r, "midr", a52q_diagnostic.midr);
        log_hex(r, "mmfr0", a52q_diagnostic.mmfr0);
        log_hex(r, "pfr0", a52q_diagnostic.pfr0);
        log_hex(r, "cntfrq", a52q_diagnostic.cntfrq);
        log_hex(r, "ctr", a52q_diagnostic.ctr);
        log_hex(r, "isar0", a52q_diagnostic.isar0);
        log_hex(r, "isar1", a52q_diagnostic.isar1);
        log_hex(r, "exception_slot", a52q_diagnostic.exception_slot);
        log_hex(r, "esr", a52q_diagnostic.esr);
        log_hex(r, "elr", a52q_diagnostic.elr);
        log_hex(r, "far", a52q_diagnostic.far);
        checksum_enabled = 0;
        log_hex(r, "crc32", log_crc ^ 0xffffffffU);
        log_string(r, "A52QDIAG END\n");
    }
#ifdef A52Q_HANDOFF
    log_handoff(r);
#endif
    __asm__ volatile("dsb sy" ::: "memory");
    ramlog_commit(r);
    __asm__ volatile("dsb sy" ::: "memory");
    active = 0;
}
#endif

static void publish(uint64_t stage)
{
    __asm__ volatile("dsb sy" ::: "memory");
    a52q_diagnostic.stage = stage;
    __asm__ volatile("dsb sy" ::: "memory");
#ifdef A52Q_RAMOOPS_CONFIG
    log_snapshot();
#endif
}

#ifdef A52Q_DISPLAY_TEST
#include "display_probe.h"
#endif

#ifdef A52Q_XNU_PAYLOAD
int a52q_load_embedded(void);
void a52q_loader_stage(uint64_t stage) { publish(stage); }
#endif

void diag_main(uint64_t dtb)
{
    a52q_diagnostic.magic = 0x4741494451323541ULL; /* LE "A52QDIAG" */
    a52q_diagnostic.version = 2;
    a52q_diagnostic.image = (uintptr_t)_head;
    a52q_diagnostic.image_end = (uintptr_t)_end;
    a52q_diagnostic.dtb = dtb; /* preserve, but do not dereference unvalidated x0 */
    publish(1);
    a52q_diagnostic.current_el = READ_REG("CurrentEL");
    a52q_diagnostic.sctlr = a52q_diagnostic.current_el == 8 ?
        READ_REG("sctlr_el2") : READ_REG("sctlr_el1");
    a52q_diagnostic.mpidr = READ_REG("mpidr_el1");
    a52q_diagnostic.midr = READ_REG("midr_el1");
    a52q_diagnostic.mmfr0 = READ_REG("id_aa64mmfr0_el1");
    a52q_diagnostic.pfr0 = READ_REG("id_aa64pfr0_el1");
    a52q_diagnostic.cntfrq = READ_REG("cntfrq_el0");
    a52q_diagnostic.ctr = READ_REG("ctr_el0");
    a52q_diagnostic.isar0 = READ_REG("id_aa64isar0_el1");
    a52q_diagnostic.isar1 = READ_REG("id_aa64isar1_el1");
    publish(2);
#ifdef A52Q_HANDOFF
    if (a52q_diagnostic.current_el != 4 || (a52q_diagnostic.sctlr & 5)) {
        publish(0xec);
        return;
    }
    for (unsigned i = 0; i < A52Q_HANDOFF_COUNT; i++) {
        handoff_active = i;
        __asm__ volatile("dsb sy" ::: "memory");
        handoff_values[i] = *(volatile const uint32_t *)handoff_addresses[i];
        __asm__ volatile("dsb sy" ::: "memory");
        handoff_done = i + 1;
        publish(0x20 + i);
    }
    handoff_active = UINT64_MAX;
    publish(0x80);
#ifdef A52Q_DISPLAY_TEST
    display_probe();
#endif
#endif
#ifdef A52Q_XNU_PAYLOAD
    int error = a52q_load_embedded();
    publish(0xe0 + (uint64_t)error);
#endif
}

void diag_exception(uint64_t slot)
{
    a52q_diagnostic.exception_slot = slot;
    if (READ_REG("CurrentEL") == 8) {
        a52q_diagnostic.esr = READ_REG("esr_el2");
        a52q_diagnostic.elr = READ_REG("elr_el2");
        a52q_diagnostic.far = READ_REG("far_el2");
    } else {
        a52q_diagnostic.esr = READ_REG("esr_el1");
        a52q_diagnostic.elr = READ_REG("elr_el1");
        a52q_diagnostic.far = READ_REG("far_el1");
    }
    publish(0xff);
}
