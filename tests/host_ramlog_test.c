#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../shim/a52q/ramlog.h"

int main(void)
{
    _Alignas(4) uint8_t backing[32];
    memset(backing, 0xa5, sizeof(backing));
    volatile struct ramlog *r = (volatile struct ramlog *)backing;
    ramlog_begin(r);
    assert(r->sig == 0 && r->size == 0 && r->start == 0);
    for (const char *s = "ABCDE"; *s; s++)
        ramlog_char(r, 16, *s); /* only four data bytes fit */
    ramlog_commit(r);
    assert(r->sig == 0x43474244 && r->size == 4 && r->start == 4);
    assert(memcmp(backing + 12, "ABCD", 4) == 0);
    for (unsigned i = 16; i < sizeof(backing); i++)
        assert(backing[i] == 0xa5);
    /* Linux persistent_ram_save_old reconstructs data[start:size] then [0:start]. */
    char old[5] = {0};
    memcpy(old, backing + 12 + r->start, r->size - r->start);
    memcpy(old + r->size - r->start, backing + 12, r->start);
    assert(strcmp(old, "ABCD") == 0);
    ramlog_begin(r);
    ramlog_char(r, 12, 'X');
    assert(r->size == 0); /* no payload capacity */
    puts("ramoops layout, bounded writes and Linux reconstruction: PASS");
    return 0;
}
