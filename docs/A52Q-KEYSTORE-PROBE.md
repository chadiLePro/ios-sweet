# Empty KeyStore discovery probe for A52Q

V22 directly observed two AppleKeyStore matches returning NotFound. The verified
20H392 keybagd tries `IOService:/IOResources/AppleKeyStore`, then class matching,
opens user-client type zero and calls selector zero with no arguments. Its
system-bag wrapper then uses selector 14 with zero input scalars and one output
scalar. These shapes come from the unmodified master executable, not a guessed
SEP interface. The raw executable and disassembly remain private artifacts.

`A52PlatformExpert.cpp` now provides a narrowly scoped empty discovery probe for
`rd=a52ios0` only. It does not publish for diagnostic RAM roots or Redmi. The
service's compatibility matching name is AppleKeyStore and it explicitly labels
itself `A52QEmptyKeyStoreProbe`.

The connection retains its owning task, checks task ownership on every method,
and has a fresh/open/closed state. Selector zero performs the actual connection
handshake. Selector 14 reports NotFound without writing a handle because there
is no system bag. All other selectors report Unsupported. Malformed requests,
async calls, memory descriptors and variable structures are rejected. Connection
failure paths release their task/object references. Calls expose no file,
key material, physical mapping, lock state, crypto operation or storage writes.

Only keybagd method numbers and return codes are logged, bounded to 80 records
and protected by CRC triplicates. The decoder accepts the new `aks` record kind.
The expected next observation is keybagd's own disk-load path; successful bag
loading is neither implemented nor asserted. No boot task, reboot request or
failure status is converted into success. This is not a software keychain or a
substitute for SEP-backed data protection.

The native C++ check compiles the actual provider block and exercises malformed
requests, handle canaries, unsupported selectors, task transfer, closed/repeated
handshakes, initialization failures, reference cleanup, root gating and the CRC
record limit. These checks do not emulate Apple's keybagd. A kernel build and
physical trial are separate validation steps.

Working AMFI, UFS, mount/FIPS, display, memory reservations and pstore code are
unchanged. The full persistent root stays read-only and unmodified. A future
writable data volume or real software bag format still needs independent
implementation, validation and the concrete storage-write approval.

## Build validation

Source `205c4be52e9305a9d4cb1407402b8d893bde93d8` passed 132 native A52 tests,
repository checks and Linux CI 43922073263. Isolated platform rebuild
43922095033 succeeded using the verified 78-file full kernel 43909951214.
The only recompiled unit was `SweetPlatformExpert.cpp`, containing this A52-only
implementation. The kernel SHA256 is
`8b9c189d3b9c10c99f40b634255b79cfc8abe8ee5aae0fdb280e6ba1ff3d7352`.
Source/architecture/link provenance checks passed. The exact kernel passed its
QEMU diagnostic fixture with three CRC entry records and seven PID1 heartbeats;
the empty probe correctly remained unpublished for that RAM root. Apple keybag
loading and the provider's physical behavior remain unverified.

The master was fully rehashed unchanged before packaging. The checked 96 MiB
BOOT candidate SHA256 is
`62f4fc6ba95d8973fa75326fde3a2b83e99a49b97504d92986be928a32971464`.
It contains the kernel and persistent-root binding, with no diagnostic RAM root.
The next physical trial remains pending; it changes only BOOT temporarily and
restores the hash-verified original after recovery returns.
