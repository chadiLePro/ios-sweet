# A52Q persistent iOS root: preparation and current limits

The 2026-11-14 non-journaled BOOT-tail trial retained these lines:

```text
hfs: mounted A52ReadOnly on device b(1, 1)
panic: rootvp not authenticated after mounting @bsd_init.c:953
```

This demonstrates a UFS-backed HFS mount, **not diagnostic PID1 from UFS**.
Original BOOT was restored and a fresh full-partition readback matched its saved
SHA256. The sealed-root check is skipped for RAM roots; that earlier test did
not exercise it. The A52 overlay now permits an unsealed root only when the
mounted device is its verified UFS window and the mount is read-only. It logs
`UNSEALED` rather than claiming Apple authentication. Other roots still panic.
The original 81 Redmi patches remain unchanged.

## Full image and executable inspection

The private validated master is a regular 17,179,869,184-byte HFSX image:

```text
ios16-20H392-pristine-v11.hfs.img
SHA256 0f4bcaa7c1a6f0a531c8b4d4d67b0dd8843b5ab58c2c31a005e07b1bde312149
```

Its `.hfs.verified.json` records a clean read-only filesystem check, disabled
journaling, 47 original core/cache checksums, 184,116 files and 137,189 folders.
A fresh full-image host readback matched that hash. The staged source, verified
transfer image and original pre-repair HFS image are retained. Unicode repairs
were limited to source-matching canonical names; journal-bit changes have a
rollback record. POSIX ownership/modes/links were preserved; Apple xattrs, ACLs
and BSD file flags were not preserved. These are material compatibility limits.

Read-only appliance extraction of the master produced checksum-identical
launchd, dyld and SpringBoard. `tools/a52q_userland_audit.py` found thin plain
arm64 executables, an arm64 `MH_DYLINKER`, valid executable-page hashes and
`/usr/lib/dyld` as launchd's interpreter. Launchd links libSystem and libobjc.
The main shared-cache header identifies arm64. This establishes format and
byte consistency, not Apple CMS authentication, entitlement support, a working
shared-cache mapping, complete syscall compatibility or execution.

The optional full-root execution policy pins only the audited 20H392 launchd
and dyld CodeDirectories, only while the full UFS root is published. It preserves
XNU code-page/structure checks and the diagnostic pin. Entitlement queries still
deny access; no platform status or Apple AMFI service is fabricated. Other
executables and the shared cache are not automatically accepted. This is an
instrumented next-stage experiment, not a policy sufficient for SpringBoard.

## Concrete storage layout

Captured primary/backup GPT CRCs and Linux sysfs agree on 4 KiB UFS blocks.
BOOT is only 96 MiB, super is about 9.67 GiB, and other named partitions cannot
hold this root. No partition is considered expendable because of its name or
apparent unused space. Android's encrypted F2FS free space does not imply raw
unallocated blocks available to XNU.

The proposed layout uses the **existing userdata partition**, without changing
GPT. These numbers apply to the captured SM-A525F/DS only and are revalidated:

| Region | UFS LBA start / count (4096 bytes) | Relative byte range in `/dev/block/sda31` |
| --- | --- | --- |
| Existing userdata | 3,165,696 / 27,911,647 | `[0, 114326106112)` |
| Read-only iOS root | 3,165,696 / 4,194,304 | `[0, 17179869184)` |
| Proposed future writable var | 7,360,000 / 1,048,576 | `[17179869184, 21474836480)` |

The root's absolute UFS byte range is `[12966690816, 30146560000)`.
Writing even its first 16 GiB destroys the existing encrypted Android data
filesystem. The untouched tail is not an Android backup and is not claimed
recoverable. The future var range is reserved in this plan only; it is **not
part of an initial root-only installation**. No GPT, metadata, modem, persist,
bootloader, recovery, DTBO or vbmeta write is part of this root layout.

The driver exposes a separate `/dev/a52ios0` selected by `rd=a52ios0`. It checks
the live primary GPT header CRC, entry-array CRC and userdata entry against the
captured plan, then checks the first root block through the BSD strategy path.
The kernel sees exactly 16 GiB, independently of the larger containing partition.
Block and raw writes return `EROFS` before submitting a command. There is no
RAMDisk property or diagnostic-init substitution in a full-root payload.

`tools/a52q_persistent_root.py` streams the regular host image with bounded
memory, checks its validation report/hash/headers and binds a root plan to the
exact kernel and captured UFS proof. `--ufs-ios-root-plan` passes it to the
payload builder and BOOT packager. The filesystem remains a separate file;
it is never copied into BOOT or into the embedded kernel payload.

## Writable state

The master has `/var -> private/var`, `/tmp -> private/var/tmp` and
`/etc -> private/etc`. A separate 4 GiB non-journaled host HFS image has been
prepared from the master's `/private/var`, preserving POSIX metadata and links.
A checksum-mode rsync comparison and filesystem check passed. The proposed
storage mount is that volume at `/private/var`, covering temporary files,
runtime state, logs, databases and CrashReporter directories. This is a disk
volume, not a RAM disk. Device nodes would still use devfs.

**The kernel currently has no bounded write implementation or data-volume mount
hook.** The first root-only experiment therefore remains entirely read-only and
may fail on an early write. A writable data volume requires those changes,
separate validation and separate installation approval. The existing Cryptex
files remain on the read-only root; Apple APFS role discovery, preboot updates
and any additional write requirements remain unimplemented. There is no fstab
in the extracted base image to silently repurpose.

## Installation and rollback contract

Host preparation is reversible and does not write the phone. Before a root
installation, present the exact candidate hashes, target/range and loss of
Android data. The user has explicitly waived a full userdata backup; retain
that waiver in the private install receipt rather than claiming a backup exists.
Retain and verify original BOOT/recovery/DTBO/vbmeta and a small metadata backup.
Unmount Android data and all its aliases before accessing raw userdata. Reject
changed partition bounds, unexpected devices, mounted userdata or short writes.

The prospective raw root write is equivalent to the following **after approval**:

```text
adb shell -T dd of=/dev/block/sda31 bs=4194304 count=4096 conv=fsync
```

It must receive the checked 16 GiB master on stdin through a bounded host
stream; do not push it into TWRP's RAM-backed `/tmp`. Verify the first 16 GiB
readback against the master SHA256 before installing a candidate BOOT. A
read-only device-side readback is equivalent to:

```text
adb shell -T "dd if=/dev/block/sda31 bs=4194304 count=4096 | sha256sum"
```

A full-root trial also temporarily replaces only the checked 96 MiB BOOT image.
Prepare its log-collection/restoration watcher first. On return to TWRP, capture
pstore, restore original BOOT and verify the whole partition hash; remain in
recovery. Volume Down + Power until black, then immediately Volume Up + Power
with USB connected returns to TWRP. Decline format/factory-reset prompts.

BOOT restoration does **not** restore Android data. Without a userdata backup,
returning to Android requires reinstalling the appropriate ROM and explicitly
formatting/reinitializing its data later; neither action is authorized by a
BOOT trial. The retained kernel/recovery backups do not make that data loss
reversible.

## Validation labels

The existing QEMU runner can test this exact kernel with a small diagnostic HFS
RAM root. It does not emulate the Samsung UFS controller or attach the full iOS
root as a block device. Do not label that check as an exact full-root boot.

Track these separately: UFS diagnostic mount; diagnostic PID1 from UFS; Apple
launchd executed; Apple services started; visible SpringBoard lock screen.
The guarded display frame is not IOMobileFramebuffer/IOSurface or a measured
60 Hz compositor. No graphics/daemon patch is justified by the rootauth panic.
