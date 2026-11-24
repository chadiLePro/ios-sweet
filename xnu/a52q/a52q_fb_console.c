/* Static boot artwork only. Kernel/daemon logging remains in pstore.
 * Keep the established API and ownership values: 1 boot, 2 GUI. */
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <sys/systm.h>
#include "a52q_ui_bridge.h"
#include "a52q_ui_profile.h"
#include "a52q_fb_console.h"
#include "a52q_boot_logo.h"
static int a52logo_state,a52logo_busy;
int a52q_fb_console_owner(void) {
    return __atomic_load_n(&a52logo_state,__ATOMIC_ACQUIRE);
}
void a52q_fb_console_putc(char c) { (void)c; }
void a52q_fb_console_tick(int force) { (void)force; }
void a52q_fb_console_panic(void) {}
void a52q_fb_console_start(void) {
    volatile uint32_t *pixels=(volatile uint32_t *)a52q_ui_pixels();
    int expected=0;
    if (!pixels || !__atomic_compare_exchange_n(&a52logo_busy,&expected,1,0,
        __ATOMIC_ACQUIRE,__ATOMIC_RELAXED)) return;
    expected=0;
    if (__atomic_compare_exchange_n(&a52logo_state,&expected,1,0,
        __ATOMIC_ACQ_REL,__ATOMIC_ACQUIRE)) {
        /* Use the measured 32-bit scanout. Never write outside visible rows. */
        for (unsigned y=0;y<A52Q_UI_HEIGHT;y++)
            for (unsigned x=0;x<A52Q_UI_WIDTH;x++)
                pixels[y*(A52Q_UI_STRIDE/4)+x]=0xff000000U;
        unsigned left=(A52Q_UI_WIDTH-A52Q_LOGO_WIDTH)/2;
        unsigned top=(A52Q_UI_HEIGHT-A52Q_LOGO_HEIGHT)/2;
        for (unsigned y=0;y<A52Q_LOGO_HEIGHT;y++)
            for (unsigned x=0;x<A52Q_LOGO_WIDTH;x++)
                if (a52q_logo_bits[y*A52Q_LOGO_ROW_BYTES+x/8] & (0x80U>>(x%8)))
                    pixels[(top+y)*(A52Q_UI_STRIDE/4)+left+x]=0xffffffffU;
        (void)a52q_ui_flush(); /* existing cache/barrier and guarded CTL_START */
    }
    __atomic_store_n(&a52logo_busy,0,__ATOMIC_RELEASE);
}
int a52q_fb_console_handoff(void) {
    __atomic_exchange_n(&a52logo_state,2,__ATOMIC_ACQ_REL);
    return !__atomic_load_n(&a52logo_busy,__ATOMIC_ACQUIRE);
}
#endif
