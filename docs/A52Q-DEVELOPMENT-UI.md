# Opt-in A52 development KeyStore and CPU display candidate

This candidate attempts two new interfaces together. It does not establish that
keybagd completes, Apple services run, or SpringBoard draws. The physical display
baseline is the guarded RGB-bars test; a working A52 IOMobileFramebuffer
compositor and measured physical 60 Hz were not demonstrated by that test.

## Preserved baseline

The UFS transport, root window, root entry source, 2,786-identity catalog, AMFI
implementation, original display diagnostic, early logging, and memory exclusions
remain unchanged in their source files. An overlay hook appends an optional var
entry after the existing root wire; native checks compare that root entry byte
for byte with the old result. Without a var node, the table output is unchanged.
The original 81 patches and Redmi behavior remain separate.

## Development KeyStore

Only `a52q_dev_keybag=1` selects the requested synthetic no-passcode model. The
owning-task/connection checks remain. Selector 14 reports fixed system handle 0,
selector 7 reports unlocked-since-boot, and selector 17 reports the upstream
libaks DER state. Bounded companion state setters are compatibility stubs.
Save/load/wrap/unwrap crypto remain unsupported. This is not real Apple keybag
validation, software keychain encryption, SEP protection, or safe credential
storage. The normal empty discovery probe remains the default.

A separate host var clone contains `keybags/systembag.kb`, owner root:root,
mode 0600, under a 0700 directory. It is a plain property-list development
metadata file with a marked local KeyBagKeys payload, not an Apple/SEP bag.
The warm fixed-handle path avoids a claim of loading that payload as real keys.
The preserved root and original var image are not changed.

## Persistent var extent

The proposed data image occupies userdata bytes [17179869184,21474836480),
4 GiB immediately after the installed read-only root, without a GPT change.
An off-phone backup of exactly this range was captured and separately compared
with the device hash. Installing the var clone still needs explicit approval;
BOOT-only trial authorization does not cover this range.

The new read-only block proxy forwards bounded reads through /dev/ra52ufs0.
It verifies the existing full-root window, nonce, non-overlap, raw-device mapping
and first-block CRC before publishing /dev/a52var0. Every write returns EROFS.
The optional filesystem table mounts it read-only at /private/var. This first
candidate does not provide writable logs/databases, and does not claim that
all services can start with read-only var. No RAM-root/var replacement is used.

## CPU display bridge

Software-only Surface, Framebuffer and Watchdog sources are reused from the
fully patched upstream build, with exact input hashes. Cached IOSurface lookup
fix 0068 stays present. A52 physical surfaces are restricted to the captured
0x9c000000/0x9e4000 splash reservation, 1080x2400, stride 4320. Other surfaces
use managed kernel buffers: 32 MiB per surface and a conservative 96 MiB total
ceiling inside the existing 255 MiB kernel RAM allocation. No protected region
is removed from allocator exclusions.

The new adapter checks the 13 captured running display registers and performs
only the already-tested command-mode START write. It sends no panel commands
and changes no clocks, resets, SMMU or display-controller mode. Its kernel and
user framebuffer mappings use the same write-combine attribute. The old display
diagnostic cannot run at the same time. That mapping/periodic-use path is new
and needs a physical test; preserving the buffer geometry does not prove it.

The timer runs every 16667 microseconds and presents composed BGRA surfaces with
bounded CPU copies and guarded refresh. This is a software notification cadence,
not a measured panel refresh rate. The copy path is not an alpha compositor,
OpenGL implementation or Metal driver. No speculative hooks to Apple's opaque
renderer have been applied. Framework selection and fallback still need observed
service logs; a missing Metal device alone does not guarantee a CPU fallback.

The opt-in power provider reports synthetic 100% AC without PMIC/SPMI access.
The software watchdog accepts check-ins and never arms a hardware watchdog.
These placeholders do not supply graphics or prove service health.

## Validation and trial requirements

Host tests cover actual KeyStore dispatch/ownership, source-transform drift,
cached surface lookup preservation, native framebuffer pins and copy canaries,
proxy read bounds/write rejection, original root-wire preservation, and payload
kernel/root/board/flag binding. Kernel compile/link, diagnostic QEMU, host-image
checks and physical tests must be reported separately. A candidate should only
be flashed after packaging, review, new-data-range approval, and a restoration
watcher are complete. Keep the root read-only and retain pstore for the next
observed failure.

