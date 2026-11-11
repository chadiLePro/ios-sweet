#!/usr/bin/env python3
"""Prepare an A52 bootstrap ADT and embedded XNU payload from captured evidence.

No Apple userland, framebuffer descriptor, storage nodes or device writes.
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


def make_adt(base, total, gic, frequency, intid, mpidr, seed=None):
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
    return node('device-tree', [('compatible', cstr('samsung,a52q') + cstr('qcom,sm7125')),
        ('model', cstr('Samsung SM-A525F/DS XNU bootstrap')),
        ('#address-cells', u32(2)), ('#size-cells', u32(2))],
        [chosen, node('defaults'), node('cpus', [('#address-cells', u32(1)),
            ('#size-cells', u32(0))], [cpu]),
         node('arm-io', [('device_type', cstr('a52q-io')), ('#address-cells', u32(2)),
             ('#size-cells', u32(2)), ('ranges', u64(0, soc, extent))], [gic_node]),
         node('pram', [('reg', u64(base + memory, PANIC))])])


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
        strx, _, _, _, value = struct.unpack_from('<IBBHQ', data, symoff + 16 * i)
        if strx >= strsize:
            raise ValueError('symbol string index exceeds table')
        if data[stroff + strx:stroff + strx + len(table_name)] == table_name:
            tables.append(value)
    if len(tables) != 1 or tables[0] % PAGE:
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
    p.add_argument('--qemu-dtb', type=Path, help='QEMU-generated virt DTB; makes a payload that phone packaging rejects')
    p.add_argument('--qemu-diagnostic', type=Path, help='matching QEMU loader diagnostic result with measured CNTFRQ')
    a = p.parse_args()
    try:
        if a.out.exists() or a.memory_mib < 128 or a.memory_mib > 1024 or a.memory_mib % 32:
            raise ValueError('output exists or invalid memory budget (128..1024 MiB, multiple of 32)')
        kernel = a.kernel.read_bytes()
        validate_kernel(kernel)
        total = a.memory_mib << 20
        base, gic, hz, intid, mpidr, dt_hash = hardware(a.evidence, a.cpu_log, total)
        environment = 'SM-A525F/DS hardware candidate'
        if bool(a.qemu_dtb) != bool(a.qemu_diagnostic):
            raise ValueError('QEMU DTB and diagnostic must be supplied together')
        if a.qemu_dtb:
            emu = Fdt(a.qemu_dtb.read_bytes())
            measured = json.loads(a.qemu_diagnostic.read_text())
            if not measured.get('scope', '').startswith('QEMU virt') or 'error' in measured:
                raise ValueError('not a successful QEMU diagnostic result')
            cpu = measured['loader_record']
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
            if not any(lo <= base and base + total <= lo + size for lo, size in banks):
                raise ValueError('QEMU RAM does not cover the payload destination')
            environment = 'QEMU virt ONLY; never flash'
        a.out.parent.mkdir(parents=True, exist_ok=True)
        tree_path = a.out.with_suffix('.adt')
        tree_path.write_bytes(adt.serialize(make_adt(base, total, gic, hz, intid, mpidr)))
        payload, info = mkpayload.build(str(a.kernel), str(tree_path),
                                       'debug=0xc serial=3 cpus=1 keepsyms=1 -v rd=md0')
        report = {'target': 'A52Q', 'status': 'bootstrap payload; physical RAM access not yet verified',
                  'environment': environment,
                  'phys_base': hex(base), 'mem_size': hex(total - PANIC), 'panic_log_size': hex(PANIC),
                  'live_dtb_sha256': dt_hash, 'kernel_sha256': hashlib.sha256(kernel).hexdigest(),
                  'cpu_log_sha256': hashlib.sha256(a.cpu_log.read_bytes()).hexdigest(),
                  'payload_sha256': hashlib.sha256(payload).hexdigest(), 'macho': info,
                  'timer_hz': hz, 'virtual_timer_intid': intid, 'gic_reg': gic,
                  'root_filesystem': 'none yet; rd=md0 is intentional next-stage boot target'}
        validate_payload(payload, report)
        a.out.write_bytes(payload)
        a.out.with_suffix(a.out.suffix + '.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    except (OSError, ValueError, KeyError, AssertionError, struct.error, IndexError) as exc:
        p.exit(1, f'A52 payload rejected: {exc}\n')


if __name__ == '__main__':
    main()
