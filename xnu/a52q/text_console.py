"""Append a nonblocking mirror after the unchanged pstore write."""
def early(text):
    anchor='    byte(c);\n    busy = 0;'
    panic='    va_end(copy);\n    string("\\n");'
    if text.count(anchor)!=1 or text.count(panic)!=1:
        raise ValueError('RAM console mirror anchors changed')
    text=text.replace('#include <stdint.h>','#include <stdint.h>\n#include "a52q_fb_console.h"')
    return text.replace(anchor,'    byte(c);\n    a52q_fb_console_putc(c);\n    busy = 0;').replace(
        panic,panic+'\n    a52q_fb_console_panic();')