The actual adapter also runs in a native mock environment: absent/conflicting
profiles perform no MMIO mapping; bad hardware guards prevent framebuffer
mapping; the allowed START completes; and a timeout leaves the adapter failed
without a reset or later submit. CRC records are checked. This tests software
control flow, not the Samsung controller or physical display output.

## Changed source files

- `xnu/a52q/A52PlatformExpert.cpp`: opt-in development KeyStore dispatch,
  display nub, and development power registration.
- `xnu/a52q/A52DevelopmentPower.cpp`: explicitly synthetic AC power provider.
- `xnu/a52q/software_ui.py`: pinned Surface, Framebuffer and Watchdog transforms.
- `xnu/a52q/a52q_ui_bridge.c`, `a52q_ui_bridge.h`, `a52q_ui_profile.h`,
  `a52q_ui_copy.h`: guarded display adapter and bounded BGRA copies.
- `devices/a52q-ui-profile.json`: reviewed framebuffer and register evidence.
- `xnu/a52q/a52q_data_proxy.c`, `a52q_var_bounds.h`, `data_fstab.py`:
  separate bounded read-only var device and optional mount-table entry.
- `xnu/a52q/apply.py`: opt-in board source/configuration integration.
- `tools/a52q_ui_profile.py`, `a52q_persistent_data.py`, `a52q_payload.py`:
  evidence checks, persistent-data planning and explicitly bound payload profile.
- `tools/relink_a52q_console.py`: disallows reusing an incompatible old overlay.
- `tests/test_a52q_keystore_probe.py`, `test_a52q_ui_profile.py`,
  `test_a52q_ui_guard_runtime.py`, `test_a52q_data_proxy.py`,
  `test_a52q_persistent_data.py`: native and host regression checks.
- This document and `NOTES.md`: scope, evidence and handoff.

The inspection also covered the target XNU raw-to-block mapping implementation,
the original boot filesystem table, fully patched upstream software graphics
units, captured display/pstore records, master image validation, and the captured
GPT. Private dumps, Apple files and device-specific installation receipts are
not committed.

## V24 physical result and correction

V24 restored original BOOT with full readback; independent fresh BOOT, recovery,
DTBO and vbmeta hashes also matched. The user saw only the Samsung splash.
CRC-valid keybag records show selector 14 returned success, but systembag opens
still returned ENOENT and keybagd requested recovery. This does not prove an
unlocked keybag or completion of keybagd.

