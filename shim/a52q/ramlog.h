#pragma once
#include <stdint.h>

/* Linux 4.14 persistent_ram_buffer without ECC, console signature (sig=0).
 * Independent single-writer implementation. Payload precedes size publication.
 * Caller provides ordering barriers before/after a complete diagnostic snapshot.
 */
struct ramlog {
    uint32_t sig, start, size;
    uint8_t data[];
};
_Static_assert(__builtin_offsetof(struct ramlog, data) == 12, "Linux ramoops header");

static inline void ramlog_begin(volatile struct ramlog *r)
{
    r->sig = 0;
    r->start = 0;
    r->size = 0;
}

static inline void ramlog_char(volatile struct ramlog *r, uint32_t capacity, char c)
{
    uint32_t used = r->size;
    /* A bounded, nonwrapping record is enough for this short diagnostic. */
    if (capacity > 12 && used < capacity - 12) {
        r->data[used] = (uint8_t)c;
        r->start = used + 1;
        r->size = used + 1;
    }
}

static inline void ramlog_commit(volatile struct ramlog *r)
{
    r->sig = 0x43474244U;
}
