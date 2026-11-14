#!/usr/bin/env python3
"""Prepare an A52 bootstrap ADT and embedded XNU payload from captured evidence.

No Apple userland or device writes. Hardware-only diagnostic nodes are opt-in.
RAM placement is a conservative snapshot candidate; the shim probes it at boot.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct

import adt
import mkpayload
from a52q_diag_log import decode_checked_console
from a52q_memory import plan, check_placement
from fdt_evidence import Fdt, physical_regs
from mkadt import node, u32, u64, cstr

BLOCK, PAGE, PANIC = 0x2000000, 0x4000, 0x100000


def qemu_placement(banks, total, excluded):
    """Software allocation in emulated RAM only; not a Samsung memory map."""
    for lo, size in banks:
        candidate = (lo + BLOCK - 1) & ~(BLOCK - 1)
        for start, end in sorted(excluded):
            if candidate + total <= start:
                break
            if candidate < end and start < candidate + total:
                candidate = (end + BLOCK - 1) & ~(BLOCK - 1)
        if candidate + total <= lo + size and all(
                candidate + total <= start or end <= candidate for start, end in excluded):
            return candidate
    raise ValueError('emulated RAM cannot fit the bootstrap outside boot data and console')


def validate_bootstrap_init(data):
    """Accept a small static arm64 Mach-O, not a disk image or Apple dyld app.

    This checks container geometry only; XNU still validates execution/signing.
    Our supported producer is tools/mkinit.py with the syscall-only init source.
    """
    if not PAGE <= len(data) <= 1 << 20:
        raise ValueError('bootstrap init must be a small static executable')
    magic, cpu, sub, kind, count, size, _, _ = struct.unpack_from('<8I', data)
    if (magic != 0xfeedfacf or cpu != 0x100000c or sub & 0xffffff or kind != 2 or
            not 1 <= count <= 64 or size > len(data) - 32):
        raise ValueError('bootstrap init must be thin plain arm64 MH_EXECUTE')
    off, entry, executable, signature = 32, None, [], False
    for _ in range(count):
        if off + 8 > 32 + size:
            raise ValueError('truncated bootstrap init command')
        cmd, length = struct.unpack_from('<II', data, off)
        if length < 8 or length % 8 or off + length > 32 + size:
            raise ValueError('invalid bootstrap init command')
        if cmd == 0x19:
            if length < 72:
                raise ValueError('truncated bootstrap init segment')
            va, mem, pos, disk, maximum, prot, sections, _ = struct.unpack_from('<4Q4I', data, off + 24)
            if (length != 72 + sections * 80 or va + mem >= 1 << 64 or disk > mem or
                    pos > len(data) or disk > len(data) - pos or prot & ~maximum or prot & 2):
                raise ValueError('unsupported bootstrap init segment')
            if prot & 4:
                executable.append((va, va + disk))
        elif cmd == 5:
            if length != 288 or entry is not None or struct.unpack_from('<2I', data, off + 8) != (6, 68):
                raise ValueError('unsupported bootstrap init thread state')
            entry, = struct.unpack_from('<Q', data, off + 16 + 32 * 8)
        elif cmd == 0x1d:
            if length != 16 or signature:
                raise ValueError('invalid bootstrap init code signature')
            pos, disk = struct.unpack_from('<2I', data, off + 8)
            if disk < 12 or pos > len(data) or disk > len(data) - pos:
                raise ValueError('bootstrap init signature exceeds file')
            signature = True
        else:
            raise ValueError('bootstrap init has unsupported/dynamic load commands')
        off += length
    if off != 32 + size or not signature or entry is None or not any(a <= entry < b for a, b in executable):
        raise ValueError('bootstrap init lacks a static entry or signature')


def make_adt(base, total, gic, frequency, intid, mpidr, seed=None, ufs_test=None, display_test=None, ufs_root=None):
    if base % BLOCK or total < 4 * BLOCK or total % BLOCK or not 16 <= intid < 32:
        raise ValueError('unsupported bootstrap memory/timer geometry')
    memory = total - PANIC
    soc = min(b for b, _ in gic)
    extent = max(b + n for b, n in gic) - soc
    cpu = node('cpu0', [('device_type', cstr('cpu')), ('compatible', cstr('ARM,v8')),
        ('reg', u32(mpidr & 0xffff)), ('cpu-id', u32(0)), ('cluster-id', u32(0)),
        ('cluster-type', u32(0)), ('die-cluster-id', u32(0)), ('cluster-core-id', u32(0)),
        ('state', cstr('running')), ('timebase-frequency', u32(frequency)),
        ('fixed-frequency', u32(frequency))])
    chosen = node('chosen', [('dram-base', u64(base)), ('dram-size', u64(memory)),
        ('random-seed', seed if seed is not None else os.urandom(64)),
        ('debug-enabled', u32(1)), ('embedded-panic-log-size', u32(PANIC)),
        ('firmware-version', cstr('a52q-xnu-bootstrap'))], [node('memory-map')])
    gic_node = node('gic', [('compatible', cstr('arm,gic-v3')), ('interrupt-controller', b''),
        ('virtual-timer-intid', u32(intid)),
        ('reg', u64(*[v for b, n in gic for v in (b - soc, n)]))])
    result = node('device-tree', [('compatible', cstr('samsung,a52q') + cstr('qcom,sm7125')),
        ('model', cstr('Samsung SM-A525F/DS XNU bootstrap')),
        ('#address-cells', u32(2)), ('#size-cells', u32(2))],
        [chosen, node('defaults'), node('cpus', [('#address-cells', u32(1)),
            ('#size-cells', u32(0))], [cpu]),
         node('arm-io', [('device_type', cstr('a52q-io')), ('#address-cells', u32(2)),
             ('#size-cells', u32(2)), ('ranges', u64(0, soc, extent))], [gic_node]),
         node('pram', [('reg', u64(base + memory, PANIC))])])
    if ufs_test:
        from a52q_ufs_selftest import adt_node
        result.children.append(adt_node(ufs_test))
    if display_test:
        from a52q_display_selftest import adt_node
        result.children.append(adt_node(display_test))
    if ufs_root:
        if ufs_root.get('layout_kind') == 2:
            from a52q_persistent_root import adt_node, validate_config
        else:
            from a52q_ufs_root import adt_node, validate_config
        if not ufs_test: raise ValueError('UFS root requires the physical UFS selftest configuration')
        validate_config(ufs_root, ufs_test)
        result.children.append(adt_node(ufs_root))
    return result


def validate_kernel(data):
    if len(data) < 32:
        raise ValueError('truncated kernel Mach-O')
    magic, cpu, sub, _, count, size, _, _ = struct.unpack_from('<8I', data)
    if magic != 0xfeedfacf or cpu != 0x100000c or sub & 0xffffff != 0:
        raise ValueError('need a thin, plain arm64 kernel, not arm64e or a fat binary')
    if not 1 <= count <= 1024 or size > len(data) - 32:
        raise ValueError('invalid Mach-O command area')
    off = 32
    symtab = None
    segments = []
    for _ in range(count):
        if off + 8 > 32 + size:
            raise ValueError('truncated Mach-O command')
        cmd, length = struct.unpack_from('<II', data, off)
        if length < 8 or length % 8 or off + length > 32 + size:
            raise ValueError('invalid Mach-O command length')
        if cmd == 0x19:
            if length < 72:
                raise ValueError('truncated segment command')
            va, mem, pos, disk = struct.unpack_from('<4Q', data, off + 24)
            name = data[off + 8:off + 24].split(b'\0')[0]
            # XNU ctf_insert adds file-only __CTF metadata with vmsize=0.
            # It is bounds checked here and intentionally not loaded by mkpayload.
            file_only_ctf = name == b'__CTF' and mem == 0
            if va + mem > 1 << 64 or (disk > mem and not file_only_ctf) or pos > len(data) or disk > len(data) - pos:
                raise ValueError('segment exceeds file or address space')
            if mem:
                segments.append((va, va + mem))
        elif cmd == 2:
            if length != 24:
                raise ValueError('invalid Mach-O symbol table command')
            symtab = struct.unpack_from('<4I', data, off + 8)
        off += length
    if off != 32 + size:
        raise ValueError('Mach-O commands do not fill declared area')
    # blacktop pins the version banner to the XNU commit, omitting the board.
    # Check the A52-only exported table and console instead of inventing a banner.
    if any(marker not in data for marker in (b'_a52q_console_l3\0',
            b'A52QXNU stage=0x', b'kernel RAM-console VA live\0')):
        raise ValueError('kernel lacks the A52Q page table and RAM console identity')
    if not symtab:
        raise ValueError('kernel has no symbols to verify page-table alignment')
    symoff, count, stroff, strsize = symtab
    if (count > 1000000 or symoff + count * 16 > len(data) or stroff + strsize > len(data)):
        raise ValueError('Mach-O symbol table exceeds file')
    tables = []
    table_name = b'_a52q_console_l3\0'
    for i in range(count):
        strx, kind, section, _, value = struct.unpack_from('<IBBHQ', data, symoff + 16 * i)
        if strx >= strsize:
            raise ValueError('symbol string index exceeds table')
        if data[stroff + strx:stroff + strx + len(table_name)] == table_name:
            # A raw relink retains N_GSYM/STABS debug entries with value zero.
            # XNU's full build strips these after dsymutil. They are not symbol
            # definitions (mach-o/nlist.h: N_STAB=0xe0, N_TYPE=0x0e, N_SECT=0x0e).
            if kind & 0xe0:
                continue
            if kind & 0x0e != 0x0e or section == 0:
                raise ValueError('A52 RAM-console L3 table is not a defined section symbol')
            tables.append(value)
    if (len(tables) != 1 or tables[0] % PAGE or
            not any(lo <= tables[0] and tables[0] + PAGE <= hi for lo, hi in segments)):
        raise ValueError('A52 RAM-console L3 table is not uniquely 16 KiB aligned')


def validate_payload(data, manifest):
    if hashlib.sha256(data).hexdigest() != manifest['payload_sha256'] or manifest['target'] != 'A52Q':
        raise ValueError('payload manifest mismatch')
    if len(data) < 0x2a8 or data[:8] != b'SWEETXNU':
        raise ValueError('invalid payload container')
    version, count = struct.unpack_from('<II', data, 8)
    virt, entry, adt_off, adt_size, end, phys, memory = struct.unpack_from('<7Q', data, 16)
    if (version != 1 or not 1 <= count <= 64 or 0x2a8 + count * 32 > len(data) or
            phys != int(manifest['phys_base'], 16) or memory != int(manifest['mem_size'], 16) or
            phys % BLOCK or memory % PAGE or not 0 < memory <= 1 << 32 or
            phys + memory >= 1 << 36 or end < virt or end - virt >= memory or
            adt_size <= 0 or adt_off % 8 or adt_off > len(data) or adt_size > len(data) - adt_off or
            data[0x2a7] != 0):
        raise ValueError('invalid payload geometry')
    intervals, entry_ok = [], False
    for i in range(count):
        va, mem, pos, disk = struct.unpack_from('<4Q', data, 0x2a8 + i * 32)
        if (va < virt or va % PAGE or mem <= 0 or disk > mem or va > end or mem > end - va or
                pos < 0x2a8 + count * 32 or pos > adt_off or disk > adt_off - pos):
            raise ValueError('invalid payload segment')
        if intervals and va < intervals[-1][1]:
            raise ValueError('payload segments overlap or are not sorted')
        intervals.append((va, va + mem))
        entry_ok |= va <= entry < va + disk
    top = ((end - virt + adt_size + PAGE - 1) // PAGE + 1) * PAGE
    if not entry_ok or top > memory:
        raise ValueError('entry or boot data lies outside kernel RAM')
    tree, used = adt.parse(data[adt_off:adt_off + adt_size])
    if used != adt_size or tree.name != 'device-tree':
        raise ValueError('invalid ADT')
    tests = [c for c in tree.children if c.name == 'a52q-ufs-selftest']
    ufs_test = manifest.get('ufs_selftest')
    if tests or ufs_test:
        if len(tests) != 1 or not ufs_test or manifest.get('environment') != 'SM-A525F/DS hardware candidate':
            raise ValueError('UFS selftest must be explicitly hardware-bound and have exactly one ADT node')
        from a52q_ufs_selftest import adt_node
        if tests[0].props != adt_node(ufs_test).props:
            raise ValueError('UFS selftest ADT differs from validated proof configuration')
    displays = [c for c in tree.children if c.name == 'a52q-display-selftest']
    display_test = manifest.get('display_selftest')
    if displays or display_test:
        if len(displays) != 1 or not display_test or manifest.get('environment') != 'SM-A525F/DS hardware candidate':
            raise ValueError('display selftest must be explicitly hardware-bound and have exactly one ADT node')
        from a52q_display_selftest import adt_node
        if displays[0].props != adt_node(display_test).props:
            raise ValueError('display selftest ADT differs from validated proof configuration')
        fb, size = display_test['reg']
        if fb < phys + memory + PANIC and phys < fb + size:
            raise ValueError('display reservation overlaps kernel RAM/panic log')
    roots = [c for c in tree.children if c.name == 'a52q-ufs-root']
    if manifest.get('ufs_diagnostic_root') and manifest.get('ufs_ios_root'):
        raise ValueError('only one UFS root layout may be selected')
    ios_root = manifest.get('ufs_ios_root')
    ufs_root = manifest.get('ufs_diagnostic_root') or ios_root
    if roots or ufs_root:
        if len(roots) != 1 or not ufs_root or not ufs_test or manifest.get('environment') != 'SM-A525F/DS hardware candidate':
            raise ValueError('UFS root must be hardware-bound with a physical selftest and exactly one ADT node')
        if ios_root:
            from a52q_persistent_root import adt_node, validate_config
            if ios_root['kernel_sha256'] != manifest.get('kernel_sha256'):
                raise ValueError('full root plan kernel hash differs')
        else:
            from a52q_ufs_root import adt_node, validate_config
            from a52q_hfs_root import hardware_root_proof
            hardware_root_proof(ufs_root['qemu_boot_proof'], manifest.get('kernel_sha256'), ufs_root['sha256'])
        validate_config(ufs_root, ufs_test)
        if roots[0].props != adt_node(ufs_root).props:
            raise ValueError('UFS root ADT differs from validated proof configuration')
        command = data[0x48:0x2a8].split(b'\0', 1)[0].split()
        if [v for v in command if v.startswith(b'rd=')] != [b'rd=a52ios0' if ios_root else b'rd=a52root0'] or any(
                v.startswith((b'rootrw=', b'ufsrw=')) for v in command):
            raise ValueError('disk root needs exactly its selected rd=a52root0 or rd=a52ios0 and no writable-root flags')
    chosen = next(c for c in tree.children if c.name == 'chosen')
    if chosen.prop('dram-base') != u64(phys) or chosen.prop('dram-size') != u64(memory):
        raise ValueError('ADT RAM differs from loader RAM')
    mmap = next(c for c in chosen.children if c.name == 'memory-map')
    ramdisk = mmap.prop('RAMDisk')
    if ufs_root and (ramdisk is not None or manifest.get('bootstrap_init') or manifest.get('hfs_test_root')):
        raise ValueError('UFS root cannot include a RAM-root fallback')
    if ramdisk is not None:
        if len(ramdisk) != 16:
            raise ValueError('invalid RAMDisk property')
        rd_phys, rd_size = struct.unpack('<2Q', ramdisk)
        if (rd_size <= 0 or rd_phys % PAGE or rd_size % PAGE or
                rd_phys < phys or rd_phys + rd_size > phys + memory or
                intervals[-1] != (rd_phys - phys + virt, rd_phys - phys + virt + rd_size) or
                intervals[-1][1] != end):
            raise ValueError('RAMDisk does not match the final protected loader segment')
        init = manifest.get('bootstrap_init')
        hfs = manifest.get('hfs_test_root')
        _, _, pos, disk = struct.unpack_from('<4Q', data, 0x2a8 + (count - 1) * 32)
        root = hfs or init
        if not root or (hfs and init) or root['sha256'] != hashlib.sha256(data[pos:pos + disk]).hexdigest() or root['bytes'] != disk:
            raise ValueError('bootstrap init/root manifest mismatch')
        if hfs:
            if manifest.get('environment') != 'QEMU virt ONLY; never flash':
                if manifest.get('environment') != 'SM-A525F/DS hardware candidate':
                    raise ValueError('unsupported HFS diagnostic environment')
                from a52q_hfs_root import hardware_root_proof
                hardware_root_proof(hfs.get('qemu_boot_proof', {}), manifest.get('kernel_sha256', ''), hfs['sha256'])
            from a52q_hfs_root import validate_hfs_test_root
            if hfs.get('volume') != validate_hfs_test_root(data[pos:pos + disk]):
                raise ValueError('HFS volume manifest mismatch')
        else:
            validate_bootstrap_init(data[pos:pos + disk])
    elif manifest.get('bootstrap_init') or manifest.get('hfs_test_root'):
        raise ValueError('bootstrap init/root manifest has no RAMDisk')


def hardware(evidence, console, total):
    data = (evidence / 'live.dtb').read_bytes()
    tree = Fdt(data)
    if 'a52q' not in ' '.join(tree.nodes['/'].strings('model')).lower():
        raise ValueError('evidence does not identify A52Q')
    cpu = decode_checked_console(console.read_bytes())['fields']
    if cpu['stage'] != 2 or cpu['current_el'] != 4 or cpu['exception_slot'] or cpu['sctlr'] & 5:
        raise ValueError('need an intact, fault-free EL1/MMU-off diagnostic')
    gics = [n for n in tree.nodes.values() if n.enabled() and 'arm,gic-v3' in n.strings('compatible')]
    timers = [n for n in tree.nodes.values() if n.enabled() and 'arm,armv8-timer' in n.strings('compatible')]
    if len(gics) != 1 or len(timers) != 1:
        raise ValueError('need one GIC and timer')
    gic = physical_regs(gics[0])
    if len(gic) != 2:
        raise ValueError('unsupported GIC register layout')
    timer = timers[0]
    if timer.cell('clock-frequency') != cpu['cntfrq']:
        raise ValueError('CPU timer frequency differs from FDT')
    interrupts = timer.props['interrupts']
    if len(interrupts) != 48:
        raise ValueError('unsupported architected timer interrupt binding')
    kind, ppi, flags = struct.unpack_from('>3I', interrupts, 24)
    if kind != 1 or ppi >= 16 or flags & 15 != 8:
        raise ValueError('virtual timer is not a level-low PPI')
    report = plan(tree, (evidence / 'iomem.txt').read_text())
    for candidate in report['candidates']:
        base = (int(candidate['base'], 16) + BLOCK - 1) & ~(BLOCK - 1)
        if base + total <= int(candidate['end_exclusive'], 16):
            check_placement(report, base, total)
            return base, gic, cpu['cntfrq'], ppi + 16, cpu['mpidr'], hashlib.sha256(data).hexdigest()
    raise ValueError('no snapshot candidate fits the requested kernel RAM budget')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kernel', required=True, type=Path)
    p.add_argument('--evidence', required=True, type=Path)
    p.add_argument('--cpu-log', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--memory-mib', type=int, default=256)
    p.add_argument('--bootstrap-init', type=Path,
                   help='static diagnostic PID1 from mkinit.py, served by mockfs; not Apple launchd')
    p.add_argument('--hfs-test-root', type=Path,
                   help='small fsck-checked HFS+ diagnostic RAM root; hardware additionally needs --hfs-qemu-proof')
    p.add_argument('--hfs-qemu-proof', type=Path,
                   help='QEMU result.json proving this exact kernel/root reached diagnostic PID1; hardware only')
    p.add_argument('--ufs-selftest-build', type=Path, help='successful physical shim one-block-read build.json')
    p.add_argument('--ufs-selftest-log', type=Path, help='matching CRC-checked physical read console')
    p.add_argument('--ufs-diagnostic-root', type=Path, help='small QEMU-proven HFS fixture for read-only BOOT padding')
    p.add_argument('--ufs-ios-root-plan', type=Path, help='stream-verified 16 GiB full-root plan; root stays on UFS, never embedded in BOOT/RAM')
    p.add_argument('--ufs-root-qemu-proof', type=Path, help='same kernel/HFS fixture must have reached PID1 in QEMU')
    p.add_argument('--ufs-root-gpt-capture', type=Path, help='CRC-checked captured GPT and live sysfs bounds')
    p.add_argument('--display-selftest-build', type=Path, help='successful standalone physical display build.json')
    p.add_argument('--display-selftest-log', type=Path, help='matching CRC-checked physical refresh console')
    p.add_argument('--display-register-sources', type=Path, help='pinned Samsung display register sources')
    p.add_argument('--qemu-dtb', type=Path, help='QEMU-generated virt DTB; makes a payload that phone packaging rejects')
    p.add_argument('--qemu-diagnostic', type=Path, help='matching QEMU loader diagnostic result with measured CNTFRQ')
    p.add_argument('--qemu-lowmem', action='store_true',
                   help='allocate within emulated low RAM instead of testing the phone high-RAM placement')
    a = p.parse_args()
    try:
        if a.out.exists() or a.memory_mib < 128 or a.memory_mib > 1024 or a.memory_mib % 32:
            raise ValueError('output exists or invalid memory budget (128..1024 MiB, multiple of 32)')
        kernel = a.kernel.read_bytes()
        validate_kernel(kernel)
        display_test = None
        display_args = (a.display_selftest_build, a.display_selftest_log, a.display_register_sources)
        if any(display_args):
            if not all(display_args) or a.qemu_dtb or b'A52Q display selftest: guarded kernel mapping' not in kernel:
                raise ValueError('display test needs new kernel, physical placement, proof build/log and pinned sources')
            from a52q_display_selftest import configuration as display_configuration
            display_test = display_configuration(a.evidence, a.display_register_sources,
                json.loads(a.display_selftest_build.read_text()), a.display_selftest_log.read_bytes())
        ufs_test = None
        if bool(a.ufs_selftest_build) != bool(a.ufs_selftest_log):
            raise ValueError('kernel UFS test needs both physical proof artifacts')
        if a.ufs_selftest_build:
            if a.qemu_dtb or b'A52Q UFS selftest: new kernel DMA pool' not in kernel:
                raise ValueError('UFS test needs the new kernel implementation and actual hardware placement')
            from a52q_ufs_selftest import configuration as ufs_configuration
            ufs_test = ufs_configuration(a.evidence, json.loads(a.ufs_selftest_build.read_text()),
                                         a.ufs_selftest_log.read_bytes())
        init = None
        hfs_root = None
        ufs_root = None
        root_args = (a.ufs_diagnostic_root, a.ufs_root_qemu_proof, a.ufs_root_gpt_capture)
        if any(root_args):
            if (not all(root_args) or a.qemu_dtb or not ufs_test or a.bootstrap_init or a.hfs_test_root or
                    b'A52Q UFS diagnostic root: bounded read-only BOOT tail' not in kernel):
                raise ValueError('disk root needs new kernel, UFS proof, GPT capture, QEMU root proof and no RAM root')
            from a52q_ufs_root import configuration as root_configuration
            from a52q_hfs_root import read_test_root
            ufs_root = root_configuration(a.ufs_root_gpt_capture, ufs_test, read_test_root(a.ufs_diagnostic_root),
                hashlib.sha256(kernel).hexdigest(), json.loads(a.ufs_root_qemu_proof.read_text()))
        if a.ufs_ios_root_plan:
            if (any(root_args) or a.qemu_dtb or not ufs_test or a.bootstrap_init or a.hfs_test_root or
                    b'A52Q UFS iOS root: bounded read-only userdata window' not in kernel):
                raise ValueError('full disk root needs new kernel, physical UFS proof and no diagnostic/RAM root')
            from a52q_persistent_root import bind_plan
            ufs_root = bind_plan(json.loads(a.ufs_ios_root_plan.read_text()), ufs_test,
                                 hashlib.sha256(kernel).hexdigest())
        if a.hfs_qemu_proof and (not a.hfs_test_root or a.qemu_dtb):
            raise ValueError('HFS QEMU proof is only for a physical HFS diagnostic root')
        root_path = a.bootstrap_init or a.hfs_test_root
        if a.hfs_test_root:
            if a.bootstrap_init or (not a.qemu_dtb and not a.hfs_qemu_proof):
                raise ValueError('HFS diagnostic excludes mockfs init and requires QEMU mode or matching boot proof')
            from a52q_hfs_root import validate_hfs_test_root, read_test_root
            init_data = read_test_root(a.hfs_test_root)
            hfs_root = {'sha256': hashlib.sha256(init_data).hexdigest(), 'bytes': len(init_data),
                        'volume': validate_hfs_test_root(init_data)}
            if a.hfs_qemu_proof:
                from a52q_hfs_root import hardware_root_proof
                proof_data = a.hfs_qemu_proof.read_bytes()
                hfs_root['qemu_boot_proof'] = hardware_root_proof(json.loads(proof_data),
                    hashlib.sha256(kernel).hexdigest(), hfs_root['sha256'])
                hfs_root['qemu_report_sha256'] = hashlib.sha256(proof_data).hexdigest()
        if a.bootstrap_init:
            init_data = a.bootstrap_init.read_bytes()
            validate_bootstrap_init(init_data)
            init = {'sha256': hashlib.sha256(init_data).hexdigest(), 'bytes': len(init_data),
                    'scope': 'static diagnostic PID1 via mockfs; not Apple launchd'}
        total = a.memory_mib << 20
        base, gic, hz, intid, mpidr, dt_hash = hardware(a.evidence, a.cpu_log, total)
        environment = 'SM-A525F/DS hardware candidate'
        if a.qemu_lowmem and not a.qemu_dtb:
            raise ValueError('low-memory allocation is QEMU-only')
        if bool(a.qemu_dtb) != bool(a.qemu_diagnostic):
            raise ValueError('QEMU DTB and diagnostic must be supplied together')
        if a.qemu_dtb:
            emu = Fdt(a.qemu_dtb.read_bytes())
            measured = json.loads(a.qemu_diagnostic.read_text())
            if not measured.get('scope', '').startswith('QEMU virt') or 'error' in measured:
                raise ValueError('not a successful QEMU diagnostic result')
            cpu = measured.get('loader_record', measured.get('diagnostic'))
            if not cpu or ('diagnostic' in measured and measured.get('status') != 'passed'):
                raise ValueError('QEMU diagnostic did not pass')
            gics = [n for n in emu.nodes.values() if 'arm,gic-v3' in n.strings('compatible')]
            timers = [n for n in emu.nodes.values() if 'arm,armv8-timer' in n.strings('compatible')]
            if len(gics) != 1 or len(timers) != 1 or cpu['current_el'] != 4 or cpu['exception_slot']:
                raise ValueError('unsupported QEMU GIC/timer/CPU setup')
            gic = physical_regs(gics[0])
            # QEMU may provide a separate second redistributor region for a
            # large vCPU capacity; the single boot CPU only uses the first.
            gic = gic[:2]
            kind, ppi, _ = struct.unpack_from('>3I', timers[0].props['interrupts'], 24)
            if kind != 1 or not 0 <= ppi < 16 or cpu['cntfrq'] <= 0:
                raise ValueError('invalid QEMU virtual timer')
            hz, intid, mpidr = cpu['cntfrq'], ppi + 16, cpu['mpidr']
            banks = [r for n in emu.nodes['/'].children
                     if n.strings('device_type') == ['memory'] for r in physical_regs(n)]
            if a.qemu_lowmem:
                from a52q_ramoops import configuration
                log = configuration(a.evidence)
                # Reserve generous whole software blocks around the Linux Image
                # and QEMU boot DTB; the loader independently checks actual spans.
                excluded = [(cpu['image'] & ~(BLOCK - 1),
                    (cpu['image'] + len(kernel) + (len(init_data) if root_path else 0) + 2 * BLOCK - 1) & ~(BLOCK - 1)),
                    (cpu['dtb'] & ~(BLOCK - 1), (cpu['dtb'] & ~(BLOCK - 1)) + BLOCK),
                    (log['base'], log['base'] + log['size'])]
                base = qemu_placement(banks, total, excluded)
            if not any(lo <= base and base + total <= lo + size for lo, size in banks):
                raise ValueError('QEMU RAM does not cover the payload destination')
            environment = 'QEMU virt ONLY; never flash'
        a.out.parent.mkdir(parents=True, exist_ok=True)
        tree_path = a.out.with_suffix('.adt')
        tree_path.write_bytes(adt.serialize(make_adt(base, total, gic, hz, intid, mpidr,
                                                   ufs_test=ufs_test, display_test=display_test, ufs_root=ufs_root)))
        payload, info = mkpayload.build(str(a.kernel), str(tree_path),
                                       'debug=0xc serial=3 cpus=1 keepsyms=1 -v -noprogress rd=' +
                                       ('a52ios0' if a.ufs_ios_root_plan else 'a52root0' if ufs_root else 'md0'),
                                       ramdisk_path=str(root_path) if root_path else None)
        report = {'target': 'A52Q', 'status': 'bootstrap payload; physical RAM access not yet verified',
                  'environment': environment,
                  'phys_base': hex(base), 'mem_size': hex(total - PANIC), 'panic_log_size': hex(PANIC),
                  'live_dtb_sha256': dt_hash, 'kernel_sha256': hashlib.sha256(kernel).hexdigest(),
                  'cpu_log_sha256': hashlib.sha256(a.cpu_log.read_bytes()).hexdigest(),
                  'payload_sha256': hashlib.sha256(payload).hexdigest(), 'macho': info,
                  'timer_hz': hz, 'virtual_timer_intid': intid, 'gic_reg': gic,
                  'root_filesystem': 'HFS+ diagnostic RAM root; not Apple userland' if hfs_root else
                                     'mockfs RAM disk with static diagnostic init' if init else
                                     'none yet; rd=md0 is intentional next-stage boot target'}
        if init:
            report['bootstrap_init'] = init
        if hfs_root:
            report['hfs_test_root'] = hfs_root
        if ufs_test:
            report['ufs_selftest'] = ufs_test
        if ufs_root:
            if a.ufs_ios_root_plan:
                report['ufs_ios_root'] = ufs_root
                report['root_filesystem'] = 'read-only full HFS image on userdata; Apple launchd attempt, not an execution claim'
            else:
                report['ufs_diagnostic_root'] = ufs_root
                report['root_filesystem'] = 'read-only HFS diagnostic fixture in BOOT tail, no RAM root or Apple userland'
        if display_test:
            report['display_selftest'] = display_test
        validate_payload(payload, report)
        a.out.write_bytes(payload)
        a.out.with_suffix(a.out.suffix + '.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    except (OSError, ValueError, KeyError, AssertionError, struct.error, IndexError) as exc:
        p.exit(1, f'A52 payload rejected: {exc}\n')


if __name__ == '__main__':
    main()
