# A52 mount correction and trial review — 2026-11-15

Latest retained physical errors, from V10:

```text
mount_hfs: Read-only file system
mount: / failed with 1
mount: failed to get boot manifest hash - No such file or directory
Boot task failed: mount-phase-1 - exited due to exit(66)
```

These follow actual Apple launchd-main, fsck and mount execution on the UFS
root. They do not establish running Apple services or a rendered lock screen.
The display remains a guarded, opt-in framebuffer diagnostic, not an implemented
IOMobileFramebuffer ABI or measured 60 Hz compositor. Existing display and RAM
console code is byte-identical between the reviewed kernel overlays.

## Changes prepared for V11

* `xnu/a52q/a52q_bootfs.c`: publish the measured Libinfo filesystem-table ABI
  only for the actual read-only HFS UFS root. Copy its actual statfs source
  alias (`root_device` initially); root device, mount flags, type and path must
  match. This prevents a redundant read-write root upgrade.
* `xnu/a52q/a52q_ufs_disk.c`, `xnu/a52q/apply.py`: include that A52-only
  provider. The BSD block reader retains its existing read-only behavior.
  There is no A52 IOMedia implementation to fix by setting `isWritable`.
* `tools/a52q_boot_manifest.py`, `tools/a52q_payload.py`: opt-in SHA384 namespace
  derived from the measured kernel/root/board-evidence hashes. The canonical
  local document is embedded alongside the chosen hash. This is explicitly
  unsealed and unauthenticated; it grants no Apple IMG4 or AMFI trust.
* `tests/test_a52q_bootfs.py`, `tests/test_a52q_boot_manifest.py`,
  `tests/test_a52q_persistent_root.py`: actual C callback checks, measured wire
  bytes, rejection guards, and payload measurement/tampering checks.
* `xnu/a52q/a52q_amfi.c`, `xnu/a52q/apply.py` (preceding enforcement fix):
  correctly mark admitted signatures CS_SIGNED and enable process enforcement
  for A52. The previous macOS default had let a rejected helper execute.
  Real QEMU negative tests now reject both an unapproved signature and a
  modified signed page. Cache and executable admission remain measured pins.
* `docs/A52Q-BOOT-FILESYSTEM.md`, `docs/A52Q-CACHE-SIGNATURES.md`,
  `docs/A52Q-PERSISTENT-ROOT.md`, `docs/A52Q.md`, `NOTES.md`: evidence and limits.

The full root is unchanged. No journal-forcing patch, root write support,
global signature-disable argument, fake SEP/keychain/power service, watchdog
disable, IOSurface provider or CoreAnimation/Metal fallback is included in this
candidate. Those interfaces cannot be established by these mount errors.
Writable `/private/var` still needs a separate bounded storage implementation
and a reviewed new write range. The prepared 4 GiB host image is not installed.

## Inspection index

Repository files inspected for this mount and preservation audit:

```text
AGENTS.md
NOTES.md
docs/A52Q.md
docs/A52Q-PERSISTENT-ROOT.md
docs/A52Q-CACHE-SIGNATURES.md
docs/A52Q-BOOT-FILESYSTEM.md
xnu/a52q/apply.py
xnu/a52q/a52q_amfi.c
xnu/a52q/a52q_ufs.c
xnu/a52q/a52q_ufs_disk.c
xnu/a52q/a52q_ufs_bounds.h
xnu/a52q/a52q_bootfs.c
xnu/a52q/a52q_display.c
xnu/a52q/a52q_early.c
xnu/a52q/A52Q.h
xnu/a52q/A52PlatformExpert.cpp
tools/a52q_memory.py
tools/a52q_payload.py
tools/a52q_boot_manifest.py
tools/a52q_persistent_root.py
tools/a52q_userland_audit.py
tools/a52q_cache_audit.py
tools/adt.py
tools/build_a52q_diag.py
tools/qemu_a52q_xnu.py
tools/validate-repo.py
tests/test_a52q_bootfs.py
tests/test_a52q_boot_manifest.py
tests/test_a52q_persistent_root.py
tests/test_a52q_payload.py
tests/test_a52q_exec_policy.py
xnu/patches/0026-sweet-builtin-hfs.patch
xnu/patches/0037-sweet-config-bindfs.patch
xnu/patches/0057-sweet-no-ext-resolver.patch
.github/workflows/a52q-diagnostics.yml
.github/workflows/xnu-a52q.yml
.github/workflows/xnu-a52q-console-relink.yml
```

