#!/usr/bin/env python3
"""Conservative host-only RAM planning from FDT and /proc/iomem snapshots.

Output is a set of candidates for further review, never permission to access RAM.
No MMIO, boot image generation, automatic placement or device writes occur here.
Dynamic pools exclude their ENTIRE allocation windows, not just requested sizes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from fdt_evidence import Fdt, regs

LIMIT = 1 << 64
PAGE = 16384  # XNU arm64 page size; alignment does not prove MMU compatibility.


def interval(base, size):
    if base < 0 or size <= 0 or base + size > LIMIT:
        raise ValueError('invalid physical interval')
    return base, base + size


def merge(ranges):
    result = []
    for lo, hi in sorted(ranges):
        if not 0 <= lo < hi <= LIMIT:
            raise ValueError('invalid interval endpoints')
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(hi, result[-1][1]))
        else:
            result.append((lo, hi))
    return result


def subtract(ranges, excluded):
    result = merge(ranges)
    for lo, hi in merge(excluded):
        remaining = []
        for start, end in result:
            if hi <= start or end <= lo:
                remaining.append((start, end))
            else:
                if start < lo:
                    remaining.append((start, lo))
                if hi < end:
                    remaining.append((hi, end))
        result = remaining
    return result


def iomem_ranges(text):
    ram, occupied = [], []
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'\s*([0-9a-fA-F]+)-([0-9a-fA-F]+)\s*:\s*(\S.*)', line)
        if not match:
            raise ValueError('malformed iomem line')
        first, last = (int(match[i], 16) for i in (1, 2))
        if last < first or last >= LIMIT or (first == 0 and last == 0):
            raise ValueError('invalid or redacted iomem interval')
        item = (first, last + 1)  # Linux prints inclusive ends.
        (ram if match[3] == 'System RAM' else occupied).append(item)
    if not ram:
        raise ValueError('iomem has no System RAM')
    return merge(ram), merge(occupied)


def allocation_windows(node):
    parent = node.parent
    ac, sc = parent.cell('#address-cells'), parent.cell('#size-cells')
    value = node.props.get('alloc-ranges', b'')
    stride = (ac + sc) * 4
    if ac not in (1, 2) or sc not in (1, 2) or not value or len(value) % stride:
        raise ValueError(f'{node.path}: dynamic reservation has no valid bounded alloc-ranges')
    size = node.props.get('size', b'')
    if len(size) != sc * 4 or not 0 < int.from_bytes(size, 'big') < LIMIT:
        raise ValueError(f'{node.path}: invalid dynamic size')
    windows = [interval(int.from_bytes(value[i:i + ac * 4], 'big'),
                        int.from_bytes(value[i + ac * 4:i + stride], 'big'))
               for i in range(0, len(value), stride)]
    if all(hi - lo < int.from_bytes(size, 'big') for lo, hi in windows):
        raise ValueError(f'{node.path}: dynamic size exceeds every allocation window')
    return windows


def plan(fdt, iomem, extra=()):
    root = fdt.nodes['/']
    if root.cell('#address-cells') not in (1, 2) or root.cell('#size-cells') not in (1, 2):
        raise ValueError('unsupported root address cells')
    banks = []
    for node in root.children:
        if node.enabled() and node.strings('device_type') == ['memory']:
            banks += [interval(b, s) for b, s in regs(node)]
    if not banks:
        raise ValueError('no enabled root memory banks')
    # Overlapping banks indicate inconsistent evidence rather than more usable RAM.
    for previous, current in zip(sorted(banks), sorted(banks)[1:]):
        if previous[1] > current[0]:
            raise ValueError('overlapping FDT memory banks')
    reserved = fdt.nodes.get('/reserved-memory')
    if not reserved or not reserved.enabled():
        raise ValueError('missing enabled reserved-memory node')
    if ('ranges' not in reserved.props or reserved.props['ranges'] != b'' or
            any(reserved.cell(k) != root.cell(k) for k in ('#address-cells', '#size-cells'))):
        raise ValueError('reserved-memory physical address translation needs manual review')
    excluded = [interval(b, s) for b, s in fdt.reservations]
    reasons = []
    for node in reserved.children:
        if not node.enabled():
            continue
        if 'reg' in node.props:
            ranges = [interval(b, s) for b, s in regs(node)]
            kind = 'static'
        else:
            ranges = allocation_windows(node)
            kind = 'entire dynamic allocation window'
        excluded += ranges
        reasons.append({'path': node.path, 'kind': kind, 'ranges': render(ranges)})
    linux_ram, linux_occupied = iomem_ranges(iomem)
    intersection = merge((max(a, c), min(b, d)) for a, b in banks for c, d in linux_ram
                         if max(a, c) < min(b, d))
    if not intersection:
        raise ValueError('FDT and iomem RAM do not intersect')
    runtime = [interval(b, s) for b, s in extra]
    candidates = subtract(intersection, excluded + linux_occupied + runtime)
    candidates = [(lo + (-lo % PAGE), hi - hi % PAGE) for lo, hi in candidates]
    candidates = [(lo, hi) for lo, hi in candidates if lo < hi]
    return {'schema': 1, 'hardware_access_validated': False,
            'limitations': ['Snapshots do not prove firmware/XPU access permissions or ownership at handoff.',
                            'Live image, DTB, initrd, stack and payload must be excluded at actual handoff.',
                            'No candidate is selected automatically; no memory has been accessed.'],
            'page_alignment': PAGE, 'dt_ram': render(banks), 'linux_ram': render(linux_ram),
            'reservations': reasons, 'memreserve': render([interval(b, s) for b, s in fdt.reservations]),
            'linux_occupied': render(linux_occupied), 'runtime_exclusions': render(runtime),
            'candidates': render(candidates)}


def render(ranges):
    return [{'base': hex(lo), 'size': hex(hi - lo), 'end_exclusive': hex(hi)} for lo, hi in ranges]


def check_placement(report, base, size):
    lo, hi = interval(base, size)
    if lo % PAGE or size % PAGE:
        raise ValueError('placement must be 16 KiB aligned in base and size')
    if not any(int(r['base'], 16) <= lo and hi <= int(r['end_exclusive'], 16)
               for r in report['candidates']):
        raise ValueError('placement crosses a hole or excluded region')
    return {'base': hex(base), 'size': hex(size), 'fits_snapshot_candidates': True,
            'hardware_access_validated': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path, help='directory containing live.dtb and iomem.txt')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--exclude', action='append', default=[], metavar='BASE:SIZE',
                        help='additional occupied RAM, hexadecimal or decimal; repeat as needed')
    parser.add_argument('--check-base', type=lambda s: int(s, 0))
    parser.add_argument('--check-size', type=lambda s: int(s, 0))
    args = parser.parse_args()
    try:
        if (args.check_base is None) != (args.check_size is None):
            raise ValueError('--check-base and --check-size must be supplied together')
        extra = []
        for value in args.exclude:
            pieces = value.split(':')
            if len(pieces) != 2:
                raise ValueError('--exclude needs BASE:SIZE')
            extra.append(tuple(int(s, 0) for s in pieces))
        dtb = (args.evidence / 'live.dtb').read_bytes()
        iomem = (args.evidence / 'iomem.txt').read_bytes()
        report = plan(Fdt(dtb), iomem.decode('ascii'), extra)
        report['input_sha256'] = {k: hashlib.sha256(v).hexdigest()
                                  for k, v in (('live.dtb', dtb), ('iomem.txt', iomem))}
        if args.check_base is not None:
            report['placement_check'] = check_placement(report, args.check_base, args.check_size)
        result = json.dumps(report, indent=2) + '\n'
        if args.out:
            args.out.write_text(result, encoding='utf-8')
        else:
            print(result, end='')
    except (ValueError, OSError) as exc:
        parser.exit(1, f'memory evidence rejected: {exc}\n')


if __name__ == '__main__':
    main()
