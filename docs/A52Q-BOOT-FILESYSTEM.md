# A52 read-only boot filesystem contract

V10 reached Apple launchd main, fsck and mount from the full UFS root. Its log
then reported `mount_hfs: Read-only file system`, `mount: / failed with 1`, and
`failed to get boot manifest hash`. BOOT was restored and fully hash-verified.
This is not a services or SpringBoard result.

## Why mount attempted to write the root

The validated root has no `/private/etc/fstab`. The exact cache's
`/usr/lib/system/libsystem_info.dylib` has LC_SOURCE_VERSION 564.120.2. Its
[matching Apple source](https://github.com/apple-oss-distributions/Libinfo/blob/Libinfo-564.120.2/lookup.subproj/file_module.c)
first queries the embedded filesystem table; if absent, it synthesizes an `rw`
root entry. The mount binary is diskdev_cmds 701.100.2. Its
[matching source](https://github.com/apple-oss-distributions/diskdev_cmds/blob/diskdev_cmds-701.100.2/mount.tproj/mount.c)
skips an already mounted read-only root only when its table entry also says
`ro`. An `rw` entry instead requests a root upgrade, correctly rejected by our
read-only block driver. No UFS write capability should be added to fix this.

## Measured consumer interface

Read-only inspection of the checksum-validated cache found the sysctl name
`vfs.generic.apfs.edt_fstab` at VM 0x1946faff6. Its consumer references it at
0x1946e2a24 and 0x1946e2a5c. The 0x1946e2dec..0x1946e2f0c code divides the
returned byte count by 236, advances each entry by 0xec, and copies these fields:

| Offset | Content | Wire space |
|---|---|---|
| 0x00 | fs_spec | 32 bytes |
| 0x20 | fs_file | 64 bytes |
| 0x60 | fs_vfstype | 32 bytes |
| 0x80 | fs_mntops | 64 bytes |
| 0xc0 | fs_type | 32 bytes |
| 0xe0 | fs_freq | signed 32-bit |
| 0xe4 | fs_passno | signed 32-bit |
| 0xe8 | not consumed by this code | four zero bytes |

The implementation publishes exactly one entry: `/dev/a52ios0 / hfs ro ro 0 1`.
It requires the verified full-root device to be the actual root device, a root
vnode mounted as HFS, and both MNT_ROOTFS and MNT_RDONLY. Other roots and writes
to the sysctl fail. No data volume, APFS filesystem, container operation, or
successful read-write remount is advertised. Other board targets are unchanged.

The native test compiles the actual callback with VFS/sysctl fixtures and checks
wire bytes, size queries, short output, writes, and wrong/unmounted/writable
roots. Kernel compilation, diagnostic QEMU and actual Apple mount consumption
remain distinct checks; the native fixture does not prove phone execution.

## Separate missing boot-manifest identifier

Mount also unconditionally requests `/chosen/boot-manifest-hash` before its
optional preboot bind mounts, including in its `OTHER` boot environment. A52 has
no Apple boot manifest. The Redmi target's fabricated hash is not reused.
The opt-in `--local-boot-manifest` identifier derives from an explicit canonical
JSON document containing measured SHA256 values for the actual kernel, full
root and captured live board DTB, plus the format, target and
`local-development-unsealed` trust label. The document uses sorted JSON keys,
ASCII and separators `,`/`:` with no whitespace or trailing newline. Its SHA384
is the 48-byte namespace identifier; the exact document is also embedded in
`a52q-local-boot-manifest` beside it. There is no hash of the containing BOOT
image, so no circular measurement. No Apple manifest or authentication is
claimed, and no signature/entitlement decision is based on this identifier.

Packaging recomputes both chosen properties from the separately validated
kernel/root/board measurements, rejects duplicate or undeclared properties,
and requires explicit full-UFS-root development mode. Changing the content,
hash, trust claim or measured inputs fails checks even after updating the
container checksum. Legacy payloads without either property remain supported.
The phone root still needs its independent whole-prefix verification before
each trial. This unsealed identifier is not a root of trust and does not provide
the firmware bind mounts required by the main-OS path. Its physical consumption
by Apple's mount remains to be tested.

The installed root and validated master remain unchanged and read-only. Writable
`/private/var` still requires a separate bounded, storage-backed implementation
and approval for a new storage range; no RAM-root replacement is involved.
