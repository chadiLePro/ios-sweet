# A52 dirs_cleaner spawn failure: evidence and resolution

The usable V14 console reports:

```text
unable to adjust OSEntitlements context without monitor: 53
proc 12: load code signature error 4 for file "dirs_cleaner"
Boot task failed: dirs_cleaner - posix_spawn: 85: Bad executable (or shared library)
```

This was resolved by the exact-executable admission in commit `79dce98`, tested
physically in V15. V16 has no retained XNU console and does not replace that
baseline. Original BOOT was restored and freshly hash-verified after both trials.

## Who emits the messages and what is required

Apple `/usr/libexec/cc_fips_test` runs the real corecrypto POST; its reported
pass is not evidence of service startup. Apple `/sbin/launchd` emits the spawn
and boot-task errors. In V14 the rejected helper did not execute those messages.
The measured launchd's embedded Boot dictionary specifies:

```text
Program: /usr/libexec/dirs_cleaner
ProgramArguments: [dirs_cleaner, /tmp, /var/run]
RequireRun: true
RequireSuccess: true
PerformAfterUserspaceReboot: true
```

The retained PID1 initialization markers plus actual boot-task execution show
Apple launchd has reached its boot logic. The FIPS pass line alone does not.
The master links `/tmp` to `private/var/tmp` and `/var` to `private/var`.
The helper attempts directory creation under `/private/var/dirs_cleaner`,
directory metadata queries, directory swaps and/or recursive contents removal.
These operations require a writable data filesystem and supported attributes.

## Target errno and rejection path

The build pins XNU `8796.141.3`. Its `bsd/sys/errno.h` defines `EBADEXEC=85`,
`EROFS=30`, `ENOEXEC=8`, and `EBADMACHO=88`. The generated A52 header has the
same normalized text as this source; differing raw hashes are line endings.
Do not decode these values with Linux headers.

Static inspection of the actual Apple launchd identifies the boot-task call to
`posix_spawnp` at unslid address `0x10003fe1c`. The return register is saved in
`x22`; the failure branch passes that same value to `strerror` and the literal
`posix_spawn(): %d: %s`. It does not fetch a new global errno for this message.
XNU's libsyscall spawn wrapper converts a negative syscall result to the error
number, restores its saved errno and returns the error number directly.

For this capture, the source and logs establish the following chain:

1. `a52q_without_monitor` had no admission for the helper's exact signature and
   returned `KERN_DENIED` (53).
2. `ubc_subr.c::accelerate_entitlement_queries` reports that rejection and returns
   `EPERM`. `ubc_cs_blob_add` propagates the validation failure.
3. `mach_loader.c::load_code_signature` maps the failed blob registration to
   `LOAD_FAILURE` (4), producing the signature-error line.
4. `kern_exec.c::load_return_to_errno` maps `LOAD_FAILURE` to `EBADEXEC` (85).
5. Launchd reports the returned error for its required boot task.

Error 85 alone has other possible causes. The adjacent signature rejection,
the source path and the successful targeted retry establish this cause here.

## Exact executable audit and narrow patch

The master helper is 54,144 bytes, SHA256
`f9ee81f822c5577cf013182d11cfd730c4e7c803b5945d91dccc44661934e10f`, matching staged
source. It is a thin arm64 `MH_EXECUTE`, CPU `0x0100000c`, subtype 0; its interpreter
is `/usr/lib/dyld`, its sole direct dependency `/usr/lib/libSystem.B.dylib`.
`LC_MAIN`, `LC_BUILD_VERSION` (iOS), segment bounds and signature commands pass
the host audit. Nine signed pages and the signed XML/DER slots verify.
CDhash: `a93c2cbaed304f83e3df51faa21f961037f7c0ad`.
LibSystem is in the already verified shared cache; no new dependency admission
was needed. No Apple CMS authentication is claimed by these local checks.

`xnu/a52q/a52q_amfi.c` admits this exact CS_VALID identity only on the same
read-only full UFS root, after validating original XML/DER slot pointers and
lengths through XNU's signature getters. It supplies the local boot-task
classification. It creates no entitlement context, grants no storage.tmp or
bindfs capability, and leaves page verification and other admission checks on.
It does not change the helper, its arguments or return value.

The associated pin is `xnu/a52q/ios16-20H392-dirs-cleaner-pin.json`;
`tests/test_a52q_exec_policy.py` covers changed identities, invalid/missing
signed metadata, wrong/writable roots and forbidden capability requests.
120 host tests, repository checks, Linux CI and the kernel build passed. The
exact kernel also passed diagnostic QEMU; that fixture is not Apple userland.

## Actual V15 result and remaining storage requirement

```text
dc_prep_temp_dir: mkdir(/private/var/dirs_cleaner/, 0700) failed with errno=30: Read-only file system
Boot task failed: launchd_cache_loader - posix_spawn: 85: Bad executable (or shared library)
```

The original helper executed and launchd advanced past it. The Apple source's
normal main path logs cleanup errors then returns zero; acceptance of the task
does not mean its directories were cleaned. Additional dc_reset text in the
retained console is bit-corrupted, so its exact errno is not established.
Logger socket creation and launchd log-file creation also fail with EROFS.

A storage-backed `/private/var` would cover `/tmp`, `/var/run`, the cleaner's
scratch directory and `/var/log`. The prepared 4 GiB HFS data image is host-only;
installation into a new userdata byte range and UFS write support are not
approved or demonstrated by these BOOT-only trials. Keep the root read-only;
do not enable writes or replace var with RAM to suppress these errors.

The next observed fatal blocker is the required `launchd_cache_loader` signature
rejection. Its exact admission is already built and host-checked in `b4414cd`.
The first phone trial of that candidate, V16, retained only a missing-pstore-file
error and is inconclusive. A controlled retry is needed. Apple persistent
services, completed cleanup and a visible SpringBoard lock screen remain unproven.
