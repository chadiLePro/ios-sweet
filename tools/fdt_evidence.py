"""Bounds-checked, host-only FDT reader for bring-up evidence (not a driver).

MMIO reg values are reported as bus addresses; no implicit bus translation.
Only root memory and /reserved-memory ranges are treated as physical here.
"""
from dataclasses import dataclass, field
import struct


@dataclass
class Node:
    name: str
    parent: object = None
    props: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    @property
    def path(self):
        return '/' if self.parent is None else self.parent.path.rstrip('/') + '/' + self.name

    def strings(self, key):
        b = self.props.get(key, b'')
        if b and not b.endswith(b'\0'):
            raise ValueError(f'{self.path}/{key}: unterminated string')
        return [x.decode('utf-8') for x in b.rstrip(b'\0').split(b'\0')] if b else []

    def cell(self, key, default=None):
        b = self.props.get(key)
        if b is None:
            if default is None:
                raise ValueError(f'{self.path}: missing {key}')
            return default
        if len(b) != 4:
            raise ValueError(f'{self.path}/{key}: expected one cell')
        return int.from_bytes(b, 'big')

    def enabled(self):
        return (self.strings('status') in ([], ['okay'], ['ok']) and
                (self.parent is None or self.parent.enabled()))


class Fdt:
    def __init__(self, data):
        if len(data) < 40:
            raise ValueError('truncated FDT header')
        magic, total, off, strings, reserve, version, last, _, slen, size = struct.unpack_from('>10I', data)
        if magic != 0xd00dfeed or not 40 <= total <= min(len(data), 16 << 20):
            raise ValueError('invalid FDT magic or total size')
        if version < 17 or last > 17:
            raise ValueError('only FDT v17-compatible headers supported')
        if off % 4 or reserve % 8 or min(off, strings, reserve) < 40:
            raise ValueError('invalid FDT block offset')
        if off + size > total or strings + slen > total:
            raise ValueError('FDT block exceeds total size')
        if off < strings + slen and strings < off + size:
            raise ValueError('overlapping FDT structure and strings')
        self.total = total
        self.reservations = []
        r = reserve
        while True:
            if r + 16 > total or any(r < hi and lo < r + 16 for lo, hi in
                                          ((off, off + size), (strings, strings + slen))):
                raise ValueError('unterminated or overlapping FDT reservation map')
            base, length = struct.unpack_from('>QQ', data, r)
            r += 16
            if not base and not length:
                break
            if not length or base + length > 1 << 64:
                raise ValueError('invalid FDT reservation')
            self.reservations.append((base, length))
        self.nodes = {}
        stack = []
        end = off + size
        saw_end = False
        while off < end:
            if off + 4 > end:
                raise ValueError('truncated FDT token')
            tok, = struct.unpack_from('>I', data, off)
            off += 4
            if tok == 1:
                zero = data.find(b'\0', off, end)
                if zero < 0:
                    raise ValueError('unterminated node name')
                name = data[off:zero].decode('utf-8')
                if '/' in name or (not stack and (name or self.nodes)):
                    raise ValueError('invalid root or node name')
                node = Node(name, stack[-1] if stack else None)
                if node.path in self.nodes or len(stack) >= 64:
                    raise ValueError('duplicate node or excessive nesting')
                if stack:
                    stack[-1].children.append(node)
                self.nodes[node.path] = node
                stack.append(node)
                off = (zero + 4) & ~3
            elif tok == 2:
                if not stack:
                    raise ValueError('unbalanced FDT end node')
                stack.pop()
            elif tok == 3:
                if not stack or off + 8 > end:
                    raise ValueError('property outside node or truncated header')
                length, nameoff = struct.unpack_from('>II', data, off)
                off += 8
                if nameoff >= slen or off + length > end:
                    raise ValueError('FDT property out of bounds')
                zero = data.find(b'\0', strings + nameoff, strings + slen)
                if zero < 0:
                    raise ValueError('unterminated property name')
                key = data[strings + nameoff:zero].decode('utf-8')
                if key in stack[-1].props:
                    raise ValueError('duplicate FDT property')
                stack[-1].props[key] = data[off:off + length]
                off = (off + length + 3) & ~3
            elif tok == 4:
                pass
            elif tok == 9:
                if stack or '/' not in self.nodes:
                    raise ValueError('unbalanced or empty FDT')
                saw_end = True
                break
            else:
                raise ValueError(f'invalid FDT token {tok}')
            if off > end:
                raise ValueError('FDT alignment exceeds structure')
        if not saw_end:
            raise ValueError('missing FDT_END')


