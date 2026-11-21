"""Append console mirror and bounded late records; retain the ordinary writer."""

LATE = r'''
/* The 256KiB ordinary log fills before service/display failures. Only AFTER
 * full, replace its final4KiB with eight fixed512-byte diagnostic slots.
 * Header and first252KiB stay intact. No wrap, allocation, printf or waits.
 * Caller supplies a bounded CRC-protected line; interruption loses at most
 * this slot. Existing busy protects normal logging and relocation is done
 * before any of these late callers run. Best effort, single-core bring-up. */
void a52q_early_critical(const char *line, unsigned length, unsigned slot)
{
    if (!line || !length || length>240 || slot>=8 ||
        position!=A52Q_RAMLOG_SIZE-12) return;
    int expected=0;
    if (!__atomic_compare_exchange_n(&busy,&expected,1,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED)) return;
    volatile uint32_t *header=(volatile uint32_t *)console;
    if (header[0]!=0x43474244 || header[1]!=position || header[2]!=position) {
        __atomic_store_n(&busy,0,__ATOMIC_RELEASE);return;
    }
    volatile uint8_t *out=console+A52Q_RAMLOG_SIZE-4096+slot*512;
    for (unsigned i=0;i<512;i++) out[i]='\n';
    __asm__ volatile("dsb sy" ::: "memory");
    unsigned copies=length<=160 ? 3 : 2;
    for (unsigned copy=0;copy<copies;copy++) {
        for (unsigned i=0;i<length;i++) out[copy*length+i]=(uint8_t)line[i];
        __asm__ volatile("dsb sy" ::: "memory");
    }
    __atomic_store_n(&busy,0,__ATOMIC_RELEASE);
}
'''

def early(text):
    anchor='    byte(c);\n    busy = 0;'
    panic='    va_end(copy);\n    string("\\n");'
    end='void sweet_early_disable(void) {}\n#endif'
    if text.count(anchor)!=1 or text.count(panic)!=1 or text.count(end)!=1:
        raise ValueError('RAM console mirror anchors changed')
    text=text.replace('#include <stdint.h>','#include <stdint.h>\n#include "a52q_fb_console.h"')
    return text.replace(anchor,'    byte(c);\n    a52q_fb_console_putc(c);\n    busy = 0;').replace(
        panic,panic+'\n    a52q_fb_console_panic();').replace(end,LATE+'\n'+end)
