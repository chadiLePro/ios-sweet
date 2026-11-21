#ifndef A52Q_FB_CONSOLE_H
#define A52Q_FB_CONSOLE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
void a52q_fb_console_putc(char);
void a52q_fb_console_start(void);
void a52q_fb_console_tick(int);
void a52q_fb_console_panic(void);
int a52q_fb_console_handoff(void);
#ifdef __cplusplus
}
#endif
#endif
