#ifndef A52Q_UI_COPY_H
#define A52Q_UI_COPY_H
#include <stdint.h>
#include <stddef.h>
/* Copy already-composed BGRA pixels only. No scaler, GPU or alpha compositor. */
static inline int a52q_ui_copy_rect(volatile uint32_t *dst,uint64_t dst_bytes,
    uint32_t dw,uint32_t dh,uint32_t dp,const uint8_t *src,uint64_t src_bytes,
    uint32_t sw,uint32_t sh,uint32_t sp,uint32_t offset,
    int32_t sx,int32_t sy,int32_t dx,int32_t dy,int32_t w,int32_t h)
{
    if (!dst || !src || ((uintptr_t)dst&3) || ((uintptr_t)src&3) ||
        (dp&3) || (sp&3) || (offset&3) || !dw || !dh || !sw || !sh ||
        dw>4096 || dh>4096 || sw>16384 || sh>16384 ||
        dp<(uint64_t)dw*4 || sp<(uint64_t)sw*4 || dst_bytes<(uint64_t)dp*dh ||
        sx<0 || sy<0 || dx<0 || dy<0 || w<=0 || h<=0 ||
        (uint32_t)sx>sw || (uint32_t)sy>sh || (uint32_t)dx>dw || (uint32_t)dy>dh ||
        (uint32_t)w>sw-(uint32_t)sx || (uint32_t)h>sh-(uint32_t)sy ||
        (uint32_t)w>dw-(uint32_t)dx || (uint32_t)h>dh-(uint32_t)dy ||
        offset>src_bytes || (uint64_t)(sy+(uint32_t)h-1)*sp+(uint64_t)(sx+(uint32_t)w)*4>src_bytes-offset)
        return 0;
    for (uint32_t y=0;y<(uint32_t)h;y++) {
        volatile uint32_t *out=(volatile uint32_t *)((volatile uint8_t *)dst+(uint64_t)(dy+y)*dp)+(uint32_t)dx;
        const uint32_t *in=(const uint32_t *)(src+offset+(uint64_t)(sy+y)*sp)+(uint32_t)sx;
        for (uint32_t x=0;x<(uint32_t)w;x++) out[x]=in[x];
    }
    return 1;
}
#endif
