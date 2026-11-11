# Archived A52Q revision 3 diagnostic kit (superseded)

This records the earlier r3 manual test kit and is retained for provenance.
Do not use its old candidate for current XNU trials. See [A52Q.md](A52Q.md) for
the current hardware results, build artifacts and remaining milestones.
The user later explicitly authorized automatic BOOT-only diagnostic trials;
this does not authorize userdata formatting or other partition writes.

Use only for the already identified SM-A525F/DS, a52q, unlocked bootloader
A525FXXSCFYF1, and the unchanged BOOT/DTBO/RECOVERY/VBMETA captured in this chat.
If firmware or any of these partitions changed, stop and reacquire evidence.
Keep the kit private: it contains the phone's current custom-ROM BOOT backup,
not certified stock Samsung firmware.

## What changes and what can go wrong

- Staging the two image files below writes about 192 MiB into `/tmp`, which was
  verified as RAM-backed tmpfs in the connected TWRP. It writes no disk partition
  and is lost on reboot. Do not substitute `/data` or internal storage.
- Installing the candidate writes **BOOT only**, `/dev/block/sda19`, 100663296
  bytes (96 MiB). Android will not boot normally until the original BOOT is restored.
- Diagnostic code writes its own RAM plus the reserved console at
  `0xb4640000..0xb4680000`. This replaces the previous RAM console record.
- No userdata format or writes to RECOVERY, DTBO, VBMETA, bootloader, modem, EFS
  or partition tables are part of this procedure. Do not select those targets.
- Bootloader rejection, an indefinite splash/blank screen, or a watchdog reset
  are possible. RAM-log survival is unverified. Do not accept factory-reset,
  repartitioning, bootloader-relock or wipe prompts.
- Restoring BOOT is not a cure for every possible hardware/firmware failure.
  Matching full Samsung recovery firmware and an off-computer backup have not
  been verified here. Know this limitation before choosing to test. Samsung Knox
  warranty state, if changed, cannot be undone by restoring BOOT.

## Files to verify before doing anything

The private ZIP includes `original-boot.img`, `candidate-r3.img`, `SHA256SUMS.txt`,
and these instructions. Keep the original ZIP and extracted original image on
the PC throughout the test. An additional independent backup is recommended.

Expected SHA256 values:

```text
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016  original-boot.img
c4aa86c551e1c580ecce1640046344662e447659783915d379f4e7d0dd028374  candidate-r3.img
```

The first candidate is superseded: do not use a file without `r3` from earlier
artifacts. Revision 3 preserves the observed Samsung trailer and diagnoses
EL1 or EL2 entry. It remains unsigned and not verified on Samsung hardware.

## Stage files only after deciding to perform this test

Start in the existing TWRP with USB connected. Use a PC terminal in the extracted
kit directory, with the already downloaded Android platform-tools `adb` on PATH
or its full executable path. Check that exactly the intended phone is connected.

These commands are provided for manual execution; Codex has not run them:

```powershell
adb devices
Get-FileHash .\original-boot.img -Algorithm SHA256
Get-FileHash .\candidate-r3.img -Algorithm SHA256
adb push .\original-boot.img /tmp/a52q-original-boot.img
adb push .\candidate-r3.img /tmp/a52q-diag-r3.img
adb shell sha256sum /tmp/a52q-original-boot.img /tmp/a52q-diag-r3.img
```

Stop on any unexpected hash or transfer failure. Staging into `/tmp` is not a
persistent recovery backup; the original host copy must remain accessible.

## The actual BOOT write: perform in TWRP yourself

In TWRP, use **Install -> Install Image**, browse to `/tmp/a52q-diag-r3.img`,
select the **Boot** partition, check that Boot is the only target, and confirm
the write yourself. Do not choose Recovery, System, Vendor or any other target.
Reboot to System without installing extra TWRP apps or modifying other partitions.

Expect a splash/blank screen, not an Apple logo or usable OS. The diagnostic
records its results and parks; it does not start Android or reset automatically.
After roughly 10 seconds, force restart using Volume Down + Power for about
8-10 seconds. When the screen goes black, immediately use Volume Up + Power
with USB connected to boot the existing TWRP. The reset may lose the log.

## Retrieve the result immediately

After TWRP reconnects, read the old RAM console to the PC:

```powershell
adb pull /sys/fs/pstore/console-ramoops-0 .\a52q-diag-console.txt
```

A diagnostic success is an `A52QDIAG v1` record with stage 2. Stage `0xff` means
an exception and includes ESR/ELR/FAR. This demonstrates the shim only; it does
not demonstrate XNU, display operation, storage compatibility or iOS support.
An absent record does not identify the failure by itself. Restore BOOT either way.

## Restore the current ROM's BOOT before returning to normal use

The first `/tmp` copy disappeared on reboot. Push the saved original again:

```powershell
adb push .\original-boot.img /tmp/a52q-original-boot.img
adb shell sha256sum /tmp/a52q-original-boot.img
```

In TWRP, use **Install -> Install Image**, choose `/tmp/a52q-original-boot.img`,
and write it to **Boot only**. This second BOOT write restores the saved image.
Verify by reading its hash before rebooting:

```powershell
adb shell sha256sum /dev/block/by-name/boot
```

It must match the original hash above. Then reboot to the existing ROM. Do not
wipe or relock. If TWRP cannot be reached, stop; entering Download Mode is the
fallback, but a firmware-specific restoration plan must be reviewed before any
additional write. Do not improvise with PIT/repartitioning or downgrade images.