def regs(node):
    if node.parent is None:
        raise ValueError('root has no parent address space')
    ac = node.parent.cell('#address-cells', 2)
    sc = node.parent.cell('#size-cells', 1)
    if ac not in (1, 2) or sc not in (1, 2):
        raise ValueError(f'{node.path}: unsupported address/size cell counts {ac}/{sc}')
    b = node.props.get('reg', b'')
    stride = 4 * (ac + sc)
    if not b or len(b) % stride:
        raise ValueError(f'{node.path}: invalid reg length')
    out = []
    for i in range(0, len(b), stride):
        base = int.from_bytes(b[i:i + ac * 4], 'big')
        length = int.from_bytes(b[i + ac * 4:i + stride], 'big')
        if not length or base + length > 1 << 64:
            raise ValueError(f'{node.path}: invalid range')
        out.append((base, length))
    return out


def describe(fdt):
    def ranges(items):
        return [{'base': hex(b), 'size': hex(s), 'end_exclusive': hex(b + s)} for b, s in items]

    root = fdt.nodes['/']
    result = {'model': root.strings('model'), 'compatible': root.strings('compatible'),
              'memory': [], 'reserved': [], 'dynamic_reservations': [],
              'memreserve': ranges(fdt.reservations), 'devices': []}
    for node in fdt.nodes.values():
        if not node.enabled():
            continue
        if node.parent is root and node.strings('device_type') == ['memory']:
            result['memory'] += ranges(regs(node))
        if node.parent and node.parent.path == '/reserved-memory':
            if 'reg' in node.props:
                result['reserved'].append({'path': node.path, 'ranges': ranges(regs(node))})
            else:
                result['dynamic_reservations'].append(node.path)
        comp = node.strings('compatible')
        if any(c in ('arm,gic-v3', 'arm,armv8-timer', 'arm,psci-1.0', 'arm,psci-0.2',
                     'qcom,ufshc', 'simple-framebuffer') for c in comp):
            result['devices'].append({'path': node.path, 'compatible': comp,
                                      'properties_hex': {k: v.hex() for k, v in node.props.items()
                                                         if k in ('reg', 'interrupts', 'clock-frequency',
                                                                  'method', 'width', 'height', 'stride', 'format')}})
    return result


def simplefb(fdt):
    """Require an explicit enabled simplefb, root physical addressing, reserved backing.

    This validates an FDT description, not Samsung's actual scanout/latch state.
    A splash carveout or panel size alone is deliberately insufficient.
    """
    candidates = [n for n in fdt.nodes.values()
                  if n.enabled() and 'simple-framebuffer' in n.strings('compatible')]
    if len(candidates) != 1:
        raise ValueError('need exactly one enabled simple-framebuffer; splash carveout alone is insufficient')
    n = candidates[0]
    if n.parent.path not in ('/', '/chosen') or 'ranges' in n.parent.props:
        raise ValueError('simplefb address translation needs manual review')
    rr = regs(n)
    if len(rr) != 1:
        raise ValueError('simplefb needs one physical range')
    base, length = rr[0]
    width, height, stride = (n.cell(k) for k in ('width', 'height', 'stride'))
    fmt = n.strings('format')
    if (not 32 <= width <= 8192 or not 32 <= height <= 8192 or stride % 4 or
            not width * 4 <= stride <= 65536 or stride * height > length or base % 4 or
            fmt not in (['a8r8g8b8'], ['x8r8g8b8'])):
        raise ValueError('unsupported simplefb geometry/format')
    backing = list(fdt.reservations)
    for reserved in fdt.nodes.values():
        if (reserved.enabled() and reserved.parent and
                reserved.parent.path == '/reserved-memory' and 'reg' in reserved.props):
            backing += regs(reserved)
    if not any(b <= base and base + length <= b + s for b, s in backing):
        raise ValueError('simplefb is not fully backed by reserved memory')
    return {'base': base, 'size': length, 'width': width, 'height': height, 'stride': stride}
