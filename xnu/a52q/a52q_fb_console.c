/* Best-effort bitmap mirror of the EXISTING console stream, never a log source.
 * Producer: static bounded queue, try-lock only, no MMIO/allocation/printf.
 * Consumer: verified UI mapping, bounded refresh, single display owner.
 */
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <sys/systm.h>
#include <kern/clock.h>
#include <mach/mach_time.h>
#include <pexpert/pexpert.h>
#include "a52q_ui_bridge.h"
#include "a52q_ui_profile.h"
#include "a52q_fb_console.h"
#include "a52q_text_grid.h"
extern unsigned char iso_font[256*16]; /* Existing XNU Latin-1 8x16 font. */
enum { A52TEXT_QUEUE=16384 };
static unsigned char a52text_queue[A52TEXT_QUEUE];
static unsigned a52text_head,a52text_count;
static int a52text_queue_busy,a52text_draw_busy,a52text_state; /* 0 queue,1 own,2 GUI,3 off */
static struct a52text_grid a52text_screen;
static uint64_t a52text_deadline;
int a52q_fb_console_owner(void)
{
    return __atomic_load_n(&a52text_state,__ATOMIC_ACQUIRE);
}
static int a52text_try(int *lock)
{
    int expected=0;
    return __atomic_compare_exchange_n(lock,&expected,1,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED);
}
void a52q_fb_console_putc(char c)
{
    if (__atomic_load_n(&a52text_state,__ATOMIC_ACQUIRE)>=2 || !a52text_try(&a52text_queue_busy)) return;
    if (a52text_count==A52TEXT_QUEUE) {
        a52text_head=(a52text_head+1)%A52TEXT_QUEUE;--a52text_count;
    }
    a52text_queue[(a52text_head+a52text_count++)%A52TEXT_QUEUE]=(unsigned char)c;
    __atomic_store_n(&a52text_queue_busy,0,__ATOMIC_RELEASE);
}
void a52q_fb_console_start(void)
{
    int enabled=0;
    if (!PE_parse_boot_argn("a52q_text_console",&enabled,sizeof(enabled)) || enabled!=1) {
        __atomic_store_n(&a52text_state,3,__ATOMIC_RELEASE);return;
    }
    if (!a52q_ui_pixels() || __atomic_load_n(&a52text_state,__ATOMIC_ACQUIRE)!=0) return;
    a52text_init(&a52text_screen);
    __atomic_store_n(&a52text_state,1,__ATOMIC_RELEASE);
    printf("A52Q text console: guarded 8x16 font at 2x; pstore retained\n");
    a52q_fb_console_tick(1);
}
void a52q_fb_console_tick(int force)
{
    if (__atomic_load_n(&a52text_state,__ATOMIC_ACQUIRE)!=1 || !a52q_ui_pixels() ||
        (!force && mach_absolute_time()<a52text_deadline) || !a52text_try(&a52text_draw_busy)) return;
    if (__atomic_load_n(&a52text_state,__ATOMIC_ACQUIRE)!=1) goto done;
    nanoseconds_to_deadline(100*NSEC_PER_MSEC,&a52text_deadline);
    unsigned limit=force ? A52TEXT_QUEUE : 4096,used=0;
    unsigned char batch[256];
    while (used<limit && a52text_try(&a52text_queue_busy)) {
        unsigned n=a52text_count;
        if (n>sizeof(batch)) n=sizeof(batch);
        if (n>limit-used) n=limit-used;
        for (unsigned i=0;i<n;i++) batch[i]=a52text_queue[(a52text_head+i)%A52TEXT_QUEUE];
        a52text_head=(a52text_head+n)%A52TEXT_QUEUE;a52text_count-=n;
        __atomic_store_n(&a52text_queue_busy,0,__ATOMIC_RELEASE);
        if (!n) break;
        for (unsigned i=0;i<n;i++) a52text_put(&a52text_screen,batch[i]);
        used+=n;
    }
    if ((used || force) && a52text_draw((volatile uint32_t *)a52q_ui_pixels(),
        A52Q_UI_BYTES,iso_font,&a52text_screen)) {
        if (force==2) (void)a52q_ui_flush_quiet();
        else (void)a52q_ui_flush();
    }
done:
    __atomic_store_n(&a52text_draw_busy,0,__ATOMIC_RELEASE);
}
int a52q_fb_console_handoff(void)
{
    /* Surface export serializes against normal rendering through its workloop.
     * Presentation also checks here; a concurrent panic renderer returns busy. */
    int old=__atomic_exchange_n(&a52text_state,2,__ATOMIC_ACQ_REL);
    if (old==1) printf("A52Q text console: framebuffer client requested handoff\n");
    if (!a52text_try(&a52text_draw_busy)) return 0;
    __atomic_store_n(&a52text_draw_busy,0,__ATOMIC_RELEASE);return 1;
}
void a52q_fb_console_panic(void)
{
    /* Never wait for a preempted renderer or reclaim a GUI-owned display. */
    a52q_fb_console_tick(2);
}
#endif
