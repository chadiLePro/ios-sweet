#!/usr/bin/env python3
"""macOS-only leaf rebuild using actual, verified A52 link inputs.

Requires the full build's tree/archive/logs. Refuses board, patch-set or overlay
logic changes: those need a full build. Never uses a Redmi control archive.
The original console-only invocation remains supported. Select another isolated
implementation with --leaf; board headers and unselected leaves must match.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys

LEAVES = {
    'console': ('a52q_early.c', 'osfmk/arm64/sweet_early.c', 'sweet_early.o', 'osfmk'),
    'cpu': ('A52CPU.cpp', 'iokit/Kernel/arm/SweetCPU.cpp', 'SweetCPU.cpo', 'iokit'),
    'platform': ('A52PlatformExpert.cpp', 'iokit/Kernel/arm/SweetPlatformExpert.cpp', 'SweetPlatformExpert.cpo', 'iokit'),
    'serial': ('a52q_serial.inc', 'pexpert/arm/pe_serial.c', 'pe_serial.o', 'pexpert'),
    'ram-root': (None, 'iokit/Kernel/IOService.cpp', 'IOService.cpo', 'iokit'),
}
# xnu-8796.141.3 + the original 81 patches, independently identical in the
# successful full A52 build and original patched source. No Redmi objects used.
ROOT_MEDIA_BASE_SHA256 = '3e97419a2ce90729537e65cd5de200887e7eaddebd01e90502f05a485efbe7a3'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--artifact', required=True, type=Path)
    p.add_argument('--log', required=True, type=Path)
    p.add_argument('--base-sha', required=True)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--leaf', choices=sorted(LEAVES), default='console')
    a = p.parse_args()
    if sys.platform != 'darwin' or not re.fullmatch('[0-9a-f]{40}', a.base_sha):
        raise SystemExit('requires macOS and a verified base commit SHA')
    root = Path(__file__).resolve().parents[1]
    base = a.artifact.resolve()
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=False)

    def run(*cmd, **kwargs):
        return subprocess.check_output(list(map(str, cmd)), **kwargs)

    # Only the selected implementation may differ from the compiled source.
    for name in ('xnu/a52q/A52Q.h', 'xnu/a52q/apply.py', '.github/workflows/xnu-a52q.yml'):
        old = run('git', 'show', a.base_sha + ':' + name, cwd=root)
        new = (root / name).read_bytes()
        # One reviewed transition for a RAM-only root: enable the existing
        # no-IOStorageFamily handling, and nothing else in the overlay logic.
        if a.leaf == 'ram-root' and name == 'xnu/a52q/apply.py' and old != new:
            addition = b"    'iokit/Kernel/IOService.cpp',\n"
            if new.count(addition) != 1 or new.replace(addition, b'') != old:
                raise SystemExit('full build required: unreviewed overlay change')
        elif old != new:
            raise SystemExit('full build required: changed ' + name)
    if run('git', 'diff', '--name-only', a.base_sha, 'HEAD', '--', 'xnu/patches', cwd=root).strip():
        raise SystemExit('full build required: base patch set changed')
    for key, (name, _, _, _) in LEAVES.items():
        if name and key != a.leaf and run('git', 'show', a.base_sha + ':xnu/a52q/' + name, cwd=root) != (root / 'xnu/a52q' / name).read_bytes():
            raise SystemExit('full build required: unselected implementation changed: ' + name)
    report = json.loads((base / 'a52q-overlay.json').read_text())
    if report['target'] != 'A52Q':
        raise SystemExit('artifact is not an A52Q build')
    old_kernel = base / 'kernel.development.a52q'
    old_hash = hashlib.sha256(old_kernel.read_bytes()).hexdigest()
    if old_hash != (base / 'SHA256SUMS').read_text().split()[0]:
        raise SystemExit('base kernel hash mismatch')
    # The artifact is produced by our own verified full build. Check all member
    # paths before extracting into this new job's dedicated build directory.
    import tarfile
    work = root / 'dxb'
    work.mkdir(exist_ok=False)
    with tarfile.open(base / 'buildtree.tgz') as archive:
        members = archive.getmembers()
        for member in members:
            path = Path(member.name)
            if path.is_absolute() or '..' in path.parts or path.parts[0] not in ('xnu', 'build', 'fakeroot'):
                raise SystemExit('unsafe build-tree member')
            if member.issym() or member.islnk():
                dest = (work / member.linkname if member.islnk()
                        else (work / member.name).parent / member.linkname)
                if not dest.resolve().is_relative_to(work.resolve()):
                    raise SystemExit('build-tree link escapes the build directory')
        archive.extractall(work)
    for name, expected in report['files_sha256'].items():
        if hashlib.sha256((work / 'xnu' / name).read_bytes()).hexdigest() != expected:
            raise SystemExit('base source hash mismatch: ' + name)
    name, unit, member, component = LEAVES[a.leaf]
    if a.leaf == 'ram-root':
        source = work / 'xnu' / unit
        original = source.read_bytes()
        if hashlib.sha256(original).hexdigest() != ROOT_MEDIA_BASE_SHA256:
            raise SystemExit('RAM-root base source differs from the reviewed build')
        guard = b'defined(ARM64_BOARD_CONFIG_SWEET)'
        if original.count(guard) != 3:
            raise SystemExit('RAM-root guard count differs')
        source.write_bytes(original.replace(guard, b'(defined(ARM64_BOARD_CONFIG_SWEET) || defined(ARM64_BOARD_CONFIG_A52Q))'))
        name = 'IOService.cpp (reviewed absence-of-IOStorageFamily guards only)'
    else:
        source = work / 'xnu' / Path(unit).parent / name
        if source.relative_to(work / 'xnu').as_posix() not in report['files_sha256']:
            raise SystemExit('base build lacks the selected A52 implementation')
        source.write_bytes((root / 'xnu/a52q' / name).read_bytes())
    # Recover the exact compiler command from the full build, not guessed flags.
    commands = set()
    for line in a.log.read_text().splitlines():
        match = re.search(r'(/Applications/\S+/usr/bin/clang(?:\+\+)?\s+.*)', line)
        if match and line.rstrip().endswith('/xnu/' + unit) and '-DARM64_BOARD_CONFIG_A52Q' in line:
            if '-c' in shlex.split(match[1]):
                commands.add(match[1])
    if len(commands) != 1:
        raise SystemExit('need one unambiguous A52 compiler command for ' + unit)
    cmd = shlex.split(commands.pop())
    old_root = cmd[-1].split('/dxb/xnu/')[0]
    cmd = [word.replace(old_root, str(root)) for word in cmd]
    obj = out / member
    if '-o' in cmd:
        cmd[cmd.index('-o') + 1] = str(obj)
    else:
        cmd += ['-o', str(obj)]
    cwd = work / 'build/xnu.obj/DEVELOPMENT_ARM64_A52Q' / component / 'DEVELOPMENT'
    run(*cmd, cwd=cwd)
    linkdir = base / 'kernel.development.a52q.link'
    archive = out / 'kernel.development.a52q.a'
    shutil.copy2(linkdir / archive.name, archive)
    before = run('xcrun', 'ar', '-t', archive).splitlines()
    if before.count(member.encode()) != 1:
        raise SystemExit('selected object is not unique in base archive')
    run('xcrun', 'ar', '-r', archive, obj)
    run('xcrun', 'ranlib', archive)
    if before != run('xcrun', 'ar', '-t', archive).splitlines():
        raise SystemExit('archive member order changed')
    library = work / 'fakeroot/usr/local/lib/kernel'
    library.mkdir(parents=True, exist_ok=True)
    shutil.copy2(base / 'libfirehose_kernel.a', library)
    flags = shlex.split((linkdir / 'kernel.development.a52q.linkarguments').read_text())
    flags = [word.replace(old_root, str(root)) for word in flags]
    kernel = out / 'kernel.development.a52q'
    run('xcrun', 'clang++', *flags, '-Wl,-force_load,' + str(archive),
        '-Wl,-exported_symbols_list,' + str(linkdir / 'kernel.development.a52q.exp'),
        '-Wl,-alias_list,' + str(linkdir / 'kernel.development.a52q.alias.exp'), '-o', kernel)
    # Source/header/architecture and actual table alignment are independently
    # checked by the same validator used before constructing a phone payload.
    from a52q_payload import validate_kernel
    validate_kernel(kernel.read_bytes())
    (out / 'kernel.symbols.txt').write_bytes(run('xcrun', 'nm', '-n', kernel))
    digest = hashlib.sha256(kernel.read_bytes()).hexdigest()
    (out / 'SHA256SUMS').write_text(digest + '  kernel.development.a52q\n')
    (out / 'relink.json').write_text(json.dumps({'target': 'A52Q', 'base_commit': a.base_sha,
        'base_kernel_sha256': old_hash, 'kernel_sha256': digest,
        'changed_translation_unit': unit, 'implementation': name,
        'implementation_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'status': 'relinked diagnostic kernel; no CTF/dSYM regeneration or boot claim'}, indent=2) + '\n')


if __name__ == '__main__':
    main()
