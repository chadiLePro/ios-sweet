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

## Physical V11 result and next correction

V11 completed and original BOOT was restored. The receipt and a fresh complete
BOOT readback matched the original hash; recovery/DTBO/vbmeta were unchanged.
Three CRC-valid entry frames and three launchd-main markers survived with
system/process signature enforcement enabled. Both filesystem-table queries
reported the actual mounted read-only source `root_device`. The root-upgrade
and missing-boot-hash failures are absent. The next retained error is:

```text
mount: failed to mount .../usr/standalone/firmware -> /usr/standalone/firmware - Operation not permitted(1)
Boot task failed: mount-phase-1 - exited due to exit(77)
```

The source path in the unprotected console has retention corruption; its exact
hash bytes are not reconstructed. This result proves advancement to the bind
mount, not a completed mount phase or services/UI startup.

XNU `bind_vfsops.c::bindfs_mount` checks `com.apple.private.bindfs-allow` before
reading its source-path argument, returning EPERM when denied. The actual
IOKit path calls AMFI's `copyEntitlementAsOSObjectWithProc`; our previous callback
returned KERN_NOT_FOUND for every key. Inspection of the exact measured mount
binary confirms the signed XML Boolean is true, after code-page and XML/DER
special-slot verification.

The next correction shares mount's existing signature/root validator between
admission and queries. Only a signed, valid process with that exact admitted
platform blob on the read-only root may query that one true Boolean. The C++
bridge in `A52PlatformExpert.cpp` returns the real retained OSBoolean singleton
through its public API. Other keys, contexts, signatures and roots are rejected.
No C++ object layout/reference ABI is guessed, and no general entitlements
dictionary is fabricated. This is an explicit local development capability,
not Apple CMS authentication. Signature and executable-page enforcement remain.

Native tests compile the actual callbacks and check the positive object/type
contract, twenty changed-hash cases, process/blob flags, invalid XML/DER API
results, wrong/writable roots, other entitlement names and copy failure. The
underlying XML/DER hash algorithms retain their separate mutation tests.
Physical bindfs capability consumption remains pending a new kernel trial.

Additional inspected files: pinned XNU `libkern/c++/OSBoolean.cpp`,
`libkern/libkern/c++/OSBoolean.h`, `bsd/sys/codesign.h`, `osfmk/mach/kern_return.h`,
and the exact mount signature blobs. Modified for this next correction:
`xnu/a52q/a52q_amfi.c`, `xnu/a52q/A52PlatformExpert.cpp`,
`xnu/a52q/ios16-20H392-mount-pin.json`, `tests/test_a52q_exec_policy.py`, this
review and `NOTES.md`. Display, logging and storage transport remain unchanged.

The first full build of this correction (43703934486) caught a missing
`sys/proc_internal.h` include for `proc_getcsflags`. The proper private header
and its actual uint64 API are now used; native checks still pass. Corrected
full build 43705321913 must succeed before packaging or another phone trial.

## Independent service inventory

Read-only master extraction checked these additional files against native source
hashes, then verified every signed code page and XML/DER entitlement slot:

| Executable | Signed pages checked |
|---|---:|
| `/usr/libexec/backboardd` | 280 |
| `/usr/libexec/securityd` | 764 |
| `/System/Library/CoreServices/powerd.bundle/powerd` | 146 |
| `/usr/libexec/watchdogd` | 33 |
| `/usr/libexec/mobileactivationd` | 572 |
| `/System/Library/CoreServices/SpringBoard.app/SpringBoard` | 9 |

The matching `System/Library/LaunchDaemons/com.apple.{backboardd,securityd,powerd,
watchdogd,mobileactivationd}.plist` files were inspected. Backboardd is configured
RunAtLoad/KeepAlive and advertises CARenderServer/display/HID services. Watchdogd
has an IOWatchdog matching event; this does not demonstrate a running watchdog
or justify disabling it. Powerd's actual path is its CoreServices bundle.

The private complete inventory is `E:/A52-iOS16/master-service-audit-v3/report.json`.
These are host file/hash checks, not Apple CMS authentication, admission policy
changes, daemon execution or hardware/graphics compatibility. No service plist
or executable was modified. The earlier serial-export timeout and unresolved
native-path attempt were preserved as incomplete audits, not labelled passes.

## Checked bindfs candidate and V12 trial

Corrected full kernel build **43705321913**, source
`5c34a0499b63bae2d52cf64f2a636b541d2120a0`, passed. Kernel SHA256:
`b50504036500e95d19b7c4aa8a45c46204bbf7a483269a65d233c649106d3d9b`.
All 73 reviewed overlay hashes match. Only `a52q_amfi.c` and
`A52PlatformExpert.cpp` differ from the V11 overlay. Display, memory, logging,
UFS read transport and the read-only mounted-root table are unchanged.

