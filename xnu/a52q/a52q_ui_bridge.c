/* Optional CPU surface adapter. Existing a52q_display.c stays unchanged.
 * No DSI/panel setup, clocks, resets, SMMU or reserved-RAM changes.
 */
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <sys/param.h>
#include <sys/systm.h>
#include <kern/clock.h>
#include <mach/mach_time.h>
#include <machine/machine_routines.h>
#include <vm/pmap.h>
#include <pexpert/pexpert.h>
#include <pexpert/device_tree.h>
#include <libkern/libkern.h>
#include "a52q_ui_profile.h"
#include "a52q_ui_bridge.h"
#include "a52q_fb_console.h"
extern vm_offset_t ml_io_map(vm_offset_t, vm_size_t);
extern vm_offset_t ml_io_map_unmappable(vm_offset_t, vm_size_t, unsigned int);
static volatile uint32_t *a52ui_regs[13];
static volatile uint32_t *a52ui_frame;
static int a52ui_state, a52ui_busy;
static unsigned a52ui_frames;
static uint64_t a52ui_nonce;

static int a52ui_property(DTEntry node, const char *name, void *out, unsigned length)
{
    const void *data; unsigned size;
    if (SecureDTGetProperty(node,name,&data,&size)!=kSuccess || size!=length) return 0;
    memcpy(out,data,length); return 1;
}
static void a52ui_report(unsigned phase)
{
    char body[64];
    int n=snprintf(body,sizeof(body),"%016llx/%02x/%08x",a52ui_nonce,phase,a52ui_frames);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    for (unsigned i=0;i<3;i++) printf("A52G1 %s %08x\n",body,crc^0xffffffffU);
}
/* V24 rejected before prepare. Diagnose the existing guards; never relax them.
 * reason 1: profile, 2: register mapping, 3: register value, 4: frame mapping,
 * 5: DSI MDP busy timeout, 6: START completion timeout.
 * Never writes DSI_STATUS to force an idle state.
 * index ff means no individual register; value is a public display register.
 */
