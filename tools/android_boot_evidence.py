"""Strict Android boot v0-v2 inspection; no image generation or signing.

Unlike an unpack-and-slice script, rejects truncated sections and honors the
explicit recovery_dtbo_offset. Trailing Samsung/AVB data is reported, not copied
into a new unsigned image under the assumption its signatures remain valid.
"""
import hashlib
import struct
import gzip

SEANDROID_TRAILER = b'SEANDROIDENFORCE\0'


def inspect(data):
    if len(data) < 1632 or data[:8] != b'ANDROID!':
        raise ValueError('not a complete Android boot v0-v2 header')
    ks, ka, rs, ra, ss, sa, ta, page, version, osv = struct.unpack_from('<10I', data, 8)
    if version not in (0, 1, 2):
        raise ValueError(f'unsupported boot header version {version}')
    hsize = (1632, 1648, 1660)[version]
    if page not in (2048, 4096, 8192, 16384) or len(data) < page or hsize > page:
        raise ValueError('invalid boot page size or truncated header page')
    align = lambda n: (n + page - 1) // page * page
    result = {'header_version': version, 'page_size': page,
              'kernel_addr': hex(ka), 'ramdisk_addr': hex(ra),
              'second_addr': hex(sa), 'tags_addr': hex(ta), 'os_version_raw': hex(osv),
              'os_version': f'{osv >> 25 & 127}.{osv >> 18 & 127}.{osv >> 11 & 127}',
              'os_patch_level': f'{2000 + (osv >> 4 & 127):04d}-{osv & 15:02d}',
              'name': data[48:64].split(b'\0')[0].decode('utf-8', errors='replace'),
              'sections': {}, 'file_bytes': len(data),
              'sha256': hashlib.sha256(data).hexdigest()}
    off = page

    def section(name, start, size):
        if start < page or start % page or start + size > len(data):
            raise ValueError(f'{name}: misaligned or truncated section')
        if size:
            for previous in result['sections'].values():
                if start < previous['offset'] + previous['size'] and previous['offset'] < start + size:
                    raise ValueError(f'{name}: overlapping boot sections')
            result['sections'][name] = {'offset': start, 'size': size,
                                       'sha256': hashlib.sha256(data[start:start + size]).hexdigest()}

    for name, size in (('kernel', ks), ('ramdisk', rs), ('second', ss)):
        section(name, off, size)
        off += align(size)
    if not ks:
        raise ValueError('missing kernel')
    if version >= 1:
        rsize, roff, declared = struct.unpack_from('<IQI', data, 1632)
        if declared != hsize:
            raise ValueError('unexpected boot header_size')
        if rsize:
            section('recovery_dtbo', roff, rsize)
            if roff < off:
                raise ValueError('recovery DTBO overlaps earlier aligned sections')
            off = roff + align(rsize)
    if version == 2:
        dsize, daddr = struct.unpack_from('<IQ', data, 1648)
        section('dtb', off, dsize)
        result['dtb_addr'] = hex(daddr)
        off += align(dsize)
    result['aligned_image_end'] = off
    result['trailing_bytes'] = max(0, len(data) - off)
    result['avb_footer'] = len(data) >= 64 and data[-64:-60] == b'AVBf'
    result['seandroid_trailer'] = data[off:off + len(SEANDROID_TRAILER)] == SEANDROID_TRAILER
    if result['avb_footer']:
        result['avb_metadata'] = inspect_avb_footer(data, off)
    return result


def inspect_avb_footer(data, aligned_image_end):
    """Structural checks only. Does not validate an AVB cryptographic signature."""
    _, major, minor, original, offset, size = struct.unpack_from('>4sIIQQQ', data, len(data) - 64)
    errors = []
    if major != 1:
        errors.append('unsupported AVB footer major version')
    if not aligned_image_end <= original <= offset or offset + size > len(data) - 64:
        errors.append('AVB footer offsets disagree with current boot image geometry')
    if size < 256 or data[offset:offset + 4] != b'AVB0':
        errors.append('AVB footer does not reference a VBMeta header')
    return {'version': f'{major}.{minor}', 'original_image_size': original,
            'vbmeta_offset': offset, 'vbmeta_size': size,
            'structural_errors': errors, 'signature_verified': False}


def template_trailer(data, info=None):
    """Preserve only the exact Samsung trailer observed at the aligned image end.

    The marker is a format artifact, not a signature or a bypass of verification.
    Signed AVB data is never returned by this function.
    """
    info = info or inspect(data)
    offset = info['aligned_image_end']
    if data[offset:offset + len(SEANDROID_TRAILER)] == SEANDROID_TRAILER:
        return SEANDROID_TRAILER
    if data[offset:offset + len(SEANDROID_TRAILER) - 1] == SEANDROID_TRAILER[:-1]:
        raise ValueError('unsupported Samsung trailer termination')
    return b''


def kernel_contract(data, info=None):
    info = info or inspect(data)
    part = info['sections']['kernel']
    kernel = data[part['offset']:part['offset'] + part['size']]
    if kernel[:2] != b'\x1f\x8b':
        raise ValueError('only the observed gzip kernel wrapper is supported')
    raw = gzip.decompress(kernel)
    if len(raw) < 64 or raw[56:60] != b'ARM\x64':
        raise ValueError('template has no arm64 Linux Image header')
    offset, size, flags = struct.unpack_from('<QQQ', raw, 8)
    if offset % 4096 or offset > 0x200000 or flags & 1:
        raise ValueError('unsupported template Image offset/endianness')
    return {'text_offset': offset, 'image_size': size, 'flags': flags, 'compression': 'gzip'}