Host CI 43705322098 and all 120 tests pass. Exact-kernel diagnostic QEMU retained
three entry frames and seven heartbeats; it is not full iOS/UFS emulation.
Plan-v8 rehashed the complete master unchanged. The candidate contains no RAM
root and binds the same 16 GiB read-only UFS filesystem. BOOT SHA256:
`b1b3bc6569b79772dd9162db54432df655a407a7c5fcd369b5ad1325a5ec9f27`.

The user confirmed readiness for V12. The installer freshly verified the full
stored root, wrote/read back only BOOT, and confirmed recovery USB departure.
V12 is running; no physical success is claimed. Logs and automatic restoration
use `backup/a52q/ios-ufs-v12/receipt.json` and the C: original BOOT backup.
Return to TWRP after five minutes with the button sequence above. Until that
receipt confirms restoration and complete readback, BOOT restoration is pending.
No data format or other partition write is included.

Further source inspected without modification: XNU `IOPlatformExpert.cpp`
instantiates a normal IOPMrootDomain in the inherited platform path. This does
not establish a battery provider or running powerd. Original patches 0046,
0056, 0061, 0068 and 0079 contain Redmi IOSurface/framebuffer glue and a roughly
60 Hz software notification timer. These are outside the current A52 provider
set and have not been enabled by this mount correction. Their presence is not
evidence of a working A52 IOMobileFramebuffer compositor.

## V12 retained result

V12 returned to TWRP after the watcher's ten-minute deadline. The collection and
restoration command was run immediately, and the entire original BOOT hash
matched again. No restoration remains pending. Protected hashes were unchanged.

The retained console has three valid XNU-entry frames but ends after platform
registration and CPU self-SGI initialization. No UFS, root, launchd or bindfs-query
record is retained. This is inconclusive for the capability correction. It does
not establish a specific early-kernel failure, successful bindfs, or a new
userland milestone. A later accidental reboot does not remove the already saved
computer copies. The 8,394-byte console's SHA256 is
`239e7cbc3603fc232a5dd9b15edd87cfb5645f6e4997cafd35092a8d950bc6c8`.
An additional byte-identical archive and hash manifest were retained separately.

Further startup source inspected: `IOStartIOKit.cpp::IOKitInitializeTime`, called
between buffer initialization and the A52 vfs/UFS hook, includes a bounded RTC
resource wait. The saved log does not pinpoint a stall there. A controlled,
fully timed retry of the unchanged checked candidate is needed before changing
CPU initialization or treating this as a deterministic regression.

V13 is a controlled retry of the same checked BOOT and unchanged root. After
fresh readiness confirmation, the full installed root was rehashed, BOOT was
written/read back, and native reboot confirmed USB departure. The user was
asked to wait five full minutes from actual departure before returning to TWRP.
The new watcher waits up to 30 minutes for recovery; original BOOT restoration
remains pending until its complete readback is confirmed. New logs use a
separate `backup/a52q/ios-ufs-v13` directory; the V12 computer copies are preserved.
No new kernel, root, signing, memory or display change is involved in this retry.

## Physical V13 result: both mount phases advanced

V13 returned to TWRP, and its watcher collected the log and restored original
BOOT with full readback. A fresh subsequent whole-partition hash also matched.
Three valid kernel-entry frames survive. Unlike V12, this controlled retry
reached UFS and Apple launchd; the incomplete earlier capture is not evidence
of a deterministic regression in the unchanged candidate.

The log advances past both mount phases. Bindfs reaches source-path lookup
(ENOENT), rather than rejecting the entitlement with EPERM. The missing optional
preboot firmware, Pearl and factory-data paths are tolerated. This demonstrates
advancement of the mount tasks, not a writable data volume: the log still reports
the data volume absent. Persistent Apple services and SpringBoard remain unproven.

The next required failure is:

```text
proc 9: load code signature error 4 for file "cc_fips_test"
Boot task failed: fips - posix_spawn: 85: Bad executable (or shared library)
```

Apple launchd's embedded boot-task XML specifies `/usr/libexec/cc_fips_test`
with both RequireRun and RequireSuccess. Earlier signature rejections for
seputil, mobile_obliterator and MSUEarlyBootTask were nonfatal; they are not
included in the next admission change.

The exact master FIPS executable is 52,208 bytes, plain arm64, and matches the
native staged source. All nine signed pages pass; there are no XML/DER
entitlements. Its only direct dylib is libSystem.B; imports include the real
`fipspost_post` and trace interface. Metadata is in
`xnu/a52q/ios16-20H392-fips-pin.json`; extracted files remain private.

The next AMFI-only change admits that exact entitlement-free identity on the
same read-only root, with the local boot-task classification needed by launchd.
It grants no capabilities, changes no launch arguments or binary bytes, and
does not set the executable's test-disable option or force a successful POST.
Admission and future execution/POST results must be reported separately; neither
constitutes FIPS certification. Native tests cover twenty mutated hashes,
wrong/writable roots, invalid signatures and entitlement-bearing variants; the
FIPS task cannot query mount's bindfs capability.

