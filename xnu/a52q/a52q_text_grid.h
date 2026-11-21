#ifndef A52Q_TEXT_GRID_H
#define A52Q_TEXT_GRID_H
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#define A52TEXT_COLS 67U
#define A52TEXT_ROWS 74U
struct a52text_grid {
    unsigned first,row,col,escape,escape_bytes;
    unsigned char cells[A52TEXT_ROWS][A52TEXT_COLS];
};
static inline void a52text_init(struct a52text_grid *g)
{
    memset(g,0,sizeof(*g));memset(g->cells,' ',sizeof(g->cells));
}
static inline void a52text_newline(struct a52text_grid *g)
{
    g->col=0;
    if (g->row+1<A52TEXT_ROWS) ++g->row;
    else g->first=(g->first+1)%A52TEXT_ROWS;
    memset(g->cells[(g->first+g->row)%A52TEXT_ROWS],' ',A52TEXT_COLS);
}
static inline void a52text_put(struct a52text_grid *g,unsigned char c)
{
    if (g->escape) {
        if (g->escape==1 && c=='[') {g->escape=2;return;}
        if (g->escape!=2 || (c>='@' && c<='~') || ++g->escape_bytes>=32) g->escape=0;
        return;
    }
    if (c==27) {g->escape=1;g->escape_bytes=0;return;}
    if (c=='\r') {g->col=0;return;}
    if (c=='\n') {a52text_newline(g);return;}
    if (c=='\b') {
        if (g->col) g->cells[(g->first+g->row)%A52TEXT_ROWS][--g->col]=' ';
        return;
    }
    if (c=='\t') {
        unsigned n=4-g->col%4;
        while (n--) a52text_put(g,' ');
        return;
    }
    if (c<32 || c==127) return;
    if (g->col==A52TEXT_COLS) a52text_newline(g);
    g->cells[(g->first+g->row)%A52TEXT_ROWS][g->col++]=c<128 ? c : '?';
}
static inline void a52text_glyph(volatile uint32_t *frame,const unsigned char *font,
    unsigned row,unsigned col,unsigned char c)
{
    for (unsigned y=0;y<32;y++) {
        volatile uint32_t *line=frame+(row*32+y)*1080+col*16;
        unsigned bits=font[(unsigned)c*16+y/2];
        for (unsigned x=0;x<16;x++) line[x]=bits&(1U<<(x/2)) ? 0xffffffffU : 0xff000000U;
    }
}
static inline int a52text_draw(volatile uint32_t *frame,uint64_t bytes,
    const unsigned char *font,const struct a52text_grid *g)
{
    if (!frame || ((uintptr_t)frame&3) || !font || !g || bytes<1080ULL*2400*4 ||
        g->first>=A52TEXT_ROWS || g->row>=A52TEXT_ROWS || g->col>A52TEXT_COLS) return 0;
    static const unsigned char banner[]=" A52Q IOS16 - VERBOSE CONSOLE ";
    for (unsigned row=0;row<=A52TEXT_ROWS;row++) {
        for (unsigned col=0;col<A52TEXT_COLS;col++) {
            unsigned char c=row ? g->cells[(g->first+row-1)%A52TEXT_ROWS][col] :
                col<sizeof(banner)-1 ? banner[col] : ' ';
            a52text_glyph(frame,font,row,col,c);
        }
        /* The 8-pixel right margin is outside the 67 complete text cells. */
        for (unsigned y=0;y<32;y++)
            for (unsigned x=A52TEXT_COLS*16;x<1080;x++) frame[(row*32+y)*1080+x]=0xff000000U;
    }
    return 1;
}
#endif
