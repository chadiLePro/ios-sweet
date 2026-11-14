# A52Q iOS 16 shared-cache signature registration

The full iOS 16.7.16/20H392 root is stored on the approved 16 GiB userdata
prefix and remains read-only. The second full-root trial executed Apple dyld
and libignition, then reported:

```text
dyld cache '(null)' not loaded: code signature registration for shared cache failed
Library not loaded: /usr/lib/libSystem.B.dylib
initproc failed to start
```

These lines do not prove that Apple launchd reached main. The cache index
contains libSystem; fabricating a replacement dylib would hide the first failure.
Some other retained console bytes are corrupted, so source tracing and host
reproduction are recorded separately from intact log lines.

## Operation and rejection

Disassembly of the actual dyld-1067 binary identifies command 97 at offset
0x3a7b8, calling fcntl at 0x3a7bc: F_ADDFILESIGS_RETURN. XNU kern_descrip.c
passes the signature to ubc_cs_blob_add. Its
OSEntitlements.adjustContextWithoutMonitor callback previously admitted only
the diagnostic init and the two measured Apple launch executables. Each cache
CodeDirectory was rejected with KERN_DENIED (53). ubc_subr.c maps a failed
context adjustment to EPERM (1), so registration fails before cache loading.
A native harness compiled from the old policy reproduces rejection of all 44
verified cache hashes. This is independent of reset-corrupted console text.

## Completed integrity audit

All 44 cache file SHA256 values match the master's recorded original values:
3,330,359,296 bytes total. All 202,845 signed 16 KiB pages match their embedded
CodeDirectory hashes. The 44 unique directories use version 0x20400, SHA256,
flags 0x2 and platform 0; no cache has XML or DER entitlements. The signature
format is supported by this XNU parser. CMS presence is recorded, but Apple
CMS trust authentication is not claimed.

The private report is E:/A52-iOS16/cache-code-signatures-v1.json. Public
xnu/a52q/ios16-20H392-cache-pins.json contains only measured metadata/hashes.
The validated master SHA256 remains
0f4bcaa7c1a6f0a531c8b4d4d67b0dd8843b5ab58c2c31a005e07b1bde312149.
Neither the master nor installed root was modified for this fix.

## Narrow policy and checks

The A52-only callback admits those 44 CodeDirectory hashes only with the
full-root target a52ios0 and no entitlement object/XML/DER blobs. It grants
no entitlements, platform status or general signature exemption. Other cache
hashes remain rejected. The existing Redmi implementation is unchanged.

XNU's shared-region submap explicitly enables code-signing enforcement;
system cache enforcement defaults to enabled. Full-root packaging rejects
signature-disable boot arguments. cs_debug=2 enables the existing successful
signature-attachment log after registration, without a page-by-page log flood.

The exact new C policy passes all 44 pins and rejects 880 changed hashes,
unknown/NULL signatures, wrong-root use and entitlement-bearing cache contexts.
The host auditor rejects an altered page even if its expected whole-file hash
is updated. These are host tests, not a phone test of altered executable pages.

Kernel build 43607167940 succeeded, SHA256
b52bb868b5138677b0b99ecdbea80af773689768782d7cf4312be408a3054c76.
The exact kernel passed the small diagnostic RAM-root QEMU fixture. QEMU does
not emulate this Samsung UFS root. BOOT candidate SHA256 is
3c6224d3b9ca65e6cb98ab2fe94484ca5ae97fac1f76041ba3634654a4d69c37.
It keeps the previous ignition settings and adds only cache policy plus CS
logging. The physical registration result is recorded below; launchd main remains unproven.

A successful allowlist callback is not itself successful registration. Require
the post-attachment CODE SIGNING log for cache files, then distinct evidence
of Apple launchd reaching main. Userland services and a visible SpringBoard
lock screen remain separate, later milestones.

## Physical result: cache registration passed; mapping rejected

The third full-root trial retained 35 intact post-attachment CODE SIGNING lines,
plus damaged lines kept verbatim, through .42.dyldlinkedit. The .symbols companion
is audited but not requested by this loader. Dyld progressed to its shared-region
mapping syscall. Registration is therefore demonstrated on the actual A52;
this is stronger evidence than an allowlist acceptance message alone.

The next intact error is:

```text
dyld cache '(null)' not loaded: syscall to map cache into shared region failed
initproc failed to start
```

The preceding shared_region diagnostic identifies a missing SIP-protected vnode
flag. The pinned kernel source returns EPERM at its SF_RESTRICTED check. BSD
flags were not preserved by filesystem staging. The next A52-only patch permits
that one missing flag only for an already registered, valid, approved cache
CodeDirectory on the same read-only root mount. Root ownership checks remain
before it; normal cache-directory, signature-range and page checks remain after
it. No CSR boot argument, trust-cache success or general code-signing exemption
is introduced. Unknown/modified pins, unrelated/writable mounts, non-root
mounts, non-regular files and missing/invalid signatures fail the native harness.

