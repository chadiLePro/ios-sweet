#!/usr/bin/env python3
"""Cross-build isolated A52 diagnostic core; deliberately produces no boot.img.

Uses the existing shim's GNU freestanding AArch64 toolchain/flags. A native
Windows aarch64-none-elf toolchain can be used with --cross-prefix PATH/PREFIX.
No kernel RAM base, splash address, boot header offsets or signing assumed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import secrets
from a52q_ramoops import configuration
from android_boot_evidence import kernel_contract

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cross-prefix', default='aarch64-linux-gnu-')
    p.add_argument('--out', type=Path, default=ROOT / 'shim/out/a52q')
    p.add_argument('--evidence', type=Path, help='enable candidate ramoops output from verified live DT/runtime parameters')
    p.add_argument('--payload', type=Path, help='validated embedded A52 XNU payload (requires adjacent .json manifest)')
    p.add_argument('--handoff', choices=('display', 'ufs'), help='read-only MMIO snapshot, no kernel/controller initialization')
    p.add_argument('--register-sources', type=Path, help='four pinned Samsung register source files')
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    # A failed rebuild must not leave an earlier success manifest usable.
    (a.out / 'build.json').unlink(missing_ok=True)
    source = ROOT / 'shim/a52q'
    flags = ['-O2', '-ffreestanding', '-nostdlib', '-fno-pic', '-fno-pie',
             '-mgeneral-regs-only', '-mstrict-align', '-fno-stack-protector',
             '-Wall', '-Wextra', '-Werror']

    def run(tool, *args):
        return subprocess.check_output([a.cross_prefix + tool, *map(str, args)], text=True)

    try:
        output = None
        contract = None
        handoff = None
        if a.handoff:
            if not a.evidence or not a.register_sources or a.payload:
                raise ValueError('handoff needs evidence/register sources and cannot include XNU')
            from a52q_handoff import layout, header
            handoff = layout(a.evidence, a.register_sources, a.handoff)
            handoff['capture_id'] = secrets.randbits(64)
            (a.out / 'handoff-config.h').write_text(header(handoff))
            flags += ['-DA52Q_HANDOFF', '-I', str(a.out.resolve())]
        if a.evidence:
            output = configuration(a.evidence)
            contract = kernel_contract((a.evidence / 'boot.img').read_bytes())
            (a.out / 'ramoops-config.h').write_text(
                '/* Live FDT ' + output['live_dtb_sha256'] + ' */\n' +
                f'#define A52Q_RAMOOPS_BASE {output["base"]}UL\n' +
                f'#define A52Q_RAMOOPS_SIZE {output["size"]}U\n')
            flags += ['-DA52Q_RAMOOPS_CONFIG', '-I', str(a.out.resolve()),
                      f'-DA52Q_TEXT_OFFSET={contract["text_offset"]}']
        compiler = run('gcc', '--version').splitlines()[0]
        objects = []
        names = ['start.S', 'diag.c']
        payload_manifest = None
        if a.payload:
            if not a.evidence:
                raise ValueError('embedded kernel requires evidence-bound ramoops output')
            from a52q_payload import validate_payload
            data = a.payload.read_bytes()
            payload_manifest = json.loads(a.payload.with_suffix(a.payload.suffix + '.json').read_text())
            validate_payload(data, payload_manifest)
            if payload_manifest['live_dtb_sha256'] != output['live_dtb_sha256']:
                raise ValueError('payload and shim device evidence differ')
            base, size = (int(payload_manifest[k], 16) for k in ('phys_base', 'mem_size'))
            (a.out / 'payload-config.h').write_text(
                f'#define A52Q_PAYLOAD_BASE {base}ULL\n#define A52Q_PAYLOAD_SIZE {size}ULL\n'
                f'#define A52Q_PAYLOAD_END {base + size}ULL\n', encoding='ascii')
            asm = a.out / 'payload.S'
            asm.write_text('.section .payload,"a"\n.balign 8\n.global _payload_start, _payload_end\n'
                           '_payload_start:\n.incbin "' + a.payload.resolve().as_posix() + '"\n_payload_end:\n',
                           encoding='utf-8')
            flags += ['-DA52Q_XNU_PAYLOAD', '-I', str(a.out.resolve())]
            names += ['loader.c']
        for name in names:
            obj = a.out / (Path(name).stem + '.o')
            run('gcc', *flags, '-c', source / name, '-o', obj)
            objects.append(obj)
        if a.payload:
            obj = a.out / 'payload.o'
            run('gcc', *flags, '-c', a.out / 'payload.S', '-o', obj)
            objects.append(obj)
            loader_relocs = run('readelf', '-rW', a.out / 'loader.o')
            if 'R_AARCH64_ABS' in loader_relocs:
                raise ValueError('loader contains absolute relocations')
        relocs = run('readelf', '-rW', objects[1])
        if 'R_AARCH64_ABS' in relocs:
            raise ValueError('C code contains absolute relocations; cannot run at arbitrary load address')
        elf = a.out / 'diag-core.elf'
        run('gcc', *flags, '-static', '-T', source / 'diag.ld', '-Wl,--build-id=none',
            '-Wl,--no-warn-rwx-segments', '-Wl,-N', *objects, '-o', elf)
        final_relocs = run('readelf', '-rW', elf)
        if 'R_AARCH64_' in final_relocs:
            raise ValueError('unresolved linked-image relocations')
        image = a.out / 'diag-core.Image'
        run('objcopy', '-O', 'binary', elf, image)
        symbols = run('nm', '-n', elf)
        sizes = [int(words[2]) for line in run('readelf', '-sW', elf).splitlines()
                 if len(words := line.split()) >= 8 and words[-1] == 'a52q_diagnostic']
        if len(sizes) != 1:
            raise ValueError('cannot determine diagnostic record size from ELF')
        end = next(int(line.split()[0], 16) for line in symbols.splitlines()
                   if line.split()[-1] == '_end')
        raw = image.read_bytes()
        if raw[56:60] != b'ARM\x64' or struct.unpack_from('<Q', raw, 16)[0] != end:
            raise ValueError('invalid arm64 Image header or image_size')
        if len(raw) > end:
            raise ValueError('binary exceeds linker image size')
        image.write_bytes(raw + bytes(end - len(raw)))
        (a.out / 'symbols.txt').write_text(symbols, encoding='utf-8')
        (a.out / 'disassembly.txt').write_text(run('objdump', '-d', elf), encoding='utf-8')
        report = {'target': 'a52q', 'compiler': compiler, 'bytes': end,
                  'diagnostic_record_bytes': sizes[0],
                  'status': 'compiled diagnostic core; not packaged, emulated or phone-tested',
                  'output': output or 'own-image RAM record only; no persistent or external output',
                  'template_kernel_contract': contract,
                  'image_sha256': hashlib.sha256(image.read_bytes()).hexdigest()}
        if payload_manifest:
            report['embedded_payload'] = payload_manifest
        if handoff:
            report['handoff_probe'] = handoff
        (a.out / 'build.json').write_text(json.dumps(report, indent=2) + '\n')
    except (OSError, subprocess.SubprocessError, ValueError, StopIteration, KeyError) as exc:
        p.exit(1, f'diagnostic build failed: {exc}\n')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
