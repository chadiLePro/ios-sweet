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

Full HFS build 43624481615/source a46569c is pending. Original BOOT was restored
and freshly read back as d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016;
recovery, DTBO and vbmeta were unchanged. The root image was not rewritten.
