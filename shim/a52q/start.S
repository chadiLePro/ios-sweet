/* Diagnostic core only. Linux arm64 Image entry contract, linked at zero.
 * Never packaged as Samsung boot.img by this build. No copied sweet MMIO.
 */
.section .text.head, "ax"
.global _head
#ifndef A52Q_TEXT_OFFSET
#define A52Q_TEXT_OFFSET 0
#endif
_head:
    b _start
    .long 0
    .quad A52Q_TEXT_OFFSET
    .quad _end
    .quad 0xa
    .quad 0, 0, 0
    .ascii "ARM\x64"
    .long 0

.text
_start:
    msr daifset, #0xf
    /* Only EL1 is implemented. Do not write EL1 state from another EL. */
    mrs x9, CurrentEL
    cmp x9, #4
    b.ne park
    /* The Linux boot protocol requires MMU off. Leave unknown state alone. */
    mrs x9, sctlr_el1
    tbnz x9, #0, park
    mov x19, x0
    msr spsel, #1
    adr x9, _stack_top
    mov sp, x9
    adr x9, _bss_start
    adr x10, _bss_end
1:  cmp x9, x10
    b.hs 2f
    str xzr, [x9], #8
    b 1b
2:  adr x9, vectors
    msr vbar_el1, x9
    isb
    mov x0, x19
    bl diag_main
park:
    wfe
    b park

.macro vector slot
    .balign 0x80
    mov x0, #\slot
    b exception
.endm
.balign 0x800
vectors:
    vector 0
    vector 1
    vector 2
    vector 3
    vector 4
    vector 5
    vector 6
    vector 7
    vector 8
    vector 9
    vector 10
    vector 11
    vector 12
    vector 13
    vector 14
    vector 15
exception:
    /* Fresh stack: exception capture does not depend on a damaged C frame. */
    adr x9, _stack_top
    mov sp, x9
    bl diag_exception
    b park
