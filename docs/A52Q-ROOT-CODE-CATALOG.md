# Measured 20H392 root code admission

V20 completed early boot and admitted xpcproxy. Its children reached service
exec attempts; SpringBoard, notifyd, configd and backboardd were then rejected
at signature admission. The saved backboardd line contains a corrupt byte
(`load #ode`); the original capture is preserved. Missing persona type 6 and
read-only var errors also remain. Original BOOT was restored and independently
rehashed. Persistent service startup and UI composition remain unproven.

The catalog replaces incremental service admission with a set derived from the
unchanged master image. The isolated Linux appliance attached both the master
and the stopped development distro as read-only virtual disks; ext4 used
`ro,noload`. Its Python scanned the master without changing either disk.

The traversal audited 181744 readable regular paths, including 2790 signed
Mach-O files with 2786 distinct CodeDirectory identities. All 252793 signed
code pages and 2910 signed XML/DER metadata slots verified. The existing 44
shared-cache containers retain their independent admission/page checks.

Two Thai WorkflowKit `.shortcut` resource paths could not be read through Linux
HFS lookup even after normalization attempts. They are listed, unmeasured and
unadmitted. Five kernel extensions and four non-ARM64 Metal archives are excluded.
This does not claim successful execution or exhaustive readability of every
resource in the filesystem. Every requested core/service executable appears in
the measured set. Backboardd's absent Apple-internal liblinkguard load is weak
(`LC_LOAD_WEAK_DYLIB`); no replacement library is manufactured.

The generated header records each exact CodeDirectory identity and signed-slot
lengths. A binary search checks membership, CS_VALID, the actual read-only
a52ios0 root mount, regular vnode type and the original metadata getters,
pointers and lengths. Core XNU continues validating signed pages and special
slots. Successful admission adds CS_SIGNED and local CS_PLATFORM_BINARY status.
It does not manufacture CS_VALID, ad-hoc status, get-task-allow or an entitlement
context. These flags are not substitutes for executable validation. This is
local development trust in measured content, not Apple CMS authentication.

Unknown or changed identities, invalid metadata and wrong/writable mounts remain
rejected. A future writable var mount receives no implicit code trust. Existing
exact mount/bindfs and cache-loader query rules remain separate; the catalog
does not grant those privileges to other services. Signed entitlements may need
further implementation when actual consumers fail. No fake SEP, power, watchdog,
IOSurface, GPU or framebuffer provider is introduced by this admission change.

Files:

- `tools/a52q_root_code_catalog.py`: bounded read-only scanner and header emitter.
- `xnu/a52q/a52q_root_code_catalog.h`: generated identity/metadata table.
- `xnu/a52q/ios16-20H392-root-code-catalog.json`: audit totals, exclusions, hashes
  and selected service identities; no Apple executable bytes.
- `xnu/a52q/a52q_amfi.c`: measured catalog membership and admission.
- `xnu/a52q/apply.py`: stage the new header; other implementations stay intact.
- `tools/relink_a52q_console.py`: reject an old or mismatched catalog baseline.
- `tests/test_a52q_root_code_catalog.py`, `tests/test_a52q_exec_policy.py`: synthetic
  page/slot mutations, malformed fat slices and actual C-policy boundary checks.

The native policy test checks every catalog identity, 55720 changed hashes,
invalid signed metadata, missing CS_VALID, wrong/writable roots and forbidden
capabilities. Full kernel compilation and exact-kernel diagnostic QEMU are
separate from the hardware trial. The validated master, UFS driver, mount/FIPS
work, memory reservations, guarded RGB display test and pstore code are unchanged.
RGB bars establish physical framebuffer output; they do not establish a working
IOMobileFramebuffer/IOSurface/CoreAnimation pipeline or visible SpringBoard.

Validation: all 128 host tests, repository checks and Linux CI `43900310051`
passed. Full HFS kernel build `43897768441` succeeded with legacy warnings and
no build errors. All 76 archived overlay hashes matched the expected sources.
The generated header hash uses canonical LF; the initial Linux integrity-test
failure from a Windows CRLF hash was corrected without changing measured
identities or compiled C/header content. The redundant automatic build was
cancelled after the successful full build.

The exact kernel passed diagnostic QEMU with three CRC entry records and seven
diagnostic PID1 heartbeats. This fixture does not execute Apple services. The
master was rehashed before packaging BOOT SHA256
`63a6199b0dcc3254cfe3c588f350ebb25a0360519212d19aaab41d122e55012a`;
kernel SHA256 is
`b9f5ab95d6c57d13efb9bcebbf72a2d320ee4d6264b0dc3ffaf289bbe36833a3`.

The recoverable phone trial temporarily replaces only BOOT `/dev/block/sda19`,
bytes `[0,100663296)`, then retains the first log and restores the original full
BOOT with readback when TWRP returns. C: holds the verified original backup;
recovery, DTBO and vbmeta are hash-checked. No root/data formatting or other
partition write is included. The installed root stays read-only and unchanged.
Original BOOT restoration cannot recover the Android data destroyed by the
earlier approved 16 GiB root installation. Recovery requires Volume Down + Power
until black, then immediately Volume Up + Power with USB. Physical service
startup and graphics remain questions for the retained trial log.