The overlay also observes the existing PID1-only kern.initproc_spawned write,
which XNU documents as launchd reaching main. The actual launchd binary contains
that sysctl name. Logging does not set it or launch any program.

Full HFS build 43624481615/source a46569c passed. All 71 overlay source hashes
matched the reviewed source. Kernel SHA256:
09e97749a7856e81c640668665a20de36c21440ee3ea384c3ef13f5aa345c3a1.
That kernel passed the diagnostic QEMU baseline (three valid entries and seven
heartbeats). This does not exercise the full UFS filesystem or Apple cache.
New BOOT candidate SHA256:
64a78adae4d4ce7f50264cfabb3d8b1726984c4512f716e3abeb88235c3cd5ad.
The complete master hash was rechecked after a host-drive disconnect and again
matched 0f4bcaa7...312149. Physical cache-mapping/main results remain pending.
The previous trial's Original BOOT was restored
and freshly read back as d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016;
recovery, DTBO and vbmeta were unchanged. The root image was not rewritten.

## Physical result: cache mapping and Apple launchd main passed

The fourth full-root trial contains three intact markers:

```text
A52Q: PID1 set kern.initproc_spawned=1 (launchd main marker)
```

They are followed by Apple's own hello and Darwin Bootstrapper Version 7.0.0
messages, then system-domain creation. The actual launchd binary references
that sysctl 56 bytes after LC_MAIN. This demonstrates early Apple launchd main
from the full persistent UFS filesystem, beyond loader execution. It does not
demonstrate userland services or SpringBoard.

The next actual failure is fsck signature rejection, followed by:

```text
userspace panic: boot task is not a platform binary (fsck, /sbin/fsck)
```

The master fsck is checksum-identical to the native staged source. All 13
signed 4 KiB pages pass; no XML/DER entitlements are present. Actual launchd
calls csops(CS_OPS_STATUS) at offset 0x3feac; error or missing bit26 branches
to this panic. XNU derives that bit from csb_platform_binary.

The next policy explicitly classifies only that exact fsck CodeDirectory as a
local development platform boot task, only on the same read-only full A52 root.
It grants no entitlements and makes no Apple CMS trust claim. The cache policy
continues to grant no platform status. Native tests reject changed/unapproved
hashes, writable/unrelated mounts, entitlement blobs and missing/invalid signatures.
Kernel-only build 43627967750 succeeded; source/kernel hashes and its QEMU
diagnostic baseline passed. Candidate 1c78fb37...5f9d2e is ready for the next
BOOT-only phone trial; no root filesystem change is required.
Original BOOT was restored and freshly hash-verified after the fourth trial.

The first fsck-policy phone capture ended after CPU self-SGI initialization,
without root or fsck records, despite the user's three-minute wait. It is
inconclusive for the new policy. An immediate repeat produced no XNU log;
TWRP's log and unchanged Linux boot ID/uptime show that its GUI reboot path
restarted the recovery process rather than the kernel. Both trials restored
original BOOT. The private runner now requires recovery USB departure and
records Linux boot identity, using the installed native reboot command to
bypass that GUI path. A longer unchanged-candidate trial is pending. None of
these incomplete attempts proves fsck execution or invalidates the earlier
Apple launchd-main result.

A subsequent native reboot changed Linux boot identity but returned straight to
recovery. Its retained Linux log records restart command `shell`, with no XNU
entry. The pinned Samsung sec_debug_update_restart_reason source leaves the
PMIC boot reason unchanged for an unrecognized command; an `adb` prefix selects
normal boot explicitly. The next unchanged-candidate trial uses that supported
reason. This is a source-based hypothesis pending fresh XNU-entry evidence,
not a claim that the fsck policy passed. No raw PMIC, GPT or filesystem write
was added. Source: [pinned Samsung restart policy](https://github.com/LineageOS/android_kernel_samsung_sm7125/blob/f6bbda4e5986f09e4d51ceffd1b645b2d5aa75b4/drivers/samsung/debug/sec_debug.c#L337).

The explicit Samsung `adb` reason then reached XNU: a changed recovery boot ID,
three valid entry frames, three root-window frames and three Apple launchd-main
markers survived. BOOT was restored and its full hash matched. Fsck registration
now passes with flags 0x04000003, but launchd still rejects its platform status.

The missing contract is CS_SIGNED (0x20000000). kern_exec propagates that flag
to the process, and kern_cs.c::csproc_get_blob returns NULL without it. Therefore
CS_OPS_STATUS cannot inspect the registered blob's platform field. Existing
Redmi patch 0036 documents the same dependency. The next narrow change adds
CS_SIGNED only in the already verified fsck branch; other executable/cache
pins, entitlement denials and page enforcement remain unchanged. The native
policy regression check now requires this process-status visibility, while
retaining changed/unapproved hash rejection. Build 43632122116/source 92eede2
passed; its new kernel is b238ddc535b0eec0d9d47c3d10e4d76ee061e1544a6984a5526aff218828eb3d.
Physical fsck execution remains unproven; no root filesystem edit was made.
