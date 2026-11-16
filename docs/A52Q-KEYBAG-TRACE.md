# Keybag failure after measured root-code admission

V21 admitted the measured seputil, mobile_obliterator, MSUEarlyBootTask and
keybagd. Apple keybagd ran and reported failure to load the system bag, then
requested recovery. FIPS passed all self-tests again (181 ms). This trial did
not reach launchd's early-boot completion, persistent services or SpringBoard.
The later `Halt/Restart Timed Out` panic comes from the shutdown timer following
the recovery request; it is not evidence of a graphics fault.

Original BOOT was restored automatically and independently rehashed; protected
partition hashes were unchanged. The 16 GiB UFS root remains read-only.

The exact keybagd was re-extracted from the unchanged master and matched the
full code catalog. Its SHA256 is
`747271703b7aff98420ed23788a362716025506d8d0ba8c703fb78e5b3ec1b9b`.
The master has no `/private/var/keybags` directory. Static inspection also shows
Apple KeyStore IOKit matching/open calls. The first failing operation and its
returned error still need direct observation. Neither a fabricated keybag nor
a fake successful boot-task result is justified.

`xnu/a52q/keybag_trace.py` adds A52-only diagnostics to the exact open1 and
single-service IOKit matching implementations. It snapshots the bounded pathname
before open processing, reports the original result unchanged, and observes the
already computed matching result. Open traces cover var/keybag and relative
paths, avoiding dyld/cache noise. Other processes do not produce these records.
Each trace kind permits 80 records. No file contents, keys, secrets, matching
properties, new memory maps or storage writes are introduced.

Because earlier console text contains bit corruption, each bounded record has
CRC32 and three copies. `tools/a52q_keybag_trace.py` rejects corrupted records
and conflicting valid copies. The existing pstore region, its initial entry
records and fatal-exit diagnostics remain intact.

`xnu/a52q/apply.py` stages the two transforms. The isolated relinker rejects an
archive predating or differing from this transform, so a full kernel build is
required. Tests compile the actual open helpers, check path/copy bounds, verify
unchanged errors and event limits, exercise CRC corruption/conflicts and prove
the non-A52 source text and original return paths remain unchanged.

The next BOOT-only trial should identify a missing path, a read-only failure or
an unavailable provider. It does not supply software KeyStore compatibility,
writable var, graphics or a working keychain. A future persistent var write still
requires its concrete layout and separate approval; no such write is included.

## Checked candidate, hardware result pending

Corrected source `a9783bdd96893c39b00caa86c35b97018c8b510a` passed 131 host
tests and CI `43909878860`. Full HFS build `43909951214`, attempt 2, compiled
and linked successfully; its 78 source-overlay hashes matched the expected
manifest. Kernel SHA256:
`a88f7cde889c19dff7b34932557332d54fde25c09a7008ac9b726734a91bbd88`.
The exact kernel passed its diagnostic QEMU fixture with three CRC entry copies
and seven PID1 heartbeats. That fixture does not run Apple's keybagd.

The preserved master was rehashed unchanged. The BOOT-only candidate SHA256 is
`f754ca8e4d85aca3bd4a851fefc7750408f6adc5bdff8d617e739e37a7c878a0`.
Packaging binds the kernel and read-only persistent root; no diagnostic RAM root
is included in the phone payload. Hardware trace results remain pending.

## V22 hardware result

Original BOOT was restored automatically and a fresh complete hash matched the
saved original. Recovery, DTBO and vbmeta also matched. The installed root was
rehashed unchanged before the trial, remained read-only, and its BSD window was
confirmed by two valid records. Three XNU entry records passed CRC validation.

The first KeyStore match returned:

```
match/1 class=AppleKeyStore result=0xe00002f0 found=none
match/2 class=AppleKeyStore result=0xe00002f0 found=none
```

Those records have three and two valid copies respectively. The target XNU
IOReturn header defines this value as `kIOReturnNotFound`. No system-bag file
open was observed. Timezone opens returned Darwin ENOENT; they do not establish
a keybag permission or read-only failure. Some other console text is corrupted
and has not been repaired or treated as an exact numerical result.

Static inspection of the verified 20H392 keybagd distinguishes the failed match
from its wrapper result: without a connection the wrapper retains generic
`kIOReturnError`, whereas its disk-load branch expects NotFound from the
system-bag query. The next bounded probe implements discovery and that empty
query contract only; see [the probe scope](A52Q-KEYSTORE-PROBE.md).
