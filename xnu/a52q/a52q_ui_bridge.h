#ifndef A52Q_UI_BRIDGE_H
#define A52Q_UI_BRIDGE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
int a52q_ui_framebuffer(uint64_t *, uint32_t *, uint32_t *, uint32_t *);
uintptr_t a52q_ui_pixels(void);
int a52q_ui_flush(void);
int a52q_ui_physical_allowed(uint64_t, uint32_t, uint32_t, uint32_t);
#ifdef __cplusplus
}
#endif
#endif
