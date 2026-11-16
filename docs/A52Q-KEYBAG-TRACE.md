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