The new var block device verified its window/header, but the initial fstab entry
used pass 0. The pinned 20H392 mount executable (SHA256
ac55c4c7d200d0153cc266b39d69d4d771a9707ac91eefec94f83eb2522364df)
compares the entry's fs_passno with the requested phase at
0x100005290..0x1000052a0 and skips mismatches. This agrees with
[Apple's matching mount source](https://github.com/apple-oss-distributions/diskdev_cmds/blob/diskdev_cmds-701.100.2/mount.tproj/mount.c).
Pass 0 therefore skipped var in both phases. The correction publishes pass 2,
retaining the unchanged read-only entry and original root wire. The native test
now consumes the actual proxy's fstab callback, rather than a replacement entry,
and checks phase selection. Physical var mounting remains to be demonstrated.

Three CRC-valid A52G1 records report phase e0, zero frames: the UI adapter
rejected initialization. The original generic record cannot identify which guard
failed. New A52G2 diagnostics distinguish profile rejection, register mapping,
register-value mismatch (index/observed value), and framebuffer mapping. All
original guards and mappings remain enforced; this is diagnosis, not proof of a
fixed display adapter. Native tests check the detail CRC and rejection behavior.

## V25 physical result: persistent var mounted, timezone initialization blocked

V25 mounted `A52IOSVar` from `/dev/a52var0` at `/private/var` read-only. CRC-valid
records prove systembag opens returned zero; the development MKB task reached
`DONE MKB_INIT`. This is not real keybag cryptography or a functional keychain.
Usermanagerd subsequently attempted usersession/persona writes and saw EROFS.
Boot advanced to tzinit, which failed creating `/var/db/timezone/zoneinfo` with
Darwin EROFS (30). Original BOOT was restored and independently hash-verified,
along with recovery, DTBO and vbmeta. No visible UI was reported.

The preserved var subtree has no zoneinfo or icutz link. The preserved master
does contain `/usr/share/zoneinfo.default` and the timezone components under
`/usr/share/icu`. The exact tzinit SHA256 is
`1e13c6f7c32b810a043a5e28dccc1d24ddf83b69ddc3323d500d3aefa91ff9ef`;
all 27 signed code pages verified, CDhash
`3a1538960c0be7257ea41eaddeb7727c5ad61c25`. Its current-dataset parser at
0x10000642c..0x100006510 explicitly recognizes the system zoneinfo target.
Preparing a separate host clone with the system-default zoneinfo symlink fixes the
missing initial state without skipping or patching tzinit. The planner accepts
only that exact path/target and root ownership. The default ICU directory has
`icudt70l.dat` and `icutzformat.txt`, with no separate `icutz*.dat` patch; the
optional icutz link stays absent. The first host check incorrectly required a
patch file and failed; that unvalidated intermediate was never installed.
Actual Apple task completion
still requires a phone test; services may require a writable var afterward.
No writable UFS implementation or RAM-var replacement is introduced.

The display rejection identified register index 6, `0x0ae94008`: observed 0,
captured expectation 5, in two CRC-valid copies. This is DSI_STATUS, not a mode
register. The pinned Samsung
[MDP-idle implementation](https://github.com/LineageOS/android_kernel_samsung_sm7125/blob/f6bbda4e5986f09e4d51ceffd1b645b2d5aa75b4/drivers/gpu/drm/msm/dsi-staging/dsi_ctrl_hw_cmn.c#L1576)
polls bit 2 until clear. V26 permitted the two observed states 0/5,
but also waited at most 100 ms for idle zero before mapping or START. It rejected unknown
or error states. It never writes the status register to force success. Other
configuration guards, physical geometry, the old RGB diagnostic, UFS/root code,
code catalog, reservations and pstore remain unchanged. Native tests cover idle,
busy-to-idle, busy timeout, unexpected/error bits, and unchanged START timeout.

### V27: refresh idle-wait regression and the SpringBoard assertion

Original BOOT was restored with full readback and independent protected-partition
hash checks. The operator saw no console text. After one completed START, the
CRC-valid record `A52G2 f7d1eef0bf0947e4/05/06/00000005 e4066bc4` identifies the
next failure as our added DSI-idle wait at register index6, status5. The earlier
physically visible RGB diagnostic accepted that same captured status5, wrote
only START, and bounded START completion; it imposed no DSI-idle precondition.

The inspected pinned vendor
[pre-kickoff clock-change path](https://github.com/LineageOS/android_kernel_samsung_sm7125/blob/f6bbda4e5986f09e4d51ceffd1b645b2d5aa75b4/drivers/gpu/drm/msm/dsi-staging/dsi_display.c#L7910)
waits for DSI idle while a clock change is pending. Our refresh changes no clocks,
panel modes or DSI configuration. The correction removes that extra idle wait
and retains the exact observed status predicate0/5, all other configuration pins,
framebuffer mapping/geometry, sole START write, barriers and100ms completion
timeout. Unknown/error status still fails. Native execution now covers repeated
successful submissions while DSI remains5 and unchanged rejection/START-timeout
paths. Legacy timeout records remain decodable. Physical output needs a new test.

SpringBoard PID26/93 saved PC/LR0x1e0580ca8 and cache slide0x44c18000 have three/two
CRC-valid copies. Unslid PC0x19b968ca8 lies in FrontBoardServices, at `brk #0`.
The matching master's code and constant-cache files were fully SHA256-verified.
Decoding the referenced CFString using its actual cache slide-v2 mask yields
“failed to find the main CADisplay.” This establishes the failing assertion; it
does not establish why the main display object was unavailable. No assertion is
skipped and no fake display object is returned. Root, var, MKB and early boot
progress remain observed; the UEA capability fix still lacks positive runtime
proof in the retained log, which filled at about48.88 seconds.

V28 host candidate built successfully: sourcecf23c5a, HFS44942860068 and
hostCI44942854724 (150tests). All96 archived source hashes match, with only the
UI bridge implementation and comment-only profile header changed from V27.
Exact-kernel diagnostic QEMU passed3 entry records/13 PID1 heartbeats; the
pristine16GiB master rehash and independent BOOT payload validation passed.
BOOT SHA256 b6d971e320bcd61c4005b9fee7180a8510470b93a31c7994f59f0b7ddb5385f2.
The candidate is unflashed; physical console output and the main CADisplay
condition require the next phone trial. Original BOOT is restored and verified.