static void a52ui_rejection(unsigned reason,unsigned index,uint32_t value)
{
    char body[64];
    int n=snprintf(body,sizeof(body),"%016llx/%02x/%02x/%08x",a52ui_nonce,reason,index,value);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    for (unsigned i=0;i<3;i++) printf("A52G2 %s %08x\n",body,crc^0xffffffffU);
}
static int a52ui_guard_read(unsigned index,uint32_t *value)
{
    *value=*a52ui_regs[index];
    if (!a52q_ui_guard_value_matches(index,*value)) return 0;
    if (index!=6 || !*value) return 1;
    uint64_t deadline;nanoseconds_to_deadline(100*NSEC_PER_MSEC,&deadline);
    do {
        if (mach_absolute_time()>=deadline) return -1;
        *value=*a52ui_regs[index];
        if (!a52q_ui_guard_value_matches(index,*value)) return 0;
    } while (*value);
    return 1;
}
int a52q_ui_framebuffer(uint64_t *phys,uint32_t *w,uint32_t *h,uint32_t *stride)
{
    unsigned reason=1,index=0xff;uint32_t observed=0;
    if (!phys || !w || !h || !stride) return 0;
    if (!a52ui_state) {
        int enable=0,expected=0;
        DTEntry node,chosen,other;
        if (!PE_parse_boot_argn("a52q_ui",&enable,sizeof(enable)) || enable!=1 ||
            SecureDTLookupEntry(NULL,"/a52q-ui-bridge",&node)!=kSuccess ||
            SecureDTLookupEntry(NULL,"/a52q-display-selftest",&other)==kSuccess) return 0;
        if (!__atomic_compare_exchange_n(&a52ui_state,&expected,-1,0,__ATOMIC_ACQ_REL,__ATOMIC_ACQUIRE)) return 0;
        uint64_t reg[2],start,base,size; uint32_t geometry[3];
        struct a52q_ui_guard guards[13];
        if (!a52ui_property(node,"nonce",&a52ui_nonce,sizeof(a52ui_nonce)) || !a52ui_nonce ||
            !a52ui_property(node,"reg",reg,sizeof(reg)) ||
            !a52ui_property(node,"geometry",geometry,sizeof(geometry)) ||
            !a52ui_property(node,"guards",guards,sizeof(guards)) ||
            !a52ui_property(node,"start-register",&start,sizeof(start)) ||
            SecureDTLookupEntry(NULL,"/chosen",&chosen)!=kSuccess ||
            !a52ui_property(chosen,"dram-base",&base,sizeof(base)) ||
            !a52ui_property(chosen,"dram-size",&size,sizeof(size)) ||
            !a52q_ui_profile_matches(reg,geometry,guards,start,base,size)) goto reject;
        for (unsigned i=0;i<13;i++) {
            index=i;reason=2;observed=0;
            a52ui_regs[i]=(volatile uint32_t *)ml_io_map(guards[i].address,4);
            if (!a52ui_regs[i]) goto reject;
            reason=3;
            int sampled=a52ui_guard_read(i,&observed);
            if (sampled<0) {reason=5;goto reject;}
            if (!sampled) goto reject;
        }
        /* Match IOSurface's user mapping attribute. Never map this frame with
         * a cached alias, or concurrently with the old VM_WIMG_IO diagnostic. */
        reason=4;index=0xff;observed=0;
        a52ui_frame=(volatile uint32_t *)ml_io_map_unmappable(reg[0],reg[1],VM_WIMG_WCOMB);
        if (!a52ui_frame) goto reject;
        __atomic_store_n(&a52ui_state,1,__ATOMIC_RELEASE);
        a52ui_report(0x10);
        a52q_fb_console_start();
    }
    if (__atomic_load_n(&a52ui_state,__ATOMIC_ACQUIRE)!=1) return 0;
    *phys=A52Q_UI_PHYS;*w=A52Q_UI_WIDTH;*h=A52Q_UI_HEIGHT;*stride=A52Q_UI_STRIDE;
    return 1;
reject:
    __atomic_store_n(&a52ui_state,-2,__ATOMIC_RELEASE);
    a52ui_rejection(reason,index,observed);
    a52ui_report(0xe0);return 0;
}
uintptr_t a52q_ui_pixels(void)
{
    return __atomic_load_n(&a52ui_state,__ATOMIC_ACQUIRE)==1 ? (uintptr_t)a52ui_frame : 0;
}
int a52q_ui_physical_allowed(uint64_t phys,uint32_t w,uint32_t h,uint32_t stride)
{
    return a52q_ui_pixels() && phys==A52Q_UI_PHYS && w==A52Q_UI_WIDTH &&
        h==A52Q_UI_HEIGHT && stride==A52Q_UI_STRIDE;
}
static int a52ui_flush_internal(int report)
{
    int expected=0;
    unsigned reason=3,index=0xff;uint32_t observed=0;
    if (!a52q_ui_pixels() || !__atomic_compare_exchange_n(&a52ui_busy,&expected,1,0,__ATOMIC_ACQ_REL,__ATOMIC_ACQUIRE)) return 0;
    /* The only write is the exact START consumed by the previous RGB test. */
    for (unsigned i=0;i<13;i++) {
        index=i;
        int sampled=a52ui_guard_read(i,&observed);
        if (sampled!=1) {reason=sampled<0 ? 5 : 3;goto fail;}
    }
    __asm__ volatile("dsb sy" ::: "memory");
    *a52ui_regs[1]=1;
    __asm__ volatile("dsb sy" ::: "memory");
    uint64_t deadline;nanoseconds_to_deadline(100*NSEC_PER_MSEC,&deadline);
    reason=6;index=1;
    while ((observed=*a52ui_regs[1])&1) if (mach_absolute_time()>=deadline) goto fail;
    ++a52ui_frames;
    if (report && a52ui_frames<=3) a52ui_report(0x30);
    __atomic_store_n(&a52ui_busy,0,__ATOMIC_RELEASE);return 1;
fail:
    __atomic_store_n(&a52ui_state,-2,__ATOMIC_RELEASE);
    if (report) {a52ui_rejection(reason,index,observed);a52ui_report(0xe1);}
    __atomic_store_n(&a52ui_busy,0,__ATOMIC_RELEASE);return 0;
}
int a52q_ui_flush(void) { return a52ui_flush_internal(1); }
/* Panic caller must never re-enter printf or its console locks. */
int a52q_ui_flush_quiet(void) { return a52ui_flush_internal(0); }
#endif