Primary source inspected: pinned XNU 8796 `bsd/kern/kern_cs.c`,
`bsd/kern/mach_loader.c`, `bsd/kern/kern_exec.c`, `bsd/kern/bsd_init.c`,
`bsd/vfs/vfs_subr.c`, `bsd/vfs/vfs_syscalls.c`, `bsd/sys/mount.h`,
`bsd/sys/sysctl.h`, `bsd/miscfs/bindfs/bind_vfsops.c`,
`iokit/Kernel/IOUserClient.cpp`; Apple HFS 627.100.6 `mount_hfs/mount_hfs.c`;
matching Apple diskdev_cmds 701.100.2 `mount.tproj/mount.c`,
`edt_fstab/edt_fstab.c`, `edt_fstab/edt_fstab.h`; Libinfo 564.120.2
`lookup.subproj/file_module.c`; dyld's published `dyld_cache_format.h`.
The exact Libinfo cache consumer's code was also inspected read-only.

Private evidence/artifacts inspected (kept out of Git):

```text
backup/a52q/ios-ufs-v10/{receipt.json,console.txt}
E:/A52-iOS16/cache-code-signatures-v1.json
E:/A52-iOS16/cache-fstab-audit-v1/{report.json,fresh-source-hashes.json,__TEXT.bin,
  edt-fstab-reference-disassembly.txt,libsystem-info-text-disassembly.txt}
E:/A52-iOS16/exec-policy-fixtures-v1/manifest.json
E:/A52-iOS16/exec-enforcement-result-v1.json
E:/A52-iOS16/builds/43640145137/{verified-build.json,artifact/a52q-overlay.json}
E:/A52-iOS16/builds/43643720989/{verified-build.json,artifact/a52q-overlay.json}
E:/A52-iOS16/ios16-20H392-pristine-v11.hfs.verified.json
E:/A52-iOS16/ios-root-plan-v7.json
shim/out/a52q-bootfs-qemu-v1/run/result.json
shim/out/a52q-ios-ufs-hardware-v9/build/{build.json,a52q-ios-ufs-UNTESTED.img.json}
```

Private host scripts inspected/updated: `research/a52q_xnu_device_test.py`,
`research/prepare_bootfs_artifacts.py`, `research/verify_root_kernel_build.py`,
`research/finish_bootfs_artifacts.py`, `research/start_bootfs_trial.py`,
`research/watch_ios_ufs_v11_restore.py`, and the cache/negative-fixture audit
scripts. They contain local artifact paths, not distributable Apple binaries.

## Validation and phone operation

Full kernel build **43643720989**, source **67f6d6bd63ecd0bab0c42eec93fb40f7fe360780**,
passed. All **73** overlay file hashes matched the reviewed source. Kernel:
`87b660ae13249c8281eaf618110899ff6d77249b5acf23ccf49a996865f3196e`.
Host CI **43643867819** and **120** tests passed. Repository checks passed for
81 unchanged patches, 41 Python tools and seven shell scripts.

Exact-kernel diagnostic QEMU: three valid entry records, diagnostic PID1 and
seven heartbeats. It does not emulate Samsung UFS or boot the full iOS root.
The full master was rehashed unchanged when generating plan-v7.

Prepared 96 MiB BOOT SHA256:
`96e668f4343c40f616dd30af5e4784e54d36595c55702a7e0d76e149f8d6680c`.
V11 may temporarily write only `/dev/block/sda19` bytes `[0,100663296)` under
the existing authorization. It first rehashes the installed 16 GiB UFS prefix.
No root/var/GPT/recovery/DTBO/vbmeta/metadata write or format is included.

After five minutes, return to TWRP: Volume Down + Power until black, immediately
Volume Up + Power with USB. The watcher collects pstore, restores the original
BOOT from its C: backup and checks the complete partition against
`d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016`.
Remain in TWRP; restoring BOOT does not restore the previously overwritten
Android userdata. The authoritative live trial/restoration state is the private
`backup/a52q/ios-ufs-v11/receipt.json`, not this preparation document.
