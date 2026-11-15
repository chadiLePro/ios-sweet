# A52 local boot-cache query

V18 retained three matching fatal-exit descriptions:

```text
A52Q crash reason[1]: ns=7 code=0x1 desc=Unable to find AMFI
A52Q crash reason[2]: ns=7 code=0x1 desc=Unable to find AMFI
A52Q crash reason[3]: ns=7 code=0x1 desc=Unable to find AMFI
```

The original BOOT was restored and freshly hash-verified. The 70,470-byte saved
console SHA256 is `0dbc408843842045a90137005ccde7af280f2b98a1bdcc964595e35eff3ae0da`.
The reason copies are unprotected text, separate from the three CRC entry records.
This identifies the measured loader's missing IOKit service lookup. It does not
establish successful cache registration, service startup or SpringBoard.

## Observed contract and scope

Static inspection of the exact 20H392 loader follows its successful code checks
to `IOServiceMatching("AppleMobileFileIntegrity")`, user-client type 0, then:

| Field | Accepted value |
| --- | --- |
| Selector | 6 |
| Input scalars | One scalar equal to 1 |
| Input structure | Exactly one recognized 20-byte CodeDirectory cdhash |
| Output scalar/structure counts | Both zero |
| Memory descriptors and asynchronous requests | Rejected |
| Caller | Exact signed loader, owning task, same read-only full root |

The query precedes `SecCodeMapMemory`. A legacy IOUserClient implements this one
observed operation. Other selectors, caller identities and argument forms are
rejected. Connections retain their owning task; every method rechecks the owner
and the signed identity so a forwarded connection is insufficient. Original
XML/DER metadata is verified; no global entitlement context, IOUserClient-class
array, trust-cache privilege or other entitlement is fabricated.

The compatibility service and class names satisfy the observed lookup. This is
a local development measurement service, not Apple's AMFI implementation or CMS
authentication. The registry property `A52QLocalDevelopment` labels that scope.
There is no cache-upload API, signature-enforcement disable or hardware provider.

## Recognized content and kernel registration

Only the original `/System/Library/xpc/launchd.plist` and its `.sig` are recognized.
Their complete sizes and SHA256 digests, both signed CodeDirectories and query
metadata are in `xnu/a52q/ios16-20H392-launchd-cache-pin.json`. All 356 code pages
verify under both directories. The full file digests also match the preserved
native staged source, independently of the master extraction.

For a query, the kernel reads and SHA256-measures both exact paths, verifies
regular-file type and exact lengths, and requires the actual read-only a52ios0
root mount. It accepts only the recorded CDhashes. Unknown hashes, altered file
or signature bytes, wrong lengths/mounts, and failed reads reject. No filesystem
write or mutable measurement cache is introduced.

Detached registration of this same data cache additionally requires the
registering blob's vnode to be the measured path's actual vnode, CS_VALID, no
entitlements and an exact recognized CodeDirectory. Core XNU signature format,
special-slot, range and page checks continue. The data cache gains no platform
classification or entitlement. All other executable/cache admission rules stay
in force. XNU performs the AMFI callback before taking its vnode lock; the
measurement reads use ordinary `UIO_READ`, not a recursive locked-vnode read.

## Files and validation

- `xnu/a52q/A52PlatformExpert.cpp`: software service, guarded connection lifecycle
  and the single external method.
- `xnu/a52q/a52q_amfi.c`: caller authorization, read-only VFS measurements and exact
  detached data-cache admission.
- `xnu/a52q/a52q_boot_cache_policy.h`: shared request and identity boundaries.
- `xnu/a52q/apply.py`: stage that header into both existing translation units.
- `xnu/a52q/ios16-20H392-launchd-cache-pin.json`: audited content identities.
- `tests/test_a52q_boot_cache.py`, `tests/test_a52q_exec_policy.py`: compile the
  actual policy; reject mutated hashes/digests, malformed arguments, changed
  metadata, wrong/writable roots, wrong callers and unrelated capabilities.

121 local host tests and repository integrity checks pass. These tests cover
policy boundaries, not a live VFS/IOKit exchange. The new service still requires
a full kernel build, exact-kernel diagnostic QEMU and a recoverable phone trial.
Storage drivers, display, reserved RAM and fatal-exit/pstore logging are intact.
The full root/master stays read-only and unchanged; writable var is not installed.
