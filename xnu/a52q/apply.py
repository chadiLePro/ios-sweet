#!/usr/bin/env python3
"""Apply the A52 bootstrap overlay AFTER the existing 81 patches.

Only reviewed software-provider guards are shared. SWEET remains undefined on
A52, so its UFS/persistent-log/USB/SPMI/RPMh/display/touch/key/SMP drivers stay out.
The original patch set and Redmi target remain usable without this overlay.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import zlib
import static_init

HERE = Path(__file__).resolve().parent

# Portable providers and bootstrap support, not Qualcomm device drivers.
COMMON = [
    'iokit/Kernel/IOService.cpp',
    'bsd/kern/kern_trustcache.c', 'bsd/sys/pthread_internal.h',
    'bsd/pthread/sweet_pthread_synch.c', 'bsd/pthread/sweet_pthread_support.c',
    'bsd/pthread/sweet_pthread_init.c',
    'osfmk/prng/prng_random.c', 'osfmk/prng/entropy.c', 'osfmk/vm/vm_kern.c',
    'osfmk/kern/debug.c', 'pexpert/arm/pe_fiq.c', 'pexpert/pexpert/arm/protos.h', 'osfmk/arm64/sleh.c',
    'libkern/crypto/corecrypto_aes.c', 'libkern/crypto/corecrypto_md5.c',
    'libkern/crypto/corecrypto_sha1.c', 'libkern/crypto/corecrypto_sha2.c',
] + ['libkern/crypto/sweet_' + name + '.c' for name in (
    'aes', 'aes_ct', 'aes_ct_enc', 'aes_ct_dec', 'aes_ct_cbcenc', 'aes_ct_cbcdec',
    'md5', 'sha1', 'sha2big', 'enc32le', 'enc32be', 'enc64be',
    'dec32le', 'dec32be', 'dec64be')]


def apply(root, filesystem='mockfs'):
    if filesystem not in ('mockfs', 'hfs'):
        raise ValueError('unsupported A52 filesystem configuration')
    changes = {}
    originals = {}

    def read(name):
        if name not in originals:
            originals[name] = (root / name).read_text()
        return changes.get(name, originals[name])

    def replace(name, old, new, count=1):
        text = read(name)
        if text.count(old) != count:
            raise ValueError(f'{name}: expected {count} occurrences of {old!r}, got {text.count(old)}')
        changes[name] = text.replace(old, new)

    for name in COMMON:
        text = read(name)
        for macro in ('SWEET', 'ARM64_BOARD_CONFIG_SWEET'):
            # Including !defined: negate the entire disjunction, not one arm.
            text = text.replace(f'defined({macro})', f'(defined({macro}) || defined(ARM64_BOARD_CONFIG_A52Q))')
        if text == read(name):
            raise ValueError(f'{name}: expected portable provider guard missing')
        changes[name] = text
    changes[static_init.TARGET] = static_init.transform(read(static_init.TARGET))
    replace('bsd/kern/sweet_amfi.c', '#if defined(ARM64_BOARD_CONFIG_SWEET)',
            '#if defined(ARM64_BOARD_CONFIG_A52Q)\n#include "a52q_amfi.c"\n#endif\n#if defined(ARM64_BOARD_CONFIG_SWEET)')
    changes['bsd/kern/a52q_amfi.c'] = (HERE / 'a52q_amfi.c').read_text()
    replace('bsd/dev/sweet_ufs.c', '#if defined(ARM64_BOARD_CONFIG_SWEET)',
            '#if defined(ARM64_BOARD_CONFIG_A52Q)\n#include "a52q_ufs.c"\n#endif\n#if defined(ARM64_BOARD_CONFIG_SWEET)')
    changes['bsd/dev/a52q_ufs.c'] = (HERE / 'a52q_ufs.c').read_text()
    changes['bsd/dev/a52q_display.c'] = (HERE / 'a52q_display.c').read_text()
    changes['bsd/dev/a52q_display_pattern.h'] = (HERE.parents[1] / 'shim/a52q/display_pattern.h').read_text()
    replace('bsd/conf/files', 'bsd/dev/sweet_ufs.c\t\t\tstandard\n',
            'bsd/dev/sweet_ufs.c\t\t\tstandard\nbsd/dev/a52q_display.c\t\t\tstandard\n')
    for name in ('a52q_ufs_disk.c', 'a52q_ufs_bounds.h'):
        changes['bsd/dev/' + name] = (HERE / name).read_text()
    for name in ('ufs_nop_protocol.h', 'ufs_read_protocol.h'):
        changes['bsd/dev/a52q_' + name] = (HERE.parents[1] / 'shim/a52q' / name).read_text()
    replace('bsd/kern/bsd_init.c', '\tvfsinit();\n',
            '\tvfsinit();\n#if defined(ARM64_BOARD_CONFIG_A52Q)\n'
            '\textern void a52q_ufs_selftest(void);\n\ta52q_ufs_selftest();\n'
            '\textern void a52q_display_selftest(void);\n\ta52q_display_selftest();\n#endif\n')
    # Observed on disk-root v2: HFS mounts, then FSIOC_KERNEL_ROOTAUTH panics.
    # A RAM root bypasses this path. Permit only our published, read-only UFS
    # root; leave every other A52 root and the Redmi policy unchanged.
    replace('bsd/kern/bsd_init.c',
            '\t\t\t\tpanic("rootvp not authenticated after mounting");',
            '''#if defined(ARM64_BOARD_CONFIG_A52Q)
                extern int a52q_ufs_rootdev(dev_t *dev);
                dev_t a52_root;
                if (a52q_ufs_rootdev(&a52_root) == 0 && a52_root == rootdev &&
                    (mountlist.tqh_first->mnt_flag & MNT_RDONLY)) {
                    printf("A52Q: verified read-only UFS root is UNSEALED (rootauth error %d)\\n", autherr);
                } else
#endif
                panic("rootvp not authenticated after mounting");''')
    root_hook = '''#if defined(ARM64_BOARD_CONFIG_A52Q)
    if (strcmp(rdBootVar, "a52root0") == 0 || strcmp(rdBootVar, "a52ios0") == 0) {
        extern int a52q_ufs_rootdev(dev_t *dev);
        extern int a52q_ufs_root_named(const char *name);
        OSSafeReleaseNULL(matching);
        int error = a52q_ufs_rootdev(root);
        if (error || !a52q_ufs_root_named(rdBootVar)) panic("IOFindBSDRoot: A52 read-only disk unavailable: %d", error);
        strlcpy(rootName, rdBootVar, rootNameSize);
        *oflags = 0;
        goto iofrootx;
    }
#endif

'''
    replace('iokit/bsddev/IOKitBSDInit.cpp',
            '#if defined(ARM64_BOARD_CONFIG_SWEET)\n//\n//\tSWEET: root on a GPT partition',
            root_hook + '#if defined(ARM64_BOARD_CONFIG_SWEET)\n//\n//\tSWEET: root on a GPT partition')

    replace('makedefs/MakeInc.def', 'VMAPPLE SWEET\n', 'VMAPPLE SWEET A52Q\n')
    replace('makedefs/MakeInc.def', 'ifneq ($(CURRENT_MACHINE_CONFIG),SWEET)',
            'ifeq ($(filter SWEET A52Q,$(CURRENT_MACHINE_CONFIG)),)')
    replace('makedefs/MakeInc.def', 'MACHINE_FLAGS_ARM64_SWEET =',
            'MACHINE_FLAGS_ARM64_A52Q = -DARM64_BOARD_CONFIG_A52Q -march=armv8.2-a+crypto\nMACHINE_FLAGS_ARM64_SWEET =')
    for name in ('bsd/conf/Makefile.template', 'libkern/conf/Makefile.template'):
        replace(name, 'ifeq ($(CURRENT_MACHINE_CONFIG),SWEET)',
                'ifneq ($(filter SWEET A52Q,$(CURRENT_MACHINE_CONFIG)),)')
    # Upstream lists this diagnostic as standard, while its task-side half is
    # SWEET-only. A52 does not expose the matching /dev/mem ioctl or need it.
    replace('bsd/conf/files', 'bsd/dev/sweet_sample.c\t\t\tstandard\n', '')
    changes['config/MASTER.arm64.a52q'] = read('config/MASTER.arm64.sweet').replace(
        '# sweet (Redmi Note 10 Pro, SM7150):', '# a52q (Samsung SM-A525F/DS, SM7125):')
    if filesystem == 'mockfs':
        changes['config/MASTER.arm64.a52q'] = changes['config/MASTER.arm64.a52q'].replace(
            ' mockfs sweet_hfs ', ' mockfs ')
    # The optional hfs feature reuses Apple's staged OSS filesystem and its
    # software-only VFS glue. SWEET_HFS is a filesystem option, not the SWEET
    # board macro: it enables no UFS/USB/display/clock drivers. Content protection
    # is disabled by the reviewed kext compatibility header; use plain test data.
    replace('pexpert/pexpert/arm64/board_config.h', '#ifdef ARM64_BOARD_CONFIG_SWEET',
            '#ifdef ARM64_BOARD_CONFIG_A52Q\n#include <pexpert/arm64/A52Q.h>\n'
            '#define MAX_L2_CLINE 6\n#define MAX_CPUS 1\n#define MAX_CPU_CLUSTERS 1\n'
            '#define CORE_NCTRS 8\n#endif\n\n#ifdef ARM64_BOARD_CONFIG_SWEET')
    replace('pexpert/pexpert/arm64/Makefile', '\tSWEET.h', '\tSWEET.h \\\n\tA52Q.h')
    changes['pexpert/pexpert/arm64/A52Q.h'] = (HERE / 'A52Q.h').read_text()
    replace('osfmk/arm64/proc_reg.h', '#elif defined (SWEET)', '#elif defined (SWEET) || defined(A52Q)')
    replace('osfmk/arm64/machine_routines.c', '#if defined(SWEET)\n/*\n * sweet: arm_vm_init()',
            '#if defined(SWEET) || defined(A52Q)\n/*\n * sweet: arm_vm_init()')
    replace('osfmk/arm64/sweet_early.h', '#if defined(SWEET)', '#if defined(SWEET) || defined(A52Q)')
    # This source is already in files.arm64. Preserve the Redmi implementation.
    replace('osfmk/arm64/sweet_early.c', '#if defined(SWEET)',
            '#if defined(A52Q)\n#include "a52q_early.c"\n#endif\n\n#if defined(SWEET)')
    changes['osfmk/arm64/a52q_early.c'] = (HERE / 'a52q_early.c').read_text()
    # Keep independent implementations in the two existing build units, whose
    # Redmi bodies remain guarded by SWEET. No change to the original patches.
    for stem in ('A52PlatformExpert', 'A52CPU'):
        legacy = {'A52PlatformExpert': 'SweetPlatformExpert', 'A52CPU': 'SweetCPU'}[stem]
        replace(f'iokit/Kernel/arm/{legacy}.cpp', '#if defined(SWEET)',
                f'#if defined(A52Q)\n#include "{stem}.cpp"\n#endif\n\n#if defined(SWEET)')
        changes[f'iokit/Kernel/arm/{stem}.cpp'] = (HERE / f'{stem}.cpp').read_text()
    replace('iokit/KernelConfigTables.cpp', '#if defined(ARM64_BOARD_CONFIG_SWEET)',
            '#if defined(ARM64_BOARD_CONFIG_A52Q)\n'
            '    " { \'IOClass\' = A52PlatformExpert; \'IOProviderClass\' = IOPlatformExpertDevice;"\n'
            '    "   \'IONameMatch\' = \'samsung,a52q\'; \'IOProbeScore\' = 10000:32; },"\n'
            '    " { \'IOClass\' = A52CPU; \'IOProviderClass\' = IOPlatformDevice;"\n'
            '    "   \'IONameMatch\' = \'ARM,v8\'; \'IOProbeScore\' = 10000:32; },"\n'
            '#endif\n#if defined(ARM64_BOARD_CONFIG_SWEET)')
    # Read-only software observation of CPU signal state, not SMP startup.
    replace('osfmk/arm64/cpu.c', '#if defined(SWEET)\n/* Bring-up observer:',
            '#if defined(SWEET) || defined(A52Q)\n/* Bring-up observer:')
    changes['pexpert/arm/a52q_serial.inc'] = (HERE / 'a52q_serial.inc').read_text()
    replace('pexpert/arm/pe_serial.c', 'int\nserial_init(void)',
            '#if defined(A52Q)\n#include "a52q_serial.inc"\n#endif\n\nint\nserial_init(void)')
    # RAM console has no SoC UART base and needs no ADT serial/device lookup.
    replace('pexpert/arm/pe_serial.c', '\tsoc_base = pe_arm_get_soc_base_phys();',
            '#if defined(A52Q)\n\tregister_serial_functions(&a52q_ram_functions);\n'
            '\ta52q_ram_init();\n\tserial_do_transmit = 1;\n\tuart_initted = true;\n\treturn 1;\n#endif\n'
            '\tsoc_base = pe_arm_get_soc_base_phys();')
    # Route serial output to RAM before any UART lookup, even without arm-io.
    replace('pexpert/arm/pe_serial.c', 'uart_putc(char c)\n{',
            'uart_putc(char c)\n{\n#if defined(A52Q)\n\tsweet_early_putc(c);\n\treturn;\n#endif')
    # The A52 never executes the two SWEET framebuffer blocks in start.s.
    replace('osfmk/arm64/start.s', '#if !VMAPPLE && !defined(SWEET)',
            '#if !VMAPPLE && !defined(SWEET) && !defined(A52Q)')
    replace('osfmk/arm64/start.s', '#if defined(SWEET)\n\t/* Complete local TLB',
            '#if defined(SWEET) || defined(A52Q)\n\t/* Complete local TLB')
    # A no-stack, MMU-off marker identifies real XNU entry even if its MMU
    # bootstrap faults before C code. Each of three copies carries a CRC32.
    entry = b'A52QXNU ENTRY v1\n'
    frame = entry + f'crc32={zlib.crc32(entry):08x}\n'.encode() + b'A52QXNU END\n'
    record = frame * 3
    padded = record + bytes(-len(record) % 4)
    asm = ['#if defined(A52Q)', '\tMOV64 x0, A52Q_RAMLOG_BASE', '\tstr wzr, [x0]']
    for offset in range(0, len(padded), 4):
        value, = struct.unpack_from('<I', padded, offset)
        asm += [f'\tMOV64 x1, {value}', f'\tstr w1, [x0, #{12 + offset}]']
    asm += [f'\tmov w1, #{len(record)}', '\tstr w1, [x0, #4]', '\tstr w1, [x0, #8]',
            '\tdsb sy', '\tMOV64 x1, 0x43474244', '\tstr w1, [x0]', '\tdsb sy', '#endif', '']
    replace('osfmk/arm64/start.s', '\tmov\t\tx21, #0\n', '\tmov\t\tx21, #0\n' + '\n'.join(asm))
    # No current CPU/bus clock was captured. Leave those ADT fields absent,
    # report zero, and avoid pe_identify_machine's unconditional divide by zero.
    replace('pexpert/arm/pe_identify_machine.c', '\t/* Set the num / den pairs form the hz values. */',
            '#if defined(A52Q)\n\tif (gPEClockFrequencyInfo.bus_clock_rate_hz == 0) {\n'
            '\t\tgPEClockFrequencyInfo.bus_clock_rate_num = 0;\n'
            '\t\tgPEClockFrequencyInfo.bus_clock_rate_den = 1;\n'
            '\t\tgPEClockFrequencyInfo.bus_to_cpu_rate_num = 0;\n'
            '\t\tgPEClockFrequencyInfo.bus_to_cpu_rate_den = 1;\n'
            '\t\tgPEClockFrequencyInfo.bus_to_dec_rate_num = 0;\n'
            '\t\tgPEClockFrequencyInfo.bus_to_dec_rate_den = 1;\n\t\treturn;\n\t}\n#endif\n'
            '\t/* Set the num / den pairs form the hz values. */')
    marker = '\t/* Ensure TTEs are visible */'
    mapping = '''#if defined(A52Q)
    /* One L3 table for ONLY the reserved console. RAM is below 64 GiB,
     * hence V=P L1 index zero, whose L2 was allocated first. */
    adrp x6, EXT(a52q_console_l3)@page
    add x6, x6, EXT(a52q_console_l3)@pageoff
    MOV64 x10, A52Q_RAMLOG_BASE
    and x11, x10, #(ARM_TT_L3_INDEX_MASK)
    lsr x11, x11, #(ARM_TT_L3_SHIFT)
    add x11, x6, x11, lsl #TTE_SHIFT
    mov x12, #(A52Q_RAMLOG_SIZE / ARM_PGBYTES)
    MOV64 x13, (ARM_TTE_VALID | ARM_TTE_TYPE_TABLE | ARM_TTE_BLOCK_SH(SH_OUTER_MEMORY) | ARM_TTE_BLOCK_ATTRINDX(CACHE_ATTRINDX_DISABLE) | ARM_TTE_BLOCK_AF | ARM_TTE_BLOCK_PNX | ARM_TTE_BLOCK_NX)
La52q_console_pages:
    orr x9, x10, x13
    str x9, [x11], #8
    add x10, x10, #ARM_PGBYTES
    subs x12, x12, #1
    b.ne La52q_console_pages
    orr x6, x6, #(ARM_TTE_VALID | ARM_TTE_TYPE_TABLE)
    MOV64 x10, A52Q_RAMLOG_BASE
    and x12, x10, #(ARM_TT_L2_INDEX_MASK)
    lsr x12, x12, #(ARM_TT_L2_SHIFT)
    add x13, x25, #(2 * ARM_PGBYTES)
    str x6, [x13, x12, lsl #TTE_SHIFT]
#endif

'''
    replace('osfmk/arm64/start.s', marker, mapping + marker)
    # Reuse the exact L3 console pages in final TTBR1; do not map a 32 MiB block.
    mapping = '''#if defined(A52Q)
#define A52Q_EARLY_VA (VM_MIN_KERNEL_ADDRESS + ARM_TT_L2_SIZE)
extern uint64_t a52q_console_l3[2048];
static void a52q_early_map_final(void)
{
    vm_map_address_t va = A52Q_EARLY_VA;
    assert(va + ARM_TT_L2_SIZE <= gVirtBase);
    tt_entry_t l1 = cpu_tte[(va & ARM_TT_L1_INDEX_MASK) >> ARM_TT_L1_SHIFT];
    assert((l1 & (ARM_TTE_VALID | ARM_TTE_TYPE_MASK)) == (ARM_TTE_VALID | ARM_TTE_TYPE_TABLE));
    tt_entry_t *l2 = (tt_entry_t *)phystokv(l1 & ARM_TTE_TABLE_MASK);
    tt_entry_t *slot = &l2[(va & ARM_TT_L2_INDEX_MASK) >> ARM_TT_L2_SHIFT];
    assert(*slot == ARM_TTE_EMPTY);
    *slot = kvtophys((vm_offset_t)a52q_console_l3) | ARM_TTE_VALID | ARM_TTE_TYPE_TABLE;
    __asm__ volatile("dsb ishst" ::: "memory");
}
#endif

'''
    replace('osfmk/arm64/arm_vm_init.c', 'void\narm_vm_init(uint64_t memory_size, boot_args * args)',
            mapping + 'void\narm_vm_init(uint64_t memory_size, boot_args * args)')
    replace('osfmk/arm64/arm_vm_init.c', '\tarm_vm_physmap_init(args);',
            '#if defined(A52Q)\n\ta52q_early_map_final();\n#endif\n\tarm_vm_physmap_init(args);')
    replace('osfmk/arm64/arm_vm_init.c', '\tset_mmu_ttb(invalid_ttep & TTBR_BADDR_MASK);',
            '#if defined(A52Q)\n\tsweet_early_relocate(A52Q_EARLY_VA + (A52Q_RAMLOG_BASE & (ARM_TT_L2_SIZE - 1)));\n#endif\n'
            '\tset_mmu_ttb(invalid_ttep & TTBR_BADDR_MASK);')
    # All checks above complete before writing any source file.
    for name, text in changes.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode('utf-8'))
    report = {'target': 'A52Q', 'status': 'source overlay applied, not a boot claim',
              'filesystem': filesystem,
              'shared_software_guards': COMMON,
              'files_sha256': {n: hashlib.sha256(t.encode()).hexdigest() for n, t in changes.items()}}
    (root / 'a52q-overlay.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'A52Q overlay: {len(changes)} files; SWEET macro remains undefined on A52.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--filesystem', choices=('mockfs', 'hfs'), default='mockfs')
    a = p.parse_args()
    try:
        apply(a.source, filesystem=a.filesystem)
    except (ValueError, OSError) as e:
        p.exit(1, f'A52Q overlay rejected: {e}\n')
