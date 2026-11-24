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
static unsigned a52ui_sequence;
static uint64_t a52ui_heartbeat_deadline;
static char a52ui_latest[6][240];
static unsigned a52ui_latest_length[6];
static int a52ui_latest_busy[6];
static unsigned a52ui_printed[6];

/* Public state only. CRC records supplement ordinary pstore text; after full
 * the fixed slots retain the latest record without changing its header. */
void a52q_ui_observe(unsigned slot,const char *payload)
{
    if (!a52ui_nonce || slot>=6 || !payload) return;
    char body[208],line[240];
    unsigned sequence=__atomic_add_fetch(&a52ui_sequence,1,__ATOMIC_RELAXED);
    int n=snprintf(body,sizeof(body),"%016llx/%08x/%02x/%.168s",
        (unsigned long long)a52ui_nonce,sequence,slot,payload);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    for (int i=0;i<n;i++) if ((unsigned char)body[i]<32 || (unsigned char)body[i]>126) body[i]='?';
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    n=snprintf(line,sizeof(line),"A52OBS1 %s %08x\n",body,crc^0xffffffffU);
    if (n<=0 || (unsigned)n>=sizeof(line)) return;
    int expected=0;
    if (__atomic_compare_exchange_n(&a52ui_latest_busy[slot],&expected,1,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED)) {
        memcpy(a52ui_latest[slot],line,(unsigned)n);
        a52ui_latest_length[slot]=(unsigned)n;
        __atomic_store_n(&a52ui_latest_busy[slot],0,__ATOMIC_RELEASE);
    }
    a52q_early_critical(line,(unsigned)n,slot);
    if (__atomic_fetch_add(&a52ui_printed[slot],1U,__ATOMIC_RELAXED)<64)
        for (unsigned i=0;i<(slot ? 3U : 1U);i++) printf("%s",line);
}

void a52q_ui_heartbeat(unsigned poweroff)
{
    /* Called only by the framebuffer workloop, every5s. Reads only the same
     * mapped registers and64 bounded framebuffer samples; no device writes. */
    if (mach_absolute_time()<a52ui_heartbeat_deadline) return;
    nanoseconds_to_deadline(5000*NSEC_PER_MSEC,&a52ui_heartbeat_deadline);
    /* Repeat last matching/open/selector results into late slots, even when
     * the corresponding service operation happened before the log filled. */
    for (unsigned slot=1;slot<6;slot++) {
        int expected=0;char line[240];unsigned length=0;
        if (__atomic_compare_exchange_n(&a52ui_latest_busy[slot],&expected,1,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED)) {
            length=a52ui_latest_length[slot];
            if (length) memcpy(line,a52ui_latest[slot],length);
            __atomic_store_n(&a52ui_latest_busy[slot],0,__ATOMIC_RELEASE);
            if (length) a52q_early_critical(line,length,slot);
        }
    }
    int state=__atomic_load_n(&a52ui_state,__ATOMIC_ACQUIRE);
    if (state!=1) {
        char body[64];snprintf(body,sizeof(body),"tick state=%d owner=%d off=%u",
            state,a52q_fb_console_owner(),poweroff);a52q_ui_observe(0,body);return;
    }
    uint32_t hash=2166136261U,first=0;unsigned colour=0;
    for (unsigned i=0;i<64;i++) {
        uint64_t offset=i==63 ? (A52Q_UI_HEIGHT/2)*A52Q_UI_WIDTH+A52Q_UI_WIDTH/2 :
            (uint64_t)i*(A52Q_UI_WIDTH*A52Q_UI_HEIGHT-1)/63;
        uint32_t value=a52ui_frame[offset];
        hash=(hash^value)*16777619U;
        if (value!=0xff000000U && value!=0xffffffffU) {if (!colour) first=value;++colour;}
    }
    char body[168];
    snprintf(body,sizeof(body),"tick state=%d owner=%d off=%u frames=%u dsi=%08x start=%08x sample=%08x colour=%u first=%08x",
        state,a52q_fb_console_owner(),poweroff,a52ui_frames,*a52ui_regs[6],*a52ui_regs[1],hash,colour,first);
    a52q_ui_observe(0,body);
}

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
 * 5: legacy DSI idle-wait timeout, 6: START completion timeout.
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
    /* V27 proves our extra idle wait stalls after START with status5. The
     * earlier visible RGB test used this same status5 and bounded START.
     * Vendor idle-wait is used before dynamic clock changes; we change none.
     * Retain the exact 0/5 status predicate and every configuration pin. */
    return a52q_ui_guard_value_matches(index,*value);
}
static int a52ui_mapping_valid(void)
{
    uintptr_t va=(uintptr_t)a52ui_frame;
    /* Use XNU's wired-mapping translator, which protects PAR_EL1 from IRQs. */
    uint64_t pa0=ml_vtophys(va),pa1=ml_vtophys(va+A52Q_UI_BYTES-1),mair;
    __asm__ volatile("mrs %0, mair_el1" : "=r"(mair));
    printf("A52Q scanout map: pa0=%llx pa1=%llx mair=%llx\n",
        (unsigned long long)pa0,(unsigned long long)pa1,(unsigned long long)mair);
    return pa0==A52Q_UI_PHYS && pa1==A52Q_UI_PHYS+A52Q_UI_BYTES-1;
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
            if (!sampled) goto reject;
        }
        /* Match the clean XNU RGB probe and the physical IOSurface user mapping:
         * uncached Device memory throughout; no WriteCombine/cache aliases. */
        reason=4;index=0xff;observed=0;
        a52ui_frame=(volatile uint32_t *)ml_io_map_unmappable(reg[0],reg[1],VM_WIMG_IO);
        if (!a52ui_frame) goto reject;
        reason=7;
        if (!a52ui_mapping_valid()) goto reject;
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
static void a52ui_boot_readback(void)
{
    uint32_t hash=2166136261U;unsigned black=0,white=0,other=0;
    for (unsigned y=0;y<A52Q_UI_HEIGHT;y++)
        for (unsigned x=0;x<A52Q_UI_WIDTH;x++) {
            uint32_t pixel=a52ui_frame[(uint64_t)y*(A52Q_UI_STRIDE/4)+x];
            hash=(hash^pixel)*16777619U;
            if(pixel==0xff000000U) ++black;
            else if(pixel==0xffffffffU) ++white;
            else ++other;
        }
    char body[160];
    snprintf(body,sizeof(body),"bootframe hash=%08x black=%u white=%u other=%u",hash,black,white,other);
    a52q_ui_observe(0,body);
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
        if (!sampled) goto fail;
    }
    __asm__ volatile("dsb sy" ::: "memory");
    if (report && !a52ui_frames) a52ui_boot_readback();
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