## Physical V14 result: real FIPS test passed

The unchanged full UFS root supplied the verified Apple FIPS executable. Its
retained console reports the real corecrypto subtests and:

```text
fipspost_post:206: all tests PASSED (183 ms)
Boot task failed: dirs_cleaner - posix_spawn: 85: Bad executable (or shared library)
```

Original BOOT was automatically restored and its complete hash matched again
in a fresh readback. Protected partitions were unchanged. The 51,944-byte saved
console SHA256 is `6c4dccd9e0fc3d72e42edb83be3625501b7243afa78bde899bcd53a671307109`.
Some ordinary console text has known bit corruption; no corrupted bytes were
silently corrected. These actual test results do not constitute certification.

Apple launchd next requires `/usr/libexec/dirs_cleaner /tmp /var/run`. The exact
master executable matches the staged source, all nine code pages pass, and the
signed XML/DER slots pass. It carries `com.apple.private.security.storage.tmp`.
The pin and slot sizes/hashes are recorded in
`xnu/a52q/ios16-20H392-dirs-cleaner-pin.json`.

The [Apple 701.100.2 cleanup source](https://github.com/apple-oss-distributions/diskdev_cmds/blob/diskdev_cmds-701.100.2/dirs_cleaner/dirs_cleaner.c)
uses filesystem mutations for temporary-directory cleanup. This motivates
retaining all existing storage read-only guards, rather than enabling writes
for an untested task. A successful spawn alone will not establish cleanup or a
writable data volume. The source's ordinary main path logs cleanup errors then
returns zero; report any such errors even if launchd proceeds.

The next policy change admits only this exact valid identity with its verified
signed slot geometry on the same read-only root, classified locally as a boot
task. No entitlement context or storage.tmp/bindfs capability is granted. It
changes neither cleanup arguments nor results, enables no writes, and leaves
the master/root, display code and pstore intact. Tests exercise twenty changed
identities, invalid signed slots, wrong lengths, missing metadata, wrong or
writable roots and forbidden capability queries. Services and SpringBoard
remain unproven.

Host validation for this cleanup admission passed: 120 local tests, repository
integrity checks, Linux CI `43713815679`, and isolated kernel build `43713827487`.
The exact new kernel also passed the diagnostic QEMU baseline with three CRC
entry records and seven diagnostic PID1 heartbeats. This does not emulate
Apple's cleanup task. The original 16 GiB master rehash matched before packaging.
The checked 96 MiB BOOT candidate is
`bc50a99b72cbb6fe862eacfadb5d69cb8e163d8c3fd4412a77651029c96ffa8f`;
physical cleanup execution is still unproven. No new phone write is included in
these host checks; original BOOT remains restored while readiness is pending.

## Physical V15 result: cleanup executed; boot-cache loader rejected

Original BOOT was restored automatically, protected hashes were unchanged, and
a fresh whole-partition BOOT readback matched the original. Three valid entry
records survive. The 69,640-byte retained console SHA256 is
`c81ec593b98390e34258aa17f34020327675dc7b5dd56ebf2cdb435551904b7e`.

```text
dc_prep_temp_dir: mkdir(/private/var/dirs_cleaner/, 0700) failed with errno=30: Read-only file system
Boot task failed: launchd_cache_loader - posix_spawn: 85: Bad executable (or shared library)
```

The authentic cleanup executable ran and launchd continued. This does not prove
cleanup succeeded: the log reports the failed directory creation, and the system
logger also cannot bind its socket on the read-only filesystem. A writable data
volume is still absent. This trial enables no UFS write or root modification.

The next required boot task is now demonstrably rejected before execution.
`launchd_cache_loader` from the master is 72,336 bytes and matches staged source;
all 13 signed code pages and its XML/DER slots pass. The exact pin is recorded in
`xnu/a52q/ios16-20H392-launchd-cache-loader-pin.json`. The narrow admission change
checks that identity, CS_VALID, signed slot getters/pointers/lengths and the same
read-only root, then supplies the local boot-task classification. It creates no
entitlement context, AMFI provider or trust-cache response; it grants neither
`can-check-trust-cache` nor an IOKit user-client capability. Tests retain changed
hash, invalid/missing signed metadata, wrong-root and forbidden-capability cases
for both signed helper identities. Other optional helpers remain denied.

Independent read-only host inspection also extracted the original
`/System/Library/xpc/launchd.plist` and its detached signature. All 356 code pages
pass both the SHA1 and SHA256 CodeDirectories (version 0x20500). Neither CMS trust,
kernel admission of that data cache, cache-loader execution nor submission to
launchd is established. Observe the next actual failure before implementing any
cache/provider change. Persistent services and SpringBoard remain unproven.
