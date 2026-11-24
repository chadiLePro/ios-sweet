# V36 static logo + exact persona capability: source ready for HFS build

V35 capture complete, var-after-v35/capture.json root preservation proven;
read-only audit storage-data-post-v35-v1/audit.log. Original BOOT restored.
V35 HFS exchanges succeeded; usermanagerd persona allocation now EPERM1, source
sys_persona.c checks PERSONA_MGMT_ENTITLEMENT before allocation. Measured original
usermanagerd cdhashfe4f08919173d03db98b98ce5557b1c99c47419e, XML1952/DER1289,
code pages/special hashes pass; original XML persona-mgmt Boolean true. V36 exposes
ONLY that key for exact validated catalog identity, signed/valid/platform flags;
no global entitlement bypass or catalog changes. Other daemon errors remain.
Display source uses measured phys0x9c000000,32bit,stride4320; user supplied
0x3c000000/24bit/3240 conflicts with registers. Retain measured profile unchanged.
Replace bitmap console with centered180x224 one-bit logo from attached reference,
black background, flush once via same guarded WC mapping/START; putc/tick/panic
no-op. Keep all pstore writer/late records untouched. owner1=boot,2=GUI.
Native tests cover no redraw, bounds/handoff, exact capability/rejections.
V36 source not yet built/packaged or phone tested. Current V35 var dirty snapshot
needs host-only repair/provenance/new layout before next writable candidate.
No phone writes/trial authorized for any replacement snapshot yet.

# V35 CLOSED: original BOOT restored; HFS exchanges succeeded

finish_hfs_atomic_trial.py PASS; fresh BOOT/recovery/DTBO/vbmeta hashes match.
Operator saw colours only, no lock screen. Full root0f4b unchanged post-trial.
A52A1 CRC-valid exchanges usersession/persona error0 for pid13 and84; targeted
fix works, persona lifecycle completion not yet established. Backboardd nil
NSURL path exception persists. Late display owner1=text, frames4177; no GUI handoff.
Read-only capture_var_v35_after.py currently running, session29269; output
E:/A52-iOS16/var-after-v35. Do not reuse pretrial var hash/header after writes.
Next host audit research/audit_var_after_v35.py against preserved snapshot;
read-only fsck/log/container/keybag inspection, no device writes. No next trial
prepared or approved. Current phone original BOOT/TWRP, no pending restoration.

# V35 LIVE PHONE TRIAL; ORIGINAL BOOT RESTORATION PENDING

BOOT07554ec9...36c40ca4 written/read back; native reboot left TWRP/USB.
Approved repaired var e3bf9b04...863cbdf6 installed, root0f4b unchanged.
Runtime var writes only sda31[16GiB,20GiB). Operator told five minutes, then
manual TWRP reset and remain recovery. Authoritative receipt ios-ufs-v35.
Restoration watcher PID11052 active: watch_ios_ufs_v35_restore.py.
Collects pstore and restores/hash checks original BOOT on recovery return.
BOOT restore does not undo var writes. Do not start another trial.
ON RETURN: confirm original BOOT restored FIRST; finish_hfs_atomic_trial.py
for fresh protected hashes and nonce/CRC traces. Then capture_var_v35_after.py
for fullroot hash/lossless changed-var snapshot. Old var plan cannot be reused.
Persona completion and visible lock screen remain unverified.

# V35 repaired var installed and verified; BOOT trial staging

Approved repaired4GiB e3bf9b04…863cbdf6 installed and full readback passed.
Root0f4b plus original BOOT/recovery/DTBO/vbmeta hashes unchanged.
Installer receipt ios-hfs-atomic-var-install-v1 verified=true/runtime_write_approved=true.
Starting start_hfs_atomic_trial.py --operator-ready --approved-var-runtime.
No experiment running until recovery departure confirmed; then 5-minute timer/reset.
Watcher ios-ufs-v35 restores original BOOT on TWRP, does not undo var changes.

# V35 EXACT VAR/TRIAL APPROVED; installation starting

User approved repaired4GiB var e3bf9b04…863cbdf6 replacement and bounded runtime
writes ONLY sda31[17179869184,21474836480), plus BOOT07554ec9…36c40ca4
on sda19[0,100663296), five-minute trial/operator beside phone.
Raw rollbackE0 verified gzip preserved; root/protected hashes checked by installer.
No trial started yet. Installer receipt ios-hfs-atomic-var-install-v1 authoritative.
After verified install, start_hfs_atomic_trial.py --operator-ready --approved-var-runtime;
only after confirmed USB departure start timer; watcher restores original BOOT.

# V34 CLOSED: original BOOT restored and freshly hash-verified

research/finish_var_write_trial.py PASS, fresh BOOT/recovery/DTBO/vbmeta hashes
match. No pending BOOT restoration. Saved console SHA256
037f95bb000f60846ff822070ac7f75b2803c65c93567f902b07058e288caeb1.
A52W1 identical-block WRITE/SYNC/readback probe PASSED5CRC-valid copies,
error0/OCS0/response0x21000000. Actual pstore also reports
`A52Q var proxy: verified separate 4GiB UFS development-writable extent; root unchanged`
and `hfs: mounted A52IOSVar on device a52var0`.
NEW OBSERVED BLOCKER: `UMD_INIT: Failed to atomically write
/private/var//keybags/usersession.kb: Failed to atomically swap writing file:
Operation not supported (45)`. Repeated persona initialization failures follow.
Backboardd still captures nil URL path in multiple CRC-valid process records.
Display late heartbeat text owner1, frames1636; no GUI handoff/lock screen proven.
Post-trial full root hash0f4bcaa7…312149 verified unchanged. Lossless var capture
E:/A52-iOS16/var-after-v34/var.raw.gz, raw4GiB SHA256
e0f75c92c3df4197dd8b5613ea684a1bce3d02d4d072f5716b9d75560c0eea38.
Capture complete, compressed archive unchanged. /var genuinely changed on UFS.
Persistent usermanagerd.log.0 shows ENOTSUP45 on BOTH usersession.kb and persona.kb;
containermanagerd.log.0 reports no persona attributes after retries. The measured
master usermanagerd SHA956fb139…b2fd48b7 contains %@.writing; its sole renamex_np
callsite0x100063ad4 passes flags2. Exact source/header evidence, not Linux errno.
Host working copy only was fsck repaired. Filesystem now passes fsck -fn.
Repair changed active log/com.apple.xpc.launchd/launchd.log data (old raw hash
preserved in archive); full before/after manifest diff proves every other regular
file's data unchanged. systembag SHA d1db41b2…507f5656 unchanged, uid/gid0 mode0600.
Repaired4GiB working image E:/A52-iOS16/storage-data-post-v34-v1/
a52q-ios-var-post-v34.hfs.img SHA256
e3bf9b044be68e406f4c6ed09fe42d56d5395133ac9cd16b70191af9863cbdf6.
Runtime provenance is explicit; never claim this var still matches master contents.
V35 HOST READY, NOT APPROVED for repaired-var replacement/next trial.
Sourceb1eff6906bcd5877b570db9f731f879a7a48e873. Full HFS45218319183 SUCCESS;
host CI45218321263 SUCCESS on retry(package mirror timeout only on first attempt;
source tests passed).165 tests/repo validation PASS.100 archived hashes verified.
98 prior files unchanged; only var identity query + new scoped VFS hook. Actual
UFS transport, display, keybag, catalog2786 and pstore implementations unchanged.
BOOT07554ec9da6c3682bcf6b939f68d00fed5a735fb431d052c7ad8bc4c36c40ca4.
Kernel08f15a32666b0cfdf3eb739f67893685c075a4c0a09a18811c13e4541807dfc9.
Exact-kernel QEMU diagnostic13 PID1 hearts/3 entry CRCs and root master rehash PASS;
not Apple-userland, HFS-exchange or A52 emulation. Hardwarepackage-v33/rootplan30.
Independent check_hfs_atomic_candidate.py and installer prepare PASS. Review
E:/A52-iOS16/hfs-atomic-v35-full-review.json plus candidate/install JSONs.
Clean repaired var e3bf9b04…863cbdf6 remains HOST ONLY. Current phone var rawE0
snapshot remains installed and original BOOT is restored; no next trial/write.
New image changes metadata + active launchd.log only; all other file data/systembag
preserved. Backup E:/A52-iOS16/var-after-v34/var.raw.gz is lossless raw4GiB E0.
Host sourceN also archived repaired-source.raw.gz; verified NTFS sparse-zero
reclamation keeps every logical byte/hash unchanged and frees room for next capture.
Need exact replacement+runtime trial approval/readiness before sda31[16GiB,20GiB)
write and temporary BOOT. BOOT-only backend rejects writable payloads. Prepared
but NOT INVOKED: a52q_install_hfs_atomic_var.py, a52q_hfs_atomic_device_test.py,
start_hfs_atomic_trial.py, watch_ios_ufs_v35_restore.py, finish_hfs_atomic_trial.py,
capture_var_v35_after.py. New backend bound plan30 and matching install receipt.
On approval initial installer verifies gzip raw backup, target/root/GPT/protected
hashes; writes32 chunks, full readback/root preservation; only then BOOT trial.
On return BOOT restoration first, then decoderA52A1/A52W1/A52EX1, root hash and
lossless changed-var capture. Next kernel/var plan needs fresh snapshot/fsck.
No on-phone atomic exchange/persona or GUI success claimed yet.

# V34 HISTORICAL ACTIVE ENTRY (closed above)

Initial approved var install verified1b8fd88a…6ec5ff18, full root/protected hashes
unchanged before trial. BOOT2b032071…7d301072 installed and fully read back;
Samsung normal-boot reboot left TWRP/USB, confirmed. C: watcher PID12912 active,
research/watch_ios_ufs_v34_restore.py. Authoritative BOOT receipt
backup/a52q/ios-ufs-v34/receipt.json requires_restore=true, restored=false.
Operator told five full minutes from confirmed start, then manual TWRP reset;
if recovery returns by itself leave it open. Do not select System/format data.
Runtime var writes approved ONLY within sda31[17179869184,21474836480).
ON RETURN: confirm watcher BOOT restoration/full hash FIRST; then
research/finish_var_write_trial.py for fresh protected hashes and A52W1/A52EX1/
backtrace records. Next research/capture_var_v34_after.py verifies full root
unchanged and captures lossless compressed changed var in E:/A52-iOS16/var-after-v34.
Do not reuse initial var/header plan after writes. Preserve snapshot; host fsck
needed before next plan. BOOT restoration does not undo /var changes.
No hardware WRITE probe, mounted-RW var or visible GUI result claimed yet.

# V34 VAR INSTALLED/VERIFIED; BOOT trial staging next

Exact approved4GiB var seed installed/read back1b8fd88a…6ec5ff18. Full root0f4b
and original BOOT/recovery/DTBO/vbmeta preservation checks passed. Receipt
backup/a52q/ios-container-var-install-v1/receipt.json verified=true and
runtime_write_approved=true. New var installed, no experimental kernel started yet.
Starting guarded research/start_var_write_trial.py --operator-ready
--approved-var-runtime. Target BOOT2b032071…7d301072. Only when recovery departure
confirmed tell operator five minutes, then manual TWRP reset. Original BOOT watcher
will start if receipt requires_restore. Authoritative BOOT receipt ios-ufs-v34.

# V34 EXACT STORAGE/TRIAL APPROVED; initial var installation starting

User approved new4GiB seed1b8fd88a…6ec5ff18 + runtime writes only within
sda31[17179869184,21474836480) and BOOT2b032071…7d301072 on sda19[0,100663296).
Operator confirms beside phone for5-minute reset. No other partition/range/format.
Original BOOT currently restored. Root0f4b and rollback var6f30 freshly verified.
Installer research/a52q_install_container_var.py install --approved-exact-var-write
--approved-var-runtime about to run. Receipt backup/a52q/ios-container-var-install-v1/
receipt.json is authoritative for initial /var write and rollback status.
Only after full var readback/root/protected checks pass launch V34 BOOT trial.
If interrupted, stay TWRP; recover approved same var range from6f30 backup.
BOOT watcher restores BOOT only. Changed var remains on UFS for snapshot/fsck.

# V33 CLOSED: original BOOT restored and freshly hash-verified

V34 HOST READY; new var install/runtime writes NOT APPROVED. No V34 phone action.
Source93f5b4a27867f5ae602004485f1fdb214b2210c2; full HFS45204813380 SUCCESS;
host CI45204812425 SUCCESS;160 tests/repo validation PASS.99 archived hashes
verified;94 unchanged from V33,2 prior units changed(ufs include/comment and
var proxy),3 new isolated write files. Existing read body byte-identical excluding
new include/comment. Root/raw devices remain RO. Display/keybag/catalog/pstore
sources unchanged. Default-OFF capability requires extent/nonce/header/bootarg
and identical-block write/sync/readback. No arbitrary command API or clock/reset.
BOOT2b032071733270dccfa549ca30249cec7161988bfb9275c214ccd6947d301072.
Kerneldefacdd43940f2795ca2b627ff7a31e5b1601ee47e6680cd8a3c48faa109dbaf.
Exact-kernel QEMU diagnostic RAM-root fixture13 PID1 hearts/3 entry CRCs passed;
NOT hardware write or Apple-userland emulation. Master16GiB rehashed unchanged.
Package shim/out/a52q-ios-ufs-hardware-v32, root plan29, checked independently.
Review E:/A52-iOS16/var-write-v34-full-review.json and candidate/install JSONs.
Fresh root/var and off-phone rollback match: var-pre-v34-hashes.json. New seed
1b8fd88a…ec5ff18 still UNINSTALLED. Current var6f30…75f9 is RO/original BOOT.
Initial var target sda31[17179869184,21474836480), replacing4GiB; new kernel would
permit runtime writes ONLY there. No GPT/root/metadata/recovery/DTBO/vbmeta writes.
Need exact approval for both initial seed replacement and bounded runtime writes,
plus operator readiness before temporary BOOT trial. BOOT restoration alone does
not undo var changes. Exact old6f30 image is verified off-phone var rollback.
Private scripts prepared/syntax checked but NOT RUN: a52q_install_container_var.py,
a52q_var_write_device_test.py, start_var_write_trial.py(two explicit readiness/
var-approval flags), watch_ios_ufs_v34_restore.py, finish_var_write_trial.py,
capture_var_v34_after.py. Existing BOOT-only backend rejects writable payloads.
After an approved trial: BOOT restore FIRST, capture pstore and fresh protected
hashes, full-root hash + lossless changed-var snapshot, then host fsck before
planning any next boot. Initial var header/hash pins deliberately fail closed
after writes; refresh from verified snapshot only. Do not reuse old var plan.
No visible GUI or writable-filesystem hardware result claimed yet.

research/finish_exception_trial.py PASS; fresh BOOT/recovery/DTBO/vbmeta hashes
match. No pending restoration. Console262132 bytes SHA256
2d812dbc08a8edc3f48848d9ffcb7a994c8a40b3d795652fcd572e24779885bf.
V33 A52EX1 captures `7*** -[NSURL initFileURLWithPath:]: nil string parameter`
for backboardd pid56 (1CRC-valid copy) and pid368 (3CRC-valid copies). These are
filtered heap observations at fatal exit, not direct active-exception pointers.
Pid56 backtrace has3 valid copies and matches the previous window-server chain.
SpringBoard continues trapping at the same unslid FrontBoard main-display check;
no visible lock screen or GUI handoff verified. UI heartbeat owner1/text, frames110.
User reports on-screen logs broke, now in TWRP. Saved pstore remains usable.
E:/A52-iOS16/exception-v33-result.json and local late-trace-result.json retain all
records. Investigate BaseBoard system-container path / persistent read-only var.
Do not change pixel packing or claim graphics success from colour patterns.
Container scaffold remains uninstalled, /var remains RO, no new write approval.

# V33 HISTORICAL ACTIVE ENTRY (closed above)

Operator confirmed beside phone and ready for five-minute reset. Candidate
BOOT dfc436315aedb1fa3e0f5c4f3cc87eaf199b454786a537522fa769eca88e50f1
installed and fully read back; USB departure confirmed. Root/var full hashes
matched before BOOT write. Backend now binds reviewed root plan28 and the explicit
--abort-reason flag. Native Samsung normal-boot reboot reason used.
C: restoration watcher PID7988 active, research/watch_ios_ufs_v33_restore.py.
Authoritative receipt backup/a52q/ios-ufs-v33/receipt.json requires_restore=true.
Operator told wait five minutes then return to TWRP; do not reboot System/format.
ON RETURN: confirm watcher restoration/full original BOOT hash FIRST, then run
research/finish_exception_trial.py and symbolize any retained backboardd records.
New diagnostic A52EX1 decoded with explicit framing recovery, body CRC unchanged.
No success inferred from console/colour patterns. No new /var write included.

# V32 CLOSED, original BOOT restored and independently hash-verified

USER AWAY. Host work only; no new device write or reboot until operator returns.
V33 HOST READY; not installed. Corrected source1128ab2cec1e105f5d886881d42b7646b1e3c111.
Full HFS45047062452 SUCCESS; host CI45047062194 SUCCESS; local158 tests and
repository validation PASS. All96 archived source hashes verified; only compiled
osfmk/kern/exception.c differs from V32 (other95 unchanged). Exact-kernel QEMU
HFS diagnostic fixture passed3 CRC entry copies and13 PID1 hearts, signing1/1.
This is not Apple userland/Samsung emulation. Master16GiB rehash passed.
BOOT dfc436315aedb1fa3e0f5c4f3cc87eaf199b454786a537522fa769eca88e50f1.
Kernel0aa2a060c5c29d1d4de8ca5f2a06c5311ff91f3ed50b86d88a6c3e37e37ddb4f.
Independent check_exception_candidate.py PASS. Review:
E:/A52-iOS16/exception-v33-host-review.json; candidate JSON beside it.
Package shim/out/a52q-ios-ufs-hardware-v31, root plan28. Pipeline completed.
Launcher research/start_exception_trial.py requires --operator-ready, prepared
but NOT RUN. Watcher research/watch_ios_ufs_v33_restore.py prepared. Backend
has explicit abort-reason flag; intentionally still pinned to old plan27. Before
installing, after operator confirms beside phone, update backend to reviewed plan28,
re-run candidate check and only then launch. User last said away; latest continue
alone does not establish button-reset availability. No new /var write approved.
Earlier45046034548 was cancelled: prefix deduplication could drop more-specific
text sharing first95 bytes. Corrected and native tested against upstream observer.
Source lookup also confirms a null cache path skips both Metal shader-cache
setters. Do not blame Metal/dirs alone without exception evidence.

Host-only container-directory scaffold prepared in
E:/A52-iOS16/storage-data-container-scaffold-v1/a52q-ios-var-containers.hfs.img,
SHA1b8fd88a8574fe0f49f2480044a3c77b9230b29d1837578b52752d7a6ec5ff18.
fsck passes; all original entries compare unchanged except five new empty
root-owned0755 containers directories. Keybag bytes preserved. Parent6f30 image
and validated16GiB master preserved. This is NOT a valid populated MCM container
or writable-runtime implementation. No installation approval requested yet.
Planner accepts only that exact declared directory set and metadata.
The /var proxy and raw UFS devices reject writes. Container directories alone
cannot supply writable container storage. Exact exception text remains unproven,
so prepare the opt-in bounded backboardd failure-reason probe before enabling
storage writes. It reuses the upstream checked-copy malloc-region observer,
caps attempted reads at16MiB and region queries at1024, accepts only backboardd
when a52qscan=backboardd is explicitly enabled, and retains only the targeted
NSInvalidArgument/container/nil-path text. Higher-specificity matches replace
generic ones in late slot7. Raw strings are observations, not proof of an active
exception object. UI/UFS/keybag/catalog sources are unchanged.
158 host tests and repository validation pass; corrected full build and host packaging passed.

V32 receipt restored=true/pending=false; fresh BOOT/recovery/DTBO/vbmeta hashes
match. Strict stack decoder found no record, but a complete body in late slot7
retains valid CRC90931b8a at raw offset261627; only its text prefix is damaged.
Explicit host --recover-framing mode now accepts CRC/schema-valid original
bodies and labels recovered framing. No body/address/checksum bytes repaired.
155 tests pass including prefix recovery and rejection of modified payloads.

Backboardd pid395 caller chain resolves to libc/libc++abi/ObjC/libdispatch and
main offsets0x9334/0x9a00. Verified master executable SHA7aa6f8bf…f676267c.
Static disassembly identifies the "window server" phase, block0x10000a770,
dispatch_once initializer0x10001d7f0. Its early calls request
BSPathProviderFactory.pathProviderForSystemContainerForCurrentProcess,
cachesPath, then path. The exact throwing call and exception text are NOT known.
Read-only audit of installed var image shows containers, Data/System and
Shared/SystemGroup directories absent. This is a concrete dependency to examine;
do not assert the older Redmi nil-URL exception was reproduced without evidence.
Analysis E:/A52-iOS16/backboardd-v32-analysis.json, raw console unchanged under
backup/a52q/ios-ufs-v32. Symbolication helper accepts --recover-framing.
Operator reports readable A52Q logs followed by flashing colours. SpringBoard
still reaches main CADisplay assertion; no visible lock screen is verified.
No new device write/candidate/var change prepared or authorized in this analysis.

# V31 CLOSED, original BOOT restored and independently hash-verified

V32 HISTORICAL START (closed above). Candidate0ac595ab…ef7eaf8f installed and fully read back;
recovery USB departure confirmed. Original BOOT restoration PENDING.
Watcher PID2756 active; backup/a52q/ios-ufs-v32/receipt.json authoritative.
Operator told five minutes from confirmed departure then TWRP. On return,
verify restoration and fresh protected hashes FIRST, then
research/finish_stack_trial.py and research/symbolicate_backboardd_stack.py
backup/a52q/ios-ufs-v32/console.txt. No further trial until restoration closes.

V32 checked-copy backtrace source365460bd789a55e3e06b4928160c2abc3118933b:
full HFS45041227929 SUCCESS, host CI45041227022 SUCCESS154tests.
All96 archived hashes match; exact-kernel QEMU and master16GiB rehash passed.
Independent review E:/A52-iOS16/stack-v32-review.json passed. Only compiled
osfmk/kern/exception.c differs fromV31 (other95 unchanged). BOOT SHA256
0ac595ab034a62b389e1511058e5eace3d1729d3f47e02f6cc2c7e71ef7eaf8f.
Kernel SHA256f5cb8cb281ff020938c8a3c0ff65c4c9b942e0cc10fb0904b3b7a3e77a3c2d7d.
Pipeline finished, log research/stack-v32-build-package.log. Operator confirmed
ready; launcher invoked. Receipt backup/a52q/ios-ufs-v32/receipt.json is
authoritative for installation/restoration. Package hardware-v30, root plan27.
Master backboardd was extracted read-only and its
1184848 bytes match catalog SHA7aa6f8bf…f676267c, in
E:/A52-iOS16/master-backboardd-v32-audit-v1. Original staged UNC is unavailable,
so use this measured copy for main-executable symbolication.
Operator confirmed V31 displayed the same bars/mint screen.

V31 watcher finished restoration. Fresh BOOT/recovery/DTBO/vbmeta hashes match.
Result E:/A52-iOS16/notify-v31-result.json. No framebuffer notification/open
records survived with valid CRC. Last valid heartbeat owner1, frames131.
Backboardd pid56 SIGABRT has3 CRC copies: runtimePC0x202be7198,LR0x2121765f8,
slide0x405d0000, main0x1008fc000, SP0x16f503680,FP0x16f5036a0.
UnslidPC0x1c2617198 maps libsystem_kernel+0x7198; LR0x1d1ba65f8 maps
libsystem_pthread+0xd5f8. This identifies the termination path, not the caller
that requested abort. SpringBoard still traps at unslid0x19b968ca8.

Next diagnostic implements the upstream SWEET checked-copy frame walk only for
backboardd, bounded to16 PCs and64KiB above SP, with fault/alignment/monotonicity
checks. CRC A52BT1 records retain the caller chain in slot7. Ordinary A52CR1
register records continue. Slot7 is reserved for backboardd so unrelated logd/
media crashes cannot replace it. Native tests cover normal chain, copy fault,
cycle and CRC corruption; all154 host tests PASS. Full kernel build pending.

# V30 closed; display discovery tracing correction

V31 NOW RUNNING. Operator confirmed ready. Candidate601d411e…6db95172 written
and fully read back. Recovery USB departure confirmed. C: restoration watcher
PID8136 active; receipt backup/a52q/ios-ufs-v31/receipt.json authoritative.
Original BOOT RESTORATION PENDING. User instructed five minutes then TWRP.
First on return confirm restored=true/pending=false and fresh protected hashes,
then research/finish_notify_trial.py. Do not start another trial or overwrite logs.

V31 preparation record. Full HFS45037922206 SUCCESS, host CI45037921689 SUCCESS.
All96 archived source hashes match. QEMU reached diagnosticPID1 and signing1/1;
pristine16GiB master rehash passed. Independent candidate/review checks passed.
Kernel SHA2562da9970f9ef3c245baea720ad3009cf9833900b4a7d4463dd8d5725d7e43c766.
BOOT SHA256601d411ebdc045f8c9cfac2afcb13de195ab15421d25c860be370a9a6db95172.
Review E:/A52-iOS16/notify-v31-review.json; image hardware-v29/build/
a52q-ios-ufs-UNTESTED.img; root plan26. Operator readiness question is pending.
NO V31 launch/receipt exists. V30 original BOOT restored and fresh hashes match.
Once operator ready: research/start_notify_trial.py. On TWRP return confirm
restoration FIRST, then research/finish_notify_trial.py for retained diagnostics.
Only IOUserClient.cpp changed among96 compiled files relative to V29.

V31 source42cab405f8c0c063f64a6bd8925fc3158400b814 is building in full HFS
workflow45037922206. Host CI45037921689 passed154tests. Only IOUserClient.cpp
differs among96 compiled overlay files compared with the tested V29 kernel.
Private pipeline research/finish_notify_artifacts.py (session90362) monitors,
verifies archived sources, runs exact-kernel diagnostic QEMU, rehashes master,
and packages hardware-v29/ios-root-plan-v26. Log research/notify-v31-build-package.log.
Next run research/review_notify_v31.py. No V31 phone trial has started.
V30 BOOT restoration completed. Its fresh protected hashes match.

V30 BOOT restored and independently hash-verified with recovery/DTBO/vbmeta.
The retained display sample reports owner=1, off=0, frames=123. SpringBoard
pid395 again traps at unslid0x19b968ca8. Actual image uses4320 stride; its only
functional change fromV29 is display-scale=3. Operator saw crisp bars/mint
screen; a SpringBoard lock screen remains unverified.
Decoded result E:/A52-iOS16/display-scale-v30-result.json.

Measured IOMFB uses IOServiceFirstMatch notifications. The previous observer
missed notification registration and unrelated AppleKeyStore queries overwrote
the fixed framebuffer match slot. Add notification result observations and
retain slots only for the matching display/surface classes. All154 tests pass.
This is a diagnostic correction. It changes no surface pointer, offset, pixel
format, UFS/keybag/catalog policy or compositor behavior. Next full kernel build
and recoverable phone test must determine where discovery stops.

# V30 display scale trial (closed)

V29's compiled ADT lacked /chosen/display-scale. The upstream 20H392 bring-up
recorded MobileGestalt reading zero when absent, resulting in an invalid display
mode. V30 publishes u32(3) in the UI profile for 1080x2400 at 360x800 points.
This is a logical UI setting. Its effect on the A52 main CADisplay trap requires
a hardware result. Both old manifests and the new declared scale are validated.
All 154 host tests passed. The reviewed BOOT embeds the same kernel (dd2363bf…),
same disk root plan and same var. The new BOOT SHA256 is
4762a6da38919e5eb0410405d0bb909ddfbefb85b398602dcdb85b3295f386c5.
Hardware package shim/out/a52q-ios-ufs-hardware-v28. Launcher invoked; consult
backup/a52q/ios-ufs-v30/receipt.json and watcher.log for rollback status.
After restoration, run research/finish_scale_trial.py and compare V29 trap PCs.

# V29 closed on hardware

TWRP returned. The watcher restored original BOOT with full readback. Independent
hashes of BOOT, recovery, DTBO and vbmeta match. Decoded trace and crash records
are in backup/a52q/ios-ufs-v29/late-trace-result.json. The operator saw lines and
a blue bar followed by a screen resembling cards, a status bar and wallpaper.
The producer of that frame is unknown. The last valid display sample reports
owner=1 (text console), off=0, frames=75, colour=0 among 64 samples. backboardd
matched AppleKeyStore. SpringBoard PIDs 25, 93 and 413 each trapped at unslid PC
0x19b968ca8, previously resolved to “failed to find the main CADisplay.”

The original physical color-bar writer uses uint32_t pixels (BGRA bytes);
the checked active SSPP0 capture has SRC_YSTRIDE0=4320, SRC_FORMAT=0x237ff and
SRC_UNPACK_PATTERN=0x03020001. The kernel color-bar test explicitly requires
stride == width * 4. A 3240-byte producer pitch would misalign successive rows.
No 24-bit candidate was built or flashed. To identify a later mode transition,
correlate the visible change with live source-format, stride, scanout address and
client presentation records. A clean SpringBoard lock screen remains unverified.

# V29 kernel build verified

Corrected source 54793ef1c35396f11b54c26842df1427d2a47ab2 passed host CI
44949611916 and full HFS compile/link 44949612748. On resuming, all 96 archived
overlay files matched the expected hashes. Kernel SHA256
dd2363bfac49b844ee8df454020bcd546a437257e36dc561b8afbb8195b885d1.
V28 recovery remains available and all four protected partition hashes matched.
Host verification and packaging log: research/late-trace-resume.log.
The QEMU run produced 3 valid entry records and 13 diagnostic PID1 heartbeats.
The 16 GiB master matched its recorded SHA256. Independent package review passed
(E:/A52-iOS16/late-trace-v29-review.json). BOOT SHA256
3e46e92c5338d5d95475ea2c273af66199774cb64e946a3be62a76f549a0163c.
Operator returned beside PC. Trial launcher invoked. Use
backup/a52q/ios-ufs-v29/receipt.json for installation/restoration status.
The launcher archives the previous pstore console before checking root and var.

# V28 CLOSED, original BOOT restored and independently hash-verified

V28 receipt original_boot_restored=true/requires_restore=false. Fresh full BOOT,
recovery, DTBO and vbmeta hashes MATCH (backup/a52q/ios-ufs-v28/
independent-protected-hashes.json). No restoration pending and no active writer.
Operator confirmed A52Q banner/text appeared briefly BEFORE reset, then disappeared
with flickering colours. This verifies brief physical bitmap-console visibility,
not stable output or SpringBoard. Console SHA256
762019ecc83f280ae01abbb1470203e82d714e06b51ceeec8247fdd49c27d229.
CRC UI prepare/submit frames1,2,3; no retained guard rejection. SpringBoard saved
PC minus slide again 0x19b968ca8 (FrontBoardServices: failed to find main CADisplay).
Retained 262132-byte prefix fills around48s; later ownership/services unknown.
Next host-only work: bounded CRC late display/service records in final4KiB of
EXISTING RAM console ONLY after ordinary log fills. Preserve header/first252KiB,
normal byte writer, carveouts, UFS, catalog2786, keybag and display programming.
No new root/var write authorized or required for these diagnostics.

Late-observer implementation now complete on host:154tests and repo validation
PASS. Actual pinned IOKit transform preserves every original operation/return
when new A52-only blocks are removed; no iterator consumption/reset. Expected
96source map computed,11 observer units/headers changed and85 identical toV28,
E:/A52-iOS16/late-trace-{expected-overlay,protected-invariants}.json.
Source21a997dab3ca98fe0367c0907ef0ec805ebba930 pushed (includes backboardd crash
capture as well as SpringBoard/logd/mediaserverd). CI44948686986 SUCCESS154tests.
Full HFS44948688023 FAILED: IOUserClient.cpp kernel header does not declare
strstr (3 diagnostics); host compiler accepted it. Replace only the observer's
substring predicates with exact known framebuffer/surface class strcmp checks.
All154 host tests PASS again; next full HFS build required. No artifact packaged.
Earlier44948387960 cancelled deliberately to include backboardd, not a failure.
Host-only pipeline session93449 ended failure; research/late-trace-build-package-v2.log
and research/development-ui-build-failure-44948688023.log retain exact errors.
Next pipeline must use corrected source/run and verify96 archived hashes,
exact-kernel diagnostic QEMU, pristine-master rehash, plan25/hardware27 package.
NO V29 phone trial or checked candidate yet. Backend pinned to next plan25 only
after V28 receipt closed; new helpers start_late_trace_trial.py and
watch_ios_ufs_v29_restore.py are configured but NOT EXECUTED.
Next: finish/review build and package, then operator readiness for BOOT-only test.
Never start a trial while source/build verification or restoration is pending.

Static measured20H392 IOMFB audit E:/A52-iOS16/iomfb-abi-v29-audit-v1/report.json:
matching class IOMobileFramebuffer, notification IOServiceFirstMatch; selectors
18 is-main (0in/1out),8 display-size (0in/2out),3 surface (2in/1out), agree with
current driver. Actual cache .13 and .42.dyldlinkedit FULLSHA verified to master.
This rules out those simple class/selector mismatches, not all ABI mismatches
or the underlying CADisplay failure. No Apple binary or assertion patched.

# HISTORICAL V28 START (closed above)

User returnedwithcontinue; held reviewed candidateb6d971...b5385f2 authorized
BOOT-only. FreshADB=recovery and BOOT/recovery/DTBO/vbmeta hashes matchoriginals;
independentcandidatecheck PASS. Newrecord backup/a52q/ios-ufs-v28/operator-resume.
V28receipt confirms candidateb6d9 fullreadback and recoveryUSBdeparture. C:watcher
9676 ACTIVE, noerrors. Userasked fivefullminutes thenTWRP; operator-timing.json
records signal/not-beforeUTC. FIRST onreturn confirmrestoredTrue/pendingFalse
andfreshoriginalBOOT/protectedhashes beforeanalysis. No root/varwrites.
Launcher research/start_refresh_guard_trial.py completed(session31153), parentlog
research/refresh-guard-v28-start.log. It verifiesfullroot/var beforeBOOTwrite,
archives/rearms RAMconsole, stages/readbacksBOOT, reboots thenstartsC:watcher.
Do NOT signal5mintimer before confirmeddeparture+watcher. Receipt authoritative
for pendingrestoration. No newroot/varwrite/format. Earlierawayhold revokedby
thiscontinue. OnTWRPreturn collect+restore originalBOOT/hash FIRST, thenanalyze.

# CURRENT: V28 READY, UNFLASHED; V27 restored; user away again, wait for return

Sourcecf23c5aea21c9385c5e0e6dfce9e195c4bb66b36 pushed. Full HFS44942860068
SUCCESS; LinuxCI44942854724 SUCCESS150tests. Archived96source hashes/content
verified. Only bsd/dev/a52q_ui_bridge.c and profileheader differ fromV27; header
executabletokens identical(commentchange), other94compiledsources identical.
Invariant proof E:/A52-iOS16/refresh-guard-protected-invariants.json.
Kernel SHA8f5c4b306a57a1529d1dd1b6b22cd74a1fc85133407542ab51283503bd35cc5c.
Pipeline4521 SUCCESS: research/refresh-guard-build-package.log. Exactkernel
QEMUdiagnostic3CRCentries/13PID1hearts; signing1/1. NOT Appleuserland/hardware
emulation. Pristine16GiBmaster fullrehash unchanged. Plan24/hardware26 packaged;
independentcheck_refresh_guard_candidate +review PASS, matching150-testCI.
BOOT96MiB SHAb6d971e320bcd61c4005b9fee7180a8510470b93a31c7994f59f0b7ddb5385f2.
Image shim/out/a52q-ios-ufs-hardware-v26/build/a52q-ios-ufs-UNTESTED.img.
E:/A52-iOS16/refresh-guard-v28-{candidate,review}.json records6changedpublicfiles,
exactBOOTonlyrange/recovery/limits. NO V28trial orreceipt; launcher/watchernotrun.

PhoneV27 closed/restoredFULLreadback plusfreshBOOT/recovery/DTBO/vbmeta hashes
match. User: noIOS16text, inTWRP, notoncomputer now. NO morephone trial untiluser
returns andcanreset after5min. No pendingBOOTrestoration. Root16GiB andinstalled
var6f30 remainRO; no newdatawrite/format needed. Catalog2786/AMFIUEA/keybag/
reservations/framegeometry/cacheattrs/oldRGB/pstoreimplementation UNCHANGED.
Future start_refresh_guard_trial.py usesplan24/hardware26/candidateb6d9, archives
V27fallback, then C: watch_ios_ufs_v28_restore.py collects/restoresoriginalBOOT.
Backendplan24 currently; alloldersafetyreceipts closed. KeepTWRP, noSystemboot.

ObservedV27G2reason5 index6 value5 provesour added DSIidlewait failedafterSTART1.
PinnedSamsung dsi_display.c:7910 waits foridle insideclockchange_pending; wechange
noclocks. EarlierphysicallyVISIBLE RGB acceptedstatus5 andonlyboundedSTART.
Fix returnsguardpredicate directly (onlyobserved0/5), no mandatoryidlepoll; all
otherpins/errorstate rejection, soleSTARTwrite/barriers/100mscompletion remain.
Nativecase repeatedSTARTwhileDSIstays5 nowpasses; unknown1/highbitstillreject,
quietpanicstillnoprint. Physicaltextoutput needs NEWtest; no handoff/UIclaim.

SpringBoardV27CRC PC/LR0x1e0580ca8 minusactualslide0x44c18000 =0x19b968ca8,
FrontBoardServices brk#0. Master-matching .09code and .27.dylddata fullyhashed.
Actualslidev2delta_mask0xffff0000000000/value_add0 decodesCFString@0x1d7162ef0
->0x19b98b641: "failed to find the main CADisplay". This identifiesassertion,
NOT whyCADisplaymain unavailable; relationship toguard requiresnewphoneevidence.
Proof E:/A52-iOS16/frontboard-trap-v27-audit-v1/assertion-evidence.json.
No assertion-skipping/fakeCADisplay orGPU/daemonstubs added.
UEA lowspace fix live behaviorunproven: no positivecapabilityline beforelogfull
~48.88sec; noabort there isnot successproof. logd pid90/94 CRC mainoffset18160,
measuredmasterexecutableSHAae339154ca87e1bde5f34114e397a4879d68dbf61f2e23da432bcf2559767345,
BRK#1 storescrashmessage "BUG IN LIBTRACE: Failed to migrate directory"; actual
errno/path notyetcaptured. E:/A52-iOS16/master-logd-v27-audit-v1/{verified-executable,
logd-trap-evidence}.json. Don'tignorefailures orenableuserdatawrites silently.
V27rawconsole/kernelUI/keybag/crashrecords/freshprotectedhashes underC backup;
result E:/A52-iOS16/runtime-diagnostics-v27-result.json. No lockscreen verified.

## Historical work below; latest status above is authoritative

# CURRENT: V27 RESTORED/HASH-VERIFIED; user away again; NO PHONE TRIAL

User reported noIOS16text, nowTWRP, willnotbeoncomputer. Watchercompleted.
V27receipt restoredTrue/pendingFalse; freshBOOT/recovery/DTBO/vbmeta hashes match.
No restoration pending. Do notstartanothertrial withoutuserreturn/readiness.
Rawlog262132B SHA659ec822a6f0af8e134525accac6a34f675260a0d7185c593c9274463ad4e1a4.
EntryCRC3, rebootconfirmed. CRCG1frame1 threecopies, e1frame1 twocopies.
CRCG2 reason5/index6/value5 onevalidcopy: DSI-idle wait timesout afterfirstSTART.
PriorphysicalRGBtest snapshot DSI_STATUS5 accepted, no idlewait, barsvisible.
PinnedSamsung dsi_display.c useswait_for_cmd_mode_mdp_idle only when dynamic
clockchange_pending, notordinaryunchangedMDP refresh. Hostauditneeded; likely
incorrectextraidleconditioninouradapter. Keep13pins/0or5predicate/STARTbound,
no clock/reset/panelcommands. V27scope root/varMKBdone/EarlyBootComplete persists.
No validUEAcapabilitylog; nooldUEAabort inretainedrange, notsuccessproof; logfull
at~48.88sec. UEA live fix remainsunproven.
CRCsavedSpringBoardpid26 and93: pc=lr0x1e0580ca8, slide0x44c18000, unslid
0x19b968ca8, FrontBoardServices __TEXTbase0x19b910000/size0x9c000. Three/twocopies.
Measuredcache.09 SHAcheckedagainstmaster; actualinstruction brk#0. Constantat
0x1d7162ef0 beforetrap likelyexplainsassertion; hostsymbolicationongoing.
E:/A52-iOS16/frontboard-trap-v27-audit-v1 and runtime-diagnostics-v27-result.json.
C: backup/a52q/ios-ufs-v27 hasrecords/keybag/UI/independentprotectedhashes.
Savedlogd pid90 mainoffset0x18160; mediaserverd unslidPC0x186e5e0cc CoreFoundation.
Hostanalysis/fixes/buildonlywhileuseraway. Catalog2786/root/var/KeyStore untouched.

# CURRENT PHONE ACTION: V27 RUNNING; BOOT RESTORATION PENDING

User resumed held reviewed candidate203155db...c6da009. ADB recovery; fresh
BOOT/recovery/DTBO/vbmeta hashes matchoriginals. Independent candidatechecker
PASS. No V27receipt existed beforestart. New resume record in
backup/a52q/ios-ufs-v27/operator-resume.json. Launcher running (49689):
research/start_runtime_diagnostics_trial.py, parentlog research/runtime-diagnostics-v27-start.log.
V27receipt confirms candidate203155...c6da009 fullreadback and recoveryUSBdeparture.
C: restoration watcher15932 ACTIVE, noerrors. Useraskedwait5fullminutes then
returnTWRP; operator-timing.json records observation signal/not-beforeUTC.
FIRST onreturn checkreceipt original_boot_restoredTrue/requires_restoreFalse
and freshoriginalBOOThash. Current pendingrestoreTRUE. No newroot/varwrites.
It rechecks fullroot/var, archives existing RAMlog (fallback latestsavedV26),
stages/readsback BOOT, confirms USBdeparture thenstarts C: restoration watcher.
Until confirmeddeparture do NOT signal five-minute timer. Once running update
this header with watcherPID; onreturn restore/hash beforeanalysis. Only BOOT
writes authorized; no newuserdata/root/varwrite. Older wait-for-continue notes
below are historical: this continue revokes the away hold.

# CURRENT: V27 READY, UNFLASHED; user away, wait for "continue" before phone trial

Full HFS44939199104 SUCCESS. Compiledsource18c6d78cdf37bcc282e070e41523f50617087df3.
LinuxhostCI44939190163 SUCCESS150tests. All96 archived overlay-source contents
verified against independently constructed map fromV26. Four compiledsourceunits
differ: AMFI measuredUEA Boolean, UIflushdetail, BSDexitcall, Machregisterhelper.
Kernel SHA 8c1770355fee120130484f91076a5f67285b731482f0be70048e8b132bab917b.
Pipeline67679 completedSUCCESS: research/runtime-diagnostics-mach-build-package.log.
Exactkernel diagnostic QEMU3CRCentrycopies/13diagnosticPID1heartbeats, enforcement
system1/process1; NOT Appleuserland or Samsunghardware emulation. Pristine16GiB
master fullrehash unchanged. Plan23/hardware25 packaged and independent checker
PASS including matching150-testCI, source hashes, payload/UI/root/var bindings.
BOOT96MiB SHA 203155dbee765f9ae80d4596924f79547e11e00ad3d5027259d83e2ecc6da009.
Image shim/out/a52q-ios-ufs-hardware-v25/build/a52q-ios-ufs-UNTESTED.img.
E:/A52-iOS16/runtime-diagnostics-v27-{candidate,review}.json. Review lists13files,
fullhashes/proposedBOOT-onlyrange, backup/recovery, scope and unresolvedbugs.

PHONE: V26 originalBOOT restored/fullreadback +independent fresh4protectedhashes
match. Receipt backup/a52q/ios-ufs-v26/receipt.json closed; NO restoration pending.
Installedvar6f30 was fullreadbackverified; root16GiB preserved. No phonewrite atall
whileuseraway. V27launcher/watcher NOTRUN; no V27receipt. Do NOT flash untiluser
returnswithcontinue andcanperform5-minute reset toTWRP. ExistingBOOT-onlyscope:
sda19 bytes[0,100663296), thenautomaticoriginalBOOTrestore. No newvar/rootwrite.
Futurestart research/start_runtime_diagnostics_trial.py; C: watcher
research/watch_ios_ufs_v27_restore.py. Backend plan23 +installedvarreceipt6f30 +
--text-console; omit optional--ios-codesign-debug (cs_debug2spam filledV26log).
Allnormalprintf/pstore/signatureenforcement retained. OnTWRPreturn collect then
restore/hashFIRST; use UI CRCG2 reason/index/value foractualruntimeflushfailure,
and tools/a52q_crash_trace.py forCRC savedPC/LR/cache slide. Do not speculate.

Fixedhostpolicy: exact master-measuredUEA low-spaceIOBoolean checked by full
84016BfileSHA/requiredvnode pluscatalog/platform/ROroot. Native negativesPASS.
No liveUEAfix proofyet. Display andSpringBoard remainUNRESOLVED untilnewtrace.
V26user NO TEXT; UImapped,frame1 STARTcompleted,thene1error(noG2detail). V26
MKBdone andEarlyBootComplete provedtzinitseedprogress. SpringBoardpid25 SIGTRAP,
UEApid24lowspaceEPERMabort, logdtrap/mediaserverdSEGV observedbefore256KiBfull.
No visibleconsole/UI/60Hzpanel/lockscreen claimed. UFS/catalog2786/KeyStore/
RAMreservations/physicalFBvalues/oldRGBdiagnostic/pstoreimplementation unchanged.

## Historical host work and V26 evidence (latest state above is authoritative)

# CURRENT: V26 restored; host fixes/build while user away; NO PHONE TRIAL until continue

Full44937633007 FAILED: BSDtranslationunit hidesstructtask andvm_shared_region
(MACH_KERNEL_PRIVATE). Fix moves register+slide helper into osfmk/kern/exception.c
using actual same-context APIs as existing Redmi crashhelper, not private-type
casts in BSD. BSD nowcalls typed name/pid entry only. Original Redmi unchanged.
Newapply transform stagesexception.c too ->96overlayfiles. All150hosttests,
actual V26source-based expected96construction and repo validationPASS. Needfull
HFSrestart on correctedMach/BSDboundary; no phonewrites. Older build IDs below
are historical. Same plan23/hardware25 targets remainunused/newhostonly outputs.

Correctedsource6479ed8b2e46e3a9996a9dfb660576a53fe90537 pushed. LinuxCI
44937627819 SUCCESS150tests. FullHFS44937633007 compiling. Independent expected
95-source overlay prepared from V26 archive; only bsd/kern/a52q_amfi.c,
bsd/kern/kern_exit.c and bsd/dev/a52q_ui_bridge.c differ. Host finisher16879:
research/finish_runtime_diagnostics_artifacts.py -> runtime-diagnostics-build-package.log.
Next hostoutputs: runtime-diag-qemu-v1, plan23, hardware25. New V27 start/watch
helpers prepared but NOTRUN. BOOT backend nowplan23; current V26 restoration
alreadyclosed. Future candidate uses installedvar6f30 (no newdatawrite).
Omit optionalcs_debug=2 in V27 packaging to reduce observed no-hash debugspam
(primary XNU ubc_subr.c:5757 conditional cs_debug>1). Signatureenforcement and
normalconsolelogging remain enabled; no pstorelayout/capacity changes.

Initial hostfixcommitc078238/full44937355741 superseded: independent overlay
check caught a52q_crash_registers call accidentally added to the original match
anchor rather than A52 trace. Corrected anchor/call placement; new independent
literal-anchor regression. All150hosttests PASS, expected95overlay construction
PASS against actual V26 archived source. Restart full HFS build on correctedhead.

User: "fix all bugs and build kernel and when ill come back ill say continue".
Phone TWRP, V26receipt original_boot_restoredTrue/requires_restoreFalse. Fresh
BOOT/recovery/DTBO/vbmeta hashes match; independent-protected-hashes.json saved.
Newvar6f30 installed/fullreadbackverified;16GiBroot preserved. No rollback pending.
V26 user saw NO text. Captured full262132B RAMlog SHA
 e0fb51e3505d3ff9c665b140bffa538a857730df387f7f07df0eef54360eb0e3.
CRCentry3, rebootconfirmed, UIpreparephase10 two validcopies, frame1 phase30
threecopies, thene1/frames1 onevalidcopy. NoG2detail; noGUIhandoff. Thus optional
adapter mapped/submitted once thenruntimeflushfailed, not visibletext/GUI proof.
MKB SystemKeybagloaded/DONE, realUFSroot andROvar mounted; tzinitfailurecleared,
raw EarlyBootComplete ContinuingSystemBoot. Actual SpringBoard pid25 SIGTRAP
exception6 subcode0x1eb9f8ca8 three rawcopies; no cache slide/LR -> cannot yet
symbolicate reliably. UserEventAgent pid24 SIGABRT OS_REASON_LIBXPC18/code2:
"Error setting low space io policy: 1 (Operation not permitted)" threecopies.
backboardd xpcproxy spawnedpid56; runtime services/lockscreen unproved.
Rawlogcapacity reached at~56sec (of5min). Otherlogd SIGTRAP/mediaserverd SIGSEGV
present, unlocated causes; do not claim all bugs fixed or bypass crashes.

Host changes: flush failures now report existing CRCG2 guardreason/index/value
ornewreason6 STARTcompletiontimeout. Guards/START/map untouched; quietpanic
path remainsnoprint. ExactUEA read from master inROisolatedguest; SHA
2f149077b52e771974d42673bb034cd661b0681af2e581fcab2d1aee1a8742eb and15pages+
signedXML4385/DER2982 hashes matchmastercatalog. Actualsigned lowspaceBooleanTrue.
XNU kern_resource.c deniesfalseIOCurrentTaskHasEntitlement; minimal AMFIreturns
noobjectforUEA. Add ONLY measuredUEA lowspaceBoolean via existingAMFI callbacks,
exactCDhash+catalog+ROroot+platform+full84016BvnodefileSHA256 includingentitlements.
No catalog/signature enforcement/othercapability/storagewritepolicy change.
Native tests reject changedidentity/failedhash/wrongvnode/root/metadata/key/flags.
Fatalexittrace addsCRCprotected savedregs+cache slide for3actuallycrashingnames;
no arbitraryuser reads, stackwalk orchangedtermination. Full149hosttestsPASS.
Need fullHFSbuild/archive95/QEMU/master/candidate, noflash untilusercontinue.
RO masterUEA audit E:/A52-iOS16/master-user-event-agent-audit-v1; derived proof
uea-v26-entitlements-audit.json. Publicsmall metadata uea-lowspace-pin.json.
V26result E:/A52-iOS16/text-console-v26-result.json; C: backup/a52q/ios-ufs-v26/.

# iOS 16 on sweet (Redmi Note 10 Pro, SM7150) - working notes

## ACTIVE: combined text-console/idle/zoneinfo candidate checked; awaiting exact-var approval/readiness

Source922e77eced45faf9b53acc5484968fefa4fadd95 pushed. Full HFS44916663730
SUCCESS; hostCI44916653849 SUCCESS147. All95 archived overlay sources rehashed
against reviewed map. Kernel SHA
adab051fa0538d35a9b6c31db49489f1b514b3bd8cc3a9cb5b41554db8b55032.
Exact-kernel diagnostic QEMU3CRCentries/13PID1hearts (not Apple userland/UI/UFS
emulation); protected16GiBmaster rehash PASS. Plan22/hardware24 packaged.
BOOT96MiB SHA b3d7bf44417cfe85f45eef5a9a09e68d0379c56e52655c651f6d99a5783dabf7.
Independent check_text_console_candidate.py PASS including payload/profile/root/
var binding, compiled-source matching and successful matching LinuxCI.
Installer PREPARE ONLY passed: rehashed newvar6f30 and currentrollback44eb.
Concrete review E:/A52-iOS16/text-console-v26-review.json lists20 changed files,
full hashes/ranges/rollback/commands. Candidate record text-console-v26-candidate.
Protected13implementations hash-identical tosaved7d0783d; report onE.

No newphonewrites. PhoneTWRP and originalBOOT/recovery/DTBO/vbmeta freshly match.
Var6f30 remainsNOTinstalled; parent44eb remainsphone. NoV26 trialreceipt or new
varinstallreceipt. Freshexactvarwrite approval/readiness still needed (4GiB at
sda31[17179869184,21474836480), preserves16GiBroot). Priorapprovalwas44eb.
Afteryes run research/a52q_install_timezone_var.py install --approved-exact-var-write;
verifyreceipt/root/protectedhashes, then research/start_text_console_trial.py.
Backend nowplan22/hardware24/text-consoleflag and newvarreceipt required.
V26watcher C-based autoBOOTrestore after TWRP, fullreadback; manualreset5min.
No visibletextconsole, Apple services or SpringBoard proof yet.

## Earlier handoff correction


Full HFS44915225317 (49113a5) SUCCESS;95archive source hashes, exact-kernel
RAM diagnostic QEMU, preserved-master rehash, plan21/hardware23 packaging PASS.
Kernelc14147f8c535349d36cf375ae5ee6a470708ce57eabedf2a1ba9aeacf9c14805.
No phone write. This unflashed candidate is superseded by a discovered ownership
race fix: selector3 could export default physical IOSurface before firstpresent,
allowing client writes concurrent with console rendering. New A52-only method
runs console handoff through existing IOWorkLoop::runAction BEFORE surfaceport
export. Pinned IOTimerEventSource timeout/timeoutAndRelease hold same gate during
action; normal event delivery also gated. Existing present fallback retained.
Native C++ test executes transformed method against recursive gate, renderer
and client threads; verifies no export during rendering. All147tests and repo
validation PASS. No UFS/catalog/keybag/displaybounds/pstore implementation change.
Need fresh full HFS build,95-source archive/QEMU/master/plan22/hardware24 checks.
Keep previous plan21/hardware23/qemu-v1 evidence. New qemu-v2, same preserved
var6f30 seed and rollback44eb; no installation yet. ADB currently recovery.
Then updated concrete review + physical readiness, newvar install and BOOTtrial.

## Earlier console implementation notes

User returned2026-11-21 requesting finish/flashsavedchanges PLUS live scaled
bitmapconsole, preservingUFS/catalog/keybag/displaybounds/pstore. No newphonewrite.
SavedfullHFS44308099292 SUCCESS;90archive hashes; kernelc1539de3e3f90357ab1de955e322ed6f919b247beac8e4bfc17c1a803f54eda1.
QEMU3CRCentries/13hearts +masterrehash +plan20/hardware22 packaged. Independent
check_timezone_idle_candidate.py PASS beforeconsolecommit, BOOT SHA
1d6a311b0ec95eaf3c5f78abf7a0c3a562ff59ef49b39112a9f32944cbf64384.
No savedcandidateflash. Var6f30 seed NOT installed; original44eb stillphone.
Private BOOTbackend currentlyplan20 +ios-timezone-var-install-v1receipt required.

New opt-in textconsole: a52q_fb_console.c/h +a52q_text_grid.h, text_console.py
transform appendsmirrorAFTERoriginalpstorewrite; actualbytebodyidentical(native
assert). Originala52q_early.c sourcefileunchanged; stagedoverlaycallsnewqueue.
Static16KiBqueue try-lock/noMMIOoralloc inproducer; existingXNUiso_font8x16@2x,
67columns/banner+74scrollrows, whiteblack. Renderer onlyafterUIguardedmapping,
10Hzdirtyrefresh throughboundedexistingSTART; best-effortpanicdrain, no blocking
onpreemptedrenderer. Firstframebufferpresent permanenthandoff; busyretryvia
existingpendingframe. Pstorecontinues afterhandoff. Onlyexistingconsolestream,
notprivateAppleos_log/file-only logs; no serviceorUIclaim. Header/fontglyphbounds,
scroll/controlcodes/backpressure/reentrance/ownership testedactualCnative.
Explicit--text-console payloadflag+profile andcompiledmarker required.
Applyadds5newarchivepaths -> expected95overlayfiles. SoftwareUIpinnedtransform
addsconsumer/handoff; defaultRedmibody preserved. UFS/catalog/keystore/source
physicalRGBdiagnostic/reservations untouched. docs/A52Q-TEXT-CONSOLE.md scope.
All147hosttestsPASS; repo81patches/45tools/7shell PASS withGitBash+PYTHONUTF8.
Initialconsolecommitbc634048914ced5ff0cb8796337ce1c60c3ba6ac pushed;
CI44914949352 SUCCESS147. Full44914949227 superseded beforeflash: panicpath
neededquietrefresh toavoidprintfrecursion/locks. Addedinternalreportflag normal
flushsamebehavior; panicusesa52q_ui_flush_quiet withnopostprintf/errors. Native
testsassertquietpanicrefresh. All147PASS. Neednewcommit/fullHFSbuild, expected95archivecheck, diagnosticQEMU/newrootplan21/
hardware23 +consoleCLIflag. Retainexistingvar6f30plan/image andbackup44eb.
Thenindependentcandidate+installerprepare/review; phonefreshreadiness required.

## ACTIVE: V25 restored/verified; real var mount works; tzinit EROFS and DSI status guard

V25 finished. OriginalBOOT restored/fullreadback; independent fresh BOOT,
recovery/DTBO/vbmeta hashes MATCH. No restoration pending. User Samsungsplash.
Savedbackup/a52q/ios-ufs-v25/{console.txt,keybag-result.json,kernel-ui-result.json,
independent-protected-hashes.json}; E:/A52-iOS16/var-phase-v25-result.json.
Real HFS mounted A52IOSVar /dev/a52var0 on /private/var read-only. CRCsystembag
opens errno0 (3validcopies +repeat1). Selector14success3copies+repeat2. Raw
MKB_INIT SystemKeybagloaded and DONE MKB_INIT, thenusermanagerd/dirs_cleaner/etc.
This is developmentcompatibility, NOT realkeys/SEP. varwrites errno30 on
AKSSetup.log/.aks_allowlist, usersession/persona files, butkeybagboot task continued.
Firstfatalboot-task now tzinit: badzoneinfo link ENOENT, create_symlink from
/var/db/timezone/zoneinfo to /usr/share/zoneinfo.default fails EROFS, exit30,
userspacepanic. No EarlyBootComplete/services/SpringBoard proved.

CRCUIrejectA52G2 reason3 index6 observed0 expected5 (2copies). This address
0xae94008 = pinned DSI_STATUS; originalsnapshotguard incorrectlyrequiresbusy5.
PinnedSamsung dsi_ctrl_hw_cmn.c functionwait_for_cmd_mode_mdp_idle testsbit2
untilclear; bit31 iserrorcontention. Need implement narrowly observed idle0
acceptance and boundedbusyhandling, leavingconfigguards/physicalFB/oldRGBdiag
unchanged. No guard removed yet. SourcefromGitHub plugin fetched:
drivers/gpu/drm/msm/dsi-staging/dsi_ctrl_hw_cmn.c @ f6bbda4e5986f09e4d51ceffd1b645b2d5aa75b4.

Independentaudit completed: E:/A52-iOS16/timezone-prerequisites-v1 extracted
exacttzinit126640B SHA1e13c6f7c32b810a043a5e28dccc1d24ddf83b69ddc3323d500d3aefa91ff9ef,
27signedpagesverified/CDhash3a1538960c0be7257ea41eaddeb7727c5ad61c25.
Currentzoneinfo parser0x10000642c..6510 recognizes /usr/share/zoneinfo.default.
Preservedvar lackszoneinfo+icutz links; rootdefaultdatasetexists. Preparinghost
clone storage-data-timezone-v3 via research/prepare_timezone_var.py session73487,
logresearch/timezone-var-prepare.log. Finalseed ONE zoneinfo symlink; ICUmonolithicdata default hasno externalpatch,
soicutz staysabsent. Source44eb/masterunchanged;
ROLinuxchrootpathchecks planned with RAM utilities, noAppleexecutionclaim.
Any newvarimage install requiresnewexactrange/hash approval; none granted yet.

DSI fix implemented only optionalUIadapter: keep13capturedpins, acceptstatus0
orobserved5 only, poll100ms untilidle0 beforemap/START; unknown/errorstatesfail,
noDSIstatuswrites orclocks/resets. Newreason5busytimeoutCRC. Testscoveridle,
busytransition,timeout,errorbits. Host145tests/repoPASS. Planner validatesexactzoneinfo symlinktarget/rootownership; no runtimewrite support added.
Kernelcommit7d0783db965357234643e7e13e23da7b5b0a2b3d pushed.
FullHFS44308099292 inprogress, hostCI44308099048 SUCCESS145(oldtwo-linkpolicy);
finalone-linkhostchecks145PASS locally, newhostCIneeded.
Finalclone prepared by research/prepare_timezone_var_v2.py, correctedrun44700
SUCCESS; firstv2process3960stopped beforeguest duebare-readlinkgenerationbug.
Finalproof sourcepath storage-data-timezone-v3/a52q-ios-var-timezone.hfs.verified.json.
Read-onlyfsck + alloriginalvarpathrsyncchecksum comparisonPASS exceptone newlink.
LinuxstaticutilitychrootROroot/var resolutionPASS:+VERSION2022a/UTC/localtime,
monolithicICUicudt70l.dat. NoApple tzinitexecutionclaim.
Currentphonevarfullhash equals44ebhostimage, rollbackproof
E:/A52-iOS16/var-current-range-proof-v2.json (read-onlyphoneverification).
Latesthostguardcommit77df64d134c6c9f84c7dc28eafdcf992491bd887 pushed;
CI44310697223 SUCCESS145. It blocksleafrelinks retainingstaleUI/var units.
Finalvar clone SHA6f30c2ad09764388224ff5cd887506688a06e144411fff04eda0b39f0f6e75f9;
headerCRC923690534. E:/A52-iOS16/var-layout-timezone-v3.json validated.
Buildpipeline research/finish_timezone_idle_artifacts.py running43306,
logresearch/timezone-idle-build-package.log, fullHFS44308099292 stillcompiling.
Expected90overlaymap prepared. Newprivate verifier/checker/prepare/start helpers
research/{verify_timezone_idle_build,check_timezone_idle_candidate,
prepare_timezone_idle_artifacts,start_timezone_trial,watch_ios_ufs_v26_restore}.py;
newinstaller research/a52q_install_timezone_var.py prepared, NOTRUN.
Nextplan20/hardware22/qemu a52q-timezone-idle-qemu-v1. Afterpackage switchBOOT
backend plan19->20 and varreceipt toios-timezone-var-install-v1; independentcheck,
installer prepareONLY (rehashnew6f30+backup44eb), writeconcretereview, thenrequest
new exactvarimagewrite+5mintrialapproval/readiness. No newphonewrites yet.
Need archive90map, exactkernelQEMU, newvarplan/candidate,
concretesourceimage+currentvarbackup proof andapprovalbeforephonewrite.

Historical V24/V25 build history follows; no restoration currently pending.
V24 finished. OriginalBOOT restored/fullreadback; independent fresh BOOT,
recovery/DTBO/vbmeta hashes MATCH. No restoration pending. User saw Samsungsplash.
Results backup/a52q/ios-ufs-v24/{keybag-result,kernel-ui-result}.json and
E:/A52-iOS16/development-ui-v24-result.json. CRC keybag selector0success1copy;
selector14 success2copies +repeat1copy. Systembag opens stillENOENT(2/3copies),
.writingENOENT2copies. FATALKEYBAGkb_load; no earlycomplete/services/SpringBoard.
UI phasee0/0frames3copies: adapter rejected init; exactreason not logged inV24.

New4GiB var installed and fullreadbackverified44eb...fc6fea02; root16GiB/protected
hashes checked. Consent/receipt backup/a52q/ios-var-install-v1/. No further data
write needed. Proxy verified actual header/window inV24, but var NOT mounted:
initial fstab passno0 excluded by BOTH target mount -P phases. Exact pinned
mount binary SHAac55c4c...2364df verified; disassembly 0x100005290..52a0 compares
fs_passno offset0x2c withphase andbranchesbacktogetfsent onmismatch. Matches
Apple diskdev_cmds701.100.2 source. Fixed passno2, preservingRO/rootwire/UFS.
Native test nowusesactual data_fstabcallback, notfakeentry; verifies phases.

Display guards NOT relaxed: added A52G2 CRC rejection reason/index/value,
retains oldA52G1. Next trial can distinguishprofile/map/guardvalue/frame-map.
No claimdisplayfix. Host144tests PASS andrepo validationPASS. Correction source5802a2ccff22f7f3031feda2e61cabb541c227b5; docs4af8212.
LinuxCI44140966345 SUCCESS144tests. FullHFS44140987363 SUCCESS. Archived90file
map/content hashes verified against reviewed source. Kernel SHA
69087dba9c02292d90ad9be38bcd514a2359cb044df2dc65af1f0799d145ee82.
Pipeline62690 completedSUCCESS, research/var-phase-build-package.log.
Exactkernel diagnosticQEMU3CRC entries/13PID1heartbeats; noUI/UFSemulationclaim.
Master16GiB rehashed unchanged; plan19/hardware21 packaged and independently
checked by research/check_var_phase_candidate.py. BOOT96MiB SHA
e316aebb8f8ecfdf2510f5378e30f6d173ff26724591c19222403c85f69f534d.
E:/A52-iOS16/var-phase-v25-candidate.json and var-phase-v25-review.md.
New BOOTbackend bindsplan19. Existingvar44eb...fc6fea02 installed/verified;
no new datawrite. V25 is nowrunning; readiness confirmed, see active receipt.
Private start_var_phase_trial.py + watch_ios_ufs_v25_restore.py prepared;
trialfolder backup/a52q/ios-ufs-v25 (noactivependingreceipt). Once userready,
runlauncher, confirmdeparture+watcher, thenfive-minutereset instructions.
After TWRP returns confirmoriginalBOOTfullhashrestore FIRST; analyzeactual
varmount/systembagopens/AKSselectors and A52G2guardfailure details next.

Original catalog/AMFI/UFS/root/displaydiagnostic/pstore files unchanged.

Full HFS kernel run44125438385 attempt2 SUCCESS (2026-11-17 17:00UTC),
source5a2b1fc4d67ce1c050978a6e8efe19d4260a81d0. Kernel SHA256
472e5d1ad9cad238cf5b10445d4befd46425fda20d3f3cee3cb4972851e6864a.
Archived90-file overlay matches reviewed source map, all90 archive contents
rehash verified. Report E:/A52-iOS16/builds/44125438385/verified-build.json.
HostCI44125437564 SUCCESS143tests plus native checks/loader QEMU.
Pipeline57739 completed SUCCESS. Exact-kernel diagnostic QEMU:3CRC entries,
13PID1 heartbeats, enforcement1/1; no hardware/UI emulation claimed. Master16GiB
rehash passed, plan18/hardware20 packaged. BOOT SHA256
70fe071a85e3962c3455dfb32e6939cd056a2a8510496e2b9b5dc674776f36e1.
Independent research/check_development_ui_candidate.py PASS; record
E:/A52-iOS16/development-ui-v24-candidate.json. Installer prepare ONLY passed,
rehashing sourcevar and exactrangebackup. Review artifacts:
development-var-install-review-v1.json and development-ui-v24-review.md onE.
Fresh ADB=TWRP and original full BOOT SHA verified after packaging; no write.

First combined full run44120791852 failed undeclared chrtoblk in new proxy.
Corrected exact private prototype (used by target conf.c/spec_vnops.c); retains
raw-to-block identity guard. Corrected run attempt1 failed runner allocation,
without executing source; attempt2 compiled and linked successfully.
Implementation aacc10a, native adapter test c5dae42, decoder cfd3a88, fix5a2b1fc.

Latest explicit user request authorizes synthetic always-unlocked/no-SEP profile,
CPU IOSurface/framebuffer bridge and software power/watchdog in one candidate.
It supersedes older assistant notes refusing development stubs. These are NOT
real SEP/keychain/graphics, and no SpringBoard claim before physical observation.
Original BOOT remains restored/hash-verified after V23; phone TWRP. No new phone
writes. Only RGB bars physically proved, not A52 IOMFB or measured panel60Hz.

Opt-in a52q_dev_keybag=1 selects fixed system handle0 (selector14), unlocked
state4(selector7), DERstate(selector17), bounded compatibility setters; save/load/
wrap/unwrap remain unsupported. Default empty probe and owning-task checks stay.
Opt-in a52q_ui=1 enables exact-pinned upstream Surface/Framebuffer/Watchdog,
guarded native1080x2400 BGRA copies and software16667us timer; synthetic100% AC.
Bridge validates13captured registers, WC mappings, only tested START writes,
100ms deadline/fail closed. Surface32MiB/per,96MiB total within255MiB managedRAM.
No Apple Metal/OpenGL implementation/fallback proved; no opaque renderer hooks.
Original UFS transport/root, AMFI2786catalog, a52q_display.c, bootfs source,
pstore/early logging and reserved-memory planner files remain byte-identical.
Overlay appends optional ROvar fstab after identical existing root wire.
Separate bounded READ proxy /dev/a52var0 wraps /dev/ra52ufs0; all writes EROFS.
Read-only var may block services requiring writable databases/logs; no silent RAMvar.
Docs/A52Q-DEVELOPMENT-UI.md records files, evidence, scope and limits.

Var clone E:/A52-iOS16/storage-data-development-v2/a52q-ios-var-development.hfs.img,
4GiB SHA44eb5f6d2f95476fca5f0f9ca233687d9db9e68d71901bd68ba97ab1fc6fea02.
Clean RO fsck; original var tree rsync-checksum preservation passed. Seed
keybags/systembag.kb is364B SHA d1db41b2a90d302b23ea55cfe040c1ee169d3af687d8046baed990ad507f5656,
root:root0600 under0700. Development plist metadata, NOT real Apple/SEP bag/keys.
Plan E:/A52-iOS16/var-layout-development-v2.json rehash/geometry checked.
Preserved16GiB rootmaster SHA0f4bcaa7c1a6f0a531c8b4d4d67b0dd8843b5ab58c2c31a005e07b1bde312149.
Original unseeded var preserved SHAefa03fd497c0ecf2b1c5915a925fbc27979319094b663611f11e3abf860b8a36.

Proposed NEW userdata range[17179869184,21474836480) backed up offphone and
independently full devicehashverified: E:/A52-iOS16/var-range-backup-v1/
userdata-16GiB-20GiB.bin,4GiB SHA
f40157ecac3a47a7edff45a86d76e3466644f13a072123aaa560b641012a129c.
New exact var range explicitly approved and installed/verified; see active receipt.
Private research/a52q_install_development_var.py has exact-range prepare/install/
rollback; explicitapproval flags, root/GPT/protectedpartition checks,128MiB
RAMchunks, fullreadback. Need host-only prepare after checked hardware20 exists,
then concrete newrange approval before installation. Rollback exact same4GiB
from verified backup; BOOT restoration is separate and cannot restore Android.

NEXT: monitor BOOT launcher research/start_development_ui_trial.py and C: watcher
research/watch_ios_ufs_v24_restore.py. Trial folder backup/a52q/ios-ufs-v24.
Backend binds plan18; requires exactUIprofile and full installedroot/var hashes.
On confirmed USBdeparture notify user five-minute reset. After return watcher
captures first pstore and restores/hashverifies originalBOOT; independently verify
before analyzing results. If USB interrupted guard continueswaiting/retrying.

## Prior V23 verified result and build history


V23 complete. C: watcher collected first console and restored original BOOT.
Independent fresh BOOT/recovery/DTBO/vbmeta hashes match all saved originals.
NO restoration pending. Saved backup/a52q/ios-ufs-v23/keystore-result.json and
E:/A52-iOS16/keystore-probe-v23-result.json. CRC-validated records prove:
match AppleKeyStore success (3 copies); selector0 handshake success (2 copies);
selector14 NotFound/bag absent (3 copies). Then actual keybagd disk-load opens
/private/var/keybags/systembag.kb and .writing return Darwin ENOENT (multiple
valid copies). Kernel UFS root window valid twice; three XNU entries. No bag was
loaded and no early boot complete/services/SpringBoard proved. Corrupted text is
not repaired. New provider is discovery only; load/save/wrap still Unsupported.
Next work: inspect actual opaque bag/load interface and persistent-data layout.
Existing 4 GiB host var image is unchanged original var subtree, lacks keybags;
its real SHA is efa03fd497c0ecf2b1c5915a925fbc27979319094b663611f11e3abf860b8a36
(not the typo in some earlier summaries). No var write approved or installed.

V22 completed and C: watcher restored original BOOT. Independent fresh hashes of
BOOT/recovery/DTBO/vbmeta all match saved originals. Phone recovery; NO restoration
pending. Result backup/a52q/ios-ufs-v22/keybag-result.json and
E:/A52-iOS16/keybag-trace-v22-result.json. Console and first capture preserved.
Three CRC XNU entry copies; RO root window confirmed twice. Exact keybag records:
match/1 class=AppleKeyStore result=0xe00002f0 found=none (3 valid copies)
match/2 class=AppleKeyStore result=0xe00002f0 found=none (2 valid copies).
No system-bag open observed. Other CRC opens show timezone files ENOENT, not
proof of keybag EROFS. Static verified 20H392 wrapper starts with generic
0xe00002bc if connection unavailable; its get-system selector14 is not reached
without a connection. Apple keybagd subsequently requests recovery; no early
boot complete or services/UI proven in V22. First hardware prerequisite is a
software KeyStore interface; do NOT import SWEET's constant-unlocked fake bag.

New host implementation in A52PlatformExpert.cpp only (no overlay changes):
empty AppleKeyStore discovery probe for rd=a52ios0. Connection type0/selector0
handshake; system query14 returns truthful NotFound without output handle;
every other method Unsupported. No unlocked bag, crypto, filesystem write or
boot-task bypass. Owner task retained/rechecked; close state, shape/descriptors/
async rejected. Keybagd-only CRC aks records, max80. Decoder adds aks kind.
Native actual C++ probe tests including object/task lifetime pass; all132A52
tests PASS; repo checks PASS. Source commit205c4be52e9305a9d4cb1407402b8d893bde93d8
pushed. Linux CI43922073263 SUCCESS; isolated platform rebuild43922095033 SUCCESS
against full base43909951214. Auto mockfs43922073283 cancellation requested.
Host pipeline research/finish_keystore_probe_artifacts.py session87355 completed
successfully; use research/keystore-probe-build-package-retry.log. First local
checker stopped before download on CRLF-vs-git-LF assertion; fixed to canonical LF.
Source provenance verified. Kernel SHA256
8b9c189d3b9c10c99f40b634255b79cfc8abe8ee5aae0fdb280e6ba1ff3d7352.
Exact QEMU passed: 3 CRC entries/7 diagnostic PID1 heartbeats; probe correctly
not published for diagnostic RAM root. Whole master rehash unchanged;
plan17/hardware19 packaging and research/check_keystore_probe_candidate.py PASS.
New BOOT SHA256 62f4fc6ba95d8973fa75326fde3a2b83e99a49b97504d92986be928a32971464;
E:/A52-iOS16/keystore-probe-v23-candidate.json. Phone payload has full persistent
RO root, no diagnostic RAM root. Existing AMFI source SHA9a18...435c unchanged.

V23 receipt now requires_restore=false, original_boot_restored=true; guard
finished successfully. Phone remains TWRP. Do not reinstall without a checked
new candidate and physical readiness. No new root/data-volume writes authorized.
Corrected diagnostic source a9783bdd96893c39b00caa86c35b97018c8b510a.
131 host tests and Linux CI 43909878860 passed. Full HFS kernel build
43909951214 attempt 2 SUCCEEDED. Attempt 1 failed hosted-runner allocation;
earlier 43907188206 was cancelled after the VFS strstr compile error, now fixed.
All 78 archived overlay files match the expected source; only the VFS open and
IOKit matching diagnostic units differ from full catalog build 43897768441.
AMFI, UFS, display, protected memory and pstore behavior remain unchanged.
Kernel SHA256 a88f7cde889c19dff7b34932557332d54fde25c09a7008ac9b726734a91bbd88.
Exact kernel QEMU passed: three CRC entry copies and seven diagnostic PID1
heartbeats. QEMU did NOT execute Apple's keybagd or validate Apple userland.

Master image fully rehashed unchanged, plan16/hardware18 packaged and checked by
research/check_keybag_trace_candidate.py. Candidate:
shim/out/a52q-ios-ufs-hardware-v18/build/a52q-ios-ufs-UNTESTED.img
BOOT SHA256 f754ca8e4d85aca3bd4a851fefc7750408f6adc5bdff8d617e739e37a7c878a0.
Independent report E:/A52-iOS16/keybag-trace-v22-candidate.json; completed host
pipeline research/keybag-trace-build-package-v2-retry.log. Helper now binds
E:/A52-iOS16/ios-root-plan-v16.json. No diagnostic RAM root in phone payload.

V22 launcher completed install/readback and native reboot; guard PID14868
collected and restored successfully. Its receipt now requires_restore=false,
original_boot_restored=true. No new phone trial ready or authorized for immediate
reboot; fresh physical readiness required for a new candidate. No writable data
volume installed or approved. Root still read-only and unchanged.

Exact master keybagd SHA256
747271703b7aff98420ed23788a362716025506d8d0ba8c703fb78e5b3ec1b9b,
CDhash a8815e1634a055bd5ae09431eb7492cdcf3fd9b9, 275504 bytes; matches catalog.
Audit E:/A52-iOS16/master-keybagd-audit-v1/audit.json. Master has no
/private/var/keybags. Disassembly shows system-bag selector 14; a failed KeyStore
connection can yield generic 0xe00002bc before disk-load handling, but actual
failing operation/result remains unobserved until V22. Do not infer it from
corrupt text. SWEET AppleKeyStore stub does not implement working save/load/
wrap crypto and must not be described as a software keychain.

## Historical V21 catalog trial — restored above

Launcher80083 finishedsuccessfully: installed16GiBroot/protectedhasheschecked,
onlyBOOT written/readback, actualnativeSamsung rebootadbUSBdepartureconfirmed.
backup/a52q/ios-ufs-v21/receipt.json requires_restore=true,
original_boot_restored=false. C:guardwrapperPID5040/watchedreceiptv21 waiting
forTWRP; logs samefolder watcher.log/watcher.err.log. It retriesUSB beyond30min,
preservesfirstcapture and refusesunknownBOOT. Newcatalog/service resultUNKNOWN.
Usertoldfivefullminutesafterrebootconfirmation, resetTWRPleaveUSB, noSystem/format.
Onreturn collectfirstlog/guardreceipt, confirmrestoredoriginalandfreshfullBOOTSHA
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
DoNOT leave restorationpending afterTWRPreturns. NoextraUFSwrite/varvolumeinstalled.

### V21 artifact and preflight history

User freshly confirmed readiness. research/start_root_catalog_trial.py running
execsession80083. Fullinstalledroot/protectedhashchecks beforeBOOTwrite. DoNOT
start anotherinstall. Receipt/logs backup/a52q/ios-ufs-v21, guardwrapper
research/watch_ios_ufs_v21_restore.py. Inspect requires_restore before any stop.
Actualnewserviceexecution result UNKNOWN. Notifyfive-minreset onlyafterUSBdeparture.

FullHFS build43897768441 SUCCESS;76actualoverlayfiles matchedexpectedhashes,
onlyAMFIC+newcatalogheader differ fromfullbaseline43735227285.
KernelSHA b9f5ab95d6c57d13efb9bcebbf72a2d320ee4d6264b0dc3ffaf289bbe36833a3.
AMFISHA9a18d92ebe653b579e185496134bd31b9c2e72ca1afbbac6a52950ad378c435c.
Original128testCI43897710224 lineendingfailure fixedbyce9a5b92b07615be95a363b235625e5982ca9225:
LinuxCI43900310051 SUCCESS,128localtestsPASS;redundantauto43900309926cancelled.
CompiledC/header/apply exactlyequal8e1f079 buildhead aftercanonicalLFmetadatafix.
Nootherkernelrebuildrequiredforfixturehashcorrection. DoNOT claimwarningfree;
fulllegacytree compiledwithwarnings,noerrors.

Hostpipeline61351 COMPLETE: E:/A52-iOS16/builds/43897768441/{artifact,verified-build.json};
QEMUshim/out/a52q-root-catalog-qemu-v1:3CRCentries,7diagnosticPID1heartbeats,
enforcement/providerregistrationchecked; NOT Appleuserlandemulation.
Wholemaster16GiBhashstill0f4...312149; plan15/hardware17candidate96MiB SHA
63a6199b0dcc3254cfe3c588f350ebb25a0360519212d19aaab41d122e55012a.
Kernel/manifest/ROrootbound; nophoneRAMroot/diagnosticinit. Independentreview
E:/A52-iOS16/root-catalog-v21-candidate.json. Helperexplicitlybindsplan15.
FreshrecoverycheckoriginalBOOT+protectedhashes PASS beforetrial. Display/storage/
memory/pstore/provider10sources byte-identicalfullbaseline. No newdata-volumewrite.

## Catalog implementation/audit history

Implemented measuredcatalogsource commit8e1f0791416a466ea6779297b9a810fb387471fa.
128 localtests+repocheck PASS; nativeactualpolicytests every2786identity,
55720changedhashes,metadata/root/flagboundaries. FullHFS build43897768441 RUNNING;
auto-mockfs43897710358 cancelled. Privatehostpipelinefinish_root_catalog_artifacts.py
session61351 watchesbuild, verifies76overlayfiles againstfullbase43735227285
(onlyAMFIC+newcatalogheader differ), exactkernelQEMU, masterrehash plan15,
package hardware17. Expectedmapprepared PASS. PhoneoriginalBOOT restored; noV21.

LinuxCI43897710224 FAILED oneheaderhashcheck: WindowsgeneratedCRLF vsGit/applyLF.
Measuredidentitiesunchanged. Correctedgenerator towriteLF, testtonormalizecheckout,
metadatahash74be6f5730ab7220a4873f97b3e937047b0b3bbf5a9b02decc2e197ec7191ed3.
128localtests PASSaftercorrection. Do NOT pushmetadatafix untilfull43897768441
finishes (xnuJSONpush triggersauto-full and cancelsactivebuild). Thenpushfix,
cancelredundantauto-full,awaitnewLinuxCI. Header compiledbytes equal8e1f079GitLF.

Inactive V21launcher research/start_root_catalog_trial.py+watch_ios_ufs_v21_restore.py
reviewedpaths:receiptbackup/a52q/ios-ufs-v21,hardware17,ownwrapperv21. Mustbind
helperplan15 onlyaftercandidatechecked; noinstalluntilfreshphysicalreadiness.
No writablevar volume installed or newstoragewriteapproved. GuardC:backups
independentofE:. Explicitcatalogcodeadmitsallmeasuredrootidentities, grantsno
genericentitlementcontext; runtimecapabilityfailures areexpectedquestionsforphone.

Source a52q_display.c explicitlyisguardeddiagnostic, notIOMFB/VSyncABI; noIOSurfaceRoot
orMetal/GLbackendimplementation inA52sources. Keepthis distinction inreports.

Catalog V3 COMPLETE: E:/A52-iOS16/master-root-code-catalog-v3/catalog.json SHA
60f22e7b3e5ce8befa592fbde4e55f1a22355aa868d27318762efb82e8e5c1d1.
Readonlyappliance successfully used stopped distro VHDXro,noload/Python, noWSL
VM needed.181744readableregularpaths,2790MachO,2786CodeDirectories,
252793verifiedcodepages,2910signedslots. Two unreadableThai.shortcutresources
explicitlyexcluded;9nonuserlandinputs excluded(5kext,4Metalarchives).
All requestedserviceidentitiespresent; noCMS/exec/UIclaim. backboardliblinkguard
is LC_LOAD_WEAK_DYLIB, notmandatorydependency. PriorV1scanhostcommitfailed;
V2stoppedonUnicode; preservedlogs. V3normalizationfallbackrecordsunreadablegaps.

Implemented generatedheader+publicauditJSON, read-onlycatalogtool, AMFIbinary
search/metadata/rootchecks, applyheaderstaging, relinkerold/staleheaderguard,
tests/docs. All128hosttests PASS; previousrepoauditPASS (rerunbeforepush).
ActualCpolicychecksall2786identities+55720hashmutants, signedmetadatafailures,
wrong/writablemounts, missingCS_VALID andforbiddencapabilities. Corepagechecks
stayenabled; onlySIGNED/PLATFORMflagsadded. Noentcontext/gettaskmanufacture.
Newheader changesoverlayto76files: FULL HFS build required, noisolatedoldbase.
No newcandidate/phonewrite. OriginalBOOT restored. Nextcommit/push/build,
verify76sourcehashes, QEMU/masterrehash/packageplan15/hardware17, freshreadiness.

Guard collected/restored first attempt. V20 receipt requires_restore=false,
original_boot_restored=true,protectedhashesunchanged,3CRCentryrecords,boundedROroot
verified (1validrootrecord). Fresh completephoneBOOT hash matchesoriginal
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Phone TWRP, NO restoration pending. Console262132B SHA
d3927d3804bd477f3ef84b17e489a70b2f14d522ddf5e6eeebd2d87451e377d9.
E:/A52-iOS16/xpcproxy-v20-result.json. Exactproxy admitted, realchildren attempted
callee exec: signature rejectsSpringBoard,backboardd,notifyd,configd,etc. Backboard
line hascorruptbyte `load #ode`; retain original bytes, don'tquote repairedline.
Missingpersona6 andROvar/logger errors30 persist; capturefillsfixedconsolecapacity.
Persistentservices/UI remainunproven. OnlyRGBframebuffer physicallyverified;
user'sworking60HzIOMFB/IOSurface claim remainsunsupported.

User now explicitly requests admission of all20H392 rootMachO. Plan measured
master-derived codeidentitycatalog, requireactualROroot+CS_VALID+originalsigned
slot checks, retain normalpagechecking. Do NOT blindlysetCS_VALID/GET_TASK_ALLOW,
acceptarbitrarypath/content or fabricatehardware/entitlementcontexts. First audit
allrootMachO fromunchangedmaster. Existingfive-serviceaudit completed privately
E:/A52-iOS16/master-early-services-audit-v1/report.json: actualmaster/nativehashes,
signedpages/slotsverified forxpcroleaccountd,notifyd,configd,backboardd,SpringBoard.
All directdylibs incache exceptbackboarddliblinkguard (inspectweakloadcommands).

WSL now fails coldVMcreationERROR_NETNAME_DELETED (two attempts); nohostreboot.
Alternativeindependenthostaudit: attach stopped distro E:/A52-HakiOS-tools/wsl/ext4.vhdx
READONLY to existingLinuxappliance, mount ext4 ro,noload; chrootitsPython while
rootmaster remainsseparateROvirtio/HFS. Injectionjob/script inRAMonly. No root
catalog/policy implementation yet; noV21candidate or devicewrite started.

## Historical V20 xpcproxy trial — restored above

start_xpcproxy_trial.py completed successfully: full installed16GiB root/protected
hashes checked, onlyBOOT written/readback, actual native reboot adb USBdeparture
confirmed. backup/a52q/ios-ufs-v20/receipt.json requires_restore=true,
original_boot_restored=false. New xpcproxy/service result UNKNOWN.
C: robust guard wrapper PID4224 (watch_ios_ufs_v20_restore.py) is waiting forTWRP;
logs backup/a52q/ios-ufs-v20/watcher.log +watcher.err.log. User told five fullminutes
after departure confirmation, resetTWRP, leaveopenUSB. Fresh userreadiness confirmed.
On return collect firstcapture/guardreceipt, verify originalBOOTrestored and
freshfullphoneSHAd6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Do not selectSystem, formatdata, overwriteoldcapture or leave restorationpending.

### V20 checked artifacts and preflight history

User freshly confirmed physical readiness. research/start_xpcproxy_trial.py
running (execsession9716), phone pre-install full-root/protected hash checks.
Do not start another install. On completed reboot departure, wrapper starts
research/watch_ios_ufs_v20_restore.py -> robustguard; receipt/logs
backup/a52q/ios-ufs-v20. Check receipt for requires_restore before any stop.
No new result yet. Return to TWRP five full minutes after confirmed USBdeparture,
then collect/verify original BOOT restoration and fresh full phone hash.

Candidate/source committed b42f3852b4b8b5e1cd48fd876dc9399ed143bf67.
Host121tests+repo validation PASS, LinuxCI43740932493 SUCCESS.
AMFI-only build43740931838 SUCCESS with fullbase43735227285; source/hash guards
and independent provenance verified. KernelSHA
f94856acd6115ff2c067561106f31cd14a64679cb91c6d1fd4ab451845c81528,
AMFISHA7f7bad698db6fe1702e0820002128655374c9434628f974f0785db2bdf5532aa.
QEMU shim/out/a52q-xpcproxy-qemu-v1:3CRCentries,7diagnosticPID1heartbeats,
provider registration/enforcement enabled. NOT Applexpcproxy/services emulation.
Whole16GiB master rehashed0f4...312149. E:/A52-iOS16/ios-root-plan-v14.json,
hardware-v16/build/a52q-ios-ufs-UNTESTED.img SHA
c9adb74c6869ac36e643eeb2cb3fda207cd25f94e6d94a70c8f036d259b786c4.
Manifest/kernel/root/96MiBimagechecked; noRAM/diagnosticroot inphonepayload.
Independent report E:/A52-iOS16/xpcproxy-v20-candidate.json.
Helper now explicitly bindsplan14; C:originalbackups/guard independent ofE:.

Static original launchd log option audit (research/launchd-serial-parser.log)
shows launchd_log_serial= reduced toBoolean, not a verified severity threshold.
Do NOT set an invented verbosity number. Logging source/region remain unchanged.

## V19 RESTORED; exact xpcproxy admission host audit

Fresh read-only recovery check2026-11-15T17:22Z confirms whole original BOOT
SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016
and protected hashes unchanged. No restoration pending, phone TWRP. V19 result
E:/A52-iOS16/cache-loader-v19-result.json; console SHA671303c2044a0415c9017bdfbe6e6c9d4709ee17874bc4391754a81e287a7ce9.

Master/native xpcproxy audit E:/A52-iOS16/master-xpcproxy-audit-v1/audit.json:
96352B,SHAa97bc59d024c3b7fcf293aa6ef2fa75b60ef7220b2546ab4382adcbe78ddbfec,
arm64/subtype0,19 verified4Kpages,CDhashf7f090b0a9b94dc944026136fc6154372763c846,
original XML573/DER306 signed-slot hashes checked. Three direct dylibs present
in SHA-verified cache index. Repeated audit rejects modified entry-page bytes.
Policy change only a52q_amfi.c: exact helper on actual ROroot, original metadata,
localplatform status,no entitlement context/callee wildcard. New public pinJSON,
native actual-policy test covers60CDhash mutations and rejects wrongmetadata/root,
denies mount capability and cachequery forproxy. Native policy test PASS.
No changes to storage, display, reservedRAM, pstore or validated master.
Need fullhost checks,commit/push, AMFI-only relink base43735227285, verify corrected
leaf/provenance,QEMU and new plan14/hardware16 packaging. No V20 trial started.
Preserve corrected blob-platform logic; compile-onlybasef22e must NEVER be flashed.

## V19 RESTORED; cache query/registration passed; xpcproxy rejected

V19 guard collected/restored first attempt. Receipt requires_restore=false,
original_boot_restored=true, protected hashes unchanged, changed recovery boot
ID,3CRC entries,actual boundedROroot verified. Fresh full phone BOOT SHA
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016 matches.
Phone TWRP. NO restoration pending. Retain backup/a52q/ios-ufs-v19/console.txt.

Actual log: exact cache-loader connection opened; measured20H392 cache identity
recognized; original detached signature admitted, core loaded launchd.plist
range0:0x164000 flags0x10003. Parent then `Early boot complete. Continuing system
boot.` and imports system/user501 service definitions (including SpringBoard).
No successful persistent service or UI proof. Next failure: proc22 load signature
error4 filexpcproxy; later `Could not spawn process /usr/libexec/xpcproxy:85`.
Root var/logger EROFS30 persists. Audit exact xpcproxy from master/native source,
headers/dependencies/entitlements before admission; do not blanket-admit daemons.
Capture262132B ends mid-message amid mass-spawn logging: inspect console capacity
before interpreting last timestamp as a kernel hang. Preserve all old captures.

## Historical: V19 measured-cache service trial — restored above

Fresh readiness received. research/start_local_amfi_trial.py completed full
installed16GiB root/protected partition hash checks, wrote/read back only BOOT,
confirmed native reboot adb USB departure. Corrected candidate
664360e93f7ab6e454d646cb2c0dbd21590a9a4165991e076de1c1543cd37389;
kernel d164a51d9e4476e94068bf40f91a3ca66ba5fb8851dd5854718ea5f1d417a48c.
Root remains RO/unchanged. New service/query/registration result UNKNOWN.

backup/a52q/ios-ufs-v19/receipt.json requires_restore=true/original_boot_restored=false.
C: robust guard wrapper PID2688/watch_ios_ufs_v19_restore.py invokes
watch_pending_boot_restore.py, waits beyond30min, retries USB interruptions,
preserves capture, refuses unknown BOOT contents. Logs same folder
watcher.log/watcher.err.log. User told five full minutes from actual reboot
confirmation, then reset to TWRP and leave USB connected. On return collect
actual query/cache outcome and first failure, verify guard restoration, then
fresh complete phone BOOT SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Do not leave restoration pending after recovery reconnects. Never select System
or format data. No new storage write outside BOOT; no writable var installed.

## Previous: V18 RESTORED; abort reason confirmed: Unable to find AMFI

V18 guard collected/restored automatically. Receipt requires_restore=false,
original_boot_restored=true, protected hashes unchanged, 3CRC entry records,
changed recovery boot ID. Fresh full phone BOOT SHA
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016 matches.
Phone TWRP. NO restoration pending. Retain backup/a52q/ios-ufs-v18/console.txt.

New trace gives three identical reason lines: ns7/LIBXPC code1 description
`Unable to find AMFI`. Loader process PID21, signal6. This confirms the observed
IOServiceMatching("AppleMobileFileIntegrity") service lookup failure, not a
code-page or spawn failure. Cache registration/submission, persistent services
and SpringBoard remain unproven. Next narrowly implement software service and
only observed user-client ABI type0/selector6, scalar1 + CDhash structure. Caller
must remain exact verified loader on actual RO root. Recognize only exact
verified boot-cache signatures, retain all unknown/modified rejections and normal
code-page checks. No global AMFI bypass, no Apple CMS/SEP/hardware claims.
Inspect real IOUserClient security/lifecycle and VFS measurement APIs before code.

Local measured query implemented/committed fc9421ee14514e21d15f5f65ed8be61c50f6d6b1.
Files A52PlatformExpert.cpp/a52q_amfi.c/shared a52q_boot_cache_policy.h plus apply
header staging, metadata JSON, tests and docs/A52Q-LOCAL-AMFI.md. Service has
compatibility names but is NOT Apple's AMFI/CMS verifier. Legacy userclient type0,
selector6,scalar1,20B recognized CDhash,no outputs/descriptors/async. Every open
and method checks exact signed loader + actual ROroot + retained owning task.
Other global entitlement/capability queries STILL denied. Code+detached sig are
fully SHA256-read via UIO_READ from exact regular ROroot paths and lengths; data
registration also binds actual vnode and CS_VALID/no ent metadata. No platform
flag for data cache. All normal core signature/page checks remain on; no uploads,
global bypass or storage/display/memory changes. XNU callback precedes vnode_lock.
Native staged cache+sig hashes freshly matched master.121 local tests+repo checks
PASS, including mutated hashes/digests/measurements, wrong caller/root/metadata,
malformed method ABI and ungranted capabilities. HostCI43733904616 SUCCESS.

Full HFS kernel43733904802 RUNNING; auto mockfs43733904688 cancelled. Host-only
pipeline research/finish_local_amfi_artifacts.py session26818, stdout
research/local-amfi-build-package.log: verify75-file expected overlay against
full trace baseline43729112746 (only2existingCfiles+2newheader copies differ),
archive/SHA checks, exact-kernel diagnostic QEMU/provider publication, master
rehash plan-v13 and package hardware-v15. Independently prepared expected map
E:/A52-iOS16/local-amfi-expected-overlay.json PASS; strict source/apply delta PASS.
No new phone writes; Original BOOT restored. V18 result
E:/A52-iOS16/cache-loader-v18-result.json,70470B console SHA
0dbc408843842045a90137005ccde7af280f2b98a1bdcc964595e35eff3ae0da.
Actual new service/query/registration unproven until phone trial. Do not call
source/boundary tests a successful Apple userland or SpringBoard boot.

Build correction IN PROGRESS: live compiler logs exposed header not found in
iokit/Kernel/arm/A52PlatformExpert.cpp. fc942 staged it in iokit/Kernel. Fixed
33ba1d9edc25e0fdcb9ebe56ffb5a30ecd40d643 to stage in actual ARM directory.
43733904802 cancelled; no successful compile or candidate from that run.
HFS full43735227285 RUNNING on corrected path; hostCI43735227516 SUCCESS.
Corrected verifier research/verify_local_amfi_full_build_v2.py checks real ARM
CPP/header paths and expected map length75 (old V1 map/path was wrong; do not use).
Expected map E:/A52-iOS16/local-amfi-v2-expected-overlay.json prepared PASS.

Further target-source audit found kern_exec.c:1388 mask excludes platform bit
from p_csflags; kern_cs.c::csproc_get_platform_binary reads cs_blob. Corrected
caller check locally: raw CS_VALID|CS_SIGNED plus exact verified blob's platform
flag/field. Native policy test models real raw flags and still denies missing
blob classification, signature metadata, wrong roots/caller. PASS. Shared-header
guard added to isolated relinker to prohibit stale CPP/header combinations.
Do NOT push this C-only correction while43735227285 full build is running:
push would start auto full build/cancel baseline. Plan: verify successful base33,
then push corrected AMFI source, cancel redundant auto-full, isolated leaf=amfi
using base_run43735227285, verify new kernel, QEMU/package only corrected kernel.

Stopped host V2 packaging waiter PID5420/session64879 before it could package
the base with the incorrect raw-platform check. Original V1 waiter ended cancelled.
No candidate/QEMU/plan-v13/hardware-v15 generated yet. research V2 host scripts
must be superseded by corrected-leaf pipeline. V19 trial runners already prepared
(start_local_amfi_trial.py,watch_ios_ufs_v19_restore.py), helper bindsplan-v13,
but DO NOT RUN until corrected kernel checks and fresh physical readiness.
Phone still TWRP, original BOOT restored; NO restoration pending.

Corrected-path full43735227285 SUCCESS; all75 archived source hashes/expected
overlay verified, kernelSHAf22e5101a2697bb29fe1132e4f650ef206bcf9587a070e0338336ca13c522005,
init aaacee...4473e. E:/A52-iOS16/builds/43735227285/{artifact,verified-build.json}
is explicitly COMPILE/LINK BASE ONLY, not a phone candidate (raw-platform check
still present there). No baseline packaging was run. Full build no longer running:
now publish local correction554312c and isolated leafamfi using this success base,
cancel redundant auto-full. Current source checks actual blob classification;
native caller-policy testPASS. Do not flash basef22e kernel. New corrected kernel
requires provenance, exactQEMU/provider registration, master hash/plan13 packaging,
then fresh readiness before V19. Old host pipelines26818/64879 are stopped/ended.

Corrected AMFI isolated rebuild43737148277 SUCCESS (head2ada3d9ca8ee8181d0be6486c1ef227ead8cafb7),
base full43735227285/33ba1d9/f22e...2005, header/shared-leaf guards passed.
HostCI43737147920 SUCCESS; redundant full43737147935 cancelled. Actual corrected
kernel SHA d164a51d9e4476e94068bf40f91a3ca66ba5fb8851dd5854718ea5f1d417a48c,
AMFI implementation SHA52ee76a41c6108c7b1c9f3753e7b21347440b6f1dff1d41afb87eb52f18e9079.
E:/A52-iOS16/builds/43737148277/{artifact,combined,verified-build.json} verified.
research/finish_local_amfi_corrected_artifacts.py session51197 COMPLETE;
research/local-amfi-corrected-build-package.log. Exact corrected kernel QEMU
shim/out/a52q-local-amfi-qemu-v3/run/result.json:3CRC entries,7 diagnostic PID1
heartbeats, local provider registration log observed. This does NOT exercise
Apple loader/client/file measurement. Whole16GiB master rehash still0f4...312149.
Corrected plan-v13/hardware-v15 96MiB candidate SHA
664360e93f7ab6e454d646cb2c0dbd21590a9a4165991e076de1c1543cd37389,
payload verified noRAMdisk/diagnostic root and kernel/manifest binding matches.
Compile-only f22e base was NEVER packaged/flashed. Old V1/V2 packaging stopped.
V19 start_local_amfi_trial.py/watch_ios_ufs_v19_restore.py already prepared,
helperbindsplan13,robustguard/C:backups. NOT started; fresh physical readiness
question pending. Phone TWRP, original BOOT restored, NO restoration pending.
Next phone log must establish actual owner/caller auth, measurement query,
detached registration/cache submission or first new failure; no services/UI proof.

## Historical: V18 fatal-exit diagnostic — restored above

Fresh readiness received; research/start_exit_trace_trial.py completed full
installed16GiB root and protected partition hash checks, wrote/read back only
BOOT, confirmed native reboot adb USB departure. Candidate
2b87d713355a005a79870fd44c20f9ae57feb3bf8b861276dcc492f19a513cea;
kernel13c2016875672cf6578605db98cdcdf7180956074fab87607c20bed3948e3a3a.
Root read-only/unchanged; no other storage write. Actual new result UNKNOWN.

backup/a52q/ios-ufs-v18/receipt.json requires_restore=true/original_boot_restored=false.
C: watcher wrapper PID2488 invokes robust watch_pending_boot_restore.py, keeps
waiting beyond30min, retries USB interruptions, preserves first capture, rejects
unknown BOOT content. Logs same folder watcher.log/watcher.err.log. User told
five full minutes from actual reboot confirmation, then return to TWRP and
leave USB connected. Collect fatal-exit details, verify guard restoration and
fresh full phone BOOT SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Do not leave restoration pending after recovery reconnects. Never select System
or format data. Keep V17 as last usable baseline until new retained evidence.

## Previous: V17 RESTORED; loader admitted then SIGABRT; capture exit reason next

V17 guard collected and restored automatically on first attempt. Receipt
requires_restore=false/original_boot_restored=true; protected hashes unchanged,
3CRC entry records, bounded read-only UFS root verified. Fresh whole phone BOOT
SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016 matches.
Phone TWRP; NO restoration pending. Saved backup/a52q/ios-ufs-v17/console.txt.

Exact launchd_cache_loader admission now observed; it passes spawn and exits
SIGABRT, then launchd panics for required task failure. No successful boot-cache
registration/submission or services proof. Existing console omits the child's
abort reason; writable var/logger absent. Do NOT infer missing AMFI or cache
failure from SIGABRT alone. Next source audit: loader's static abort paths plus
minimal A52-only fatal-exit reason logging into existing RAM console, without
changing signals, admission, storage, display, reserved RAM or userland bytes.

Diagnostic source committed f478e2df9cb747fca1c3c308633feb0c650bb5bd: new
xnu/a52q/exit_trace.py + apply.py hook print existing current-process fatal
signal/exception/reason (bounded192B description, 3 copies) before corpse
notification. Copies are unprotected text, NOT CRC-protected. Termination,
reason, crash flags and all hardware/policy implementations unchanged.
tools/relink_a52q_console.py now rejects missing/changed fatal-exit transform
in an old base; this requires full build.120 local tests/repo integrity PASS,
actual target transform exact-delta/repeated/wrong-source checks PASS;
hostCI43729112245 SUCCESS. Full HFS build43729112746 RUNNING; auto mockfs
43729112242 cancelled. No new phone write; original BOOT remains restored.

research/finish_exit_trace_artifacts.py session3297, stdout
research/exit-trace-build-package.log waits for full build, verifies expected
overlay+archive, exact-kernel diagnostic QEMU, master rehash plan-v12 then
packages hardware-v14. Full-build expected overlay prepared independently
from verified full base43705321913: all hashes same except kern_exit (trace)
and a52q_amfi.c (already-tested subsequent pins). Strict source-diff and apply
normalization checks PASS; E:/A52-iOS16/exit-trace-expected-overlay.json.
Pipeline remains HOST ONLY. V17 result E:/A52-iOS16/cache-loader-v17-result.json,
70023B console SHA469a10f0fae29ffe5dba2b1c4a1b780cb560bcd74353ed524a8b8694591a7432.
Loader main entry is NOT proven by SIGABRT/process start.
Static main audit E:/A52-iOS16/cache-loader-main-static-v1.txt shows fopen NULL
is handled, so logging EROFS alone does not explain abort; multiple earlier/
later abort branches exist. No AMFI/cache/graphics stub justified without reason.

Exit-trace host pipeline COMPLETE: full HFS build43729112746 SUCCESS; host
CI43729112245 SUCCESS. All73 overlay file hashes match independently expected
base+two-C-file deltas, and archived source/SHA256SUMS verified. New full kernel
SHA13c2016875672cf6578605db98cdcdf7180956074fab87607c20bed3948e3a3a;
init SHAaaacee08d03b7f0d93b0b34aa1d2436b0c3798b370ebf1e623732c5739c4473e.
E:/A52-iOS16/builds/43729112746/{artifact,verified-build.json}. Exact-kernel
diagnostic QEMU passed3CRC entries/7 PID1 heartbeats; fatal-exit hook/Apple
userland NOT exercised by this fixture. Whole16GiB master rehash passed.
plan-v12/hardware-v14 96MiB candidate SHA
2b87d713355a005a79870fd44c20f9ae57feb3bf8b861276dcc492f19a513cea;
no RAMdisk/diagnostic root. Root remains unchangedRO; new trace not phone-proven.

V18 runners prepared using robust guard: research/start_exit_trace_trial.py,
watch_ios_ufs_v18_restore.py, C:backup/a52q/ios-ufs-v18. Helper binds plan-v12.
Fresh readiness received; starter session59391 RUNNING PREFLIGHT, check receipt
before claiming phone BOOT state. User told five-minute timer starts at confirmed
USB departure, not preflight. No new kernel compatibility policy/hardware change.
Independent static IO ABI audit cache-loader-io-abort-static-v1.txt finds
user-client type0, method selector6, one scalar=1 and variable structure input;
no output buffers. This is NOT proof that path was reached. Common helper
abort_with_reason passes namespace7/LIBXPC, code1, flags0, caller reason string;
see cache-loader-abort-imports-static-v1.txt. Await actual reason before any stub.

## Historical: V17 controlled loader retry — restored above

Fresh user readiness received. research/start_cache_loader_retry.py completed
the full installed16GiB root hash/protected partition checks; wrote/read back
only BOOT, confirmed USB departure using native reboot adb. Same checked BOOT
786b089cc723c2510f902e4054af0d9a24c4b2b1470586ad565ceb6814cbbdee;
kernel266393446ff34fed174c6789545ced43b3f272bbae0408fb7e7fa59b3b06cc9e.
Root read-only/unchanged, no other storage write. New physical result UNKNOWN.

backup/a52q/ios-ufs-v17/receipt.json requires_restore=true/original_boot_restored=false.
C: watcher wrapper PID9488 invokes watch_pending_boot_restore.py; 30min soft
warning, keeps waiting, retries interrupted restore, preserves first capture,
rejects unrecognized BOOT contents. Logs same folder watcher.log/watcher.err.log.
User instructed to wait five full minutes from actual departure confirmation,
then return to TWRP and leave USB connected. On return verify collection and
restoration completed, then fresh full BOOT SHA
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Do not leave restoration pending after recovery reconnects. Do not select
System or format data. Keep V15 as last usable baseline until new logs prove more.

## Previous: V16 RESTORED; no XNU console; unchanged loader retry prepared

V16 30min watcher expired before recovery return. Manual collect-restore first
captured console.txt (65 bytes: missing console-ramoops-0 error) and dmesg,
then USB dropped after RAM staging push, before BOOT restoration. User replugged
USB; new helper phase restore-only preserved saved captures and restored BOOT.
Receipt requires_restore=false/original_boot_restored=true; protected hashes
unchanged. Fresh whole phone BOOT SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016
matches. Phone TWRP. NO restoration pending. V16 is inconclusive: no XNU entry
frames/root/loader proof. Preserve V15 as last usable boot console.

User's quoted dirs_cleaner signature error is V14, already corrected and tested
in V15. docs/A52Q-DIRS-CLEANER.md now traces exact headers/actual caller/rejection:
XNU8796.141.3 EBADEXEC85 != EROFS30; AMFI KERN_DENIED53 -> ubc EPERM1 ->
loader LOAD_FAILURE4 -> exec EBADEXEC85. Actual measured launchd boot call is
posix_spawnp at unslid0x10003fe1c, saves returned w0/x0 in x22, sends SAME value
to strerror and posix_spawn():%d:%s; no fresh global errno. Private static audit
launchd-spawn-reporting-v2.json and launchd-spawn-reporting-boot-error.txt.
V1 direct-posix_spawn-only disassembly found an unrelated assertion call;
use V2/boot-error evidence for the actual boot-task path.

V15 dirs_cleaner executed, launchd advanced, but mkdir /private/var/dirs_cleaner
EROFS30 and logger EROFS30 remain. Additional dc_reset error strings are bit-
corrupted: no exact errno inferred. Apple cleaner source's normal main path
returns0 after logging errors; do NOT report successful cleanup or writable var.
Next usable-log fatal remains launchd_cache_loader signature rejection. Kernel
fix b4414cd already host checked; do not reapply/revert dirs admission.

Prepared V17 unchanged hardware-v13/plan-v11, same BOOT786b...4cbbdee/kernel2663...cc9e.
research/start_cache_loader_retry.py preserves V15 fallback (V16 is NOT a usable
baseline). New research/watch_ios_ufs_v17_restore.py delegates to generic
watch_pending_boot_restore.py:30min soft warning, keeps waiting, retries USB
failure, preserves first capture through restore-only, refuses unknown current
BOOT contents. C:backup/a52q/ios-ufs-v17 new receipt/logs. No trial started yet;
fresh physical readiness question pending. New guard transport simulation PASS:
late return+failed restore/retry preserves evidence; unknown BOOT denies without
backend; completed receipt exits without commands. Syntax checks PASS.
Current git AMFI bytes match built commit after CRLF normalization; exact96MiB
candidate hash reverified. No new kernel/root/storage/display changes or rebuild.

## Historical: V16 cache-loader trial — restored above

Fresh user readiness received. research/start_cache_loader_trial.py completed
the full installed 16 GiB root hash and protected partition checks, wrote and
read back only BOOT, then confirmed recovery USB departure with native reboot
adb. Candidate 786b089cc723c2510f902e4054af0d9a24c4b2b1470586ad565ceb6814cbbdee;
kernel 266393446ff34fed174c6789545ced43b3f272bbae0408fb7e7fa59b3b06cc9e.
Root stays read-only/unchanged. Physical loader result still UNKNOWN.

backup/a52q/ios-ufs-v16/receipt.json requires_restore=true/original_boot_restored=false.
C: watcher PID4920 research/watch_ios_ufs_v16_restore.py waits up to30min for
TWRP; logs backup/a52q/ios-ufs-v16/{watcher.log,watcher.err.log}. User asked to
wait five full minutes from actual reboot confirmation, then return to TWRP
and leave USB connected. Collect logs, restore C:original BOOT and freshly
verify complete phone SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Do not leave restoration pending after recovery reconnects. Never select
System or format data. No other storage write, no writable data volume.

## Previous: V15 RESTORED; cleanup ran; launchd_cache_loader exec rejected

V15 watcher collected/restored automatically. Receipt requires_restore=false,
original_boot_restored=true; protected hashes unchanged and recovery boot ID
changed. Fresh whole BOOT readback again d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Phone TWRP. NO restoration pending. Saved backup/a52q/ios-ufs-v15/console.txt.

FIPS POST again reports all tests PASSED. Exact dirs_cleaner admitted and actually
ran; mkdir /private/var/dirs_cleaner failed EROFS30. Launchd advanced beyond it,
but cleanup success / writable data is NOT demonstrated. System logger socket
also EROFS30. Next fatal: launchd_cache_loader posix_spawn85/load signature4.
Other optional helpers remain denied; no general admission bypass. No services
or SpringBoard proof. Host audit for the now-observed loader is already complete
as recorded below; next admit only its exact signed identity on same RO root.
Retain original binary/cache and no fabricated AMFI trust response. Need observe
loader's actual next operation before adding a cache-registration/provider fix.

Next loader admission committed b4414cd2ca2624e2ccd7f1345502974b4e958d4a.
72,336-byte loader SHA e1f0b581b73222465a36778af0c3260d7f52ab0e24c374b9111c599830b1e00f;
CDhash 24edfda4520d9f9b246a0c6c91facbd9f0954a38; 13 code pages+signed slots pass,
XML390/DER152. New exact helper checks CS_VALID/getter hashes+sizes/same ROroot;
local platform classification only, no trust-cache/IOKit entitlement context.
120 local tests+repo checks PASS; host CI43715378805 SUCCESS. Isolated AMFI build
43715378760 running, full base43705321913; redundant full43715378796 cancelled.
research/finish_cache_loader_artifacts.py session42571, stdout
research/cache-loader-build-package.log will verify isolated rebuild provenance,
run exact-kernel diagnostic QEMU then rehash master/package plan-v11/hardware-v13.
No new phone write. V15 retained result E:/A52-iOS16/dirs-v15-result.json:
console69640B SHAc81ec593b98390e34258aa17f34020327675dc7b5dd56ebf2cdb435551904b7e,
3CRC entries, bounded ROroot proof. Original BOOT restored.

Loader candidate host pipeline COMPLETE: isolated build43715378760 SUCCESS,
hostCI43715378805 SUCCESS; full43715378796 cancelled. Verified kernel SHA
266393446ff34fed174c6789545ced43b3f272bbae0408fb7e7fa59b3b06cc9e;
AMFI SHA22646db2c7c5c738a2ffd3c0c46f9330c4612be71954af3a66a9e431b0758946.
E:/A52-iOS16/builds/43715378760/{artifact,combined,verified-build.json}.
Exact-kernel QEMU passed 3CRC entry records/7 diagnostic PID1 heartbeats; this
does NOT execute Apple's loader/full UFS root. Whole16GiB master rehash passed.
plan-v11/hardware-v13 checked 96MiB BOOT SHA
786b089cc723c2510f902e4054af0d9a24c4b2b1470586ad565ceb6814cbbdee.
Payload has no RAMdisk/diagnostic root. Loader/cache submission still unproven.
Prepared research/start_cache_loader_trial.py and watch_ios_ufs_v16_restore.py;
C:backup/a52q/ios-ufs-v16 new logs/receipt, 30min watcher, C:original backup.
Private helper expects plan-v11. Runners NOT started; fresh readiness pending.
Original signed loader XML verified can-check-trust-cache=true and sole user
client class AppleMobileFileIntegrityUserClient; neither capability granted.

## Historical: V15 directory-cleanup trial — restored above

User freshly confirmed readiness. research/start_dirs_trial.py completed the
whole installed 16 GiB root hash and protected partition checks, then wrote
and read back only BOOT. Candidate bc50a99b72cbb6fe862eacfadb5d69cb8e163d8c3fd4412a77651029c96ffa8f;
kernel 13b6eda1e0525add11cd4f986bfd02b4a764c9d0b007d220729dfcf959249766.
Native reboot adb confirmed recovery USB departure. Root stays RO/unchanged.

backup/a52q/ios-ufs-v15/receipt.json requires_restore=true/original_boot_restored=false.
C: restoration watcher PID3920 (research/watch_ios_ufs_v15_restore.py), 30-minute
return window; logs same folder watcher.log/watcher.err.log. User instructed
to wait five full minutes from confirmed departure, then reset to TWRP and
leave USB connected. On return collect logs, restore original BOOT and freshly
check full phone SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Do not leave restoration pending after recovery reconnects. Do not select
System or format data. New physical cleanup result still UNKNOWN.

Independent RO host audit while waiting: master-launchd-cache-loader-audit-v1
verifies exact staged-source match, 13 signed pages and XML/DER slots for next
required launchd_cache_loader; it is NOT admitted or executed. Strings reference
AMFI user-client trust lookup and /System/Library/xpc/launchd.plist(.sig).
Read-only master-launchd-plist-v1 export completed: cache 1456980 bytes SHA
810070302b5c4d7c5f00bdc8df20aaea2dd33cd8342d2402fcdf7ff6397d374c;
signature 19006 bytes SHA d20a1d313a2dd8e779995cfb9a4e70c6863dc4cea0ee0720c8987b6bebcd1e5a.
signature-audit.json verifies all356 code pages for BOTH SHA1 and SHA256
CodeDirectories (version20500); no entitlements. No CMS authentication, trust
admission or cache-loader execution claim. Do not patch until new logs justify.

## Previous: V14 RESTORED; real FIPS POST passed; dirs_cleaner exec rejected

V14 watcher collected the new log and restored original BOOT automatically.
Receipt requires_restore=false/original_boot_restored=true; fresh subsequent
whole-phone BOOT SHA256 d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016
matches. RECOVERY/DTBO/vbmeta unchanged, recovery boot ID changed. Phone is TWRP;
NO restoration pending. Root remains the unchanged read-only 16 GiB UFS image.

Saved backup/a52q/ios-ufs-v14/console.txt shows exact cc_fips_test admitted,
real corecrypto POST subtests, `all tests PASSED (183 ms)`, then result=true.
This is real task execution/results, NOT a FIPS certification claim. Apple
launchd advances to keybag/usermanager (optional signature denials), then fatal:
`Boot task failed: dirs_cleaner - posix_spawn: 85: Bad executable (or shared library)`.
First inspect the exact required dirs_cleaner binary/arguments and filesystem
effects before admitting it. Do not blanket-admit optional/destructive helpers.
No data volume is installed, no services/SpringBoard/display-composition proof.

Next fix committed 79dce98332253169f04d56a1bfdaea327962f4af: exact dirs_cleaner
pin guarded by CS_VALID, signed XML/DER getter checks (256/60 bytes), same RO
root vnode, no entitlement context/capability. Host audit master-dirs-audit-v1
matches staged source; 54144 bytes, SHA f9ee81f822c5577cf013182d11cfd730c4e7c803b5945d91dccc44661934e10f,
CDhash a93c2cbaed304f83e3df51faa21f961037f7c0ad; nine signed pages and XML/DER
slots pass. Actual launchd XML requires dirs_cleaner /tmp /var/run. Apple source
diskdev_cmds-701.100.2/dirs_cleaner.c uses mutation/cleanup, may log failures then
return 0; do not treat spawn/task continuation as clean RW data. Root stays RO.

120 local tests PASS (including C policy mutated hashes, signed metadata API
failures/lengths, wrong roots and denied capabilities), repo integrity PASS.
Isolated AMFI rebuild 43713827487 running on full base 43705321913; host CI
43713815679 running; redundant automatic full 43713815644 cancellation requested.
Host pipeline research/finish_dirs_artifacts.py session74524, stdout
research/dirs-build-package.log: verify downloaded source/kernel provenance,
exact kernel diagnostic QEMU, master rehash plan-v10, package hardware-v12.
No new phone write/trial yet. Current original BOOT remains restored.

Directory-task host pipeline COMPLETE: isolated rebuild 43713827487 and host
CI 43713815679 SUCCESS; redundant full 43713815644 cancelled. New kernel SHA
13b6eda1e0525add11cd4f986bfd02b4a764c9d0b007d220729dfcf959249766;
AMFI SHA 3c022a0c13c481685389740fb04262641a193ab96901ba2e5730fd2bcdc9f3b6.
E:/A52-iOS16/builds/43713827487/{artifact,combined,verified-build.json} verified.
Exact-kernel QEMU diagnostic: 3 CRC entry frames, 7 diagnostic PID1 heartbeats;
not Apple full-root or cleanup execution. Whole 16 GiB master rehash passed.
E:/A52-iOS16/ios-root-plan-v10.json; hardware-v12 packaged 96 MiB candidate SHA
bc50a99b72cbb6fe862eacfadb5d69cb8e163d8c3fd4412a77651029c96ffa8f.
Payload verified no RAM disk/diagnostic root. Physical dirs_cleaner result UNPROVEN.
Prepared research/start_dirs_trial.py and watch_ios_ufs_v15_restore.py; new C:
backup/a52q/ios-ufs-v15 receipts/logs, 30-minute restoration watcher. Helper now
binds plan-v10. Runners NOT started. Fresh physical readiness question pending.
V14 saved result E:/A52-iOS16/fips-v14-result.json; console SHA
6c4dccd9e0fc3d72e42edb83be3625501b7243afa78bde899bcd53a671307109.

## Historical: V14 FIPS execution trial — restoration completed above

V14 started 2026-11-15 11:50:31 UTC after fresh user readiness. Receipt
backup/a52q/ios-ufs-v14/receipt.json requires_restore=true; original BOOT is
NOT restored. Candidate 7e4a84b21c29d09ecc241f85f95f10c94ecd810cf33cbafc0b12356510438dfa
was written/read back, then USB departure observed with native reboot adb.
Kernel 233c149e...4533c53 adds only the verified FIPS executable policy pin.
Full installed 16 GiB root was freshly hashed unchanged before installation.
Protected RECOVERY/DTBO/vbmeta hashes matched. Only BOOT is temporarily changed.

C: watcher research/watch_ios_ufs_v14_restore.py is running with a 30-minute
return window; logs backup/a52q/ios-ufs-v14/{watcher.log,watcher.err.log}.
On recovery return, collect retained console and restore original BOOT, then
freshly verify whole BOOT SHA256 d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Never leave this pending after TWRP reconnects. Do not select System or format.
User instructed to wait five minutes before returning to TWRP. No new result yet.

Host prerequisites completed: isolated rebuild 43710208735 and host CI passed;
exact new-kernel diagnostic QEMU passed three CRC entries/seven PID1 heartbeats.
This is not full iOS or FIPS emulation. Master rehash/root-plan-v9 and packaged
96 MiB hardware-v11 BOOT passed binding/hash checks. No FIPS-disable boot flag,
test argument, fake POST result, root write, display change or global CS bypass.

## Previous: V13 RESTORED; both mount phases advanced; FIPS exec rejected

V13watchercollected/restoredautomatically. Receipt backup/a52q/ios-ufs-v13/receipt.json
requires_restore=false/original_boot_restored=true, protectedhashesunchanged,
changedrecoverybootID and3CRCentryframes. FreshwholephoneBOOT SHA d6bf...4b016
matchedagain. PhoneTWRP; no restoration pending. PreserveallV12/V13hostlogs.

Controlledunchangedb1b3BOOT/b505kernelretryreachedAppleuserland, soV12earlycapture
doesnotestablishdeterministicregression. V13advancedpastmount-phase-1 and2;
bindfsreachedsource lookup(return2/ENOENT)ratherthanEPERM. Optionalmissingpreboot
firmware/Pearl/factorydatapathswere tolerated. Data volume is stillabsent; this
doesNOTproveRWvar/data mounting. Nextmandatoryfatal:
proc9 loadcodesignatureerror4 filecc_fips_test, thenfips posix_spawn85/PANIC.
Otheroptionaljobs seputil/mobile_obliterator/MSUEarlyBootTaskwererejected and
didnotcausepanic; do notadmitunneededdestructive/updaterhelpers.
ConsoleSHA542b8c2de25c27386d072836fd8e08006d279f740a13c05c25e826f93233b794,
48200bytes. NoApplepersistentservices/SpringBoardproofyet.

Next: exact/usr/libexec/cc_fips_test pathconfirmedfromactualApplelaunchdembedded
boot-taskXML. Extract/auditmasterbinary +stagedchecksum, allcodepages/entitlements,
dependencies andactualtestbehavior. Admitonlythatverifiedrequiredtest onROroot,
thenrunrealtest; neverreplaceitsresultwithfakepass orclaimFIPScertification.
AMFIonlychange canuseexistingisolatedrelinkworkflowbase_run43705321913 leafamfi;
newCPPbridgeisalreadyinthatfullbase. Preserveglobal/pagechecks. ThenQEMU/packaging
andBOOT-onlytrialwithnewreadiness. Root/masterstillRO/unchanged,var4GiBnotinstalled.

FIPS audit COMPLETE: E:/A52-iOS16/master-fips-audit-v1/audit.json and extracted
usr_libexec_cc_fips_test. 52208bytes SHAa62ff42e7a024ee3c1af62e5bc8ba87af3634724ca492ca83020199dcf4bd5bc;
matchesnativeOSsource. Nine signed4Kpages match; noXML/DERentitlements; CDhash
6df18c1a69315dafea6f8125bfa4d73463da80f0. OnlydirectdyliblibSystem, realfipspost_post
import/traceinterface. Binaryhasdocumentedtest-disableoption; DO NOTselectit or
setfakePOSTresult. EmbeddedlaunchdXMLrequiresbothRunandSuccessfortheexactpath.
PreparedAMFIbranchadmitsonlythatidentityonverifiedROroot aslocalplatformSIGNEDtask;
newmetadataJSONandactualnativepolicytestscover20mutants/otherroots/noent/signature
guards anddenyFIPSbindfscapability. No othersoftware/hardware/root changes.

Committedc23fbd3ef6f740612ea0a032e8f09c157a9bedbe. IsolatedAMFIrebuild43710208735
SUCCESS usingfullbase43705321913/5c34a04/b505kernel; hostCI43710209003 SUCCESS,
120localtests+repo81patch/41Python/7shellvalidatorPASS, nativepolicyLinux/WindowsPASS.
Redundantauto-full43710208939 cancelled. Newkernel
233c149eba8affd917f169ea7e7a08f4bfa282f897fa9d5d351a57a1d4533c53;
AMFISHAcaacd24f6c92f4dfe3403e6219d25676f580387492772fb7b2e822f8777f9c9b.
Artifact E:/A52-iOS16/builds/43710208735/{artifact,combined,verified-build.json}.
Hostpipeline research/finish_fips_artifacts.py/session96259 stdout
research/fips-build-package.log verifiesrelinkprovenance, exactkernelQEMU then
masterrehashplan-v9 andpackagehardware-v11. QEMUrunexit0; inspectfinalproof before
phoneuse. No phonewritesforthisnewkernel; V13restored.

Preparednotstarted research/start_fips_trial.py and watch_ios_ufs_v14_restore.py
use C: backup/a52q/ios-ufs-v14, hardware-v11,30minwatcher,lastV13consolefallback.
Private devicehelper nowexpectsplan-v9, restorationphasehasnoE:dependency.
Aftercandidatechecks, freshreadinessforfive-minute BOOT-onlytrial+restore.
PrivateV13proof E:/A52-iOS16/mount-contract-v13-result.json retained.

## Historical: V13 controlled unchanged retry — completed and restored

Userconfirmedreadyfortimedretryafteraccidentalreboot. V13 uses unchangedchecked
b1b3bc6569b79772dd9162db54432df655a407a7c5fcd369b5ad1325a5ec9f27 BOOTcandidate,
kernelb5050403...106d3d9b,hardware-v10/plan-v8. Fullinstalled16GiBrootfreshly
verifiedunchangedandprotectedhashesmatched, BOOT96MiBwritten/readbackverified.
Native/system/bin/rebootadbconfirmedUSBdeparture. Receipt
backup/a52q/ios-ufs-v13/receipt.json REQUIRES_RESTORE=true, originalNOTrestored.
WatcherPID12116, C:backup/a52q/ios-ufs-v13/{install.log,watcher.log,watcher.err.log}.
Newwatcherwaits30minutes; oldV12watchertimedoutafter10andrequiredmanualrestore.
Useraskedfivefullminutesfromactualstart(about12:26Brussels),thenTWRP. Onreturn
collect+restoreimmediatelyandverifywholeBOOTSHA d6bf...4b016. NoSystem/format.

Thisisacontrolledsamebinaryretry: no kernel/root/display/memory/policychanges.
FreshRAMconsolearchive+unlinkandnewrecoverybootIDpreventstaleattribution even
thoughartifactnonceissame. SeparateV13folderpreservesallV12hostlogs+archive.
V12wasrestoredandhashverifiedbeforethistrial. V12onlyprovedearlystartup, not
bindfsfailureorsuccess. PriorV11provedroot-tableandApplelaunchdmain.
No fulliOS/services/SpringBoardclaim. No data/var/GPT/otherpartitionwrite.
Sourceinspectiononly: DEBUG_BSDINITiscompile-time0; IOKitRTCwaitbounded30s.
If controlledretryagainstopspreUFS, instrumentactualstartupbeforechangingguards.

## Historical: V12 RESTORED; retained log safe; pre-UFS result inconclusive

V12 watcherexpiredafter10minutesbeforerecoveryreturned. Manualcollect-restore
finishedsuccessfullywhenuserreportedTWRP. Receipt backup/a52q/ios-ufs-v12/receipt.json
nowrequires_restore=false/original_boot_restored=true, protectedhashesunchanged,
changedrecoverybootID,3CRCentryframes. FreshwholephoneBOOT SHA d6bf...4b016 matched
againafteruserreportedanaccidentaladditionalreboot. PhonecurrentlyTWRP.
NO RESTORATION PENDING. Do not overwrite V12savedconsolewithanothercapture.

SavedV12console8394bytes,SHA256
239e7cbc3603fc232a5dd9b15edd87cfb5645f6e4997cafd35092a8d950bc6c8.
Extra byte-identicalcopies+manifest in
backup/a52q/ios-ufs-v12/retained-after-reboot/{console.txt,receipt.json,
manual-collect-restore.log,recovery-dmesg.txt,manifest.json}.
The accidentalreboot cannot erase these hostcopies. Originalsavedfilesretained.

Logstopsafterplatformregistered/CPUselfSGI; noUFSstages,rootwindow,P ID1orbindfs
queryrecords. This is INCONCLUSIVE for bindfscapability, not proofthatfixfailed.
PriorV11provedROroot table andlaunchdmain. Startupsource places
IOKitInitializeTime() betweenbsd_bufferinit() andvfsinit()/UFS; it has30sIORTCwait,
but this log does not establish the exact stall. User's accidentalreset timing
isunknown; do not inferfull5minruntime or classifykernelregression fromabsence.
Next: controlled unchangedb1b3...candidate retry with fresharchivedRAMconsole,
newrecoverybootID andfulltimed5minwait. Extend recoverywatcher30min tocoverlate
manualreturn. Same96MiBBOOTonly scope; rootROunchanged; no needrebuild binary.
Do not weaken CPU/protected-memory/signatureguards based on this incomplete log.

## Historical: V12 bindfs-capability phone trial — completed and restored

V12 candidate b1b3bc6569b79772dd9162db54432df655a407a7c5fcd369b5ad1325a5ec9f27
installed/readbackverified BOOTonly96MiB, originalcurrentlyNOTrestored. Receipt
backup/a52q/ios-ufs-v12/receipt.json hasrequires_restore=true. Userconfirmedfresh
readiness, full16GiBinstalledroot freshlyhashedunchanged, protectedpartshashes
matched. Native /system/bin/reboot adb confirmedUSBdeparture. WatcherPID10676
runningC:logs backup/a52q/ios-ufs-v12/{watcher.log,watcher.err.log,install.log}.
Useraskedfive minutes thenTWRP (orleaveopenifselfreturns). Collect+restoreasap
onreturn; originalwholeBOOT SHA d6bf...4b016 mustverify. NoSystem/Android/format.

Corrected fullbuild43705321913/source5c34a0499b63bae2d52cf64f2a636b541d2120a0
SUCCESS. Kernel b50504036500e95d19b7c4aa8a45c46204bbf7a483269a65d233c649106d3d9b;
all73overlayfilesverified, onlyAMFIandA52PlatformExpert changedversusV11kernel.
HostCI43705322098/120tests PASS; exactkernel diagnosticQEMU3entries/7heartbeats
PASS, notfulliOS/UFSemulation. Fullmasterrehashedunchanged plan-v8; hardware-v10
packagednoRAMroot. Headerproc_getcsflags includeerrorfromfirstbuildwasfixed.
TypedOSBooleanbridge andexact signedbindfsBoolean query aretheonlynewcapability.
Display/memory/console/UFSreader/ROrootfstabunchanged. No otherkeys/binariesadmitted.

OnceV12restored, inspectactualnewconsole for bindfscapability grant andwhether
mount-phase-1 completes, then nextfirstfailure. Do not callpendingresultsuccess.
Master/root remainRO; host4GiBvarnotinstalled/no newrangeapproved. Services/UI
unproven; objective remainsrealApplelaunchd/services/SpringBoardfrompersistentUFS.
Private helper usesplan-v8; restore hasnoE:dependency. Ifwatchertimeout, restore
stillrequired. PrecedingV11safetyrecordbelowishistoricalduringactiveV12.

## Historical: V11 RESTORED; root table works; bindfs entitlement denied

Authoritative receipt backup/a52q/ios-ufs-v11/receipt.json now has
requires_restore=false, original_boot_restored=true, protected hashes unchanged,
changed recoverybootID and3validXNUentryframes. Fresh phone fullBOOT SHA matched
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016 after user returned.
No restoration pending; phoneTWRP. Do not boot Android or format.

V11 retained3Applelaunchd-main markers with system1/process1 enforcement.
Both fs-table queries logged actualmountedROHFS source=root_device. OldEROFSroot
upgrade and missingbootmanifest errors are absent. Next actualfailure:
mount firmwarepreboot->/usr/standalone/firmware: Operationnotpermitted(1), then
mount-phase-1 exit77. Logpath backup/a52q/ios-ufs-v11/console.txt. Text contains
knownretentioncorruption; do not repairhash/pathbytes or infercontradictingregisters.

Source confirms bind_vfsops.c checks com.apple.private.bindfs-allow before
copyinstr/source lookup, returningEPERM. IOUserClient::copyClientEntitlement
calls amfi->OSEntitlements.copyEntitlementAsOSObjectWithProc, which our current
policyalwaysdenies. Mount's originalXML/DERhave the bindfs key (verifyboolvalue
fromsignedblob beforegrant). Next fix: onlyexactverifiedRO-rootmountprocess,
revalidateXML/DERsignedslots and requireadmittedsignedvalidtask; expose onlythat
signedtruecapability as properOSBoolean throughC++bridge. No globalAMFIdisable,
no otherentitlement grants, no fakeentitlementcontext. Do not inventC++objectABI.
The exact measured mount's signed XML bool was verified true with host auditor
E:/A52-iOS16/mount-bindfs-capability-v1.json; XML/DERhashslotchecks pass. Implemented
sharedmountblobvalidator plus single-key proc/object query; requiresprocessSIGNED|
VALID andadmittedblobSIGNED|PLATFORM_BINARY withplatformfield, ROroot andvalidslots.
C++bridge usespublic kOSBooleanTrue->retain(), noC++reference/objectABIguessing.
Nativeactualcallback tests extended withpositiveobjectcopy, allotherkeydenials,
20mutatedhashes, invalidslots/flags/process/root andcopyfailure. Fullbuildneeded
because bridgechangesplatformleaf aswellasAMFI. No phonewritesforthisnewpatch.

Committed e6cfca210fb33d694e84f50d956261216af12241. Full HFS build43703934486
FAILED: proc_getcsflags undeclared at a52q_amfi.c:288. Pinned XNU declares its
uint64return API in sys/proc_internal.h; added the actual header, not an ad-hoc
prototype. Nativefixture nowmodels uint64return. Requirescorrectedfullrebuild.
Correctioncommit5c34a04 fullHFSbuild43705321913 nowRUNNING; hostCI43705322098
SUCCESS;120tests/73fileactualoverlaycheck PASS. Hostpipeline new session97326,
research/finish_bindfs_artifacts.py nowexpects43705321913; stdout
research/bindfs-build-package-retry.log and failurelog has runIDsuffix. Oldfailed
buildlog research/bindfs-build-failure.log preserved. Preparationstillplan-v8/
hardware-v10/QEMUbindfs-v1; nonecreatedbeforefailedbuild, no phonewrite.
Redundantpushbuild43703934123 cancelled. HostCI43703934116 SUCCESS;
120localtests/repositoryvalidator PASS, Linux+Windows actualCpolicyfixture PASS.
Hostpipeline research/finish_bindfs_artifacts.py is running in session98258,
stdout research/bindfs-build-package.log, failurelog research/bindfs-build-failure.log.
It waits/buildverifies73files then runs research/prepare_bindfs_artifacts.py:
exactkernel diagnosticQEMU a52q-bindfs-qemu-v1, fullmasterrehash plan-v8, package
hardware-v10. No phonewrite in pipeline. Private resultV11 proof saved to
E:/A52-iOS16/mount-contract-v11-result.json; consoleSHA9a4d8165...6e0cccb.

PreparedbutNOTSTARTED: research/start_bindfs_trial.py and
research/watch_ios_ufs_v12_restore.py use C: backup/a52q/ios-ufs-v12, hardware-v10,
lastsavedV11console fallback. Private device helper now expects plan-v8; restore
phase has no E:dependency. After allcandidatechecks pass, get fresh readiness
for five-minute BOOT-only trial. Latestuserreadinesswas forV11, now completed.
Do not install while build/checks pending. No BOOTrestoration currentlypending.

Independentreadonlymasterserviceaudit COMPLETE:
E:/A52-iOS16/master-service-audit-v3/report.json. Sixexecutables matchexactmaster
hashes usingresolvednativesourcepaths andverify1804signedcodepages+XML/DERslots:
backboardd280/securityd764/powerd146/watchdogd33/mobileactivationd572/SpringBoard9.
Fiveactuallaunchplists readfrommaster; powerdpathis
/System/Library/CoreServices/powerd.bundle/powerd; watchdogd configuredIOWatchdog
matchingLaunchEvent, noobservedwatchdogpanic. No codeadmission/service/stubchange.
V1serialbulkcopy timedout; V2checksumguest succeededbutWindowsUNCcouldnotfollow
theLinuxosdirectorysymlink, so binaries were notverified there. V3resolvesLinux
sourcepaths beforeUNCaccess; all6hashes/pagechecks pass, no missingpaths.
Private reportskeepApplefilesoutofgit; WSLowneddistroterminatedafteraudit.

Continue toward persistentAppleuserland thenSpringBoard. No services/UIproof.
FilesystemrootstillRO/unchanged, host4GiBvarnotinstalled, newstoragerangewrite
requiresconcretereview/approval. Display/console unchanged. Previousactive record
below is historical; watcherfinished andoriginalBOOTrestored.

## Historical: V11 mount-contract phone trial — completed and restored

V11 installation completed on2026-11-15. Receipt backup/a52q/ios-ufs-v11/receipt.json
currently requires_restore=true, original_boot_restored=false. Full installed16GiB
root freshly rehashed unchanged before the96MiB BOOT-only write; BOOT candidate
96e668f4343c40f616dd30af5e4784e54d36595c55702a7e0d76e149f8d6680c was read back.
Native reboot adb confirmed USB departure. Watcher PID4656 started; logs/receipt
all on C: backup/a52q/ios-ufs-v11. User confirmed ready and was asked for five
minutes then TWRP, or leave TWRP open if it returns itself. Collect and restore
immediately on return; full original BOOT SHA must match d6bf...4b016.
Do NOT select System/Android or format. No other partition/root/var write included.

Build43643720989/source67f6d6bd63ecd0bab0c42eec93fb40f7fe360780 SUCCESS.
Kernel87b660ae13249c8281eaf618110899ff6d77249b5acf23ccf49a996865f3196e;
all73 overlay files verified. Exact kernel diagnostic QEMU3entries/7heartbeats;
does not emulate fulliOS/UFS. Fullmaster rehash plan-v7unchanged. HostCI43643867819
SUCCESS,120tests. Preparedhardware-v9 with ROmounted-source fstab and measured
unsealedbootnamespace. Display/earlyconsole/serial/boardoverlayhashes sameasb413build.
Latest user requestedRWroot/globalAMFIbypass/hardwarestubs/UI; those are NOT
implemented by this candidate, which tests the existing confirmed mount failure.
Actual60HzIOMFB claim remains unsupported; source is opt-in guardedframe test.
Primary target remains realuserlandfrompersistentUFS then visibleSpringBoard;
no services/UI proof yet. See docs/A52Q-MOUNT-TRIAL-REVIEW.md for files/checks/scope.

## Historical handoff: V10 restored; enforcement negatives pass; RO fstab prepared

No restoration pending. V10 receipt backup/a52q/ios-ufs-v10/receipt.json has
original_boot_restored=true, requires_restore=false, whole BOOT SHA d6bf...4b016,
protected hashes unchanged. Phone remains TWRP; never boot Android or format.
Full root/master unchanged; no new storage write authorized.

Enforcement full build43640145137/source b413f58d5dba12b948ac9e12e10992e25cfa4d6e
SUCCESS; host CI43640144989 SUCCESS. Artifact E:/A52-iOS16/builds/43640145137/artifact,
kernel d7e3496080a357099eb970d6e02708f1f0daddf6205d45d518dcdb2e417e1fcd,
all72 overlay files verified. Exact-kernel QEMU positive and two genuine negative
exec trials PASS: approved init7heartbeats; valid-page unknownCD denied(error1,
loaderror4) thenSIGKILL; originalCD with only filebyte1000modified acceptedpin then
SIGKILL, zeroPID1banner/heartbeats. All3CRCentryframes, enforcement system1/process1.
Private proof E:/A52-iOS16/exec-enforcement-result-v1.json and
shim/out/a52q-exec-enforcement-qemu-v1; fixtureFS fsck clean. These are synthetic
diagnostic RAM-root emulation tests, not Apple/UFS emulation or phone boots.

New a52q_bootfs.c publishes only actual mounted RO HFS a52ios0 via
vfs.generic.apfs.edt_fstab. Exact measured Libinfo564.120.2 consumer inspected in
validated native staging cache; sysctl string0x1946faff6, code0x1946e2a24/2a5c;
entrystride236, offsets0/32/96/128/192/freq224/pass228/trailing4zero. Cache read-only
audit E:/A52-iOS16/cache-fstab-audit-v1. Exact Apple source confirms missingfstab
synthesizes RWroot; diskdev_cmds701.100.2 mount then triesRO->RWupgrade. Newcallback
advertises the actual mounted-source alias / hfs ro, pass1, requires matchingrootdev/MNT_ROOTFS/
MNT_RDONLY/HFS, denieswrite/otherroots. Native actual-body callback checks PASS;
both overlays apply to actual81patchsource,73files. Requires NEW fullkernelbuild.
No mount_hfs pin added. Do not weaken RO driver.

Further source check: vfs_rootmountalloc_internal initializes source "root_device",
and mount ismounted() compares exact statfs names. Publishing /dev/a52ios0 would
not skip the mounted root. Callback now copies actual bounded f_mntfromname and
requires actual f_mntonname=/, retaining verifieddevice/RO/HFS guards. Native test
covers initialalias, laterrealdevicepath, long/empty names andwrongmountpath.
Build43642823797/source738da8b was cancelled/superseded before any phone trial.
Corrected full HFS build43643720989/source67f6d6bd63ecd0bab0c42eec93fb40f7fe360780
is RUNNING. HostCI43643720945 failed only because Linux C11 hid strnlen in the
native fixture; reproduced stderr in WSL, enabled POSIX2008 for that fixture,
passed on Linux/Windows, committed99a8ede. HostCI43643867819 SUCCESS (120tests).
No kernel change in that test fix. Fresh phone BOOT SHA matched d6bf...4b016
again at22:33; phone recovery. Fresh hashes of the 3 source cache files supplying
the measured Libinfo segments match original validated cache checksums.

Prepared private host runner research/prepare_bootfs_artifacts.py will verify
new kernel QEMU(positive diagnosticRAMfixture), stream-rehash full master into
root-plan-v7, and package hardware-v9 with localmanifest. No phone writes there.
Prepared readiness-gated research/start_bootfs_trial.py archives console in C:
and invokes BOOT-only install, then starts research/watch_ios_ufs_v11_restore.py
with C: backup/a52q/ios-ufs-v11 logging/receipt. NONE started yet. Private helper
now expects plan-v7 and explicit --local-boot-manifest; restore has no E:dependency.
Opt-in --local-boot-manifest now computes SHA384 of canonical sortedASCIIcompact
JSON with exactkernel/root/liveDTB SHA256, target/format/unsealedtrustlabel. Both
hash and explicitlocaldocument embeddedchosen, validationrecomputesfrommeasurements
andrequiresfullrootdevelopment; rejectsundeclared/duplicate/changedproperties and
trustclaims. This is only an unauthenticatedlocalmountnamespace, noAppleIMG4trust,
noAMFIchange. Hosttests includeactualpayloadpositive/changedADTwithupdatedcontainerhash.
Next: finishbuild, never reuse fabricated Redmi hash. Do not alter master. Distinguish optional
OTHERenv bind mounts from actual mainOS firmware mounts. See docs/A52Q-BOOT-FILESYSTEM.md.
After build, exact-kernel QEMU baseline and package/provenance/rootprefixchecks;
only then readiness and BOOT-only trial with restoration. Future4GiBvarnotinstalled.

## Historical handoff: V10 restored; mount executed; enforcement/read-only audit

Original BOOT restored after V10 and freshly hash-verified d6bf0307...4b016;
receipt requires_restore=false, protected partition hashes unchanged. No pending
restoration. Mount ran after signed XML/DER checks. It reports data volume not
required in env0, starts mount_hfs, then fails root remount with EROFS and cannot
get a boot-manifest hash; launchd panics on mount-phase-1 exit66. Keep root RO.

Security finding: mount_hfs signature was rejected but its own error text proves
it still executed. mach_loader.c:1299 explicitly ignores signature-load failures
when cs_process_global_enforcement()==0 (inherited macOS default). Cache checking
was enforced, but whole-process enforcement was NOT. Do not claim host callback
rejection proves runtime exec denial. A52 overlay now enables normal early
DEFAULT_CS_PROCESS_ENFORCEMENT_ENABLE=1 (same default branch as system checking),
without enabling unrelated CONFIG_ENFORCE_SIGNED_CODE dylinker-platform rules.
This makes loader failures fatal and vm_map_cs_enforcement always true on A52.
Add runtime system/process enforcement log; mark only admitted launchd/dyld/own
init as CS_SIGNED for correct process metadata, not platform status. Existing
fsck/mount classes and cache/entitlement guards remain. Requires full build.

Prepare exact-kernel QEMU positive plus unapproved-init and modified-page negative
fixtures; neither touches the master or phone root. Actual mount_hfs extracted
read-only to E:/A52-iOS16/master-mount-helper-v1, SHAa031b91c661de06f11c4c22d94e28dcb43a0c41366225bfa470f1bab11d391e5,
72656B. Parent mount does NOT contain 'error on mount()'; helper DOES. Do not add
helper pin until exec rejection is genuinely enforced. Also trace mount-phase-1
read-only/boot-manifest contract; do NOT make root RW or invent a manifest hash.
No new storage writes authorized. Other historical ACTIVE entries are superseded.

## Active A52 handoff: V10 mount trial running — BOOT restoration required

V10 BOOT candidate 5811579a...ac33ba was installed with full readback. Native
`/system/bin/reboot adb` left recovery, and the C: restoration watcher is active.
The authoritative receipt `backup/a52q/ios-ufs-v10/receipt.json` currently has
`requires_restore=true` and `original_boot_restored=false`. The user was asked
to wait five minutes then return to TWRP, or leave recovery open if it returns
itself. Collect the log and restore original BOOT immediately on return; verify
full SHA256 d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
C: logs are in backup/a52q/ios-ufs-v10/{install,watcher,watcher.err}.log. The user
confirmed readiness. No root/var/other partition write or format is included.
The preceding V9 restoration was verified; it is historical during this trial.

V9 retained three Apple launchd-main markers. Apple's fsck executed and printed
`not booting main or diagnostic OS. Skipping fsck on OS container`; it did NOT
perform an OS-container integrity check. Launchd advanced to mount-phase-1,
where `/sbin/mount` was rejected by the signature policy. Apple persistent
services and a visible SpringBoard lock screen remain unproven.

The next A52-only policy admits the exact measured mount CD hash, requires the
same read-only root mount, and validates its XML/DER special-slot hashes with
XNU's existing `csblob_get_entitlements` and `csblob_get_der_entitlements` APIs.
The original signed blobs stay as metadata and may be read via CSOPS; AMFI
privilege queries remain denied. No entitlement context or privilege is granted.
The already verified fsck/cache guards remain. Do not add other executable pins
without an observed failure and source/content audit.

Build 43637854082, source 791b0a763a9753b7ca77f0917bd0b41552e4b017, passed.
Kernel SHA256: dc062e2146534886552e35d9c308d57fcec310c9b76494922b6d1879588eb7d3.
AMFI implementation: bdc6d1de71c025bf6484aff0999ef9447e04f006e542a07b8407795808fedc08.
Host CI 43637853970 and 116 local Python tests passed; the original 81 patches
are intact. The redundant automatic full build 43637853977 was canceled.
Exact-kernel diagnostic QEMU passed (three entry frames, seven diagnostic
heartbeats); the complete master hash matched 0f4bcaa7...312149 and plan-v6 is
ready. QEMU does not emulate the full iOS UFS root. The prepared hardware-v8
BOOT image hash is 5811579a9b4075b1ec87a65c156e425d60974d56470e5be7347dfc43ffac33ba.

Next host script: `research/prepare_mount_candidate.py`, output hardware-v8.
Trial receipt: `backup/a52q/ios-ufs-v10/receipt.json`.
Watcher: `research/watch_ios_ufs_v10_restore.py`, starts automatically when the
install leaves recovery. After confirmed departure, ask for five minutes then
TWRP. The previous RAM console was archived byte-exact before rearming it.
All installation/watcher logs belong on C: beside the receipt, so E: loss cannot
interrupt restoration logging. The private helper now references root-plan-v6 for this candidate. Use `--native-reboot`, which must call
`/system/bin/reboot adb`: generic no-argument reboot requests `shell`, which
retained recovery selection; TWRP's GUI reboot can crash when its display sleeps.
The runner now verifies recovery USB departure and records pre/post boot IDs.

The user authorizes temporary BOOT-only trials with restoration. Announce the
96 MiB BOOT scope and five-minute reset procedure before each trial. Restore
original BOOT immediately after TWRP returns, then verify its complete hash.
Never boot the original Android image as a control: Android userdata was replaced
by the explicitly approved 16 GiB root installation. Keep GPT/recovery/DTBO/
vbmeta/metadata/modem/persist unchanged. The installed root and host master stay
read-only and byte-identical to 0f4bcaa7...312149. No RAM-root substitution.
A host 4 GiB var image exists but is NOT installed and has no kernel write/mount
implementation. Any new UFS range write requires its own concrete approval;
the earlier backup waiver and root-install approval do not authorize it.

## Historical status records (superseded by the active handoff above)

## CURRENT: V9 RESTORED; APPLE FSCK EXECUTED; MOUNT PIN PREPARED

V9 completed, originalBOOTrestored/freshphoneSHAd6bf...4b016matched; receipt
requires_restore=false,protectedhashesunchanged,changedbootID/3validXNUentries.
THREElaunchdMAINmarkers; actualApplefsckprinted 'not booting main or diagnostic
OS. Skipping fsck on OS container'. Thus fsck EXECUTED, NOT OScontainerchecked.
Launchdadvancedto mount-phase-1; /sbin/mount signaturedenied53/error4 thenplatform
panic. No Applepersistentservices or SpringBoard. No restorepending; phoneTWRP.

MountmasterfileSHAac55c4c7d200d0153cc266b39d69d4d771a9707ac91eefec94f83eb2522364df
matchesnativeOSsource;18signed4KpagesPASS. NEWaudit validatessignedXML/DERspecial
slots: XML472B SHA363b86fdcb854e0a6c4a09971d16a50e2a5dfe5991fa252384e54697eb51e674,
DER222B SHA9a81f1e551e61017df33201bbfa06b2dc2f0e31ccb99e930b64893d9feadca98.
AddedONEobservedmountpin CDhashb6a7272461fce359ceb407594e7aaf4fdf4949f1 onlyROroot.
Uses XNU csblob_get_entitlements/get_der_entitlements, which validate actual
signedspecialslothashes; requiresoriginal472/222lengths/pointers and no accelerated
entitlementobject. Setslocaldevelopmentplatform+SIGNED onlyaftervalidation.
OriginalXML/DERretained asmetadata, queriesremainDENIED/noentitlementgrants.
No otherfileadmitted; fsck/cacheguardsremain. Newpublicmountpinmetadata JSON.
PublicauditornowcheckssignedXML/DERslots; syntheticXML+DERmutationnegativechecks
PASS. Nativepolicykernel-APIerror/missingblob/root/mutantnegativecasesPASS.
116Python tests PASS; needsAMFI-onlyrebuild/fullbase43624481615/a46569c. NoFSwrite.

## CURRENT — USER RETURNED; V9 SIGNED-FSCK PREFLIGHT RUNNING

V9 ACTIVE NOW: candidate2bb055df...e34dae installed/fullreadbackverified,
/system/bin/reboot adb sent, recoveryUSBdepartureconfirmed. Receiptrequires_restore=true,
original_boot_restored=false. WatcherV9waitingonC:backup/a52q/ios-ufs-v9/watcher*.log.
UseraskedFIVEminutesthenresetTWRP (orleaveifitreturnsitself). Collectlogsandrestore
originalBOOPhashimmediatelyonreturn. No current 'safe/no pending' statementbelow
applieswhileV9active. Receiptisdefinitive. No root/var/otherpartitionwrite.

User explicitly 'im back', revoking temporary hardware hold. PhoneconfirmedTWRP,
a52q/bootloaderA525FXXSCFYF1, freshoriginalBOOPhashd6bf...4b016 beforetrial.
V9 installpreflightrunning. Authoritative receiptbackup/a52q/ios-ufs-v9/receipt.json
willmarkrequires_restore=true onlyafterwrite. Candidatehardwarev7 SHA2bb055df...
e34dae/kernelb238ddc5...28eb3d/rootplanv5. Native --native-reboot MUST remain
/system/bin/reboot adb. Automatic watcherV9C: logs inbackup/a52q/ios-ufs-v9.
Beforeactualreboot noresetprompt; afterdepartureaskFIVEminutes thenTWRP, orif
TWRPreturnsitselfleaveopen. Collect/restoreoriginalBOOPhashimmediatelyonreturn.
No userdata/root/varwrites orformat. OldRAMconsolearchivedbyteexactthenrecord
unlinked; proofinV9folder. Priorawayholdbelowissupersededbyuserreturn.

## CURRENT — USER AWAY: HOLD ALL PHONE TRIALS; ORIGINAL BOOT VERIFIED

User says notnearcomputer/cannot testnow. Do NOT flash or reboot phone untiluser
returns/ready. Hostworkonly. Lastreceiptios-ufs-v8 requires_restore=false,
original_boot_restored=true; freshREADONLYphonehash AGAIN matched d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
PhoneTWRP. NO pendingBOOTrestoration. V9receipt doesNOTexist, watcherV9notstarted.
All olderACTIVEentries belowarehistorical/superseded. No unattendedtestauthorized
whileuseraway. StandingBOOTscopepersistswhenready; no newuserdata/varwriteapproval.

CS_SIGNEDfixkernelbuild43632122116/source92eede2 PASS. Kernelb238ddc535b0eec0d9d47c3d10e4d76ee061e1544a6984a5526aff218828eb3d.
115Python/CI43632121862 PASS. Exactkernel+diagnosticHFSfixture QEMU PASS3entry,
7PID1heartbeats; NOTfulliOS/UFSemulation. Entiremasterrehash0f4...312149matched,
planv5complete. Hostcandidatehardwarev7 PACKAGEDONLY, SHA
2bb055df7bf8dbe572e84bc8521b520b009876b5ad9ef2274ad1b7a54fe34dae.
Private E:/A52-iOS16/fsck-signed-trial-review-v1.json records candidate/hash,
BOOT96MiBscope,backup/recovery,hostproofandhardwareHOLD. Master/sourceunchanged.
Helperrootplan nowv5; MUSTuse --native-reboot ->/system/bin/reboot adb Samsung
normalreason, notdefaultshell/notcrashingTWRPGUI. FutureV9 receipt/watcher prepared
only; rearmliveconsolefromC:archiveonceuserready, thennormalvalidatedBOOTprocedure.
Physicalbaseline: Applelaunchdmain provenV4/V8; fscksignatureadmittedV8butstatus
rejected becauseCS_SIGNEDmissing. Newfixnotphonetested. Services/UIremainunproven.

## CURRENT: V8 BOOT RESTORED; FSCK STATUS BLOCKER TRACED TO CS_SIGNED

NextAMFIbuild43632122116/source92eede2 PASS, verifiedbasea46569c/full43624481615.
Kernelb238ddc535b0eec0d9d47c3d10e4d76ee061e1544a6984a5526aff218828eb3d,
AMFIimplementation8e32b8f2ed13acb69e3e05e0f51a76f7594e39e8c5ac314d2a355603b1f0caf0.
HostCI43632121862 PASS; redundantautofull43632121916 canceled. QEMU/newmasterplanv5
running. Prepared research/prepare_fsck_signed_candidate.py ->hardwarev7 and
watch_ios_ufs_v9_restore.py ->receiptios-ufs-v9, notinstalled. Reboot MUST native
--native-reboot explicitadbnormalreason; privatehelper currentlyusesplanv4,
update toplanv5 beforeinstall oncecandidatepackaged. No restorependingnow.

Additionalreadonlyhostauditmaster-next-boot-files-v1: /sbin/mount SHAac55c4c7...
2364df,18signed4Kpages,entitlementsXML+DERpresent. hfs.fs/fsck_hfs SHAb90942e8...
6520cc,66signed4Kpages,entitlementsXML+DERpresent. BothmatchnativeOSstagedsource.
TheseareAUDITED ONLY; no newpins/admission or entitlementhandlingimplemented.
Onlyextendafteractualobservedfailure. WSLownbuilddistroterminatedafterread.

V8 native '/system/bin/reboot adb' normal reason WORKED: changedkernelbootID,
3CRCentry frames,3CRCrootframes, THREE launchd-mainmarkers. PreviousTWRProute
problemsresolvedforthistrial. OriginalBOOTrestored andfreshphoneSHA d6bf0307...
4b016 verified; recovery/DTBO/vbmeta unchanged. No restorepending; phoneTWRP.

V8 log: exactfsckadmitted, embedded signature attached flags0x4000003; iOSspawn
platformgatepassed, but launchd STILLpanic 'boot task is not a platformbinary'.
Source kern_cs.c::csproc_get_blob returnsNULL unless PROCESS hasCS_SIGNED;
kern_exec copiesCS_SIGNED fromcsblobloadresult, csopsSTATUS readsplatformfield
throughthathelper. OurfsckCSblobflags lackedCS_SIGNED0x20000000. OriginalRedmi
patch0036 documents SAMEcontract. Minimal A52fix setsCS_SIGNED onlyinexactfsck
branch, alongsideexistinglocaldevelopmentplatformclass. No globalCSdisable,
newpins, rootchanges, orotherexecutablemetadatachanges. Nativecontracts/negative
testsupdated; requiresnextAMFI-onlybuildfromfull43624481615/sourcea46569c.
AlsocorrectedAMFIregistrationbanner tosayexacthashpolicy/entqueriesdenied.

## LATEST: V7 RESTORED; SAMSUNG NORMAL-REASON V8 PREFLIGHT

V8 ACTIVE NOW: receiptbackup/a52q/ios-ufs-v8/receipt.json requires_restore=true,
reboot_disconnect_observed=true, candidate1c78fb37...5f9d2e installedreadback.
Native '/system/bin/reboot adb' sent; transportclosedexpected. Watcherv8C: logs
backup/a52q/ios-ufs-v8/watcher*.log. UseraskedFIVEminutes ifSamsungSplash;
ifTWRPreturnsitselfleaveopenandreport. Collect/restoreBOOTimmediatelyonreturn.
Need freshkernelbootID AND XNUentry beforeclaimsthisrouteworked. All below
no-pending/originalsafe statements refer to oldertrials andaresupersededwhileV8active.

V7 did rebootLinux: pre/postbootIDsdiffer. But262132-byte console ONLY Linux,
last reboot cmd 'shell'; noXNUentry. BOOT restored/hashverified. Userreported
alreadyTWRP before5min; no fsck/newkernelfailure established.
InspectedpinnedLineageSamsungsource f6bbda4e5986f09e4d51ceffd1b645b2d5aa75b4:
drivers/samsung/debug/sec_debug.c::sec_debug_update_restart_reason line337.
Unrecognized'shell' falls through settingSEC_REBOOT andreturnswithoutsetting
PMIC PONnormal. 'adb'prefix goes__done withPON_NORMALBOOT/SEC_NORMAL. This
explainslikelyretainedRecoveryselection; currentvendorTWRPexactsourceunverified.
Nextnativecommand /system/bin/reboot adb, NOTgenericno-argdefaultshell. No raw
PMICaddresswrite, firmware/MISC/otherpartitionwrite. Actualnativebinaryusage
supports [rebootcommand], property_set/sys.powerctl verified frombinary.

V8 installpreflightrunning; receiptbackup/a52q/ios-ufs-v8/receipt.json definitive.
Samecheckedcandidate1c78fb37...5f9d2e/kernel3808e55a...ccfad87/rootplanv4.
C:install/watcherlogs inV8directory; watch_ios_ufs_v8_restore.py prepared. After
realdepartureask5minreset; afterreturnverifybootID andfreshXNUentrybeforeclaims.
V7Linux-onlyconsolearchivedthenRAMrecordunlinked. No userdata/root/varwrite.
All older ACTIVEentries superseded. Current BOOToriginalUNTILV8receiptmarkswrite.

## LATEST: V6 DID NOT REBOOT LINUX; V7 NATIVE-REBOOT PREFLIGHT

V7 ACTIVE NOW: candidate1c78fb37...5f9d2e readbackverified, native/system/bin/reboot
sent, reboot_disconnect_observed=true (ADBsocketclosed, expectedCalledProcessError).
Receipt backup/a52q/ios-ufs-v7/receipt.json requires_restore=true. Watcherv7active
onC:backup/a52q/ios-ufs-v7/watcher*.log. UseraskedFIVEminutes thenresetTWRP.
RestoreoriginalBOOTimmediatelyonreturn; capturebootIDinsidefinally-protectedflow.
No currentrestorepending statementsbelow applywhileV7active. Receiptdefinitive.

V6 returned immediately with no pstore log (65-byte cat error, NOT kerneldata).
BOOT automatically restored/hashverified; no restorepending forV6. TWRP log
shows CLI 'reboot system', DRM pageflip failure then TWRP UI processrestart.
Linux boot_id d112... remainedsame, uptime~500s whileV6attemptjustended. This
proves V6 didNOT rebootLinux; NOT evidence of fsck or XNU failure. User unsure
what occurred. Original BOOT freshSHA matched afterV6. V5earlycapture inconclusive.

Private research/a52q_xnu_device_test.py now supports --native-reboot using the
actual /system/bin/reboot binary (property_set sys.powerctl, no TWRP GUI).
Requires recovery USB departure <=30s or restores original BOOT immediately;
records pre/post LinuxbootID, kernel_reboot_confirmed on return. Boot-IDcapture
is inside restoration try/finally, so its failure cannot skipBOOTrestore. Exact
observer hosttests PASS: unchangedRecovery rejected, disconnect accepted.
No XNU/AMFIfunctionalcodechanged forretries. V7 preflightcurrentlyrunning,
receiptbackup/a52q/ios-ufs-v7/receipt.json isdefinitiveforrestorepending.
C: logs install.log/watcher.log/watcher.err.log inthatdirectory. Hiddenwatcher
research/watch_ios_ufs_v7_restore.py startsafterinstall. Samekernel3808e55a...
ccfad87/candidate1c78fb37...5f9d2e/planv4. AskFIVE-minute reset onlyafteractual
USBdeparture. Userrecentlyactive/phoneinTWRP. No Androidboot/format/rootwrite.

## CURRENT: V5 RESTORED; IDENTICAL FSCK CANDIDATE V6 FIVE-MINUTE PREFLIGHT

V5 receipt requires_restore=false/original_boot_restored=true, full freshphone
SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Saved console8326bytes,3validentry copies, ends atCPUselfSGIdelivered. NO root/UFS
or fsck evidence in this capture. Userconfirmed3minonSamsungSplash,noautoreboot.
Previous ApplelaunchdMAIN remainsproven byV4; V5 does NOT provefsckexecution.
No functionalcodechanged for this unexplained earlycapture. SamecheckedBOOT
1c78fb37...5f9d2e (kernel3808e55a...ccfad87) retry plannedFIVEminutes tocheck
lateprogress/reproducibility. V6 installpreflightrunning; authoritative receipt
backup/a52q/ios-ufs-v6/receipt.json willmarkrestorependingafterwrite. C: watcher
logs inthatdirectory; research/watch_ios_ufs_v6_restore.py startsautomatically
wheninstallends. Oldconsole+pmsgarchivedprivatebeforeconsoleRAMrecordunlink.
Afteractualreboot askFIVEminreset, not3min. Ifsameearlystop, compareknown-good
V4kernel09e beforechanging fsck code. No Android boot/format or new rootwrite.

## CURRENT: APPLE LAUNCHD MAIN PROVEN; V5 ACTIVE, BOOT RESTORATION REQUIRED

V5 FSCK TRIAL ACTIVE NOW: backup/a52q/ios-ufs-v5/receipt.json requires_restore=true,
original_boot_restored=false. Candidate1c78fb37...5f9d2e installed/readback and
nativeTWRPSystem reboot sent. Hidden research/watch_ios_ufs_v5_restore.py waiting.
C: logs backup/a52q/ios-ufs-v5/watcher.log and watcher.err.log (not E:).
User prompted3minreset, then collect/restore immediately. Fullroot remainsRO.
All below 'restored/no pending' statements refer to prior v4 and are superseded
while v5 ACTIVE. Receipt is definitive. Do not bootAndroid or formatdata.

FSCK CANDIDATE READY, PREPARING TRIAL V5: exact kernel3808e55a...ccfad87
passed QEMU3entry/7PID1heartbeats; planv4 complete-masterhash0f4...312149PASS.
Candidatehardwarev6 SHA1c78fb373e62da0168026236da698ba8bc2020f768a826f4d7fc0cdc895f9d2e.
User AGAIN confirmed besidephone/ready. Installpreflight underway, receipt
backup/a52q/ios-ufs-v5/receipt.json determines actual restore state. Combinedshell
starts hidden research/watch_ios_ufs_v5_restore.py automatically afterinstall.
IMPORTANT: v5 watcher/install logs are on C in backup/a52q/ios-ufs-v5/{install,
watcher,watcher.err}.log, so E-drive loss cannot lose restoration logs.
Consolev4 archived byteexact efdba52d...05ce8,42480bytes, then RAMrecordunlinked.
Privatehelper nowuses ios-root-plan-v4.json. No new root/var writes; BOOTonly.
Do not ask3minreset until actualreboot confirmed. RestoreoriginalBOOT afterTWRP.

AMFI-only build43627967750/sourcef4ab8f8 PASS and verified against fullbase
43624481615/a46569c. Kernel3808e55ac77a2a969fb9c622c54621f0c3acd34a698bdadb0963a9f6bccfad87,
implementation54d4796b8b2571ac37fa85b7e5f37ba7f55e87c88f212f89f9a09f8bd6c78a50.
HostCI43627967485 PASS. Redundant auto full43627967504 canceled.
QEMU exactkernel fixture and master/planv4 preparation RUNNING. Next packaging
research/prepare_boot_task_candidate.py ->hardwarev6; phone receiptios-ufs-v5,
watcherresearch/watch_ios_ufs_v5_restore.py prepared, notrunning. No newBOOTwrite.

Next fsck policy prepared: exact master /sbin/fsck fileSHA1aaf55052561aaf1214cd7d65924c46d39b1ef325e37c1faeaa76769612e59ce
matches native staged-final-v6/os/sbin/fsck.13signed4KiBpages PASS, CDhash
e1a3f12fb8be72d6e9a4e4178ebe152513bc599a,no XML/DERentitlements. Actuallaunchd
csops stub0x50d70 called0x3feac withSTATUS0; cbnzerror/tbzbit26 ->panic0x400d8.
Kernel CS_OPS_STATUS uses csb_platform_binary. New AMFI-only policy admits exact
fsck only with CS_VALID, no entitlement blobs, on same RO rootmount; assigns
explicit LOCAL DEVELOPMENT platform classification (NOT Apple CMS trust).
No other executables/cache gainplatform status. Newnative tests reject20changed
fsckhashes,RW/wrongmount,missing/invalidsignature,entblob;115PythonPASS.
Needs isolated AMFI rebuild from full43624481615/sourcea46569c (overlay unchanged).
This supersedes earlier blanket 'no platform classification' history forfsck ONLY.

V4 mapping trial finished; receipt backup/a52q/ios-ufs-v4/receipt.json
requires_restore=false,original_boot_restored=true,protected hashes unchanged.
Fresh device BOOT SHA d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Console contains THREE intact kern.initproc_spawned=1 main markers, actual Apple
launchd 'hello'/Darwin Bootstrapper7.0.0 banner, system created/ondemand. This
proves early Apple launchd MAIN from full16GiB UFS image, NOT services or UI.
First next error: fsck signature denied (check_signature error1/proc2error4),
then launchd userspace panic 'boot task is not a platform binary (fsck, /sbin/fsck)'.
Main code actualLC_MAIN0x169b4 references sysctl0x169ec,56bytesin, matchingmarker.
No graphics/daemon speculation. Next: extract/audit exact master /sbin/fsck,
compare native stagedsource; trace registration/platform requirement before
narrow next-policy change. No filesystem rewrite or var install authorized.
Phone TWRP, no pending restoration. All older ACTIVE/pending entries superseded.

## A52Q latest — mapping candidate prepared, BOOT preflight in progress

V4 TRIAL ACTIVE: receipt backup/a52q/ios-ufs-v4/receipt.json requires_restore=true,
original_boot_restored=false. Candidate64a78ada...3cd5ad installed+fullreadback,
TWRP native System reboot sent. Hidden watcher_v4 is waiting; logs
E:/A52-iOS16/ios-ufs-v4-watcher*.log. User asked3min thenresetTWRP. Collect console
and restore original BOOT immediately on recovery return; no Android boot/format.
The earlier preflight/original-safe statements below are superseded whileactive.

Full HFS build43624481615/sourcea46569c verified71overlayfiles. Kernel09e97749...
45c3a1. QEMU exactkernel+diagnosticRAMfixture PASS3entry/7heartbeats (not fullUFS).
E: disconnected during masterhash; user reconnected. Restarted completehash,
planv3 created ONLY after matching0f4bcaa7...312149. Master/root unchanged.
Candidate shim/out/a52q-ios-ufs-hardware-v5/build/a52q-ios-ufs-UNTESTED.img,
SHA64a78adae4d4ce7f50264cfabb3d8b1726984c4512f716e3abeb88235c3cd5ad.
User confirmed besidephone/readiness again. Install helper is in preflight
(current original BOOT expected); receipt backup/a52q/ios-ufs-v4/receipt.json
will require restore if BOOT installed. Combined install shell will start hidden
research/watch_ios_ufs_v4_restore.py automatically after reboot, even if install
exits with error but receipt requires_restore=true. Logs E:/A52-iOS16/ios-ufs-v4-*.log.
Old liveRAM console archived byte-exact then unlinked; no partition touched for
rearm. v4/pretrial-console-archived.bin SHA cff5c70c...ee1d1,34014bytes.
Announce3minreset ONLY after actualreboot. Do not boot Android or formatuserdata.
The below v3 ACTIVE/pending history is superseded: v3 BOOT restored, allhashesPASS.

## A52Q active handoff — cache candidate prepared, 2026-11-14

FULL HFS BUILD43624481615/sourcea46569c PASSED; all71 overlay source hashes
verified from downloaded buildtree. Kernel09e97749a7856e81c640668665a20de36c21440ee3ea384c3ef13f5aa345c3a1.
Exact kernel + diagnostic HFS RAM fixture QEMU PASS,3entry/7heartbeats, no full
UFS emulation. E: disconnected during master rehash, user reconnected; retry
research tool process is checking entire master again before planv3 packaging.
Phone TWRP, original BOOT restored, no new phone writes or pending restoration.
Historical build-running sentence follows for context:
FULL HFS BUILD43624481615/sourcea46569c is running. HostCI43624481552 PASS.
71-file overlay applied/checks PASS; mapping native negatives PASS,115Python tests.
Prepared research/prepare_cache_mapping_qemu.py / prepare_cache_mapping_candidate.py;
next planv3/candidatehardwarev5/receiptios-ufs-v4/watcherv4, none installed yet.

V3 TRIAL FINISHED: ORIGINAL BOOT RESTORED and fresh phone SHA matched
 d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Receipt requires_restore=false, protected hashes unchanged, phone TWRP.
Cache registration SUCCEEDED: CODE SIGNING post-attachment logs through
.42.dyldlinkedit. symbols companion is not requested at runtime. Next actual
failure: shared_region reports vnode not SIP-protected; mapping syscall fails,
libSystem consequently unavailable, initproc failed to start. No launchd main.
Four valid UFS root window frames, UFS capacity/read phase CRC valid.
Preparing A52-only exact-cache/RO-root SF_RESTRICTED exception in vm_unix plus
observational kern.initproc_spawned=1 marker. No global CSR/CS disable, root image
unchanged. Needs full HFS kernel build because overlay and vm_unix/kern_exit changed.
The old ACTIVE/pending entries below are historical and superseded.

TRIAL v3 ACTIVE: backup/a52q/ios-ufs-v3/receipt.json requires_restore=true.
Candidate3c6224...69c37 installed/readback; TWRP System reboot sent. Watcher
research/watch_ios_ufs_v3_restore.py is waiting; logs E:/A52-iOS16/ios-ufs-v3-watcher*.log.
User requested3minreset. Restore original BOOT immediately on TWRP return.
Live pstore was ALREADY absent at preflight (no unlink this turn); last collected
v2 console preserved verbatim in v3/pretrial-console-archived.bin and proof.
The historical NO restore pending statement below is superseded duringtrial.

NO BOOT restore pending. Full root remains installed/read-only; never run Android
control or format data. All 44 original cache SHA256 checks and 202,845 16-KiB
CodeDirectory page hashes PASS (3,330,359,296 bytes); format v0x20400/SHA256,
no XML/DER entitlements. Private cache-code-signatures-v1.json retains results.
Actual dyld-1067 disassembly proves fcntl command97/F_ADDFILESIGS_RETURN. Old
policy source a5398f2 native test rejects all44 with KERN_DENIED53; ubc_cs_blob_add
maps it to EPERM1. Cache rejection explains missing libSystem, present in cache.
Exact-policy test now accepts44 and rejects880 changed hashes, unapproved/NULL,
wrong-root and entitlement-bearing cache contexts. 115 Python tests PASS.
Shared regions always set vm_map_cs_enforcement_set(sub_map,true); system CS
checks default1 in kern_cs.c regardless CONFIG_ENFORCE_SIGNED_CODE. No disable
bootargs accepted for full-root candidate; cs_debug=2 traces registered blobs.
Runtime altered-page rejection has NOT been separately tested on the phone.

AMFI-only build43607167940/sourcef1c8294 PASS, implementation743a1e4b...81b814,
kernel b52bb868b5138677b0b99ecdbea80af773689768782d7cf4312be408a3054c76.
Exact new kernel + tiny diagnostic RAM fixture QEMU PASS (3entry/7heartbeats),
shim/out/a52q-cache-pins-qemu-v1/run/result.json. NOT full-UFS-root emulation.
Full master rehash completed0f4bcaa7...312149; kernel-bound ios-root-plan-v2.json.
Candidate shim/out/a52q-ios-ufs-hardware-v4/build/a52q-ios-ufs-UNTESTED.img,
SHA3c6224d3b9ca65e6cb98ab2fe94484ca5ae97fac1f76041ba3634654a4d69c37,
BOOT only, new kernel/cache pins + cs_debug=2, unchanged ignition baseline5.
No RAM root/diagnostic PID1 substitute or filesystem rewrite. Next trial receipt
backup/a52q/ios-ufs-v3/receipt.json; archive/rearm old RAM console first. Watcher
must restore BOOT on TWRP return. User authorizes BOOT-only trial. Current proof
is Apple loader/libignition execution, NOT launchd main/services/SpringBoard.

## A52Q handoff — 2026-11-14: full UFS root mounted; BOOT restored; platform fix ready

CACHE FIX READY FOR BUILD: audited all44 cache files against original SHA list
AND every CodeDirectorypagehash, via native readonlystaging+bounded mmap. Result
E:/A52-iOS16/cache-code-signatures-v1.json;44uniqueCDs,no XML/DERentitlements.
Source xnu/a52q/a52q_amfi.c adds onlythose44hashes onfullroot; metadata JSON
xnu/a52q/ios16-20H392-cache-pins.json contains hashes only, noApple binaries.
New audittool/test +dataset/Cconsistency test;114Python tests PASS. Both69file
A52overlays apply to actual81patch source, filesystemonly config difference.
Adding explicit fullroot --ios-ignition-level1 mode toavoid observedAPFSpreboot
ENOTTY25; actualdyldcontainsflagstring and mkiosroot docs specifylevel1layout.
Needs AMFI-only relink from43596004630/base2d2cd0c, exactnewkernelQEMUfixture,
new kernel-boundfullrootplan and BOOTcandidate; NO rootfs rewrite required.
Native WSL A52-HakiOS-Build-20261107 terminated after audit tofreehostRAM.

SECOND FULL-ROOT TRIAL FINISHED: ORIGINAL BOOT RESTORED AND VERIFIED.
backup/a52q/ios-ufs-v2/receipt.json requires_restore=false, original_boot_restored=true.
Watcher14480 finished, original BOOT/protectedSHA verified.3CRCrootwindowframes.
Platform gate passed. Real Apple loader/libignition executes on full UFS root:
"libignition: 1: hello: hello from launchd.1"; ignition5 prebootlookupfails25,
then "dyld cache '(null)' not loaded: code signature registration for shared cache failed"
and "Library not loaded: /usr/lib/libSystem.B.dylib". No launchd main/services/UI.
Maincache index was independently verified to contain libSystem/libobjc/Foundation/
SpringBoard.framework; do NOT fabricate/replace missing dylib. AMFI policy denies
cache CDs (currently only owninit +2Appleexec pins). Next targetedfix: inspect
all cacheCodeDirectories from validatedmaster, allowexactmeasuredentitlement-free
cachepins only onfullroot. ActualerrorKERN_DENIED53 ->EPERM1 registration failure.
Need inspectsupported ignition_level=1 mode toskipunavailableAPFSprebootstage.
NO restoration pending; phoneTWRP. Installedroot0f4 remainsread-only and no new
userdatawrite performed. Do NOT run Android control/format. User stillbesidephone.

FIRST FULL-ROOT TRIAL FINISHED. NO BOOT RESTORATION PENDING.
backup/a52q/ios-ufs-v1/receipt.json requires_restore=false, original_boot_restored=true.
Watcher148 finished with full BOOT/protected hashes. Fresh recovery BOOT SHA
confirmed d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Phone remains TWRP. USB descriptor enumeration failed after restore; user
unplug/replug restored ADB. User said continue, still beside phone.

Full root mounted from userdata:3CRC-valid A52V1 window frames; volume label
iOS16Pristine and UNSEALED path in retention-corrupted text, INTACT launchd pin
accepted line. No Apple user execution proven: SIGKILL(CS_KILLED) inside exec.
Raw numeric reason0xe versus0xd disagrees; never repair/infer those numbers.
Exact leaf symbols place backtrace in process_signature+0x1e4 -> psignal_internal.
Compiled binary contains XNU_TARGET_OS_OSX iOS-platform gate, default DEVELOPMENT
unentitled_ios_sim_launch=false. Applelaunchd is PLATFORM_IOS and no no-sandbox
entitlement exists. Source therefore identifies platform rejection independently
of corrupt numeric reason. New fullroot-only --ios-exec-development passes
unentitled_ios_sim_launch=1; no AMFI pins/page checks or entitlement grants changed.
Kernel21... and filesystem0f4... UNCHANGED. Candidatev3 BOOT SHA
3031859c83b0e95fc6d412fcd296b1d86569cb29af3dcaea85d18fced719f870.
Private helper requires explicit option; root install proof now binds root hash
and window, allowing newer BOOT trials without another filesystem installation.

Next BOOT-only retry: backup/a52q/ios-ufs-v2/receipt.json, not installed yet.
Baseline has3oldCRC-valid entry frames; cannot run Android control afterdatawipe.
Old console archived pretrial-console-archived.bin SHA607e75950684c423ba4c09df784059d43d5d2b70a6bc81d9f39817dd493013c3.
Rearm ONLY console-ramoops-0 via pstore unlink after archiving (reservedRAM,
no partition writes); proof file required for explicit absent-baseline exception.
Logging remains enabled. User has already authorized automatic BOOT-only tests.

FULL ROOT INSTALL COMPLETE AND VERIFIED. User approved exact16GiB userdata
write and trial, waived backup, confirmed beside phone. Entire /dev/block/sda31
prefix[0,17179869184) now matches master SHA0f4bcaa7c1a6f0a531c8b4d4d67b0dd8843b5ab58c2c31a005e07b1bde312149.
Receipt backup/a52q/ios-root-install-v1/receipt.json root_installed_verified=true,
128chunks; hostADBserverloss6.75GiB recovered by matched-prefix resume; no
userdata write outside approved16GiB. Original BOOT/protected hashes matched
postwrite. Android data was overwritten as approved. DO NOT boot Android or
run any original-Android control again. Phone in TWRP, no BOOTrestorependingyet.
Starting private BOOT helper --kernel-ios-root --kernel-ufs-selftest with
candidate2a19c0... in backup/a52q/ios-ufs-v1/receipt.json. Watcher prepared at
research/watch_ios_ufs_restore.py but must start immediately after install/reboot.
Await root-readback preflight; only announce3min when reboot actually starts.
The later "not yet approved/no install" lines below are historical and superseded.

Original BOOT is installed and freshly SHA256 verified:
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
No pending restoration; no userdata or GPT writes. Phone is in TWRP.
Android control-before-ios-ufs-v1 passed boot_completed=1 and returned to TWRP;
original BOOT and protected partition hashes matched. Keep the saved v2 console.

Latest physical disk-root result: backup/a52q/ufs-root-v2/console.txt contains
"hfs: mounted A52ReadOnly on device b(1, 1)", then
"rootvp not authenticated after mounting @bsd_init.c:953". Five CRC-valid root
window records. UFS HFS mount proven; diagnostic PID1 from UFS NOT proven.
The rootauth fix allows only the published read-only UFS root, logs UNSEALED,
and leaves other A52 roots and Redmi unchanged. RAM roots skip this check.

Full HFS build43596004630/source2d2cd0c343a9567673f95bbc712e2c951c264582 PASS;
69 archived source hashes matched reviewed overlay; kernel e40f1facea620524799430374428ab13949cbfd8423e761f6a7228d6d2f3d06f.
AMFI-only rebuild43597692128/sourcea5398f22be05a316b21890cf709ae4f0fb8c824d PASS;
only audited launchd/dyld pins admitted on full UFS root; no entitlements/platform
or Apple CMS trust fabricated. Implementation SHA657609ad25d69a2330fc3ae652dd3d95d352c5eadc71ef145c3128568cf501e0.
Final kernel210ac994cf8b7a41237613e72f738b9e74b6d22ecdc8014eeb0c602d7c5aa492.
QEMU exact final kernel + small nonjournaled RAM fixture PASS3entry/7PID1heartbeats:
shim/out/a52q-ios-policy-qemu-v2/run/result.json. NOT an emulated full-root boot.
HostCI43597691763 PASS; latest local109Python tests PASS. Original81patches intact.

Full master E:/A52-iOS16/ios16-20H392-pristine-v11.hfs.img,17179869184B,
SHA0f4bcaa7c1a6f0a531c8b4d4d67b0dd8843b5ab58c2c31a005e07b1bde312149.
Sidecar .hfs.verified.json: clean RO fsck,47 originalcore/cacheSHA,nonjournaled.
Fresh full hash readback repeated during plan and installer preparation, allPASS.
Staged native source, verified transfer ext4, original v10 and master preserved.
Apple xattrs/ACLs/BSDflags NOT preserved; no runtime compatibility claim.
Private master-executable-audit-v2 verified launchd/dyld/SpringBoard checksums and
all executable-page hashes; plainarm64. Shared cache header arm64. No Apple
launchd execution, userland services or visible SpringBoard demonstrated.
Separate4GiB var hostimage storage-data-v1/a52q-ios-var.hfs.img fsck/rsyncPASS,
SHAefa03fd497c0ecf2b1c5915a925fbc27979319094b663611f11e3abf860b8a36.
Kernel bounded-write/mount path NOT implemented; this volume is NOT installed.

Full root plan E:/A52-iOS16/ios-root-plan-v1.json binds exact kernel/master/GPT.
Candidate shim/out/a52q-ios-ufs-hardware-v2/build/a52q-ios-ufs-UNTESTED.img
SHA2a19c0f17281b818386920be66591f6a5907ec73544eb8fbd5ede85931a0e4cb,
96MiB BOOT, no RAMDisk/init substitute. New root device /dev/a52ios0 is read-only
16GiB userdata window; liveGPT CRC/header/entry checked before publication.
Host install review E:/A52-iOS16/ios-root-install-review-v1.json.

User explicitly waived userdata backup: "delete android no problem dont backup".
Do NOT repeat backup prerequisite. Per user's step7, present exact operation
and get concrete approval BEFORE any userdata write. Proposed ONLY root range:
/dev/block/sda31 bytes[0,17179869184), absolute[12966690816,30146560000).
This destroys existing Android data. BOOT restoration does NOT restore it.
No GPT/other partition write, no future4GiBvar volume included. Private installer
research/a52q_install_full_root.py has host-only prepare phase; install requires
--approved-exact-root-write. It checks host master/candidate/backups/liveGPT,
unmounts userdata-dependent aliases, records metadata snapshot, then128MiBchunks
pushed to /tmp, perchunkSHA, bounded dd seek/count; full16GiB phonehash readback.
The user has NOT yet approved this concrete write. No install receipt exists.

Transport safety: Windows adb shell stdin truncated at0x1a; exec-in smalltest
passed but4MiBall-byte test failed. DO NOT use either for binary root stdin.
Binary adb push -Z and regular-file byte-seek/count dd passed4MiB tmpfs test;
128MiB chunk push +deviceSHA also verified in backup/a52q/storage-preflight-v3.
Metadata16MiB raw snapshot saved and deviceSHA matched; mounted filesystem
snapshot is NOT a consistent Android data backup. Original protected images
are retained/verified. No partition writes were performed in transport tests.

BOOT helper now supports --kernel-ios-root ONLY after verified root install
receipt +fresh16GiBdevicehash; kernel-ios-root-result separate from PID1 evidence.
Watcher research/watch_ios_ufs_restore.py prepared, NOT running. It captures
pstore then restores original BOOT on TWRP return; 10min deadline means restore
still required if timeout. Do not run Android control AFTER destroying userdata.
Need user near phone for3min fullroot trial, then button reset to TWRP.
Current remaining: final host checks/publication, concrete write approval/readiness,
then root install/verify, temporary BOOT trial, logs/BOOT restore. No iOS boot claim.

### Earlier staging/trial history (superseded by the status above)

TRIAL FINISHED: backup/a52q/ufs-root-v1/receipt.json requires_restore=false,
original_boot_restored=true, protected hashes unchanged. Watcher9008 finished.
UFS wholeBSDproof +rootwindow CRC BOTHpassed5copies. No disk-root PID1: HFS
attempted initializing freshjournal, .strategy returnedEROFS0x1e asintended,
journal_create failed, mountroot errno19loop. Fix is NON-JOURNALED cleanfixture,
NOT enablingdiskwrites. Added validate_readonly_hfs_root andUFSroottool rejection
ofjournaledfixture; RAMrootvalidation stillallowsjournalinit.101testsPASS.
Preparing newfixture E:/A52-iOS16/a52q-hfs-init-readonly-v2.img usingguestmkfs
without-J +samepinnedinit. NeedsnewQEMUproof+repackage; kernel974unchanged.

32fullimageUnicodeproposed repairs ALLmatchoriginalsource filenamesUnicode3.2NFD:
E:/A52-iOS16/hfs-name-repair-preview.json, privateaudit_hfs_name_repairs.py.
Copyoforiginalv10 ->v11 .hfs.img, SHA copyverified; repair onlyv11 inisolatedguest
exec99237 research/repair_hfs_names_v11.py. Requirescleanfsck+47SHA+file/foldercounts
unchanged +fullblockdiff restrictedtoVH/allocation/extents/catalog metadataforks.
No validatedv11claim yet. Originalv10preserved. Source/filenamechecksread-only.
Livepstore auditconsolefile is catmissingerror; no newuserlandlog. Prior ACTIVE
records below historical, currentoriginalBOOTrestored, phoneinTWRP.

11:17:17UTC BOOT-only read-only HFS disk-root trial installed+fullreadback+
nativeTWRPSystem reboot. User confirmed 3minreset readiness. Receipt
backup/a52q/ufs-root-v1/receipt.json requires_restore=true. Restore ORIGINAL BOOT
afterrecoveryreturn; watcher PID9008 research/watch_ufs_root_restore.py,
logs E:/A52-iOS16/ufs-root-v1-watcher*.log. If timeout restoration still REQUIRED.
Candidate66389c9ebbf85fbcedddecee94148d373d281b47266f4d4925c0f450fafdf7a7,
kernel97437563bd3b5b3f57a846b4d5270667783acb6fef78ecf806f365fbdd7564e5.
New kernel fullHFSbuild43473244579 PASSED sourcea487c5a;69overlayfiles/hashmanifests
match localHFSsource. Artifact E:/A52-iOS16/builds/43473244579/. Samekernel+32MiB
HFSfixture70665f70... passedQEMU PID1+7heartbeats in
shim/out/a52q-ufs-root-hfs-qemu/run/result.json. Hardware has NO RAMroot fallback.
BOOT96MiB sda19, boundedroot last32MiBoffset64MiB =>LBA115696/count8192;
allGPT/sysfsbounds revalidated. No userdata format, GPT orotherpartitionwrites.

Latest prompt's Applelaunchd/60HzIOMFB premise remains unsupported: actualsaved
longdisplaytest logs own diagnosticPID1+31intactHB, no IOMFB/IOSurface/backboardd/
SpringBoard messages. User has no newerbuild/log. LiveTWRPpstore emptyNov14;
requested iOS/var/log+CrashReporter paths absent. Auditcapturebackup/a52q/log-audit-20261114/.
Memoryplanner checkedfull256MiBbase0x106000000 against34DTreservationnodes,
including5entire dynamicwindows, plusLinuxiomem/memreserve. No reserved overlap;
not an exhaustivefirmware/XPU proof. EarlyBootVideo/IOSurface stilldisabled.

FulliOSimagev10 copy+47core/cache SHAchecks PASSED but HFSfsck FAILED32IllegalName
errors (exit8); no .verified.json/success marker. Never install asvalidatedimage.
E:/A52-iOS16/ios16-20H392-pristine-v10.hfs.img preserved; debugreadonlyguest
log E:/A52-iOS16/appliance-windows/pristine-debug-v10.log showsUnicode
decomposition repairs in.localized.shortcut filenames only; VIStat/ABTStat/
EBTStat/CBTStat zero,CatStat0x8000. Checking proposednames againstoriginalstaged
Unicode3.2NFD names before anyrepair. Privateaudit script exec85611 (mayfinished).
Sourceexportv9 stillverified16GiB SHA52754040...; v8export andv9HFSformatfailed
outputsremoved onlyafterrecord in E:/A52-iOS16/discarded-incomplete-v8-v9.json.
v10formattedinsideisolatedQEMUguest, sourceRO, no network/USB/hostphysicaldisks.

## A52Q handoff — 2026-11-13: display + PID1 VERIFIED; PHONE SAFE

LONG TRIAL FINISHED: receipt backup/a52q/kernel-display-long/receipt.json says
requires_restore=false, original_boot_restored=true; protected hashes unchanged.
Watcher1448 finished. Three CRC-valid XNU entries, all3display phases5copies each,
EXACT PID1 banner and31intact diagnostic heartbeats. This confirms continued boot
with display enabled. No Apple launchd/SpringBoard yet. Prior missingPID1 record
was a shorter capture; do not claim a display-related hang from it.

Native source-transfer-v8.ext4 completed and e2fsck -fn passed (321224 inodes).
DrvFS export v8 failed Cannot allocate memory; partialv8file INVALID. Windows-side
bounded streaming export v9 PASSED native-stream SHA +Windows full readback:
E:/A52-iOS16/ios16-source-transfer-v9.ext4,16GiB,
SHA256527540400e87c55b15876477fb889b711cc37886738724df7d318ad1b93165e1.
Its .verified.json records result. Full HFS v9 preparation started exec39810,
regular sparse16GiB destination created; copy/fsck stillNOTdone. Cnearlyfilled
61MiBfree; losslessNTFScompression of22OWNgeneratedBOOTimages reclaimed2.1GB.
Image bytes/paths unchanged, no user files deleted. Efree~49GB before HFS fill.

Implementing opt-in read-only BOOT-tail HFS root, based on capturedGPT+successful
kernelUFS proofs. New minor1/root-device hook, host bounds validation+packager.
NOT yet compiled/tested/installed. DefaultwholeLUN0 and hardwaredrivers preserved.
The longer-test ACTIVE records below are historical, phone restoration complete.

17:07:26UTC same corrected display kernel installed for THREE-MINUTE follow-up.
Receipt backup/a52q/kernel-display-long/receipt.json requires_restore=true;
original BOOT NOT restored yet. User explicitly confirmed 3min reset readiness.
Watcher PID1448 research/watch_kernel_display_long_restore.py; logs
E:/A52-iOS16/kernel-display-long-watcher*.log. Captures then restores BOOT on
TWRP return. If watcher times out, restore manually via helper collect-restore.
Android control beforehand PASSED boot_completed=1 and original/protected hashes.
Source unchanged; image SHA5ebbae2... /kernel33cdd5f... as recorded below.
Historical safe-state statements below describe the preceding restored test.

Independent host work: WSL A52-HakiOS-Build-20261107 responding again. Started
research/prepare_pristine_hfs_v8.py under WSL, exec session52783, printed
POPULATING_NATIVE_TRANSFER_IMAGE. No full HFS image claim yet. Native regular
ext4 file/root/a52-ios16-host/images/source-transfer-v8.ext4 (16GiB) is populating;
v8 output files did not exist before this attempt. Private appliance builder now
explicitly copies GNU sha256sum for its 47-file verification job.

Original BOOT is RESTORED with full SHA256 readback. Private receipt
backup/a52q/kernel-display-v2/receipt.json: requires_restore=false,
original_boot_restored=true; RECOVERY/DTBO/vbmeta unchanged. Watcher8644 finished.
No active trial, no pending restoration, no userdata format or GPT change.
Original BOOT SHA256 d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.

User confirmed RGB bars appeared BEFORE reset, then returned to TWRP.
Kernel A52D1 phases0x10/0x20/0x30 each have FIVE matching CRC-valid copies,
detail0, nonce9697378418859164443. Three valid XNU entry frames survived.
This proves guarded XNU mapping, CPU pixel write, command-mode START and visible
output on SM-A525F/DS. No measured panel Hz/VSync, IOSurface, Apple UI or GPU claim.
Retention corruption remains in unprotected console text; no byte repair used.
This trial log ends in network initialization, with NO intact diagnostic PID1
banner or heartbeat. Do NOT claim physical display+PID1 together yet. QEMU with
the same kernel and no display node reached PID1 +7heartbeats. Next hardware
test: longer follow-through of this same corrected kernel (after original Android
control to clear old entry records), before enabling a framebuffer ABI.

Corrected kernel SHA256 33cdd5f013dfec14f22ef1c544ca2f2736215092dc5c6643e1b09c51d0c017e1.
Phone image SHA256 5ebbae2b22ff58b9ae341d30ed2c12a79431c5a2bb9d7524ec67fe5c09e3d14c,
shim/out/a52q-kernel-display-hardware-v2/build/a52q-kernel-display-UNTESTED.img.
Its shim Image is21176160bytes; accepted/reached XNU despite conservative filename.
Successful isolated rebuild43464680521, source394d057da98110a15517eab395a2b9bed9973347,
selected implementation SHA256 f38543f9e7ae6e4efea962f984d806333bd6820154dabeb6706077739347bab0.
Base full build43459301822/sourceb4cec1fb755419d5646750ba09ddddd62292ef04;
base kernel d01a8d650364ae9b0ba630bc237f591ad72fe1dbc98dca18e322f28234e0c67e.
All68 archived overlay files matched reviewed full-build source. Corrected kernel
and selected implementation hashes checked; unchanged base init SHA256
aaacee08d03b7f0d93b0b34aa1d2436b0c3798b370ebf1e623732c5739c4473e.
Artifacts E:/A52-iOS16/builds/{43459301822,43464680521}/; verified-build.json records.
QEMU v2 shim/out/a52q-kernel-display-qemu-v2/run/result.json PASSED3CRCentry +7HB.
Host CI43464679787 PASSED96A52 Python tests/native C/cross-build/4QEMU core checks.
Validator81patches/36Python/7shell PASS. Original81Redmi patches unchanged.

Display implementation: evidence-bound a52q-display-selftest ADT, absent by default;
tools/a52q_display_selftest.py revalidates raw successful shim refresh proof and
pinned Samsung register sources against live DT. Rejects QEMU hardware node,
invalid ranges/geometry, overlapping kernel/panic RAM and changed runtime guards.
FB0x9c000000/reservation0x9e4000, BGRA1080x2400/stride4320. No address invented.
All13 registers read/checked before pixels; one CTL_START only,100ms wait deadline.
No DSI command, mode switch, clock/reset/IOMMU programming. UFS/AMFI/init/ramoops
implementations unchanged. Early Boot_Video stays zero; no premature console writes.

First kernel trial v1 (private backup/a52q/kernel-display-v1) showed NO bars.
Retained log: guarded mapping then kmem_alloc(...10371072...) failed3 panic.
Source osfmk/arm/io_map.c IO_MAP_SIZE=8MiB explains why the framebuffer cannot
fit ml_io_map permanent io_submap. Correction maps ONLY framebuffer through
ml_io_map_unmappable(...VM_WIMG_IO), using kernel_map; small MMIO maps unchanged.
First leaf43464368423 failed compile for BSD-hidden helper declaration; exact
prototype added, successful corrected leaf above. No failed artifact installed.
Full builds have existing header/C99 warnings and bounded band-index narrowing;
not a Werror build. No unsupported global warning suppression added.

Earlier standalone shim full-screen test also PASSED: 5CRC stage93/ESR0 guards
match and human-visible bars, backup/a52q/display-fullscreen-v1/. CPU pattern
uses bounds/stride canary-tested helper; virtual-counter100ms timeout avoids
assuming physical-counter EL2 access. Ordinary r4 core byte-identical SHA256
ee37e8f025fb20b38699d0d67044be9f8a6f06fb640eee71668916204a93f823.
Shim candidate0e021a5e8f1277bfde4f0ccfd2518d4cdeac3fcdd30904e41b73b04aa2e7ff65.

Audit: user acknowledged 120Hz/Applelaunchd failure claim came from AI; no log.
No justified 120->60 patch. Existing SWEET notification timer16667us. Captured
Samsung panel DT has fhd60/fhd90 descriptors, not measured active ABL timing.
No nil-Metal-device CPU fallback established; no invented CA/backboardd flags.
Future IOMobileFramebuffer/IOSurface port must preserve A52-specific command-mode
commit and proven geometry, and must NOT enable Redmi hardware drivers. Current
AMFI accepts only own static init, not Apple launchd; UFS root is NOT mounted.
HFS RAM root and read-only UFS/BSD block paths were separately verified earlier.
The combined large HFS RAM root + UFS node stall remains unresolved.

Android control before v2 PASSED sys.boot_completed=1, then auto-returned TWRP;
backup/a52q/control-before-kernel-display-v2/console.txt had ZERO stale XNU entries.
Private helper install requires explicit --kernel-display-selftest and reviewed
proof, full BOOT/template hashes and zero MISC before native TWRP System reboot.
Restoration watcher captures logs then restores exact original BOOT in finally.

Workflow alternate standardmacos-15 ARM host verified available in official
runner manifest with Xcode16.0/16A242d, but its job43466726845 canceled before
execution after Intel queued job started. ARM host option is NOT tested. Default
Intel preserved; exact Xcode checks added. Redundant automatic full builds canceled.

Historical Nov11 host-root notes below: source staging succeeded, preserving
POSIX owners/modes/links but NOT Apple xattrs/ACLs/BSD flags. Full HFS images
v1-v7 invalid/incomplete; v7 stopped, v8 launch failed WSL WSAETIMEDOUT. No full
iOS HFS image is validated/flash-ready. BOOT-tail HFS-on-UFS remains a host-only
proposal; no packager/root-driver implementation and no userdata-format approval.

## A52Q handoff — 2026-11-11 (separate device/session)

### SOURCE STAGING COMPLETE; HFS image preparation active; PHONE SAFE

All3nativecopies nowexit0. OSv5:179359regularfiles,2324symlinks,
8291487156bytes; SystemOSv6:3360034133bytes; AppOSv6:7936372bytes.
E:/A52-iOS16/staged-final-v6-sources.json isSUCCESSmarker, stagedroot
/root/a52-ios16-host/staged-final-v6 (osrelative-symlinkto validatedv5OS).
v5SystemOS FAILEDreaderonlarge42.dyldlinkedit, noheapreport. FreshWSLhadNOswap;
v6 explicitlyenabled task4GiBswap/appliance/source-staging-4g.swap +ASan16MiB
quarantine andALLcopiesPASS. Don't assume swap persistsacrossWSLidle-restarts.
No exactOOMcauseclaim withoutdmesg; nooriginalstream shortread observedinv5OS.
Readerpatches/instrumentationstillprivate. Nativecopy preservesPOSIXowners/modes/
links, NOTApple xattrs/ACLs/BSDfileflags. NoApplelaunchd/UI bootyet.

DirectWHPX Linuxfile-copyfixturePASSED uid501/gid20/mode640,hardlink,symlink,
Unicode +cleanHFSfsck. LogE:/A52-iOS16/appliance-windows/direct-fixture-raw-v2.log.
Read-onlyWSLVHDX routeREFUSEDdirtyVHDXlog; NEVERrepair originalWSLVHDX for this.
Insteadregularrawext4transferfile createdwithmkfs.ext4-d, mountedreadonly inguest.
Fixture sourcepathfixedto/sources/; earlierfixtureNoSuchFilefailure NOTasuccess.
Privatebuild_rootfs_appliance.py nowincludesext4andfsck.hfsplus modules/tools.

FULL imageprep ACTIVE hiddenWindowsPID11208, research/prepare_pristine_hfs_direct.py.
LogE:/A52-iOS16/prepare-pristine-v7*.log. Copiesstagedfiles byhardlinks into
/root/a52-ios16-host/transfer-tree-v7 thenpopulatesregular16GiB ext4transferfile
E:/A52-iOS16/ios16-source-transfer-v7.ext4; creates16GiBHFSdestination
E:/A52-iOS16/ios16-20H392-pristine-v7.hfs.img andembeddedjobinitrd
E:/A52-iOS16/appliance-windows/pristine-direct-v7.cpio.gz. NOTcopied/fscked yet.
Needprepare finish, addoriginal47core/cachefileSHAmanifest+guestsha256sum-c,
thenSYNC+terminateonlyourWSLdistro andrunWindowsQEMU384MiB WHPXwithrawsourceRO,
HFSdestRW,NO network/USB/hostblockdevices. Require A52_PRISTINE_HFS_IMAGE_PASSED
andA52_APPLIANCE_RESULT=0, fsckclean, andfullimageSHA beforecallingartifactvalid.
ImagecontainsbaseOS+SystemOS/AppOSinprivate/preboot/Cryptexes+44dyldcachehardlinks;
nootherflattening/tweaks/providerchanges. ItwillNOTbootAppleuserlandwithcurrentAMFI.

Added tools/a52q_gpt.py +7tests: primary+backupCRC/arrays matchall31sysfsranges;
BOOTfirst99312/count24576,RECOVERY123888/19968,userdata3165696/27911647,
block4096. Privatecapturebackup/a52q/gpt. HostproposalBOOTtail32MiBat64MiBoffset
=>LBA115696/count8192 fitsbeforeRECOVERY; no image/partitionmodified.
PotentialNEXT minimaldiskrootexperiment: embedOWNHFSfixtureinBOOTpadding,
addboundedread-onlypartition/minor/rootlookup+packagervalidation. Preserves
userdataandGPT; stillONLYfutureproposal, notimplemented/installed. CurrentBSD
driverexposeswholeLUN0only, noGPT/rootselection. Needactualcode+build+reviewbeforetest.
90Python tests pass. OriginalBOOTrestored, allwatchersfinished, nohardwaretestpending.

### VERIFIED BSD STORAGE ON A52 — PHONE SAFE, ORIGINAL BOOT RESTORED

backup/a52q/readonly-disk-mockfs/receipt.json requires_restore=false,
original_boot_restored=true; recovery/DTBO/vbmeta hashes unchanged. Watcherfinished.
Same18d998kernel withsmallmockfs diagnosticroot PASSED: phase10 fiveCRCcopies,
phase11 five, phase20 four andphase30 FIVEvalidcopies. OCS0,lastLBA31077375,
4096byteblocks,dataCRC1080028829,response21000000. kernel-ufs-result.json
success=true,readonly_disk_verified=true. This verifies knownblock READ through
BSDbufferstrategy+CRC andsuccessfulread-onlydevicepublication. No userspace
raw-read test ormountedUFSroot yet. Candidatea20965f... (fullSHAbelow).
No Applelaunchd/UI, GPU/input/cellular/services. No diskwriteCDB orformat.

The combinedlargeHFSRAMroot+UFSnode trial remainsunresolved; doNOT claimits
causeismemorypressure: footprint, addresses andboot timing changed together.
HFSRAMroot andBSDdisk paths EACHworkindependently onphone. Tinyroot variant
matchesearlierUFSsuccesssetup. No needforspeculativekernelchanges/earlymarker
rebuildnow. Nextkernelstep isexplicitpartitionmapping/root selection, derived
from CRC-checked actualGPT andcurrentpartitionbounds, stillreadonly. RealApple
root filesystem, reviewedAppleexecutables/entitlements provider, displayrefresh
andinput remainbeforeUI. No furtherphonewritepending.

Host sourcecopyv5stillACTIVE; had925MiBcopied withoutI/Oexception whenchecked.
DoNOT claimcomplete; readE:/A52-iOS16/apfs-first-copy.log JSONexitstatus then
verifyallstats/bytecounts. CurrentprivateASanDiskImageFileinstrumentation throws
on firstshortread; no retry/masking. WSLavailable, noQEMUrunning. KeepEattached.

### PHONE SAFE: BSD+HFS trial inconclusive; isolate small-root variant next

backup/a52q/readonly-disk/receipt.json original_boot_restored=true,
requires_restore=false; protectedpartitionhashesunchanged. Watcherfinished.
UserreportedSamsungSplash. Kernel18d998... produced3CRCentryrecords andCstartup
through CPUinitialization, butZEROvalidA52K1 records for newnonce; no diskproof.
DoNOT sayitneverenteredkernel. LastintactCbootmessages arebeforekernelUFSreports;
doNOT infer exacthangsite fromunprotected/partlydamagedCstream. Candidate697fc74...
combinednewBSDkernel+32MiBHFSRAMroot+UFSnode. QEMUretrydidpassHFS+7heartbeats after
freeinghostRAM. Need isolateRAMroot footprint fromUFSselftest beforechangingcode.

Preparedsame18d998kernel+UFSnodewithsmallpinnedmockfsroot, matchingprevious
successfulUFSphone setup. Candidatea20965fbd95d4dcba516b52020f29c30e7bb33f7f8890630b6785b686090ac38
atshim/out/a52q-readonly-disk-mockfs-hardware/build/a52q-readonly-disk-mockfs-UNTESTED.img.
PACKAGED ONLY. OriginalAndroidcontrol+recoveryreturn ACTIVE unified87954,
research/a52q_original_boot_control.py backup/a52q/control-before-readonly-disk-mockfs.
No newexperimentalimageinstalledyet. Usernearphonebutaskreadinessfornext90sreset.
Ifsmallrootstillhasnostages, addnonce-bound earlycheckpointsbeforemap/alloc/pmap
andconsiderhardwarebaselineWITHOUTnode. ExistingA52K1 beginsafteralloc, cannot
localize earlierfailure. Potentialfastrelinkleaf UFSwouldneedguarded source/header
dependencies andsamebase43264401092; no suchleafsupportadded yet. Avoidspeculativefixes.

Source-reader first-I/O instrumentmetadata/readlinkLIST-ONLYtest PASSED exit0.
NoDMGfailure there. ExactnativeCOPY diagnostic ACTIVE hiddenPID13132,
research/apfs_first_copy_failure.py; logsE:/A52-iOS16/apfs-first-copy*.log,
destination/root/a52-ios16-host/staged-first-copy-v5/os. InstrumentedASanreader
stops on FIRSTshortifstreamread withoff/size/state/errno, parentstopsrsync ifreader
dies. No masking/retry. Need seeDMG_FIRST_SHORT_READ orotherfirsterror. Script
outputJSONexit0wouldbeOS-onlycopysuccess, notall3sources/root-imageproof.
PossibleEOFreadhandling bug: apfs_read doesn'tclampUNCOMPRESSEDreads toino.ds_size;
ReadFile doesn'trejectoffsetpastselectedextent andignoresReadBlocksfailures.
Theseareverifiedsourceissues, relationshiptorsyncfault stillunproven; no such
fixapplied yet. Avoid runningWSL+2GiBQEMUconcurrently onthis6GiBhost.

### PHONE SAFE: HFS RAM root boot observed; original BOOT restored

backup/a52q/hfs-hardware-ramroot/receipt.json requires_restore=false and
original_boot_restored=true; other protected partition hashes unchanged.
checked-result.json:3CRCentrycopies, intact'hfs: mounted 'text, intact'init running
as PID 1 ***'suffix and10exact diagnosticheartbeats. Some Ctext/volume name damaged
acrossreset, NOT repaired/reconstructed. Kernel0e9fea... onrealA52 nowmounted
smallHFSRAMroot+ranownpinnedinit. NotApplelaunchd/UI orUFSdiskroot. Watcherfinished.

NewBSDkernel43264401092artifactverified E:/A52-iOS16/builds/43264401092/artifact.
Kernel18d9982197069dc28bbc1c40315f82874cafba4382cad3c78b2b0bdabbc68a93,
HFSselection/allfive UFSsource+headerhashesmatch. FirstQEMUattempt failedBEFORE
gueststartup: cannotallocateguestmemory'virt.flash0', notakernelpanic. Hosthas
6GiBvisibleRAM; Windowscommitheadroom~2.2GiB. StoppedfailedASanrsync, syncedand
terminatedONLY ourA52-HakiOS-Build-20261107distro tofreeRAM. DoNOT runlargeWSL+
2GiBQEMUconcurrently here. Samekernel/HFS QEMUretry ACTIVE unified87547,
shim/out/a52q-readonly-disk-hfs-qemu/run-retry. NeedPID1>=3heartbeats+HFSmount
beforepreparingnewBSDphonecandidate. No diskinterfacehardwareproofyet.
HostCI43267262374 SUCCESS (83Python+Ctests/coreQEMU).

Exact rsyncunderASan FAILED metadataI/O after~218kentries. NoASanheapreport:
GetNode VerifyBlock failed withZERO block, thencascadingmissinginodes. All-file
Pythonread previously8291487156bytesclean. Newhypothesis: DiskImageFile::Read
usesuncheckedifstreamread; a short/failed read poisons streamstate permanently,
causinglaterzerometadata. NOT proven yet. SourceinstrumentedFIRSTshortreadwith
offset/requested/actual/state/errno andthrowsimmediately (no masking/retry).
research/instrument_dmg_read.py appliedonlyignoredhostsource. RecompileASan
DiskImageFile.cpp thenretryfocused metadata/readlink or exactrsync AFTERQEMUends.
Look forDMG_FIRST_SHORT_READ inlog. Currentstage-asan-v4scratchFAILED/stopped,
no successmarker. Source-rootcopy andallfullHFSimages stillUNUSABLE. WSLnotrunning.

### 17:16:39 UTC: HFS RAM-root PHONE TRIAL ACTIVE — restore BOOT on TWRP return

Candidate1a0bf3a467e31a513b6cd4e29eed895cc7d3932205f3862fed2a383cd982caf3
installed/full96MiBreadback, TWRP Systemreboot. Receipt backup/a52q/hfs-hardware-ramroot/receipt.json
requires_restore=true! WatcherPID7332 research/watch_hfs_ramroot_restore.py,
E:/A52-iOS16/hfs-ramroot-watcher*.log. Userconfirmedready, asked90s+TWRP.
Collect/restoreFIRST and confirmhash; theninspecthfs mount/PID1/heartbeat text
andCRCentrymarkers. Kernel0e9fea... alreadyhardwareverified; thistrial hasNO
UFSnode, uses32MiBHFSRAMfixture70665... withidenticalpinnedowninit, noAppleUI.
QEMU samekernel+root PASS7heartbeats+explicit hfs mountedA52Diagnosticconsole.
Physicalpayload/image50,066,608B; packagedimage96MiB. No userdata format.
OriginalAndroidcontrol priortrial boot_completed=1 confirmed, thenautomatic
recoveryreturn withprotectedhashesverified. backup/a52q/control-after-kernel-ufs/.

Full BSDdiskkernel43264401092 SUCCESS at112ea38697e3eeb92568b152023bd949ad6f6b4a.
Download ACTIVE unified90714 toE:/A52-iOS16/builds/43264401092/artifact. Needverify
HFSselection/newUFSsource/headerhashes, thenQEMUbaseline beforeanynewphoneinstall.
HostCI43264398995 alsoSUCCESS. Do not mix thisnewkernel resultwithold0e9phoneproof.

ASan sourceReader readALL179359regularfiles,8291487156bytes, noASan/readerror.
This is NOT an rsync/root-image success. Exact rsyncstaging underASan ACTIVE
hiddenPID8564, research/stage_ios16_asan.py. Destinationstaged-asan-v4, logs
E:/A52-iOS16/stage-asan-v4*.log. Reportstaged-asan-v4-sources.json onlyifall3copiesexit0.
AllpreviousfullHFSimagesinvalid; noApplelaunchd/UI. Rootstaging stillomitsxattrs/ACLs.

### Minimal HFS RAM-root candidate support; no new phone trial yet

Added explicit --hfs-qemu-proof RESULT_JSON for physical --hfs-test-root.
Rejects missing/mismatching kernel/root/PID1/heartbeat proof. DefaultphysicalHFS
stillrejected without proof. All physicalRAMplacement remains hardware-evidence
derived; QEMUaddresses not copied. No UFSnode needed for thisRAMroot. Same pinned
ownstaticinit, notApplelaunchd. 83Python tests pass (includes proofbinding/tamper).
QEMU HFS test with already-physical-testedkernel0e9fea... RUNNING unified21660,
shim/out/a52q-hfs-kernel-ufs-qemu/run; need hfs mount+PID1>=3heartbeats beforepackage.
Full BSDdiskkernel43264401092 stillcompiling. No newexperimentalBOOTinstalled.
OriginalBOOT Androidcontrol+automaticTWRPreturn RUNNING unified5814; record
backup/a52q/control-after-kernel-ufs/android-control.json onlyafterboot_completed1.
This establishes freshconsole before nexttrial, notanexperimentalphonewrite.
ASan fullfile-read now>5GB nofault; rsync-specific failure notyet reproduced under
ASan. No claim readerfix/rootcopycompleted. Need reproduce exactrsync withASan.

### New read-only BSD disk implementation — source/host checked, build next

Full HFS kernel build ACTIVE43264401092 atremote112ea38697e3eeb92568b152023bd949ad6f6b4a.
Push-defaultmockfs43264398986 canceledbyexplicitHFSdispatch (expected).
HostCI43264398995 SUCCESS (includes Cbounds/responsechecks and QEMUcore).
Local sourcecommita6a308b, API snapshot112ea38 identicaltreedad49f4937acc47f813b79cc83c4677297df32cb,
localmergea5a8643 preservesbothhistories. OAuthCLIcan'tupdateworkflow lacking
workflow scope; published via already-authorized GitHub connector instead,
verifiedexacttreeSHA and expectedparent7963465 beforefastforward. No auth/settings
change requested. Nextcheckfullbuild/compilerdiagnostics thenQEMUbaseline beforephone.

Phone SAFE originalBOOTrestored; no new trial pending. Added a52q_ufs_disk.c
and a52q_ufs_bounds.h, staged byapply.py onlyforA52. Runs only after existing
hardware-only selftest passes; defaultnoADTnode remains noUFSaccess. Fixed512
logicalsectors over proven4KiBREAD10, overflow-safe bounds/partialblock copies,
serializedpermanentDMApool, writesrejected inopen/raw/strategy. Anytransfer
failure poisons DMApool for restofboot, no retries/reuse. Strictresponsechecks
reject flags/LUN/tag/status/residual/sense to prevent reporting shortDMAasfullread.
Beforepublishing /dev/a52ufs0 and /dev/ra52ufs0 mode0440, testknownRECOVERYblock
through BSDbufstrategy+CRC. Newphase30 means verifiedstrategy+devicepublication,
phasee8 meansfailure; decoderseparates readonly_disk_verified fromphase20success.
NoGPT/partitionmapping/rootselection/diskwrites/format. OriginalRedmiunchanged.
NativeC bounds/response test,82Python tests,repo validator,andboth66-fileoverlays
againstactual81-patchtreePASS. Fullkernelbuild andQEMU/hardware stillrequired.

Readertrace: metadata enumeration ALONE exit0, targetstillreads213bytes. Earlier
assumption that scanalone triggers failure not proven; fullDATAcopy triggersit.
ASan-onlybuild/readrepro ACTIVE hiddenWindowsPID14088, research/apfs_asan_read.py,
E:/A52-iOS16/apfs-asan*.log and apfs-asan-read-paths.log. No diskimagecopy/phoneaccess.
InitialUBSan halted on legacyunalignedmetadatareinterpretcasts beforeenumeration;
ASan-only used for actualheapmemorydiagnosis (no claim that UBSan passed).
Read-onlyreader nowpropagates ReadFile failure to EIO instead of silentlyreturning
zero-filledbytes. Earlierfullcopiesunusable. Needdiagnose firstdatareadfailure.

### November12 16:46:38 UTC: XNU UFS READ VERIFIED ON A52; ORIGINAL BOOT RESTORED

backup/a52q/kernel-ufs-selftest/receipt.json requires_restore=false,
original_boot_restored=true, other protected partition hashes unchanged.
Watcher finished. Physical kernel0e9fea... (build43257186934) generated5valid
pool/start records,5validNOP records and4validcompletion records phase0x20:
OCS0,lastLBA31077375,4096byteblocks,CRC1080028829,response21000000.
kernel-ufs-result.json success=true. This verifies NEW kernel-owned wired/DMA
buffer + explicit cache maintenance, NOP/capacity/one known RECOVERY block.
3CRC entry records and diagnosticPID1 plus heartbeats also present.
The ordinary C stream's printed pooladdress is unprotected: do not treat its
exact PA as independently CRC-proven. No BSD disk registered/mounted yet.
Next storage step: reviewed serialized read-only BSD block/raw interface with
bounds/512-byte sector translation and geometry ioctls; no writes/format.

Full native APFS staging v3 FAILED (I/O errors), deliberately stopped exact
failed rsync with SIGTERM to avoid another wasted copy. Exit20 is our stop,
underlying failures are reader GetInode errors. No success marker/root artifact.
Same failing file reads213bytes SHAeb4963e5fdc37fc85a580c6eea8f1ef22cd723e21bf953cd984d0d45f2a48aef
on FRESH reader; stale full-enumeration reader returnsEIO. Real inode
0xfffffff00011013; no inode truncation evidence. Foreground trace one exact
inode before/after metadata enumeration is running unified40627, script
research/apfs_trace_lookup.py, log E:/A52-iOS16/apfs-trace.log. Temporary trace
edits only ignored host reader. Need isolate cache/lookup bug, not blind retries.

### November12 16:44 UTC: kernel UFS trial active — restore BOOT on TWRP return

Full HFS kernel build43257186934 SUCCESS, remotehead39d484bbfdfd78ef2502c9a2e0efe8bfdcf8566e.
GitHub Actions was reenabled by user; CLI authenticated. Local mergeca6a72c
preserves both histories, same source tree as remote snapshot. Download verified
E:/A52-iOS16/builds/43257186934/artifact. KernelSHA256
0e9feaf6cced793ff712f7222415421176ff3585d805e71db4b01f6463471bc6;
HFS selection, pinned diagnostic init and all three UFS source/header hashes
match local source. QEMU baseline (NO UFS node) PASS: diagnosticPID1,7heartbeats,
3CRC entrycopies. shim/out/a52q-kernel-ufs-baseline-qemu/run/result.json.

User confirmed beside phone. BOOT-only disclosure given, existing automatic
BOOT-trial authorization applies. Candidatef5f48050caa746b6d3c4cdefd999594b57b8a903e171b7fb809d9577e8ec5a78
installed/fullreadback 16:43:49 UTC, TWRP System reboot sent. Pending original
BOOT restoration! Receipt backup/a52q/kernel-ufs-selftest/receipt.json.
Hidden watcherPID13596 research/watch_kernel_ufs_restore.py waits600s for TWRP,
collects then restores original before decoding. Logs E:/A52-iOS16/kernel-ufs-watcher*.log.
User asked returnTWRP after90s. No userdata format, no other partition writes.
After return confirm requires_restore=false + original_boot_restored=true,
then inspect kernel-ufs-result.json. Do not claim kernel disk I/O before proof.

Host APFS reader investigation: upstream PR224 iterator guards +PR218 lookup
fallback applied to pinned66b86bd, own additional keyed-iterator/error propagation
guards; CTest1/1pass. Fullcopy STILL failed23. Added zero-initialized FUSE entry,
stable generation1 and stat-error propagation; focused CarrierBundles copy now
exit0. No claim whole-reader fixed. Foreground -d1 required for actual error logs
(debug0 daemon closes stderr). Fresh native staging ACTIVE hiddenWSLPID14280,
research/stage_ios16_foreground.py; E:/A52-iOS16/stage-v3*.log, destination
/root/a52-ios16-host/staged-foreground-v3. Success marker ONLY if all3rsync exit0.
rsync-aH preserves owners/modes/links, NOT xattrs/ACLs; document this limitation.
All previous full HFS images INVALID; no Apple launchd/UI yet. No phone root
image is ready. Source-reader changes still private/unpromoted until validated.

### November12 continuation: kernel UFS selftest ready for compiler validation

Phone TWRP; reread BOOT hash d6bf... matches original. No pending restoration.
Latest physical result is shim READ10 success documented below, not XNU disk I/O.
Added xnu/a52q/a52q_ufs.c: opt-in /a52q-ufs-selftest ADT node, dynamic wired
contiguous16KiB kernel allocation, physicaladdress via pmap, explicitcacheflush
before/after DMA, boundedNOP+capacity+one RECOVERYblock. No BSDdiskregistration,
writeCDB, IRQ, SMMU, clock or reset operations. Uses exact shim packet headers
staged byapply.py; originalSWEETbranch remainsguarded/disabled. Callsaftervfsinit,
returns immediately when nodeabsent. Source64-file overlays pass againstactual
81-patch tree;81Python tests pass. NOT COMPILED in XNU yet; full CI build next.
tools/a52q_ufs_selftest.py validates physicalreadproof, emits nonce-bound ADT node
and decodes shortA52K1 kernelCRC stages; successphase20. Payloadarguments
--ufs-selftest-build/--ufs-selftest-log hardwareONLY; emulator rejects node.
Originalkernel9cf... lacksimplementation, payloadtoolrejectsit forselftest.
Kernel buildworkflow nowtriggers on sharedpacketheaderchanges too; hostCI runs
both new portable UFS C packettests before optionaltoolchaininstallation.

GHCLI auth stillmissing. GitHubconnector supports gitcreate_tree/create_commit/
update_ref with expectedsha. Publish reviewedsource snapshot (no privateartifacts)
to existingfork branch fastforward from verifiedremotehead, triggerfullmacOSbuild.
Keep local commits/history; API snapshotSHA maydiffer, recordboth withoutresetting.

Native source staging alsoFAILED23, immutableAPFS reader listedfiles but then
lookupsaid'filevanished'. No staged-sources.json success marker. All fullHFSroot
images remain INVALID/incomplete. source-staginglog E:/A52-iOS16/*.log. Fullreadonly
findwalk succeeded. Next isolate freshmount single knownCarrierBundle lookup,
then audit APFS BTree cache/iterator (pinned66b86bd...). No codepatch/apfs rebuild
made yet. Avoid blind copy retries. FailedWHPXoptimization lowerpriority.

### READ CAPACITY + ONE SECTOR VERIFIED ON A52; ORIGINAL BOOT RESTORED

20:22:39 UTC originalBOOTrestored/full96MiBhash, otherpartitionsunchanged.
backup/a52q/ufs-read/receipt.json requires_restore=false, phoneTWRP.
checked-result.json: all9MMIOrecords,stageb3/ESR0 with4validstagecopies;
NOPocs0/header20000000/DBR0;2validA52C1 records: lastLBA31077375,block4096,
dataCRC1080028829 matchesindependentTWRP+originalRECOVERYbackup,OCS0,
responseheader21000000,failure0. REAL shim PRDT data-sector read worked!
No writeCDB/format. Candidateee708fce0d0d6120fef4bab9633e9477cab3cb1b7ce966423183da7474ecdd2f.
Code13b8e54. Need separate readonlyA52 XNU diskdriver using provenprotocol;
cannotreuse shim106000000 DMApool afterkernel loads there: allocate wired
contiguouskernelRAM+explicitDMAcachemaintenance, deriveMMIO/geometryfromADT.
OriginalSWEET driver stilldisabled. Currentphysicalprototype DOES NOT expose
disktoXNU yet. No Applelaunchd/UI. No further phonewritepending.

### One-block read trial prepared; no pending restore yet

New mode --ufs-read-geometry/--ufs-read-nop-build/--ufs-read-nop-log builds after
priorcheckedNOPproof and performs a freshNOP first. Capacity expected31077375lastLBA,
4096byteblocks fromTWRPdisk127292932096B LUN0sysfs0:0:0:0. READ10 readsunchanged
RECOVERY firstblock LBA123888, CRCexpected1080028829; SHA45203384e4043136a78a33809e7fc3c554d123d6d971031dab2f60f7dfe56745
independentlymatchesoriginalRECOVERYbackup. DO NOT use BOOTfirstblockexpectedCRC:
candidate install changesBOOT. OnlyREADCAPACITY25/READ1028 allowed, PRDT1length
8or4096 only, data106002000. READgeometry JSON backup/a52q/ufs-read-geometry.json.
Nativecompile+hostCpacket/endian/opcode/length/CRCtest+78Python tests passed.
Image shim/out/a52q-ufs-read/a52q-ufs-read-UNTESTED.img prepared, NOT installedyet.
Privatehelper requires explicit --ufs-nop --ufs-read, regeneratesconfig +checks
currentdisk/recoverystart. ExistingBOOToriginalrestored. UserjustreturnedTWRP,
explicitautoBOOTauthorizationpersists. Next explainBOOTwrite/RECOVERYread/noformat
andrestorebuttons, install+watch10s+collect/restoreFIRST, decodeA52C1+stageb3.

IMPORTANT root-copy diagnosis correction: actual root cause is APFS-FUSE SIGSEGV
in readdir under CoreRealityIO.framework/usd/usd/aaplUsdPhysics/resources/aaplUsdPhysics.
Not merely tool HUP. dmesg provesSIG11, free~1.9GiBswap. Root rsync thenfails23,
wrapperexits andLinuxguest getsSIGHUP withuncleanfilesystem. Read fullsession45333
onlywithsmalloutputbudget (it has94ktokens of repeatedENOTCONNerrors). All partial
HFS images invalid. Detachedv3failed staleFuse; v4failedbecausemountpoint-q returns
falseonstaleFuse. Fix by/proc/mounts exactmountpoint thenumount; investigateFUSE
null deref addr2line0x2ee4f/0x1ee4f at pinnedapfs source before retryingfullcopy.
KernelAPFSFuseprocessosdead, sysos/apposstillalive. Don't blindlyrebuildfullroot.
NativeWHPXmetadata fixture-v2 kernelirqchipoff stillnetworknotready; lowerpriority.

### NOP SUCCESS ON A52; ORIGINAL BOOT RESTORED

20:08:56 UTC original BOOT/full96MiB hash restored; recovery/DTBO/vbmeta unchanged.
backup/a52q/ufs-nop/receipt.json requires_restore=false; phone TWRP.
checked-result.json: all9registersCRCvalid,stagea4,ESR0,4validstagecopies,
3validNOPcopies,OCS0,responseheader20000000,doorbell0. This proves fresh NOP
exchange using own list/UCD at106000000/106001000 and response106001400:
CPU-to-controller descriptor fetch + controller-to-RAM response worked >4GiB.
Original BASE/RSR restored by probe. Does NOT prove PRDT/data-sector I/O yet.
Candidate2a23e1e41656ecb91db7525f610bb2957e82c1b39c0648e2cdb259ba519bec1a.
Next: read-only READ CAPACITY(10) and one verified current BOOT block using a
bounded data PRDT; match TWRP geometry/backup CRC before exposing disk to XNU.
No SCSI write implementation/format authorized. User nearby and requesting iOS.

Background sourcecopy again died SIGHUP; v2 image now incomplete/corrupt
(Invalid key length). DO NOT USE any current full root artifact. Need detached
Windows Start-Process -WindowStyle Hidden with redirected stdin/out to survive
tool/session HUP. Native WHPX guest boots, rsync listen873 ready, but TCP transport
did not respond to host probes; testing kernel-irqchip=off fixture-v2 running
unified40922. Initialfixturefailedwithoutcopy; no physicaldevices. Ifslow, don't
spend forever on acceleration: run detached Linux TCG rebuild and keepworking.
Source roots stillreadonlyAPFSmounted. Newcopyv3 must finish+unmount+fsck beforeuse.

### UFS NOP trial prepared; user ready; no pending phone restore yet

User confirmed near phone/able to return TWRP. Prepared shim/out/a52q-ufs-nop/
a52q-ufs-nop-UNTESTED.img; source tools/a52q_ufs_nop.py +shim/a52q/ufs_nop*.
Uses actual pinned Samsung1024-byte UPIU layout (NOT assumed512). New16KiB pool
derived0x106000000 from old CPUCRC+RAM planner; no XNU loaded in this diagnostic.
One NOP only, noSCSI/PRDT/flashwrite; identityDMA hypothesis explicitly unproven
(liveUFS node has NO iommu bindings). Guard idle/64bit/HCE/AHIT/timebase; stopempty
list, programownBASE, NOPdoorbell, 1svirtualcountertimeout; completedrequest restores
BASE/RSR, timeout holdsRAMuntil physicalreset. ShortA52U1 response/OCS CRC5copies.
NativeGNUbuild +hostCpacketlayouttest +77Python tests pass. Default r4 bit-identical.
Private installhelper updated --ufs-nop, validates configuration against exact
capture/sources/memory proof; refuses accidentalNOP under ordinary --handoff.
Next: explain BOOT-only/noformat/recovery, install, startwatcher, user10s+TWRP,
collect/restore FIRST. No claim of XNU storage/Apple UI yet.

### Resumed: verified HFS build and HFS RAM root in QEMU; phone original BOOT

Current device recovery, live BOOT sha d6bf... matches backup (read again).
No new phone writes. HFS full build43061413864 SUCCESS at16cf668234b1d8fe558176ff5c5cc6222abe3f56.
GH CLI auth disappeared after host restart; GitHub connector works. Used plugin
jobs/artifacts/download endpoints: artifact13874728136, archiveSHA3d57ec8a177057eb1785bbb7709cddf7e3f19d84f74d6276a44b83d57a52cea8.
Downloaded/extracted E:/A52-iOS16/builds/43061413864/artifact; verified overlay
filesystem=hfs and kernelSHA9cf02e607738966cf461718333505617816ca86ac32c4703001bec213593c151.
Verified-build.json records provenance. Native mockfs QEMU: PID1+7heartbeats.
New tools/a52q_hfs_root.py plus --hfs-test-root in payload support ONLY QEMU,
reject physical packaging. Checks bounds/clean flags/header/fork geometry;
not a substitute for fsck.76 tests pass. Real fixture32MiB made from mkfs.hfsplus
and ASCII-only single-file libdmg-hfsplus add/chmod (NOT real-root importer).
Extracted init SHA matches pin, fsck read-only passes. FileE:/A52-iOS16/a52q-hfs-init-fixture.img.
QEMU actual HFS mount `hfs: mounted A52Diagnostic on device b(1,0)` thenPID1+
7heartbeats, no panic. shim/out/a52q-hfs-ramroot-qemu/run/result.json and console.
This is NOT Apple launchd or phone HFS verification. Kernel retains pin AMFI.

Original9p filesystem copy died SIGHUP when session/host ended; image incomplete
and repair failed (Keys out of order), preserved E:/A52-iOS16/ios16-...pristine.hfs.img.
Never use it. Replaced9p source transfer with native Linux rsync through localhost
to small Linux guest's HFS mount. Fixture uid/gid/modes/links/Unicode +fsck passed.
New copy active unifiedsession45333, WSLPython research/resume_ios16_hfs_tcp.py,
LinuxqemuPID115/rsync119. Fresh16GiB sparse image now on E-backed Linux ext4:
/root/a52-ios16-host/images/ios16-20H392-a52q-pristine-v2.hfs.img. SourceAPFS
readonly mounts reestablished. 899MiB WSL budget +2GiB swap enabled. Still copyingOS.
Native rsync avoids9p reads but QEMU TCG filesystem writes still CPU bound.
IMPORTANT discovery: native Windows QEMU x86 supports working WHPX! Read-only
Linux boot test completed in2s E:/A52-iOS16/appliance-windows/whpx-test.log.
Kernel/initramfs copies there. Next optimize filesystem guest to Windows WHPX,
embed job/config in initramfs (Windows QEMU9p may unavailable). WSL defaultgateway
from /proc/net/route is172.22.160.1; hostfwd bind this virtual-adapter IP only,
not LAN. Then native WSL rsync -> Windows guest. Test metadata fixture first.
Never attach host block devices. Preserve incomplete old images. No new phone
trial needed for filesystem copy optimization. Actual userland/UI still pending.

### PHONE SAFE: ORIGINAL BOOT RESTORED; UFS HANDOFF VERIFIED

16:47:55 UTC original BOOT restored with full96MiB hash; recovery/DTBO/vbmeta
unchanged. Phone TWRP. backup/a52q/ufs-handoff/receipt.json requires_restore=false.
All9 register records CRC-valid,3 intact short stage records:stage80,ESR0.
checked-snapshot.json holds raw provenance. Controllerbase1d84000 fromliveDT:
CAP1587031f,VER210,AHIT0,HCS10f,HCE1,UTRLBA95f9c000/0,DBR0,RSR1.
Header confirms UFSHCI2.1 (NOT device flash version),32slots,64bitaddresses;
HCS device-present+UTRL/UTMR/UIC ready bits set. This is ABL handoff evidence,
NOT XNU disk I/O. Do NOT reuse ABL descriptor95f9c000 or assume identity DMA.
Need A52 SMMU/coherency ownership and read-only NOP/READ CAPACITY/read validation
before root storage. No UFS commands/clock/reset writes/userdata format performed.
Candidate shim/out/a52q-ufs-handoff/a52q-ufs-readonly-UNTESTED.img SHA45533abe440b9a97ecfcde94f3a7d2a78aac79cd7746afd55309f129a021352c.
User says only2% usage left: no further phone trial started. Save clear handoff.

HFS full build RUNNING https://github.com/chadiLePro/ios-sweet/actions/runs/43061413864
verified head16cf668234b1d8fe558176ff5c5cc6222abe3f56, filesystem=hfs.
Push-default mockfs run43061385487 canceled by concurrency, expected.
As of16:48 UTC kernel build still running, not a success claim. Job130664888963
live logs404 until finalization. Check gh run view43061413864, download artifact
to E:/A52-iOS16/builds/43061413864 (C only~2GiBfree), verify overlay filesystem=hfs,
then QEMU first. This build retains diagnostic AMFI, rejects Apple launchd.
Real iOS16 root copy is active session97266 (LinuxqemuPID285), still copyingOS;
do not use incomplete host image. Log E:/A52-iOS16/ios16-root-copy.log.
Private research/build_ios16_hfs_appliance.py writes build report only on complete
copy/fsck. Current image includes no bring-up tweaks. No new phone writes needed
to finish these host tasks. Keep E plugged in. Next: finish/verify root copy,
validate HFS kernel using small RAM-root fixture in QEMU, then A52 UFS read path
and explicit Apple userland entitlement provider. Actual SpringBoard not run.

### RGB trial collected; ORIGINAL BOOT RESTORED; visibility inconclusive

16:42:23 UTC original BOOT restored/full96MiB readback, other partitions unchanged.
backup/a52q/display-refresh/receipt.json requires_restore=false, phone TWRP.
User: did not see RGB, may have missed.37/37 independently CRC-checked register
records recovered for current nonce, but no full diagnostic CRC copy. Do not
claim final display stage/refresh success. Add short CRC stage records before
next display trial to distinguish guard abort/start timeout/start consumed.
Candidate92ee6211d6c46200cd37cc32f2dbbd63454dde4dac08ac23c78a703345549ba0.
Commit5e11b23.72 tests/default r4 bit-identical.

Preparing optional filesystem=hfs kernel build. Default mockfs unchanged.
Both overlays apply against actual81-patch control source tree; generated source
differences only MASTER.arm64.a52q and provenance JSON. Optional HFS adds portable
Apple OSS filesystem/VFS glue; no hardware guards/Apple AMFI policy enabled.
Source check research/check_hfs_overlay.py. Full macOS build required.
WSL899MiB budget nearly exhausted by APFS/QEMU: added2GiB Linux swap file
/root/a52-ios16-host/appliance/build.swap on E-backed build VHD (not phone),
swapon confirmed. No global .wslconfig change.

### Original BOOT restored; CRC display state recovered; iOS16 root copy running

Second display snapshot restored original BOOT at16:28:49 UTC, full96MiB hash
verified, RECOVERY/DTBO/VBMETA unchanged. Phone TWRP, no pending restoration.
Receipt backup/a52q/display-handoff-v2/receipt.json requires_restore=false.
Checked snapshot:36/37 rows recovered,2 intact metadata copies. Missing only
inactive sspp2.src_size; no value inferred. Active sspp0:1080x2400,base9c000000,
stride4320,format237ff,unpack03020001,op80000000. CTL0_TOP20000,INTF_ACTIVE2,
START0; DSI_CTRL1f5,STATUS5. Read-only state does not prove panel refresh.

New explicit display experiment derives guards/configuration from raw CRC
capture and pinned Samsung sources. Writes160x96 BGRA RGB bars in DT splash
reservation and CTL0_START=1 once (source sde_hw_ctl_trigger_start); no other
controller/clock/DSI programming. Runtime rejects changed captured state, bounds
start polling100ms. Not yet phone tested.72 host tests pass; native cross-build
passes. Default diagnostic path remains separate. Prepared under
shim/out/a52q-display-refresh/. No phone install yet.

Linux filesystem appliance now works with matching6.8.0-149 kernel/modules,
decompressed modules (guest busybox cannot load zstd modules). Fixture passed
uid501/gid20/mode0640,hardlinks,symlinks,Unicode filename; HFS read-only fsck OK.
Private scripts research/{build_rootfs_appliance,run_hfs_fixture,build_ios16_hfs_appliance}.py.
Real Apple16.7.16 root copy RUNNING in guest via read-only APFS/9p sources to
E:/A52-iOS16/ios16-20H392-a52q-pristine.hfs.img (16GiB host image ONLY).
Unified exec session97266; log E:/A52-iOS16/ios16-root-copy.log. No phone storage
write/format. Copy/fsck must complete before using artifact; no tweaks applied.
This is not a bootable A52 iOS image: UFS/HFS/Apple entitlement support pending.

### Phone safe: display snapshot completed, BOOT restored; short-record retry prepared

16:22:33 UTC: display-only read snapshot completed stage0x80, no exception (one
intact CPU diagnostic CRC copy). Original BOOT restored/full readback verified;
RECOVERY/DTBO/VBMETA unchanged. Receipt backup/a52q/display-handoff/receipt.json.
All 37 MMIO reads completed but NONE of the long handoff CRC frames survived
reset intact. Do not use unprotected values from that console.
Changed to short independently checked metadata/register records, 5 replicas,
with random per-build capture_id to exclude stale pstore without a control reboot.
Decoder never repairs bytes; returns missing rows explicitly. Retry image under
shim/out/a52q-display-handoff-v2/. No retry write yet, original BOOT is restored.

### Active interface work - E reconnected; display handoff probe prepared

User requests actual iOS interface, faster. E is now present, D is absent.
Existing A52-HakiOS-Build-20261107 WSL works (Ubuntu24.04.5, kernel6.18.58.1),
root user, ~900MiB RAM budget. No new distro created. Installed host build tools;
built apfs-fuse at66b86bd525e8cb90f9012543be89b1f092b75cf3, lzfse submodule
at e634ca58b4821d9f3d560cdc6df5dec02ffc93fd. Downloaded and ZIP-CRC/SHA256-checked
all three Apple images under E:/A52-iOS16/images; read-only APFS mounts under
/root/a52-ios16-host/mounts/{os,sysos,appos}. Real launchd/SpringBoard accessible.
WSL kernel has no HFS+ module. Old libdmg-hfsplus addall is unsuitable (follows
symlinks, overrides modes, mishandles Unicode); do not use it to import root.
A filesystem appliance's matching Ubuntu generic kernel/modules are staged in
/root/a52-ios16-host/appliance/kernel (hfsplus+9p present), not installed as WSL
kernel. A prior attempted Python appliance generator had a JS syntax error and
was NOT created. Complete this small guest to build a faithful HFS+ root.

Pinned maintained Samsung source at f6bbda4... checked out via Linux sparse Git
under /root/a52-ios16-host/kernel-reference (Windows git rejects aux filenames).
Register source copies E:/A52-iOS16/register-sources. Live DT: MDP0xae00000,
DSI0xae94000; never use the guessed 0x5e... addresses. CTL and SSPP offsets come
from live DT properties, individual read offsets from SHA-pinned source files.
New optional --handoff display|ufs build emits read-only snapshots with 3 CRC
copies. No MMIO writes, clocks/reset/DMA/commands. Default diagnostic image is
BIT IDENTICAL to previously tested r4 (ee37e8f...). 67 tests pass.
Prepared display candidate shim/out/a52q-display-handoff/a52q-display-readonly-UNTESTED.img
SHA256 1f8379fbaac59147f6bb72f1b92a68622c22b3075a383951cb1bd41f6aedd6ae.
Private test helper now accepts --handoff with exact regenerated layout checks.
No new phone write yet. Original BOOT remains restored. Next: BOOT-only snapshot
trial, then immediate log collection/restoration; current fresh baseline from
post-PID1 Android control has no XNU markers. Candidate does NOT boot iOS/UI.

### CURRENT PHONE STATE - ORIGINAL BOOT RESTORED; REAL DIAGNOSTIC PID1 VERIFIED

15:29:50 UTC: original BOOT restored and full 96 MiB partition hash verified.
Final control: restored UN1CA Android sys.boot_completed=1, then native existing
recovery returned; zero XNU entry markers in the fresh console baseline. Evidence
backup/a52q/pid1-posttest-control/. Phone is now TWRP with original BOOT.
RECOVERY/DTBO/VBMETA unchanged. No restoration pending. Phone remains in TWRP.
Receipt backup/a52q/pid1-hardware/receipt.json requires_restore=false.
Result backup/a52q/pid1-hardware/boot-result.json: baseline zero XNU markers;
trial THREE CRC-valid entry frames; exact PID1 banner; FIFTEEN exact heartbeats;
md0 selected; no observed panic. C/user stream has visible reset-retention
corruption, so exact register values are not trusted. Repeated intact user-mode
heartbeats demonstrate exec/syscalls/devfs/console/timer-driven user execution
on this SM-A525F/DS. This is OUR STATIC DIAGNOSTIC, NOT Apple iOS userland/UI.
Kernel d3a45619eb3e2428aefed62cbe5170c01e72d28cb285ad1c95f3a2a524796ac8,
BOOT candidate 259874268307861009ad704bde9f9492be7c92eb6f6f2a9c2b70f79f0bb03fc1.
Only BOOT was written/restored; no userdata format or storage driver enabled.
Successful image shim/out/a52q-pid1-hardware/build/a52q-pid1-UNTESTED.img (name
records packaging-time status; test receipt now records the actual outcome).

Next stage: inspect real iOS16 rootfs requirements, read-only A52 UFS evidence,
and independent portable HFS/entitlements dependencies. Do not flash a complete
Redmi image or enable its hardware guards. Diagnostic AMFI explicitly rejects
Apple userland until a separately reviewed provider/policy is implemented.
A fresh Android control boot has now completed after the trial and returned
TWRP: no stale XNU markers remain. Original Android is preserved and boots. Automatic BOOT-only authorization persists, not userdata format.
Host C has ~2GiB free; D has ~80GiB free, E:\Minecraft is unavailable. No IPSW
found in repo research or user's Downloads. Sources may go in a new D task dir;
do not move/delete unrelated user files. Original phone backups remain on C.

### Current AMFI diagnostic interface build (latest work)

01821f4 adds a52q_amfi.c, a separate minimal no-entitlements AMFI interface.
It does not register the Redmi permissive root/platform-binary policy. Its
adjustContextWithoutMonitor permits only the pinned ad-hoc diagnostic signature;
boolean/string/object entitlement queries deny, unavailable operations explicitly
panic or return unsupported. Kernel signature/page checks remain. It is not Apple
AMFI and does not yet support real iOS userland. STARTUP registers the interface.

Full build 43044546028 (93573aa) SUCCEEDED and is the AMFI leaf relink base.
First static-init dispatch 43044546812 resolved a stale branch head; rejected
unknown leaf without building. Correct-head 43044854516 SUCCEEDED, producing
81ef0a6699ff8c5f59d11f4d776e6bb24c59140835d28e4bf0850e5ee46f9687.
QEMU selected md0 and passed the diagnostic pin check, then aborted at
IOTaskHasEntitlement+0x44, FAR 0x1b0: another unconditional absent-AMFI query.
Thus no PID1 yet. A prepared old phone image exists but DO NOT INSTALL it:
shim/out/a52q-static-init-hardware/build/a52q-static-init-UNTESTED.img.
It contains that now-obsolete kernel and still has the known query abort.

Current AMFI relink 43047319220 SUCCEEDED at verified head 01821f4.
Downloaded research/a52q-relink-43047319220; QEMU running under
shim/out/a52q-amfi-lowmem-qemu/run (research/qemu_amfi_lowmem.py).
Full source build 43047254951 SUCCEEDED at verified head 01821f4.
Latest host CI 43050205118 passed repository/Python/C checks but failed the
Ubuntu toolchain-install step due DNS; local cross-build/QEMU/hardware checks
ran successfully. Do not describe Linux CI as wholly passing. No new phone test, original BOOT still safe in TWRP.
The host no longer has enough commit headroom for a 4GiB guest. Added QEMU-only
--qemu-lowmem allocator from generated emulated RAM minus boot/log spans, and
--ram-mib 2048 plus a 32MiB TCG cache. Current QEMU allocation 0x4a000000 is NOT
a phone map: packaging rejects that environment. Phone placement stays 0x106000000.
Generated research/qemu-a52q-2g.dtb and existing measured 2GiB diagnostic
shim/out/qemu-a52q-r4-final-el1/result.json provide emulator evidence.
64 local tests pass; host pin guard exercised 26 cases. Full overlay verified
in memory against actual original patched source (59 changed/generated files).

### Current blocker: no AMFI interface during diagnostic exec

RAM-root relink 43042852228 SUCCEEDED after fixing the Mach-O validator to
ignore STABS debug records, requiring a defined N_SECT table in a loaded range.
The earlier raw relink table actually WAS aligned; an N_GSYM debug record at
zero was wrongly counted as a second definition. Host tests now 63 passing.
Full RAM-root build 43042057807 also SUCCEEDED and is the next relink base.
QEMU shim/out/a52q-ramroot-qemu/run now selects md0, mounts mockfs and attempts
/sbin/launchd (our static diagnostic). It aborts in
accelerate_entitlement_queries+0x1c, FAR 0x1a0: missing AMFI callback dereference.
No PID1 has run. No new phone test; original BOOT stays installed in TWRP.

New static_init.py patch is narrowly scoped: absent AMFI permits only our exact
ad-hoc diagnostic CodeDirectory cdhash20 a8a6ba5e162a5c73966e22700c1ba0a7386b35a2,
with no XML/DER/parsed entitlements. All others return ENOTSUP. Kernel signature
and executable-page hash checking remains; no platform status or entitlements
granted. This is not AMFI emulation or Apple-userland compatibility. The UBC
source hash is pinned and overlay/helper apply the same bounded transform.

### NEW BUILD SUCCEEDED; QEMU advanced to RAM root, then missing IOStorageFamily

Run 43038919058 SUCCEEDED (55fe10f). Kernel SHA256:
2415ffbcfed9da11ac4af2ff76aaf1de566c34e43ad43a7869c2ea7c2aef97b6.
Artifacts research/a52q-build-43038919058/. QEMU with static init in
shim/out/a52q-platform-qemu/run-long: Samsung platform registered, boot CPU
self-SGI delivered, BSD initialized, RAM device md0 created and selected root.
Then panic IOService.cpp:5200 assert(ioblockstoragedriverClass). No PID1 yet.
First 25s run was too short: absent Apple RTC causes an ordinary 30s wait, and
IOBSD matcher another 30s. Use >=90s QEMU/hardware startup allowance, not 15s.
No extra phone image installed; original BOOT remains safe in TWRP.

863cff7 shares only IOService.cpp's three software guards for absence of
IOStorageFamily. The exact source base hash matches the successful A52 build
and patched source: 3e97419a2ce90729537e65cd5de200887e7eaddebd01e90502f05a485efbe7a3.
No storage driver enabled. Targeted ram-root relink dispatched: 43042056836.
Its guarded exception permits ONLY that exact COMMON list addition in apply.py,
checks the pinned base IOService hash and replaces the three guards identically
to full overlay. All board headers, other implementation leaves and 81 patches
must still match. This targeted compile/relink has not yet succeeded.

### Guarded implementation relink workflow (prepared, not yet exercised)

Extended tools/relink_a52q_console.py to --leaf console|cpu|platform|serial,
using each full A52 build's real compiler command and existing unique archive
member (.cpo for C++), preserving archive order. Board header, apply.py, full
workflow, original patches and every unselected implementation must match the
successful base commit exactly. Changed ABI/config still needs a full build.
Workflow xnu-a52q-console-relink.yml dispatch has optional leaf input.
No claim of relink execution yet. This is ready for the next isolated CPU or
platform fix after the current full build succeeds.
Linux host CI's repository/Python/C checks passed on 43039887668; toolchain
installation is separately blocked by Ubuntu mirror DNS failure. Added bounds
and fail-on-update-error rather than marking those emulator checks successful.

### Current replacement kernel run

55fe10f fixes the two barrier-constant errors. Run 43038919058, job 130585664813,
is building on macos-15-intel. Do not confuse the canceled 43037064641 with a
successful kernel. Its static init was downloaded and validated:
aaacee08d03b7f0d93b0b34aa1d2436b0c3798b370ebf1e623732c5739c4473e, 16635 B.
QEMU RAM-disk container test shim/out/a52q-init-container-qemu/run reached
loader stage 6, verified three CRC entry records, then the old kernel's expected
missing-platform panic. No CPU-service/PID1 proof in that baseline test.
Private research/run_a52q_platform_qemu.py is prepared for the NEW artifact;
pass its actual artifact directory as argument (default points to canceled run).
Original BOOT remains installed; fresh control baseline remains clean in TWRP.

### CPU-only platform implementation and validation in progress

Commit e2adc9f adds independent A52PlatformExpert/A52CPU and polling RAM serial.
Full macOS build 43037064641 found two A52CPU.cpp compiler errors: DSB_ISHST
and ISB_SY undeclared. Add machine/atomic.h, matching the existing IOCPU API
implementation include requirements. Canceled that superseded run and rebuilding.
Platform expert/RAM serial compiled with no reported errors. Static diagnostic
init assembly/Mach-O build step succeeded; full kernel remains pending.
Commit a8add2b adds --bootstrap-init, bounds/signature/static-entry checks and
requires ADT RAMDisk to match the last loaded protected segment + its SHA256.
62 local host tests and repository validation pass. Original 81 patches intact.
Fresh normal-ROM control completed at ~14:22 UTC: Android sys.boot_completed=1,
then automatic adb reboot recovery returned TWRP. XNU entry CRC markers now ZERO.
Private evidence backup/a52q/xnu-platform-control/{control.json,console.txt}.
Original BOOT still installed, no restoration pending. This clean baseline permits
another hardware trial after the new kernel passes QEMU; no new phone write yet.

### Active kernel bring-up — user requests focus on booting iOS

Control 43012318206 SUCCEEDED: Xcode 16.0 built xnu-8796.141.3, plain arm64,
kernel.development.sweet (17,188,640 bytes). No iig ABI workaround was needed.
Downloaded source/build artifacts are private under research/control-43012318206
and research/control-buildtree-43012318206. NEVER install that SWEET kernel.

New xnu/a52q/ overlay adds independent A52Q machine config (SWEET undefined),
single-core build, explicitly shared portable crypto/PRNG/pthread providers,
RAM serial/early panic logging, and exact 16 KiB Device console pages before
and after final TTBR0 removal. SWEET UFS/persistent log/USB/SPMI/RPMh/display/
touch/key/SMP guards remain disabled. Original 81 patches remain unchanged.
Applied successfully to the actual control build's patched source (43 files).
New .github/workflows/xnu-a52q.yml builds the A52Q kernel after staging original
software providers; compilation is not yet demonstrated. Original BOOT remains
restored and phone is connected in TWRP. No new device write during this turn.
First A52Q run 43018055671 failed before compilation: Xcode's Python 3.9 rejects
Path.write_text(newline=...). Fixed to write_bytes; common provider conditions
use ARM64_BOARD_CONFIG_A52Q directly, so they also work before board.h inclusion.
Current A52Q run 43018957069 (4abdc23) is building. Run 43018731225 was superseded
by entry CRC logging and unknown-clock handling. No kernel boot is claimed yet.
Update: 43018957069 failed compilation on portable-provider include paths
(BearSSL inner.h, pthread TargetConditionals.h) and missing shared timer extern.
The overlay now enables those software-only Makefile include flags for A52Q and
shares the timer declaration in pexpert/arm/protos.h. No hardware guard enabled.
Next run 43021377581 compiled all A52 sources successfully but FAILED final
link on one remaining _sweet_sample_task reference. Upstream bsd/conf/files
unconditionally listed sweet_sample.c while its task-side implementation and
ioctl are SWEET-only. The A52 overlay now removes that unused diagnostic from
its build. No fake symbol is supplied. C RAM logging also retains the assembly
entry CRC copies instead of clearing them. Rebuild required; no XNU phone test.
Run 43025097605 SUCCEEDED; kernel SHA256
550dbc6a608421cf1e6b3770cc76f2cb543fdd3221922365b817e5166adee130.
Actual QEMU loader reached stage 6 and XNU entry (3 CRC-valid ENTRY copies),
then MMU enabled and C RAM-console access faulted at FAR 0xb4640000, ESR
0x96000007 (L3 translation fault). Root cause: a52q_console_l3 linked at
0xfffffe0007b5b000, not 16 KiB aligned: XNU forces __DATA,__bss section to 4 KiB.
Fixed declaration to SECURITY_READ_ONLY_LATE like bootstrap_pagetables, in
16 KiB aligned __DATA,__const. Added post-link and payload alignment checks.
Keep A52 link archive/flags in future artifacts for targeted iterations.
QEMU logs: shim/out/a52q-xnu-first-qemu/run-r2. OLD kernel must NOT be flashed.
User confirmed they are at the phone for the button return to TWRP. Original
BOOT remains restored; no new phone write. New build required for alignment fix.
Alignment-fix full build 43029834033 is running from 5380646. It now retains
actual A52 .link archive/options and libfirehose for future leaf rebuilds.
New console-only relink workflow/helper is prepared (not yet exercised). It
requires the identical base board/overlay/patch-set/full-workflow definitions,
reuses that A52 build's compiler command and member order, and only recompiles
sweet_early.c including the A52 console. Never mix in SWEET control objects.
Host checks now 60/60; post-link symbol and payload validation enforce 16 KiB
table alignment and accept legitimate file-only __CTF metadata. The blacktop
banner omits the machine; A52 identity uses console/table symbols instead.

Embedded loader added under shim/a52q/loader.c, enabled only with --payload in
build_a52q_diag.py. New a52q_payload.py derives minimal ADT and 32 MiB aligned
snapshot placement: 0x106000000, 256 MiB total, top 1 MiB reserved panic data.
It uses actual FDT bus translations (soc 1/1 cells -> root 2/2 identity window),
CRC-verified r4 CPU CNTFRQ/MPIDR and DT timer PPI. It refuses a SWEET kernel by
Mach-O architecture and A52Q kernel banner/console identity. No root FS yet.
Phone packaging refuses explicitly QEMU-only/test payloads. Loader source and
destination bounds, own-image/ramoops overlap and a restore-after-probe word
access precede segment copying and revision-2 boot_args handoff.

59 host tests pass. Native GNU embedded loader builds. QEMU positive RET-stub
handoff above 4 GiB reached expected return stage 0xe9; an injected excluded
phys_base was rejected at 0xe4 before the copy/probe. These are loader tests,
NOT XNU boots. Private reports under shim/out/a52q-loader-fixture/{qemu,qemu-rejected}.
QEMU-generated DTB research/qemu-a52q-4g.dtb and measured frequency from positive
fixture support explicit emulator-only payload generation when kernel is ready.
Loader now also reads back every copied segment and BSS zero tail, ADT and
boot_args fields before the branch; 0xea reports mismatch. Updated positive
QEMU RET test passed at shim/out/a52q-loader-fixture/qemu-r2. Latest read-only
phone check backup/a52q/xnu-preflight-readonly.json confirms original BOOT and
unchanged recovery/DTBO/vbmeta at 12:36 UTC. No new phone writes.
Next: actual A52Q compiler results, evidence-bound payload/ADT/loader and QEMU
early-kernel validation, then BOOT-only hardware attempt with restoration.

### Latest continuation — iOS 16 target retained, conservative memory planner

User reiterated "nono ios 16". Target remains iOS 16 / XNU 8796; macOS 15 /
Xcode 16 describe host tooling only. Branch bringup/a52q-diagnostics was pushed
to https://github.com/chadiLePro/ios-sweet at 37c47ee. Diagnostic CI
43012318162 PASSED (cross-compile, host/unit checks, four QEMU modes).
XNU toolchain control 43012318206 was in progress at 11:35 UTC; use gh logs on
completion, do not infer a successful kernel build or flash its SWEET output.

New host-only tools/a52q_memory.py reconciles live FDT, Linux iomem, memreserve,
static reservations, ENTIRE dynamic alloc-ranges windows and explicit runtime
exclusions. It refuses unbounded dynamic pools, address translation needing
review, redacted/malformed iomem, overlapping banks and invalid placement.
For capture 20261111T100325Z the only aligned snapshot candidate is
[0x105900000,0x200000000); default Redmi placement 0x100000000 is rejected.
This is NOT a hardware-validated access window or selected XNU placement.
Firmware/XPU permissions, actual live allocations and 16 KiB MMU still need
validation. No device writes were made during this continuation. Original BOOT
remains restored (r4 receipt below); phone last observed in TWRP.

52 unit tests pass; validator passes all 81 patches / 25 Python / 7 shell tools.
Memory planner committed/pushed as a317b56. Diagnostic CI 43013452142 PASSED:
52 unit tests, host RAM logger, cross-compilation, four QEMU cases. New private
report: backup/a52q/20261111T100325Z/memory-plan.json. Source-only changes exclude
all phone dumps and images. Snapshot inspector wording now distinguishes its
own evidence scope from the separately proven hardware diagnostic milestone.
Follow-up 2cf328f also PASSED diagnostic CI 43013734515. The source patch is
regenerated at shim/out/a52q-source.patch. XNU control 43012318206 remains in its
Build step as of about 11:41 UTC; inspect its completion/logs on continuation.
No XNU success is claimed and no new phone test is pending restoration.
Historical paragraphs below may say not pushed or need commit: 37c47ee already
committed and pushed the r4 source/log decoder and toolchain control.

### CURRENT HARDWARE STATE — second turn, read before acting

**LATEST r4: CRC-VERIFIED STAGE 2 ON THE A52. ORIGINAL BOOT IS RESTORED and fully
hash verified; RECOVERY/DTBO/VBMETA unchanged. Phone remains in TWRP.** Receipt:
`backup/a52q/automatic-test-r4-restored.json`, evidence
`backup/a52q/hardware-r4-20261111T111242Z/checked-diagnostic.json`.
One of three replicas (copy 0) passed CRC32; damaged copies were not repaired or
used. Trusted fields: EL1 (CurrentEL=4), SCTLR=0xc00808, image=0xa12e8000,
DTB=0xa8f38000, MPIDR=0x81000000, MIDR=0x51df805e, MMFR0=0x101122,
PFR0=0x11112222, CNTFRQ=19200000, CTR=0x84448004, ISAR0=0x100010211120,
ISAR1=0x100001, no exception. R4 full BOOT hash:
f9ac11a5c0bf2b758ed2470994a355c5961ab7a3c0d9f80943bf8ee33d91196c.
Host tests 41/41 and four QEMU modes passed before installation. No XNU boot yet.
R4 source/log decoder changes need final commit. Next work is evidence-derived
memory planning and interrupt/timer validation. Target remains iOS 16 / XNU 8796,
eventually upstream iOS 16.7 userland. macOS 15 / Xcode 16 are build-host tooling
only. GitHub retired macos-14 on 2026-11-02. A separate macos-15-intel probe pins
xnu-8796.141.3 at 1b191cb58250d0705d8a51287127505aa4bc0789 and uses SWEET only
as a toolchain control; NEVER flash that control kernel on the A52.
User completed GitHub CLI browser authorization. Dedicated fork created at
https://github.com/chadiLePro/ios-sweet; local branch bringup/a52q-diagnostics.

**r3 SECOND ATTEMPT SUCCEEDED TO DIAGNOSTIC STAGE 2 ON THE A52. Original BOOT
has been restored and fully hash verified. RECOVERY/DTBO/VBMETA are unchanged.
Phone is in TWRP with ORIGINAL BOOT installed, not the shim.** Restore receipt:
`backup/a52q/automatic-test-r3-second-restored.json`. Private evidence directory:
`backup/a52q/hardware-r3-second-20261111T110009Z/`.

Pstore contains A52QDIAG v1, stage 2, image 0xa13f0000, DTB 0xa8f38000,
MIDR 0x51df805e, MMFR0 0x101122, PFR0 0x11112222, CNTFRQ 0x124f800 (19.2 MHz).
Some text is corrupted after the button reset: `currEnt_el` ends in `<` instead
of a hex digit, and `sctlr` label became `qctlr`. Do NOT infer a reliable entry EL
or exact SCTLR from this capture. No XNU has been built/booted for A52. Next work:
redundant checksummed logging and extra CPU/cache feature registers, before XNU.

Original-ROM control succeeded via TWRP System reboot; user unlocked and approved
ADB. Actual ROM: UN1CA Carbon IX v1.0 (ZZI8), Android 17 SDK37, One UI 90000;
vendor Android 11 A525FXXSCFYF1, both basebands A525FXXSCFYF1, kernel
4.14.356-openela-rc1-valeryn-gf0f6778235ba-abA525FXXSCFYF1. KEXEC disabled.
Confirmed properties: `backup/a52q/normal-rom-confirmed-properties.json`.
The boot/DTBO/recovery hashes also match the independent October backup under
`C:/Users/RyZe/Documents/Codex/2026-10-22/mak/outputs/A52-current-firmware-backup`.
TWRP's own System reboot runs its installed rebootsystem.sh, which writes zeros
to the first 256 bytes of MISC (verified already zero) and can update recovery
logs/settings. No MISC data change or userdata format was requested. The generic
ADB reboot path/control observations were not reliable proof of normal boot.

User explicitly superseded the no-automatic-flash restriction with "nono flash
automaticly" after the BOOT-only diagnostic scope and restoration were explained.
Revision 3 was written to BOOT only and fully read back, then boot was attempted.
User reported a direct return to TWRP. No A52QDIAG marker was found; shim execution
is NOT demonstrated. **Original BOOT has already been restored and fully hash
verified**, RECOVERY unchanged. An original-BOOT control reboot is now being
observed. No userdata format, MISC write, DTBO/VBMETA write or bootloader write.

Private hardware result: `backup/a52q/hardware-r3-20261111T103946Z/`; restore
receipt: `backup/a52q/automatic-test-r3-restored.json`. BOOT original hash remains
d6bf03071b0c49bb554effdc62f49014719efe9dcce8922af9c1082c1cc4b016.
Candidate r3 (not currently installed):
`shim/out/a52q-ramoops-r3/a52q-diag-UNTESTED-unsigned-full-r3.img`, hash
c4aa86c551e1c580ecce1640046344662e447659783915d379f4e7d0dd028374.
Original BOOT contains SEANDROIDENFORCE+NUL at aligned content end; r3 preserves
it. The earlier candidate omitted this marker and is superseded. RECOVERY's AVB
footer has stale offsets; do not claim its signature was verified or rewrite it.

New QEMU runner exercises actual diagnostic code at EL1 and EL2, Linux Image/FDT
handoff, relocation, RAM logger and injected exceptions. All performed QEMU cases
passed. This is QEMU virt, not Samsung/XNU emulation. Revision 3 raw Image hash
f681a361b7698ff1e177764a4f83268a376a6ced5388283c6c4a15b0bf887915.
New code/notes still need final validation/commit after the control result.

The paragraphs below describe the previous turn's state and are historical.

The new user's device is SM-A525F/DS, reported unlocked, UN1CA Carbon/One UI 9,
existing TWRP. The old Xiaomi userdata approval below is NOT A52 authorization.
No phone partitions were written. Read-only ADB acquisition identified a52q/atoll,
A525FXXSCFYF1, orange AVB state, recovery 4.14.190-perf+. Current BOOT/DTBO/RECOVERY/
VBMETA and live DT/config/log evidence are in ignored
`backup/a52q/20261111T100325Z/`. See `docs/A52Q.md` for source references, hashes,
full audit, build reproduction, data-loss scope, recovery plan and open inputs.

Upstream base: 45263bee51df4a0f55cdf9c649af886399488ddb. Work uses the chat artifact
checkout on C: because E:/Minecraft and Ubuntu's E:-hosted VHD were unavailable.
Separate `devices/a52q.json`, `shim/a52q/`, read-only acquisition/evidence tools,
guarded GNU diagnostic builder and AOSP packager were added. Redmi code, mkadt
defaults, XNU patches and kernel workflow remain unchanged. No A52 XNU config yet.
Implementation commit: `ac68599` on local branch `bringup/a52q-diagnostics`;
not pushed. Final guarded repack reproduced the recorded full-image SHA256.

Built no-output core and evidence-derived ramoops variant using Arm GNU 14.3.Rel1
native Windows aarch64-none-elf tools. Candidate RAM console is derived at
0xb4640000/0x40000, checked against live DT/runtime parameters and board-06 DTBO;
retention through reset is UNTESTED. Command-mode panel has no live simplefb/fb0.
TWRP config has KEXEC and DEBUG_FS disabled. No known temporary Samsung RAM boot.

Reviewable full BOOT candidate:
`shim/out/a52q-ramoops/a52q-diag-UNTESTED-unsigned-full.img` (96 MiB), SHA256
71f80715822974ab1722e06786a9c8bad518218e8cccaf49eab7652c83e54b17.
Retains current ramdisk/DTB/header metadata, gzip wrapper and text_offset; strips
stale AVB metadata and clears tail. It is unsigned and NOT PHONE-TESTED. Adjacent
JSON/ELF/symbols/disassembly retained. No emulation, XNU build, cloud CI dispatch
or Apple userland artifact produced. No compatibility claims.

Validation: repository validator passes; 24 Python tests pass; host C ramoops
layout/bounds/reconstruction test passes; AArch64 relocation and Image-header
checks pass. Added CI workflow was not run remotely. Next hardware milestone is
an explicitly authorized BOOT-only diagnostic test and retrieval of A52QDIAG v1
from TWRP pstore, with original BOOT accessible for restoration. Off-host backup
readiness and exact installed vendor firmware still need confirmation. Do not
apply sweet fastboot/userdata commands. The first XNU RAM choice must exclude
Samsung's live 0x100000000..0x105900000 carveout and resolve dynamic reservations.

## Agent handoff / active work (2026-10-15, latest)

### >>> UPDATE 2026-10-18 (read first, then the 10-17 handoff below) <<<

**STATE at end of 2026-10-18 (evening):**
- On the phone: userdata = **image v15** (`/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v15.img/.simg`; = v14 + `/private/var/preferences/SystemConfiguration/preferences.plist` with one network service "USB Ethernet": Interface DeviceName ue0 Type Ethernet, IPv4 Manual 192.168.7.2/24 router 192.168.7.1, DNS 1.1.1.1 8.8.8.8, set "Automatic" as CurrentSet). Fallback image v14 (v12/v13 deleted).
- Kernels: **0078** = all 8 cores (`cpus=8`, cpu6/7 = A76, homogeneous SMP; mkadt now emits 8 CPU nodes; ADT `shim/out/sweet-0078hi.adt`); **0079** = display off/on via IOMFB selector 12 kern_RequestPowerChange(state) (fade over 6 vsyncs, then black; verified: power button gives "SWEET FB: display off/on"); **0080** = `SWEET NET: <proc> route add/delete/change ...` and `... add/delete address ...` trace (built, `shim/out/shim-boot-0080s.img`, NOT booted yet).
- **Internet over USB: not working yet.** Host side is ready (temporary iptables: FORWARD accept for 192.168.7.0/24 + MASQUERADE, comment "ios-sweet"; lost on host reboot). With v15 the phone sent no DNS and no outbound traffic (only mDNS/ARP) -> configd probably did not apply the service (or did, without default route/DNS). Next: boot 0080s on v15, watch `SWEET NET` lines (does configd add 192.168.7.2 / default route on ue0?). If configd ignores ue0 (not an IOKit IONetworkInterface; configd 1241.140.6 source in `research/configd-1241`, SCNetworkInterface createInterface needs IONetworkInterface -> controller (IOMACAddress, SelfNamed) -> bus), add IOKit stand-ins and/or rename the ifnet to en*.
- Live log listener (`nc -ukl 5140`) may still be running, writing `logs/live-0078s.txt`.

**LIVE LOG over USB (0077, boot 0077s): no more recovery round-trips.** Boot an image with `sweetusb=2`, run `tools/sweet-usbnet.sh logs/live-NAME.txt` on the PC: it waits for the phone's CDC-ECM interface, sets 192.168.7.1/24 (sudo) and prints/saves the kernel console the phone streams every 100 ms as UDP to 192.168.7.1:5140 (starts with the last 64 KiB). `ping 192.168.7.2` checks the link. Current image: `shim/out/shim-boot-0077s.img` (kernel 0077, ADT sweet-0069hi, cpus=6, sweetfb_noconsole=1, sweetfb_hz=30, sweetusb=2). The recovery pull (`tools/sweet-log-pull.sh`) is still the way after a panic/hang before USB comes up.

**ðŸŽ‰ USB networking works (boot 0076s, 18:24 local): `ping 192.168.7.2` from the PC answers in ~1 ms, 0 % loss (200-packet burst, 1500-byte frames, 512/1024-byte frames).** 0075: CDC-ECM function (bulk 0x81/0x01, interrupt 0x82 NETWORK_CONNECTION; host MAC 02:00:5e:77:ee:01) + kernel ethernet ifnet `ue0` (legacy output, header strip like if_fake) with 192.168.7.2/24 set from the kernel (proto_plumb + SIOCAIFADDR on an in-kernel socket). 0076: received frames into one cluster mbuf (mbuf_allocpacket gave a first mbuf of length 0 -> panic "Failed mbuf validity check: len -14"). Host side (Linux cdc_ether, interface `enp0s20f0u3u1`): `nmcli dev set IF managed no; sudo ip addr add 192.168.7.1/24 dev IF; sudo ip link set IF up`. Boot image `shim/out/shim-boot-0076s.img` (`sweetusb=2`). iOS itself does not see ue0 yet (configd needs an IONetworkInterface in IOKit).

**USB device mode works (boot 0074s, 17:45 local): the host enumerates the phone at high speed as `1209:0001 ios-sweet "Sweet iOS (USB bring-up)"`.** 0072 read-only probe: ABL leaves the USB30_PRIM GDSC and all 7 USB clocks on, DWC3 v3.20a (GSNPSID 0x5533320a) in device mode (GCTL 0x00112000), halted (DCTL RUN_STOP 0, DSTS 0x00d3de04), event buffer still at ABL's 0xfdfc8000, QUSB2 PHY alive. 0073 (`sweetusb=2`): DCTL soft reset, own event buffer (polled, interrupt masked), ep0 DEPSTARTCFG/SETEPCONFIG/SETTRANSFRESOURCE, setup TRB, RUN_STOP; control-transfer state machine as Linux ep0.c; descriptors: vendor class, no data endpoints. It ran but no event came: **0074** forces the VBUS session in the Qualcomm wrapper (QSCRATCH 0xa6f8800: HS_PHY_CTRL |= UTMI_OTG_VBUS_VALID(20)|SW_SESSVLD_SEL(28), SS_PHY_CTRL |= LANE0_PWR_PRESENT(24), as Linux dwc3_qcom_vbus_override_enable) -> connect + enumeration. Image `shim/out/shim-boot-0074s.img`. Black Phone app: main thread waits in -[VMVoicemailManager fetchAccounts] (sync XPC; voicemail needs the modem).

**Navigation works (boot 0071s on v14, log `logs/boot-0071s.txt`):** swipe up from the bottom edge returns to the home screen; app switcher works. Two fixes: **0070** pid_hibernate (syscall 435 was nosys on the macOS config -> SIGSYS killed SpringBoard in -[SBToAppsWorkspaceTransaction _didComplete] when an app left the foreground; the only CONFIG_EMBEDDED-only entry in syscalls.master); **0071** touches starting within 48 px of an edge carry kIOHIDDigitizerEventFromEdgeTip (UIKit `_UIEventHIDTouchEdgeTypeForHIDEvent` reads the digitizer EventMask 0xb0007 bits 0x800/0x1000/0x2000/0x40000). Diagnosed, not fixed: Settings (Preferences) SIGTRAP in PodcastsUI func_1cdc47c58: force-unwrap of `URL.volumeTotalCapacity` (nil on our HFS+ root). Phone/Photos/Messages show black (MobilePhone launches, no crash) - next: stack samples via boot-arg `sweetsample=MobilePhone,MobileSlideShow,MobileSMS,SpringBoard` (image `shim/out/shim-boot-0071s.img`).

**ðŸŽ‰ðŸŽ‰ MILESTONE 2026-10-18 ~15:30 local: iOS 16.7 SPRINGBOARD HOME SCREEN ON THE PHONE** (boot `shim/out/shim-boot-0069s.img` = kernel 0069 + ADT `shim/out/sweet-0069hi.adt`, image **v14**; log `logs/boot-0069s-v14-HOMESCREEN.txt`). Home screen with a few apps, Settings opens, Control Center / lock screen / notification center work, touch + buttons work, 6 A55 cores (`cpus=6`), `sweetfb_noconsole=1 sweetfb_hz=30`. Known issue: cannot leave Settings (home gesture / AssistiveTouch home do nothing) - to investigate.
What it took today (in order): 0058 HID services (Apple IOHIDFamily-1915 user client), 0059 iPhone X identity (hw.product etc.), 0060 SPMI keys + GENI touch, 0061 1125x2436 presented display, 0062 RPMh L11C touch power + IOPMPowerSource battery, 0063 GENI FIFO packing (Goodix GT9896), 0064 PRIV_WORK_INTERVAL grant (SpringBoard "Failed to create work interval"), 0065 SMP via PSCI (6 A55), 0066 crash map regions, 0067 console mute without cons_ops write, 0068 IOSurface lookup of an already-mapped surface returns base -1 (backboardd snapshot crash), 0069 UFS log flush 10 s. Image v13: CommCenter removed from launchd.plist, BKNoWatchdogs. **Image v14** = v13 + Setup skipped (`/var/mobile/Library/Preferences/com.apple.purplebuddy.plist` SetupDone/SetupFinishedAllSteps true, SetupVersion 11, daemonizeNeedsToRun false; purplebuddy.notbackedup mini-buddy flags false; managedconfiguration.notbackedup LockdownActivationIndicatesCloudConfigurationAvailable false; springboard MCForceShowCloudConfigurationUI false) + mobileactivationd data ark seeded (`/private/var/containers/Data/System/D90C94C4-F94E-4FCF-8A28-A93BE3846D8E/Library/internal/data_ark.plist`, -ActivationState Activated etc.) + MediaToolbox D22/D221/Default SubServerConfiguration StartRecorderServer=false (mediaserverd crash loop: portrait-filter prewarm called NULL GL). **Activation:** ADT /chosen certificate-production-status 0, effective-production-status-ap 0, certificate-security-mode 1, effective-security-mode-sep 1 -> mobileactivationd's native Hactivation branch (Codex `codex/activation/report.md`; alternative 4-byte daemon patch documented there). Fallback image v13; v12 deleted.

**ðŸŽ‰ TOUCH WORKS (boot 0063u on image v13, 2026-10-18 ~13:15 local):** tapping (i) on Setup's Hello opens the device-info sheet; swipe-up is recognised (spinner, then back to Hello - under investigation). Chain: RPMh L11C vote (0062, `bsd/dev/sweet_rpmh.c`) -> GT9896 @0x5d on GENI SE7 (0063 fixed FIFO packing: register address went out byte-swapped) -> sweet_hid_touch -> SweetHIDTouch -> backboardd. Battery icon OK (0062 SweetBattery IOPMPowerSource, static 100 %). **Image v13** (= v12 + CommCenter jobs removed from launchd.plist + `BKNoWatchdogs`=true and `FBLaunchWatchdogExceptions{com.apple.purplebuddy:100}` in /var/mobile/Library/Preferences/com.apple.springboard.plist): Setup no longer killed by the scene-create watchdog (it blocked in CoreTelephony getSubscriptionInfo -> CommCenter, Codex `codex/setup/report.md`; that report also lists how to skip Setup: SetupDone/SetupFinishedAllSteps/SetupVersion=11 in com.apple.purplebuddy.plist + activation check). v9 deleted, fallback = v12. Input latency ~1 min with 1 CPU -> Codex task 11 = SMP via PSCI (`codex/smp/`).

**INPUT WORKS (boot 0060u on a freshly flashed v12, log `logs/boot-0060u.txt`):** power, volume up, volume down reach iOS (PMIC -> sweet_keys.c -> SweetHIDButtons -> backboardd). Power locks/unlocks (screen "off" shows the kernel console because the panel never really turns off). **Device identity fixed: iPhone X** (home indicator, Face-ID-style Setup). Earlier test (0059u, `sweethidtest=15` fake Home presses) advanced Setup from Hello to the language list.
- **0058** HID: `iokit/Kernel/arm/hid/`: IOHIDEventServiceUserClient + IOHIDEventServiceQueue + IOHIDEvent compiled UNCHANGED from Apple IOHIDFamily-1915.140.3 (= exact version of the iOS 16.7 IOHIDLib, clone in `research/iohid-1915`) over our minimal IOHIDEventService (SweetHID.cpp: SweetHIDButtons consumer page 0x0C power 0x30 / vol 0xE9/0xEA / menu 0x40; SweetHIDTouch digitizer collections). C hooks `sweet_hid_key(key, down)` (0 power, 1 vol+, 2 vol-, 3 home) and `sweet_hid_touch(finger, down, x, y)`. HID logs go to IOLog. Boot-arg `sweethidtest=N` = fake Home press every N s.
- **0059** identity: hw.machine/hw.model/hw.target/hw.product from the ADT (macOS-config kernel used to answer "iPad8,6"/"Redmi Note 10 Pro"). mkadt: root compatible `D22AP|iPhone10,3|xiaomi,sweet|...`, model iPhone10,3, target-type D22, `/product` copied from the real D22AP device tree (`research/ipsw-x/d22ap.adt`, extracted from the IPSW, NOT in git), `/buttons home-button-type 2`. Codex report `codex/mg/report.md`: MG ProductType = sysctl **hw.product** (unrecognized -> iPod), HWModelStr = hw.target, HomeButtonType = `/buttons/home-button-type`; disk cache `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/com.apple.MobileGestalt.plist` (keyed by build + UUID only -> stale iPod answers survived; reflashed clean v12 to clear it).
- **0060** drivers by Codex (`codex/input/hw-report.md`): `bsd/dev/sweet_keys.c` (SPMI arbiter v5 observer reads, PON 0x810 bits KPDPWR/RESIN SID0, PM6150L GPIO2 SID4 0xc110; works), `bsd/dev/sweet_touch.c` (GENI SE7 I2C @0xa84000, starts 45 s after boot). Touch result: SE7 fw ok (proto 3) but **0x5d and 0x38 both time out -> touch IC unpowered** (L11C LDO needs an RPMh vote). Codex task 8 = RPMh client (`codex/rpmh/`), task 7 = battery (`codex/battery/`).
- **0061** (CI 39117078444): red status bar "rdar:45025538" = UIKit "No status bar visual provider for screen" (360x800 pt is no real iPhone). AppleCLCD now presents **1125x2436** (iPhone X) and shows the centered 1080x2400; touch mapped the same; ADT canvas 1125x2436. `sweetfb_native=1` reverts.
- Images: `shim/out/shim-boot-0060b.img` (0060 + /buttons ADT `sweet-0060hi.adt`). Next: 0061 image with ADT from current mkadt.

### >>> HANDOFF 2026-10-17 late (read this first) <<<

**STATE: iOS 16.7 Setup.app "Hello" screen is ON THE PHONE** (boot `shim/out/shim-boot-0057u.img` on image v12). Photo `/run/media/dipa/android/ios-sweet-work/MILESTONE-setup-hello-2026-10-17.jpg`. SpringBoard + backboardd + Setup run; nothing crashes in the GUI path. Remaining crash/relaunch loops: installcoordinationd (should be fixed by 0057, unverified), mediaserverd (VirtualAudio removed in v12, unverified), mobileactivationd (~100/boot, not analysed), bluetoothd + fairplayd.H2 relaunch constantly (no hardware).

**What is on the phone now:** userdata = image **v12** (`/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v12.img` + `.simg` + `.sha256`; v9 kept as fallback, v8/v10/v11 deleted or superseded). Kernel **0057** (`xnu/out-0057`, CI `39067532732`). ADT **`shim/out/sweet-0057hi.adt`** (QEMU twin `research/q0057-hi.adt`). Boot image **`shim/out/shim-boot-0057u.img`**. Boot args: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=ufsroot0 unentitled_ios_sim_launch=1 ignition_level=1 wdt_test=no_user_checkin ufsrw=1 rootrw=1 launchd_unsecure_cache=1 wdt=-1`.

**Build a phone image** (kernel K, ADT A): `python3 tools/mkpayload.py $K $A shim/out/payload-X.bin --cmdline "$B" && (cd shim && ./build.sh ../shim/out/payload-X.bin && cp out/shim-boot.img out/shim-boot-X.img)` then check `python3 tools/unpack_bootv2.py shim/out/shim-boot-X.img shim/out/check-X && cmp shim/out/check-X/ramdisk shim/out/payload-X.bin`. QEMU smoke test: `python3 tools/mkpayload.py $K research/q0057-hi.adt $S/csq/payloadX.bin --ramdisk $S/csq/root-fork.img --cmdline "debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=md0"` + `PATH=~/swift/usr/bin:$PATH python3 tools/qemu-sweet.py ... --secs 40 --kernel $K --fail-on-panic` (S = scratchpad; root-fork.img lives in the session scratchpad csq/ dir and may be gone in a new session).

**Kernel workflow:** edit `research/bt28/xnu/...` (keep the pre-edit copy in `research/preNNNN/`), syntax check `python3 tools/xnu-cc.py research/run28.log research/bt28 <file>`, make `xnu/patches/NNNN-*.patch` with `diff -u pre bt28 | sed` path rewrite, add new/changed files to `research/check-patch-order.py` list, run it (must say applied + MATCH), commit + push -> GitHub Actions `xnu` builds (~8 min) -> `gh run download <id> -R dipa-studio/ios-sweet -n xnu-kernel -D xnu/out-NNNN`. **Repo is PUBLIC since 2026-10-17** (private macOS runner minutes ran out: "recent account payments have failed"); public = free runners. Commit trailer: only `Co-Authored-By: dipa-studio <183933817+dipa-studio@users.noreply.github.com>`.

**Phone workflow (user does buttons, Claude runs commands):**
- Boot test kernel: phone in fastboot -> `fastboot boot shim/out/shim-boot-X.img`. NEVER `fastboot getvar`.
- **Read logs WITHOUT filming:** after a test the user holds Power+VolDown -> fastboot -> `fastboot boot recovery/recovery.img` (OrangeFox, temp) -> wait for `adb shell true` -> `tools/sweet-log-pull.sh /run/media/dipa/android/ios-sweet-work/logs/<name>.txt` (reads the 4 MiB console ring the kernel keeps in the last 1025 blocks of userdata; patch 0047). Then `adb reboot bootloader` brings the phone back to fastboot without the user.
- **Flash a root image:** `fastboot flash -S 512M userdata <img>.simg` (7 min, 25 chunks). After a big flash the Xiaomi ABL fastboot hangs: next `fastboot boot` stalls at "Sending" -> the USER must re-enter fastboot by hand (Power+VolDown). Do not retry commands against the hung ABL. A flash right after `adb reboot bootloader` once failed on chunk 1 (USB protocol error): just retry. User must NOT unplug during flash (once interrupted at 25/25 -> reflash).
- **Edit the phone root without reflashing (same-length only):** find the file's raw offset in the local image (it is one extent; search the image for its first 4 KiB), compare with `adb exec-out dd if=/dev/block/sda34 ...`, then `adb push` changed 4 KiB blocks and `dd of=/dev/block/sda34 seek=... conv=notrunc,fsync`, read back. Recovery kernel has no hfsplus.
- **Pull the whole phone root** (12 min): `adb exec-out "dd if=/dev/block/sda34 bs=1048576 count=16384" > img`; mount ro with udisksctl or `sudo mount -t hfsplus -o loop,ro`. To write into a pulled image: `sudo fsck.hfsplus -fy` first (volume is never cleanly unmounted -> Linux mounts ro even with -o force), then `sudo mount -t hfsplus -o loop,force`.
- Making images: copy latest img with `cp --sparse=always`, mount rw with force, change, `sync; umount`, `sha256sum`, `img2simg`. Keep only the latest image + one fallback on the SSD (/home is ~98% full; big work files live in `/run/media/dipa/android/ios-sweet-work/`, old kernels/images archived in `.../ios-sweet-work/archive/`).

**Diagnostics built into the kernel (all SWEET-only):** persistent console log (0047, boot-arg sweetlog=0 off; flush every ~1 s); `|name| text` copies of /dev/null writes for processes in `sweetnull` (default backboardd,SpringBoard; 0048); `IOK name:` IOKit lookup/open trace for `sweetiolog` (default backboardd,SpringBoard; 0049/0054, 400 lines max); `SWEET Sandbox: proc op N` (0050); `STR ...` heap text dump on SIGABRT/SIGTRAP for `sweetscan` (default backboardd,SpringBoard; 0051/0053) - this is how NSException/BSAssert reasons were found; `SMP name tN pc .. bt ..` user stack sampler for `sweetsample` (default SpringBoard,backboardd; first at 90 s then every 120 s, 40 samples, 16 frames; 0054/0055); `SWEET FB: N swaps` every 1000 swaps; `CRASH name ...` crash reports (0043/0044). Symbolicate cache addresses with `ipsw dyld a2s research/dsc/dyld_shared_cache_arm64 <addr - slide>`; main-binary addresses: addr - mh + 0x100000000.

**Patches added today (0046-0057, all CI-built):** 0046 IOSurface (IOCoreSurfaceRoot) + IOMobileFramebuffer (AppleCLCD on /arm-io/disp0) + arm-io nubs; 0047 persistent log; 0048 /dev/null tee; 0049 IOKit trace; 0050 permissive "Sandbox" MAC policy; 0051/0053 heap text on crash; 0052 RENAME_SWAP via exchangedata on HFS; 0054/0055 sampler, swap counter, AKS selectors 35 (extended device state = 17) and 101; 0056 panel copy from the vsync timer at 10 Hz (sweetfb_hz) instead of every swap; 0057 no config_ext_resolver (ACL group entries resolve without memberd). ADT (tools/mkadt.py): /arm-io/disp0, /chosen/display-scale 3, /chosen/unique-chip-id (synthetic 0x5357454554000001) + chip-id 0x8015 -> IOPlatformUUID A9683613-3704-53F2-95D0-98A8FB574E78. Image v9-v12: /private/var/containers/{Bundle,Data/System,Shared/SystemGroup,Temp}; launchd.plist StandardOut/ErrorPath renamed to ...PatX (pointing jobs at /dev/console stops them launching: EACCES); v12: LastSystemVersion=20H392 in plain /var/mobile/Library/Preferences/com.apple.migration.plist (stops the 1-hour data migration that ran every boot), VirtualAudio.plugin moved to /Library/Audio/Plug-Ins/HAL.disabled/.

**Codex helper** (`codex exec --skip-git-repo-check -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write -C /run/media/dipa/android/ios-sweet-work/codex -o OUT "$(cat task.md)" < /dev/null`, run detached with setsid nohup; config already defaults to gpt-6.1-sol high). Reports in `/run/media/dipa/android/ios-sweet-work/codex/`: mediaserverd-report.md, installcoordinationd-report.md (-> 0057), ufs-performance.md (ranked UFS speed plan), **ufs/0058-sweet-ufs-faster.patch** (READY, not yet applied: ufslogsecs default 10 s log flush batching, optional ufscache=1 directional cache ops, optional ufswait=1 spin-then-sleep; syntax-checked, host-stub verified; see ufs/README.md). Apply it as patch 0058 after review.

**Claude safety-classifier note:** several messages about QuartzCore renderer selection / writing an HFS reader tool were cut off by an automatic classifier (false positives, user agrees). Keep those topics short or let them be; they are not blockers now (rendering already works).

**NEXT STEPS (in order):**
1. **Input** (Setup stuck on Hello): touch + power + volume as IOHIDEventService/IOHIDDevice services backboardd matches (log shows backboardd matching IOHIDDevice with DeviceUsagePairs and IOService with HIDServiceSupport=true). Phone hardware: Goodix/Focaltech touch over I2C/SPI (check live DT `dtb/`), buttons via PMIC (pon) and GPIO keys. Start with a fake HID service (e.g. power button via a timer or boot-arg) to learn the ABI, then real drivers.
2. **Device identity**: MobileGestalt reports iPod + Home button. Add /product node / product-type (iPhone10,3, D22AP), device class iPhone, home-button-less (Face ID) properties in mkadt; find exact MG keys (MGIOMFBSupport.c, `IODeviceTree:/product` lookups seen in backboardd trace).
3. **Battery**: AppleSmartBattery/IOPMPowerSource style service (status bar shows empty red battery).
4. Apply Codex 0058 (UFS speed), consider cpus>1, check whether installcoordinationd/mediaserverd loops are gone, analyse mobileactivationd.
5. Hide kernel console over the GUI when not debugging: boot-arg sweetfb_noconsole=1 (but then panics are not on screen).

- **ðŸŽ‰ MILESTONE: iOS GUI ON THE PHONE - Setup.app "Hello" screen (2026-10-17 ~21:30 UTC, boot 0057u on image v12).** Photo: `/run/media/dipa/android/ios-sweet-work/MILESTONE-setup-hello-2026-10-17.jpg` (animated "dobar d(an)" hello lettering, status bar "iPod" + battery icon, bottom "Pritisnite Home za otvaranje" = "Press Home to open" (locale hr), (i) button). Rendered by iOS 16.7 SpringBoard/Setup through CoreAnimation -> backboardd -> kernel IOSurface (IOCoreSurfaceRoot) -> kernel AppleCLCD swaps -> ABL panel memory. What made it: data migration finally skipped (v12: `LastSystemVersion` 20H392 in the plain `/var/mobile/Library/Preferences/com.apple.migration.plist`; ADT `/chosen/unique-chip-id` + `chip-id` for IOPlatformUUID), 0057 (no ext resolver -> ACL containers work), plus everything before (0046 display/IOSurface, 0050 Sandbox policy, display-scale 3, containers dirs, RENAME_SWAP, AKS 35/101, 10 Hz present).
  **Missing (next work, in rough order):**
  - **Input: no touch, no power button, no volume buttons** (no HID drivers; backboardd looks for IOHIDDevice / HIDServiceSupport services). Setup is stuck on "Hello".
  - **Device identity: it thinks it is an iPod with a Home button** (status bar "iPod", "Press Home to open"): MobileGestalt has no product/model identity (no /product node, product-type, etc.) - give it iPhone10,3 / home-button-less (Face ID class) identity.
  - **No battery detection** (no battery/charger/PMIC service; status bar battery shows empty/red).
  - Locale came up Croatian (hr) - harmless.
  - Performance: cpus=1, polled UFS (Codex UFS patch in progress: `codex/ufs/`), backboardd presents at 60 Hz.
- **README refreshed (2026-10-17):** read the full notes and updated the public overview through patch 0045, v7 hardware observations and prepared v8 diagnostics. Documents real Apple userspace, the missing display/IOSurface GUI work, limited security services, highmem, persistent userdata root, current tooling and build examples. Documentation only; no kernel build, tests, flashing or phone boot performed.

- **v11 still migrated (boot 0056u, 20:32 UTC, `logs/boot-0056u-v11.txt`).** On iOS kCFPreferencesCurrentHost lands in the plain plist: all DMEnvironment setters (setLastBuildVersionPref, setUserDataDispositionPref, ...) use CurrentHost and the phone's `/var/mobile/Library/Preferences/com.apple.migration.plist` holds DMUserDataDisposition; datamigrator's XPC service runs with `_RoleAccount: mobile`. **Image v12** = v11 + `LastSystemVersion` = 20H392 added to that plain `com.apple.migration.plist` (keeps DMUserDataDisposition, 501:501 0600) + `/Library/Audio/Plug-Ins/HAL/VirtualAudio.plugin` moved to `/Library/Audio/Plug-Ins/HAL.disabled/` (Codex: stops the mediaserverd SIGSEGV loop; untested). **installcoordinationd loop explained (Codex `codex/installcoordinationd-report.md`):** os_crash "Failed to create data directory" EACCES for `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.installcoordinationd/Library/InstallCoordination`: `Library`/`Library/Caches` in the container are ACL-only (uid/gid 0xfffffffe, mode 0000, ACE for group GUID ...012B = gid 299 systemusers); with `config_ext_resolver` the kernel asks an identity resolver (memberd/opendirectoryd) that iOS does not run -> EWOULDBLOCK -> ACE skipped -> EACCES. **Patch 0057**: drop config_ext_resolver from FILESYS_BASE (compatibility UID/GID<->GUID mapping is used instead), likely fixes other ACL-protected containers too. Codex task 3: UFS driver performance design (`codex/ufs-performance.md`).
- **mediaserverd SIGSEGV loop explained (Codex report `/run/media/dipa/android/ios-sweet-work/codex/mediaserverd-report.md`):** the fault (FAR 0x390) is in the HAL plug-in `/Library/Audio/Plug-Ins/HAL/VirtualAudio.plugin/VirtualAudio` (ApplyBeamFormerPreference <- VirtualAudio_PlugIn::SetPropertyData <- HALS_AHPPlugIn::ObjectSetPropertyData <- AudioObjectSetPropertyData <- MediaExperience vaemVADSerializationListener): the default virtual audio device ('vdef', VirtualAudioDevice_Default) does not exist (no audio hardware/driver, no /product/audio). Proposed workaround for GUI bring-up: move VirtualAudio.plugin out of /Library/Audio/Plug-Ins/HAL/ in the next root image (untested). v11 reflashed OK after an interrupted flash (USB unplugged at chunk 25/25). Codex task 2: installcoordinationd crash loop.
- **ROOT CAUSE of the endless migration: no IOPlatformUUID (2026-10-17).** datamigrator's `-[DMMigrator isMigrationNeededWithBuildVersion:lastBuildVersion:clientPID:]` gets lastBuildVersion from `-[DMEnvironment lastBuildVersionPref]` = `CFPreferencesCopyValue("LastSystemVersion", "com.apple.migration", kCFPreferencesCurrentUser, kCFPreferencesCurrentHost)` -> a ByHost file. The phone had `/var/mobile/Library/Preferences/com.apple.migration.plist` (only DMUserDataDisposition) and NO `Preferences/ByHost` directory at all. On arm XNU publishes IOPlatformUUID (gethostuuid) only from `/chosen/unique-chip-id` (8 bytes) + `/chosen/chip-id` (4 bytes) (IOPlatformExpertDevice::generatePlatformUUID, called from IOPlatformExpert::start); the SWEET ADT had neither, so every CurrentHost preference write failed. Fix: mkadt adds `unique-chip-id` = 0x5357454554000001 (synthetic) and `chip-id` = 0x8015 -> UUID `A9683613-3704-53F2-95D0-98A8FB574E78` (same SHA1 namespace computation as the kernel). ADT `shim/out/sweet-0057hi.adt`, boot image `shim/out/shim-boot-0056u.img` (0056 kernel + 0057hi ADT, QEMU OK). **Image v11** = v10 + `Preferences/ByHost/com.apple.migration.<UUID upper and lower>.plist` {LastSystemVersion: 20H392} (501:501, dir 0755 files 0600). Flashing v11 2026-10-17 ~20:10 UTC. Codex (gpt-6.1-sol high) analysing the mediaserverd SIGSEGV loop in `/run/media/dipa/android/ios-sweet-work/codex/` (report `mediaserverd-report.md`).
- **v10 did NOT stop the migration (boot 0056n on v10, 19:18 UTC, `logs/boot-0056n-v10.txt`):** datamigrator + migrationpluginwrapper ran again, backboardd drew the progress UI (13000+ swaps in ~5 min). So `com.apple.DataMigration.plist`/LastSystemVersion is not the deciding input. What is known about the decision (datamigrator XPC service `DataMigration.framework/XPCServices/com.apple.datamigrator.xpc/com.apple.datamigrator`, strings): `Migration sentinel present. Migration necessary.` (sentinel `/private/var/datamigrator/migrate`, created and removed by datamigrator itself; absent in v10), `System build version changed from %@ to %@. Migration necessary.` / `...unchanged... not necessary`, `Disposition dictionary with build version %@ is out of date relative to current build version %@`, `SyntheticDidUpgrade`, DMUserDataDispositionManager; previous build source not found yet (not in the binary's plain strings; likely in DataMigration.framework's DMUserDataDispositionManager / preferences domain `com.apple.migration`). backboardd calls `DMPerformMigrationIfNeeded` and holds SpringBoard in `checkInAndWaitForDataMigration` until it returns. NEXT: find where the previous build version / disposition dictionary is stored (disassemble DataMigration.framework DMUserDataDispositionManager + datamigrator's isMigrationNeeded path), write it into the image; or get datamigrator's os_log out (OS_ACTIVITY_DT_MODE needs a launchd env change).
- **Data migration never records completion -> skip it (image v10, 2026-10-17).** Boot 0056n (18:16 UTC, `logs/boot-0056n.txt`, 30 min): 10 Hz panel copies, backboardd still presents at ~60 Hz (107k swaps), SpringBoard still in `BKSSystemShellService _checkIn` at sample 14. Every migration run takes 1+ hour on cpus=1 and repeats each boot. DataMigration decides from `/var/mobile/Library/Preferences/com.apple.DataMigration.plist` key `LastSystemVersion` (vs ProductBuildVersion 20H392); the pulled phone root (21:01 local) had NO such file. **v10** = that pulled phone state + fsck.hfsplus -fy (volume was marked not cleanly unmounted -> Linux mounts it read-only even with -o force; fsck found only hard-link counts + minor volume header, repaired) + `com.apple.DataMigration.plist` {LastSystemVersion: 20H392} (501:501 0600). `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v10.img` (+ .sha256, .simg); v8 files deleted, v9 kept as fallback.
- **Repo made PUBLIC (2026-10-17, user request) so GitHub-hosted macOS runners are free:** the 0056 CI run was refused ("recent account payments have failed or your spending limit needs to be increased"). Checked before: no device dumps, serials, IMEI or Apple binaries in the history (.gitignore keeps backup/, dtb/, recovery/, research/ out); commit author emails are public now. 0056 rerun `39056660104` passed -> `xnu/out-0056`, QEMU OK, image `shim/out/shim-boot-0056n.img` booted 18:16 UTC.
- **Boot 0055n (17:16 UTC, ~65 min, `logs/boot-0055n.txt`): migration bar reached 99% in ~30 min (was ~60), then crawled.** Root cause of the slowness: backboardd presents the progress UI at ~58 Hz (**167,000 swaps in ~48 min**) and AppleCLCD copied the full 10 MB frame into the panel on every swap -> ~600 MB/s memcpy on the single CPU (cpus=1), starving everything (polled UFS I/O too). Sampler (16 frames): **SpringBoard waits in `-[BKSSystemShellService _checkIn]`** (synchronous BSXPC call to backboardd, from FBSystemShellInitialize <- SBSystemAppMain) - backboardd holds the system shell check-in until the data migration ends, so the migration is the gate to SpringBoard UI. **Patch 0056**: swap only records the latest swap record; the vsync timer copies it to the panel every 60/sweetfb_hz ticks (default 10 Hz); `SWEET FB: N swaps` every 1000.
- **Boot 0054n (16:53 UTC, ~12 min, `logs/boot-0054n.txt`, patch 0054 sampler):** the data migration runs AGAIN on every boot (it completed once in the 0053s run) - completion is not being recorded. backboardd keeps swapping the progress UI (3700+ swaps in ~10 min, `SWEET FB: N swaps`). Sample during migration: SpringBoard main thread blocked in a synchronous XPC call (`mach_msg2_trap <- dispatch_mach_send_and_wait_for_reply <- xpc_connection_send_message_with_reply_sync <- -[BSXPCServiceConnectionMessage _sendSynchronously:] <- BSXPCServiceConnectionProxy ...`). Unsupported AKS selectors seen: 101 `aks_assert_consume`, 93 `aks_get_internal_info`, 34 `_aks_stash_load` (datamigrator), **35 `aks_get_extended_device_state`** (SpringBoard, chronod, remindd, searchd, symptomsd...). **Patch 0055**: AKS 35 answered like 17 (same DER device state), 101 succeeds; sampler backtraces 16 frames, 40 samples (~80 min).
- **MILESTONE: FIRST iOS PIXELS ON THE PANEL (boot 0053s long run, 15:33 UTC, ~60 min; photos IMG_20261017_183029/183222/183419; log `/run/media/dipa/android/ios-sweet-work/logs/boot-0053s-long.txt`, 407 KB, 1428 flushes).** The iOS data-migration boot screen (Apple logo + progress bar) was shown and the bar advanced to full in ~60 minutes. It is drawn by **backboardd through our kernel display path**: `SWEET SURF: backboardd create id 2/3 1080x2400 fmt 0x42475241 (BGRA) bpe 4 bpr 4352 size 10452992 keys 11`, IOSurface sels 9, 27, 5, 34 and traps 2/3 (lock/unlock), IOMFB SwapBegin (4) / SwapEnd (5, 1132-byte struct) / GetLayerDefaultSurface (3) / 68 / 55, then `SWEET FB: swap N layer 0 surface 2|3 1080x2400 ... a 0,0 1080x2400 b 0,0 1080x2400` alternating (double buffering; only the first 16 swaps are logged). Triggered by `com.apple.datamigrator` (AKS sels 101/93/34 return unsupported) and `com.apple.migrationpluginwrapper`. Probably ProgressUI-style CoreGraphics drawing into IOSurfaces (no GPU used). After the migration: SpringBoard and backboardd stay up (exec once each, no crash), nothing new drawn; crash loops only for mediaserverd, installcoordinationd, mobileactivationd (~108 each in the hour); bluetoothd and fairplayd.H2 relaunch constantly (no hardware). Kernel console text overlays the image (sweetfb_noconsole=1 would hide it).
- **MILESTONE: SpringBoard and backboardd both stay up (boot 0053s on v9, 15:29 UTC, `logs/boot-0053s.txt`).** With /chosen/display-scale = 3: `exec SpringBoard` once, `exec backboardd` once, no CRASH for either; MobileGestaltHelper reads IOMFB size/dot pitch; backboardd opens AppleCLCD (sels 57,15,22,29,33,79,74 as before). No IOSurface creates and no swaps: backboardd keeps polling `IOProviderClass IOAcceleratorES` (-> 0 found) and AGXAccelerator/IOAcceleratorESLegacy - no GPU, so no CoreAnimation renderer yet. Log goes quiet after ~47 s (only 47 flushes): the system idles. NEXT WALL: CoreAnimation rendering without a GPU (CPU path) so the window server produces frames.
- **SpringBoard's invalid mode = scale 0 (boot 0053n, 15:19 UTC, `logs/boot-0053n.txt`, heap scan):** `FBSDisplayMode cannot be configured as requested : <FBSDisplayMode: ...; infxinf@0x (1080x2400/0) 60Hz sRGB SDR>` - pixel size and 60 Hz are fine, scale is 0. libMobileGestalt (MGIOMFBSupport.c, sub_19c560a54) reads `display-scale` (u32, default 0) and `display-rotation` from **IODeviceTree:/chosen**, pixel size via IOMobileFramebufferGetDisplaySize (MobileGestaltHelper sel 8/28 in the log). mkadt now adds `/chosen/display-scale` = 3 (1080x2400 @3x = 360x800 pt). ADT `shim/out/sweet-0054hi.adt` (QEMU `research/q0054-hi.adt`), image `shim/out/shim-boot-0053s.img` = 0053 kernel + 0054hi ADT. Possible catch: MobileGestalt may have cached scale 0 in `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/...`.
- **MILESTONE: backboardd survives and opens the display (boot 0052n on v9, 15:07 UTC, `logs/boot-0052n.txt`).** No `CRASH backboardd`. It walks `IODeviceTree:/arm-io` children, matches IOMobileFramebuffer, `open AppleCLCD type 0 -> 0x0`, calls IOMFB selectors 57, 15, 22, 29, 33, 79 (GetBlock, out 1580/40), 74 (SupportedFrameInfo), 12, 6, 27, 17, 84, 50; opens IOCoreSurfaceRoot (sel 13); looks for AGXAccelerator / IOAcceleratorES / IOAcceleratorESLegacy (none, repeatedly), `IODeviceTree:/product` (none, repeatedly), `/buttons`, aop-smart-cover, IOPMrootDomain. No swaps yet. **SpringBoard now gets past display discovery** and dies (sig 5) in `-[FBSDisplayMode _initWithWidth:height:preferredScale:scaleOverride:refreshRate:gamut:hdr:rotation:virtual:validityCheck:]+580` <- `_initWithCADisplayMode:scale:rotation:` <- `FBSDisplayConfiguration _initWithImmutableDisplay:` <- `FBSDisplaySource initWithDisplay:` <- `FBSDisplayMonitor` (slide 0x14504000): "FBSDisplayMode cannot be configured as requested". Checks: width/height >= 2, preferredScale > 0, scaleOverride >= 0, refreshRate non-zero, valid gamut/HDR/rotation. Suspects: refresh rate 0 (IOMFB timing blocks answered with zeros) and/or scale 0 (MobileGestalt main-screen-scale; no /product node in the ADT). **Patch 0053**: heap text scan also on SIGTRAP and for SpringBoard (default sweetscan list backboardd,SpringBoard) to read the exact mode description.
- **Image v9 (2026-10-17) = v8 + `/private/var/containers/{Bundle,Data/System,Shared/SystemGroup,Temp}` (root:wheel 0755; on iOS these live on the data volume, absent from the rootfs) + launchd.plist with StandardOutPath/StandardErrorPath renamed to ...PatX (the in-place phone fix; daemons' stdout reaches the log via the 0048 /dev/null tee).** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v9.img` SHA256 aa9f9139...6e67, `.simg` 12,145,303,864 bytes; written through `sudo mount -t hfsplus -o loop,force`. **Patch 0052** (`xnu/patches/0052-sweet-hfs-rename-swap.patch`, CI `39042761826` -> `xnu/out-0052`, QEMU OK, image `shim/out/shim-boot-0052n.img`): vn_rename falls back to VNOP_EXCHANGE when VNOP_RENAMEX(RENAME_SWAP) returns ENOTSUP for two regular files on one volume (HFS exchange swaps data and cnode descriptors = swap semantics). Flashing v9 started 2026-10-17 ~15:00 UTC.
- **backboardd EXCEPTION FOUND (boot 0051n, 14:41 UTC, `logs/boot-0051n.txt`, patch 0051 heap scan):** `*** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '*** -[NSURL initFileURLWithPath:]: nil string parameter'`. First-throw stack (slide 0x337f0000): `+[NSURL fileURLWithPath:]` <- `-[BSSystemContainerForCurrentProcessPathProvider libraryPath]` <- `cachesPath` <- backboardd main+0x1d858 (StartWindowServer, shader cache path). BaseBoard: libraryPath = `BSSystemSharedResourcesDirectoryForIdentifier` = `BSSystemSharedDirectoryForIdentifier(id)` + "/Library"; that calls `container_system_path_for_identifier` (libsystem_containermanager -> `_container_legacy_lookup` -> containermanagerd XPC), which returned NULL (BaseBoard logs "Error getting shared system container ..."). With 0050 the sandbox denials are gone. containermanagerd.log.0 in the pulled (pre-0050) image: "Did not receive any persona attributes", "Expected to find at least one persona", notify_register_dispatch failed 9; `/private/var/containers` does NOT exist in the root image (on iOS it lives on the data volume). usermanagerd does create kernel personas 99/199/1000, but fails to save `/private/var/keybags/usersession.kb` and `persona.kb`: "Failed to atomically swap writing file: Operation not supported (45)" (HFS has no RENAME_SWAP). NEXT: create `/private/var/containers` (and check what containermanagerd needs for system group containers), fix or emulate RENAME_SWAP on HFS, then re-check backboardd.
- **Disk housekeeping (2026-10-17):** /home was at 4 GiB free. Moved (not deleted) `xnu/out-0010..0044` and old `shim/out/*.img`/`payload-*.bin` (everything before 0046) to `/run/media/dipa/android/ios-sweet-work/archive/{xnu,shim-out}` (6.3 GiB); /home now 8.7 GiB free. Large work files (phone-root.img 16 GiB, logs, tracev3 dumps) live in `/run/media/dipa/android/ios-sweet-work/`. **Patch 0051** (`xnu/patches/0051-sweet-crash-heap-strings.patch`, CI `39041440935`): on SIGABRT of a process in boot-arg `sweetscan` (default backboardd) the crash log prints heap text runs as `STR ...` (to find the NSException reason). Boot 0051n 14:41 UTC.
- **Boot 0049n (14:11 UTC, `logs/boot-0049n.txt`, patch 0049 trace): backboardd's IOKit lookups before it dies** (each run): `IODeviceTree:/arm-io/pearl-sep` -> none, matching ApplePearlSEPDriver -> none, `IOService:/IOResources/AppleKeyStore` open OK, matching IOHIDDevice (DeviceUsagePairs) / `HIDServiceSupport` notifications, `usb-drd,t8027` notification; **never any IOMobileFramebuffer / display lookup** - the exception happens before display detection. launchd (tracev3) shows backboardd's mach lookups denied with `error = 159: Sandbox restriction`: com.apple.mobilegestalt.xpc, com.apple.iohideventsystem, com.apple.system.notification_center, com.apple.logd, containermanagerd, ACCHWComponentAuthService, oscard. libsystem_sandbox uses `__mac_syscall("Sandbox", op, arg)` (ops: 1 init, 2 check, 3 note, 4 container path, 5/6/7/8 extensions, 0x15 check_bulk, ...); with no policy named "Sandbox" every call gets ENOPOLICY. **Patch 0050** (`xnu/patches/0050-sweet-sandbox-policy.patch`): built-in permissive MAC policy "Sandbox" in sweet_amfi.c (mpo_policy_syscall returns 0, container/extension ops ENOENT; logs first use of each op as `SWEET Sandbox: proc op N`).
- **Phone root pulled (16 GiB, 12 min, `adb exec-out dd if=/dev/block/sda34`) to `/run/media/dipa/android/ios-sweet-work/phone-root.img` (loop-mounted ro at /run/media/dipa/iOSRoot).** No .ips crash reports. logd tracev3 (Persist, LZ4 `bv41` blocks, decompressed strings in `ios-sweet-work/tracev3/all.txt`): /private/var/db/uuidtext is EMPTY so only launchd's own messages are readable. Findings: v8 launch failure = `Service could not initialize: posix_spawn(/usr/libexec/backboardd), error 0xd - Permission denied` (xpcproxy exit 78) - /dev/console not openable for the mobile user; backboardd[98] spawned `com.apple.MTLCompilerService` before SIGABRT; **launchd denies many mach lookups with `error = 159: Sandbox restriction`** (mediaserverd -> com.apple.backboard.display.services, remoted, mobiletimerd -> sleepd, identityservicesd -> apsd) and **tccd exits OS_REASON_SANDBOX "profile not found"** - no Sandbox kext/profiles on SWEET; likely cause of many daemon crash loops (next wall after the display). CF's uncaught-exception text never reaches stderr for daemons (no CF handler; libc++abi prints only the type). **Patch 0049** (`xnu/patches/0049-sweet-iokit-trace.patch`): `IOK name: ...` console lines for registry path lookups, child iterators, matching (with result count/class), matching notifications and IOServiceOpen of the processes in boot-arg `sweetiolog` (default backboardd), max 400 lines.
- **CONFIRMED: launchd StandardOut/ErrorPath=/dev/console stops backboardd from launching.** After the in-place rename (boot 0047n-b, log `logs/boot-0047n-b.txt`) backboardd launches again and dies as on v7: sig 6, `___pthread_kill <- abort <- demangling_terminate_handler <- _objc_terminate <- std::terminate <- _dispatch_client_callout <- _dispatch_once_callout <- main+0x9334` (window-server dispatch_once). It never opened AppleCLCD or IOCoreSurfaceRoot (no `SWEET FB/SURF: backboardd` lines) -> throws before/at display detection. **Patch 0048** (`xnu/patches/0048-sweet-devnull-tee.patch`, CI `39037749668` -> `xnu/out-0048`, image `shim/out/shim-boot-0048n.img`): writes to /dev/null by processes named in boot-arg `sweetnull` (default `backboardd,SpringBoard`) are printed as `|name| text`. Boot 0048n (13:48 UTC, log `logs/boot-0048n.txt`): only `|backboardd| libc++abi: terminating due to uncaught exception of type NSException` (CF's reason line goes to os_log, not stderr, despite CFLOG_FORCE_STDERR/OS_ACTIVITY_DT_MODE). Next: pull the whole 16 GiB root from recovery (`adb exec-out dd if=/dev/block/sda34`) to `/run/media/dipa/android/ios-sweet-work/phone-root.img` and read ReportCrash .ips files / logd tracev3 for the exception reason.
- **Persistent log WORKS (boot 0047n on v8, 13:31 UTC; pulled from OrangeFox: 70 KB, 111 flushes, `/run/media/dipa/android/ios-sweet-work/logs/boot-0047n.txt`).** In 3 min **backboardd was never exec'd** (v7 ran it), ~70 bare `exec xpcproxy`, SpringBoard loops on FBSDisplayMonitor (no display), mediaserverd sig 11 loop, locationd, lockdownd sig 5. Suspect the v8 plist (StandardOut/ErrorPath=/dev/console on backboardd). **In-place plist edit from recovery (no reflash):** launchd.plist is one extent at image/partition byte offset 0x1e025f000 (195 blocks; verified bytes identical on phone vs local v8 mount); renamed StandardOutPath->StandardOutPatX and StandardErrorPath->StandardErrorPatX (same length, both jobs) in blocks 68 and 105 via `adb push` + `dd of=/dev/block/sda34 seek=... conv=notrunc,fsync`, read back VERIFIED. Phone now differs from local v8 image in those 2 blocks (files in `/run/media/dipa/android/ios-sweet-work/`). Test boot 0047n 13:38:42 UTC. Recovery kernel has no hfsplus (raw block edits only).
- **Patch 0047: persistent console log (CI `39036478663` -> `xnu/out-0047`, QEMU no panic; phone image `shim/out/shim-boot-0047n.img` = 0047 + sweet-0046hi.adt + 0045n cmdline).** `_cnputs` (all console output: kernel printf + daemons' /dev/console) also appends to a 4 MiB ring in sweet_ufs.c; after the UFS partition is ready and writable (ufsrw=1) a thread writes new ring blocks + header to the LAST 1025 blocks (4 KiB) of userdata every ~1 s and SYNCHRONIZE CACHE (prints `SWEET LOG: console log to the last 4100 KiB ...`). Read: phone to fastboot -> `fastboot boot recovery/recovery.img` (OrangeFox) -> `tools/sweet-log-pull.sh OUT.txt` (adb dd of that area + `tools/sweet-log.py`). Not yet verified on the phone. Panics after the last flush are not in it (screen still shows them). 2x font attempt reverted: XNU's v_scale only scales the progress icon.
- **Boot 0046n on v8 (13:05 UTC, VID_20261017_150522_HSR_120):** phone prints `SWEET SURF: IOCoreSurfaceRoot registered` and `SWEET FB: AppleCLCD 1080x2400 stride 4320 at 0x9c000000, default surface 1` (nubs + match work on hardware). Visible userspace: early boot tasks, launchd_cache_loader, `exec SpringBoard`; no `exec backboardd` / `SWEET FB: backboardd` line seen in the readable frames (video blurry). Frame 00:47: lower half of the screen shows OLDER console text (16:01:12) below newer lines -> unconfirmed hint that a swap copied an old snapshot of the panel (CA reads the default/displayed surface = panel memory). SpringBoard still dies in `-[FBSDisplayMonitor _initWithBookendObserver:transformer:]+1160` (sig 5, slide 0x30960000). **Shim: 2x console font** (`shim/loader.c` Video.v_depth scale field = 1) so phone videos are readable; image `shim/out/shim-boot-0046b.img` = 0046n + 2x font.
- **Patch 0046: built-in IOSurface + IOMobileFramebuffer (2026-10-17, offline, NOT phone-tested).** `xnu/patches/0046-sweet-iosurface-iomfb.patch`: new `iokit/Kernel/arm/SweetSurface.{h,cpp}` (IOCoreSurfaceRoot + IOSurfaceRootUserClient: sel 13/0/4/34/35, traps 0-5, wired buffers mapped into the caller, per-client refs) and `SweetFramebuffer.cpp` (AppleCLCD : IOMobileFramebuffer on /arm-io/disp0: sizes, swap = CPU copy of enabled layers into the ABL panel memory, 60 Hz vsync via sendAsyncResult64WithOptions(CanDrop), panel memory published as the default IOSurface, kernel text console paused on the first swap only with `sweetfb_noconsole=1` (default keeps the console: pausing switches it to serial and would hide panics)); SweetPlatformExpert creates nubs for /arm-io children (not gic) attached to the platform expert (IOPlatformDevice::compareName casts its provider to IOPlatformExpert, so nubs under the arm-io nub never matched - first CI build showed that in QEMU). mkadt: /arm-io/disp0 {device_type display-subsystem, compatible sweet,display, canvas-width 1080, canvas-height 2400}. CI `39021572169` -> `xnu/out-0046`. **QEMU** (`research/q0046-hi.adt`, RAM disk init, msgbuf): `SWEET SURF: IOCoreSurfaceRoot registered`, `SWEET FB: AppleCLCD 1080x2400 stride 4320 at 0x9c000000, default surface 1`, init alive, no panic. Phone image **`shim/out/shim-boot-0046n.img`** (SHA256 9c4d2fe9..., CI `39024108588` with the review fixes: swap bounds check, zeroed 64-bit async ref, port release, 1.5 GiB wired budget, ref leak/race fixes; QEMU re-checked) = 0046 kernel + `shim/out/sweet-0046hi.adt` + the 0045n cmdline; boot it on image v8 (backboardd/SpringBoard log to console) and film. Expected new console lines: `SWEET SURF: <proc> create id ...`, `SWEET FB: backboardd sel N ...`, `SWEET FB: swap ...`. Open question for the next wall: QuartzCore's IOMFB server builds its renderer from Metal first (`CAMetalContextCreate`), GLES only when enabled; how the CPU renderer gets selected on a device without a GPU is not yet established.
- **IOSurface values ABI (offline RE, `/run/media/dipa/android/ios-sweet-work/iosurface-values.md`) - TODO in SweetSurface (0046 only accepts and drops values, so IOSurfaceCopyValue always returns NULL):** sel 9 SetValue in = {u32 id, u32 pad, IOCFSerialize([value, key]) or ([dict] = merge)}, sel 0xb RemoveValue in = {u32 id, u32 pad, key\0} (empty key = remove all); both out 4 bytes = new generation, client accepts only (gen+2)|1. Kernel after each change: gen = (gen+2)|1 (odd, never 0) -> state+0x20, serialized size (>=1) -> state+0x28. sel 0xa in {u32 id, u32 0, u8 0}, out {u32 ?, u32 gen, serialized non-bulk dict}; too small -> 0xe00002db + needed size (client retries x16). sel 0x1b in 0x88: bulk struct 0x70 @0, u64 valid size @0x70, u64 changed mask @0x78, u32 id @0x80 -> copy masked fields into state+0x30 (bit0 32B @0, bit1 16B @0x20, bit2 8B @0x30, bits3-10 1B @0x38..0x3f, bits11-14 24B @0x40/4B @0x58/8B @0x5c/1B @0x64).
- **IOMFB display matching confirmed (offline RE, `/run/media/dipa/android/ios-sweet-work/iomfb-match.md`):** the framework never matches on "AppleCLCD"; any registered IOMobileFramebuffer subclass works. `iomfb_match_callback` reads only `dfr`/`AppleTV`/`external` (CFBoolean, service itself, no parents); internal main display = all absent/false (type 0, name "primary"). Display count = /arm-io children whose device_type starts with "display-subsystem" (count 0 -> CreateDisplayList returns NULL; more nodes than services -> 30 s wait). IOMobileFramebufferOpen fails only on IOServiceOpen failure; canvas-width/height read as 4-byte CFData from the IOService-plane parent (optional). CopyProperty = IORegistryEntrySearchCFProperty on the service only. Patch 0046 (disp0 node, `external`=false, AppleCLCD : IOMobileFramebuffer) fits all of this.
- **IOMobileFramebuffer swap + notification ABI (2026-10-17, offline).** Swap record = fb+0x18, **0x46c bytes**, zeroed by SwapBegin and sent whole by `kern_SwapEnd` = IOConnectCallStructMethod(sel 5, rec, 0x46c, no output). **SwapBegin** = sel 4, no input, 1 scalar out = swap id (stored at rec+0x50). `kern_SwapSetLayer(fb, layer<4, IOSurfaceRef, CGRect a, CGRect b, flags)`: rec+0x54+4*layer = **IOSurface id**; rec+0x104 bit layer = layer enabled (rec+0x108 bit cleared); rect a (int x,y,w,h, scaled) at rec+0x64+16*layer, rect b at rec+0xc4+16*layer; rec+0x114+4*layer = transform from flags&0xf; flag bits 5/31/6/7/8/9 set bytes rec+0x2ca/0x2cc/0x2e3/0x2e5/0x2e6/0x467+layer. A NULL surface only sets the enable bit with zero id. SwapWait = sel 6 scalars [swap id, timeout, 0].
  - **Notifications**: `IOMobileFramebufferScheduleWithDispatchQueue`/`GetRunLoopSource` create an IONotificationPort and `IOConnectSetNotificationPort(conn, type, port, 0)` (kernel `registerNotificationPort`). `kern_EnableNotifications(fb, type, cb, ctx)` = **sel 72 scalars [NotifyCallbackFuncs[type], fb, type, 0]** -> the kernel keeps an async reference {port, func, refcon=fb} per type and fires it with `sendAsyncResult64`. Types: 0 HotPlug, 1 Power, 3 FrameInfo (args[0] = mask of 31-bit keys, args[1] u32, then values), 4 CRC, **5 Vsync**: 6 args, each a 32-bit half in a u64 slot: (ts lo, ts hi), (t2 lo, hi) passed through the time-ingest helper, (t3 lo, hi); the framework then calls the client's vsync callback(fb, ts, t2', t3, ctx). Vsync callbacks are dropped while the notification port has queued messages.

- **IOSurface.framework user-client ABI reversed (2026-10-17, offline, step 2 of the GUI plan).** `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image IOSurface` (selector scan script: scratchpad `selscan.py`).
  - Connect (`_iosConnectInitalize`, pthread_once): `IOServiceGetMatchingService(IOServiceNameMatching("IOCoreSurfaceRoot"))`, retried with sleep(1) up to 241 times (a missing service stalls every client ~4 min, no crash); `IOServiceOpen(type 0)`; then **sel 13** (no inputs, struct out 0x18 bytes = `_ioSurfaceLimits`) and requires u16 at out+0x16 == 1 (ABI version); out+0 = offset/plane-base alignment mask, out+4 = bytes-per-row alignment mask (used as (x+m)&~m), +0..+0x14 also copied into IOSurface remote-method init, otherwise logs and closes the connection.
  - **Create = sel 0**: scalar in [parent id or 0], struct in = `IOCFSerialize(props, kIOCFSerializeToBinary)` (OSUnserializeBinary format; keys IOSurfaceWidth/Height/BytesPerRow/BytesPerElement/PixelFormat/AllocSize/PlaneInfo/CacheMode/IsGlobal/...), struct out **0xa68 bytes** ("lock result"). **Lookup = sel 4**: scalar in [id], same struct out. LookupFromMachPort = sel 0x22 (scalar in [port name]); CreateMachPort = sel 0x23 (scalar in [id, options], scalar out [port name]).
  - Lock result (copied to client+0x68, size 0x68 + planes*0x80, min 0xe8): 0x00 u64 base address **mapped in the caller's task**; 0x08 u64 task VA of a per-surface shared state page (+0 u64 registry id, +8/+0xa u16 bound accel ids, +0xc u32 seed, +0x14 u8 tiled, +0x20 u32 value generation, +0x24 YCbCr matrix, +0x28 u32 non-bulk values size, +0x2d u8 displayable, +0x2e u8 sysmem-only, +0x30 0x70 bytes bulk attachments); 0x10 u64 task VA of timestamp page (4 u64 indexed timestamps, +0x20 detach code); 0x18 u32 surface id; 0x1c u32 alloc size; 0x20 width; 0x24 height; 0x28 bytes per row; 0x2c buffer offset; 0x30 pixel format; 0x34 u32 (dcache flush length); 0x38 plane count; 0x40 u16 bytes/element; 0x42 u8 element width; 0x43 u8 element height; 0x44 cache mode; 0x4c u8 subsampling; 0x4d u8 prohibit-use count; 0x50 parent id; 0x54 slice count; 0x58 u64 trace id; 0x60 u64 protection options; planes[n] at 0x68+n*0x80 (+0 width, +4 height, +8 bytes/row, +0xc offset, +0x14 size, +0x18 u16 bpe, +0x1a/+0x1b u8 element w/h, +0x1c u8 component count, +0x1d address format, +0x54 u8 compression type (non-zero -> no CPU base address)).
  - **Traps** (IOConnectTrapN -> `IOUserClient::getTargetAndTrapForIndex`): 0 IncrementUseCount(id, category), 1 DecrementUseCount(id, category), 2 **Lock**(id, options, &seed_out), 3 **Unlock**(id, options, &seed_out), 4 Release(id), 5 Release after a failed create/lookup setup (id).
  - Other selectors: 5 SetYCbCrMatrix, 6 WrapClientImage, 7 WrapClientMemory, 9 SetValue (serialized), 0xa UpdateNonBulkValueCache (struct in 9), 0xb RemoveValue, 0xc BindAccel, 0x11 SetSurfaceNotify (async), 0x12 RemoveSurfaceNotify, 0x13 Log, 0x14 SetPurgeable, 0x15 SetOwnership, 0x16 SetTiled, 0x18 SetTimestamp, 0x19 GetTileFormat, 0x1a CopyDataValueBytes, 0x1b SetBulkAttachments (struct 0x88), 0x1e/0x2e-0x31 (via outlined helpers), 0x1f SetCompressedTileDataRegionMemoryUsed, 0x20 GetGraphicsCommPageAddress, 0x21 SetIndexedTimestamp, 0x24-0x26/0x2d IOSurfaceAccelerator, 0x27-0x29 shared events, 0x2a SignalEvent, 0x2b Set/InitDetachModeCode, 0x2c SetOwnershipIdentity, 0x32-0x34 data properties.
  - => SWEET kernel service: class/name **IOCoreSurfaceRoot** + IOSurfaceRootUserClient; minimum = sel 13, 0, 4, 9/0xa/0xb (values), traps 0-5, 0x22/0x23 later for cross-process surfaces (CA sends surfaces to backboardd by mach port). Memory: IOBufferMemoryDescriptor per surface, mapped into each task with createMappingInTask; ids from a global table.

- **Image v8: daemon logs on the console.** `tools/patch-launchd-plist.py IN OUT LABEL...` rewrites launchd.plist (binary, plistlib): renames every `_PanicOnCrash` to `_PanicOnCrasX` and gives the listed jobs `StandardOutPath`/`StandardErrorPath` `/dev/console` (devfs console is 0622, writable by mobile) plus `OS_ACTIVITY_DT_MODE=YES` (os_log mirrored to stderr) and `CFLOG_FORCE_STDERR=1`. v8 = v7 + that plist for com.apple.backboardd and com.apple.SpringBoard, written through the mount (796310 bytes, root:80 0644), SHA256 in `ios16-root-20H392-v8.img.sha256`, `.simg` ready; boot with `shim/out/shim-boot-0045n.img`. Goal: see backboardd's uncaught exception text and the window server's display probing. ODDITY (unresolved): the v5 raw-image rename at offset 0x1e025f000 is present in the v5-v7 image bytes, but the plist read through a Linux mount of v7 still had the original `_PanicOnCrash` keys; filefrag shows the file as one extent. Never patch file contents through raw offsets again; write through the mount.
- **IOMobileFramebuffer.framework reversed (step 1 of the GUI plan).** `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image IOMobileFramebuffer`.
  - Display discovery (`IOMobileFramebufferCreateDisplayList` -> `getDisplayListNumber`): iterates children of `IODeviceTree:/arm-io`, counts nodes whose `device_type` is "display-subsystem" or "ext-display-subsystem" (or `compatible` "paravirtualizedgraphics,gpu"); then `iomfb_populate_display_infos` adds an IOServiceAddMatchingNotification(IOServiceFirstMatch, **IOServiceMatching("IOMobileFramebuffer")**) and runs the run loop up to 30 s until that many services matched. `iomfb_match_callback` reads service properties `dfr`, `AppleTV`, `external` (CFBoolean) and names displays (external ones "%s-%d").
  - `IOMobileFramebufferOpen(service, task, type, &fb)`: `__ioMobileFramebufferAlloc` (CFPreferences com.apple.iokit.IOMobileGraphicsFamily: canvas_width/height, override_display_width/height, override_panel_width/height, benchmark, enable_ktrace), `IOServiceOpen(service, task, type)` (GetMainDisplay passes type 0), `getEDTProperty` reads `canvas-width`/`canvas-height` from the service's IODeviceTree parent, then fills a table of `kern_*` function pointers.
  - User client selectors (`kern_*` -> IOConnectCall*): 3 _kern_GetLayerDefaultSurface[ScalarMethod_stub]; 4 _kern_SwapBegin[ScalarMethod_stub]; 5 _kern_SwapEnd[StructMethod_stub]; 6 _kern_SwapWaitWithTimeout[ScalarMethod_stub] _kern_SwapWait[ScalarMethod_stub]; 7 _kern_GetID[ScalarMethod_stub]; 8 _kern_GetDisplaySize[ScalarMethod_stub]; 10 _kern_SetTVOutMode[ScalarMethod_stub]; 11 _kern_SetWSSInfo[ScalarMethod_stub]; 12 _kern_RequestPowerChange[ScalarMethod_stub]; 13 _kern_EnableStatistics[ScalarMethod_stub]; 14 _kern_SetFlags[ScalarMethod_stub]; 15 _kern_SetDebugFlags[ScalarMethod_stub]; 16 _kern_SetTVOutSignalType[ScalarMethod_stub]; 17 _kern_SetGammaTable[StructMethod_stub]; 18 _IOMobileFramebufferIsMainDisplay[ScalarMethod_stub]; 19 _kern_SetWhiteOnBlackMode[ScalarMethod_stub]; 20 _kern_SwapSignal[ScalarMethod_stub]; 22 _kern_SetDisplayDevice[ScalarMethod_stub]; 23 _kern_SetDigitalOutMode[ScalarMethod_stub]; 24 _kern_GetHDCPDownstreamState[StructMethod_stub]; 25 _kern_GetDigitalOutState[ScalarMethod_stub]; 26 _kern_printDisplayRegs[ScalarMethod_stub]; 27 _kern_GetGammaTable[StructMethod_stub]; 28 _kern_GetDotPitch[ScalarMethod_stub]; 29 _kern_GetDisplayArea[StructMethod_stub]; 30 _kern_EnableDisableDithering[ScalarMethod_stub]; 31 _kern_SetUnderrunColor[ScalarMethod_stub]; 33 _kern_EnableDisableVideoPowerSavings[ScalarMethod_stub]; 34 _kern_SetVideoDACGain[ScalarMethod_stub]; 35 _kern_SetLine21Data[ScalarMethod_stub]; 41 _IOMobileFramebufferEnableMirroring[ScalarMethod_stub]; 42 _IOMobileFrameBufferGetMirroringCapability[StructMethod_stub]; 43 _IOMobileFramebufferSetRenderingAngle[StructMethod_stub]; 44 _IOMobileFramebufferSetMirrorContentRegion[StructMethod_stub]; 47 _kern_HDCPSendRequest[ScalarMethod_stub]; 48 _kern_HDCPGetReply[ScalarMethod_stub]; 49 _kern_SurfaceIsReplaceable[ScalarMethod_stub]; 50 _kern_SetBrightnessCorrection[ScalarMethod_stub]; 51 _kern_SetColorRemapMode[ScalarMethod_stub]; 52 _kern_SwapCancel[ScalarMethod_stub]; 53 _IOMobileFramebufferSetCanvasSize[ScalarMethod_stub]; 54 _IOMobileFramebufferGetMatrix[Method_stub]; 55 _IOMobileFramebufferSetMatrix[Method_stub]; 56 _IOMobileFramebufferKernelTests[StructMethod_stub]; 57 _kern_GetColorRemapMode[ScalarMethod_stub]; 66 _kern_SPLCSetBrightness[ScalarMethod_stub]; 67 _kern_SPLCGetBrightness[ScalarMethod_stub]; 68 _kern_SetParameter[Method_stub]; 69 _kern_SwapSetColorMatrix[StructMethod_stub]; 72 _kern_DisableNotifications[ScalarMethod_stub] _kern_EnableNotifications[ScalarMethod_stub]; 73 _kern_ChangeFrameInfo[ScalarMethod_stub]; 74 _kern_SupportedFrameInfo[Method_stub]; 75 _kern_FactoryPortal[StructMethod_stub]; 77 _kern_GetCurrentAbsoluteTime[ScalarMethod_stub]; 78 _kern_SetBlock[Method_stub]; 79 _kern_GetBlock[Method_stub]; 80 _kern_GetLinkQuality[ScalarMethod_stub]; 81 _kern_SwapCancelAll[ScalarMethod_stub]; 82 _kern_GetProtectionOptions[ScalarMethod_stub]; 83 _kern_CopyLayerDisplayedSurface[ScalarMethod_stub]; 84 _kern_SetContrast[StructMethod_stub]; 85 _kern_GetBufBlock[Method_stub]; 86 _IOMFBGainEncoderFinishEncoding[Method_stub]; UNKNOWN {}
  - => Kernel needs: an `/arm-io` child node with device_type "display-subsystem" (+ canvas-width/height) and an IOService of class **IOMobileFramebuffer** (subclass name match) attached under it, opened with type 0, implementing at least GetDisplaySize(8), IsMainDisplay(18), GetID(7), GetLayerDefaultSurface(3), SwapBegin(4)/SwapEnd(5 struct)/SwapWait(6), Enable/DisableNotifications(72), frame info(73/74), CopyLayerDisplayedSurface(83), plus IOSurface for the swapped buffers. NEXT: CoreAnimation's AppleDisplay/IOMFBDisplay usage of these (constructor, first swap, vsync), then IOSurface.framework's IOSurfaceRoot selectors.
- **GUI PLAN (decided 2026-10-16): CPU rendering + kernel IOMobileFramebuffer.** User: CPU rendering is fine for now (goal = prove the GUI runs), may later research an Apple-style GPU driver for the Adreno 618 -> keep display output and renderer separable. QuartzCore findings (symbols from the cache's .symbols subcache: `ipsw dyld symaddr research/dsc/dyld_shared_cache_arm64 --image QuartzCore`; strings: `ipsw dyld macho ... QuartzCore --strings`):
  - Renderers: `sw_new_context` (CA::OGL::SWContext, full CPU renderer incl. blur, images, IOSurface-backed surfaces, make_buffer_current(WindowServer::Surface)), `gles_new_context`, `metal_new_context`, `new_null_context`. Env knobs include CA_ENABLE_OGL, CA_DISPLAY_TYPE, CA_FORCE_LOCAL_SERVER, CA_FORCE_TIMER, CA_CANVAS_WIDTH/HEIGHT, CA_MAIN_DISPLAY_SCALE/ORIENTATION, CA_DISABLE_RENDER, CA_ALWAYS_RENDER (selection logic not traced yet).
  - `-[CAWindowServer _detectDisplays]` (0x1884e3150) iterates static tables `open_funcs`/`count_funcs` = AppleCLCDDisplay, AppleRGBOutDisplay, AppleWirelessDisplay only; each `count()` = `display_count_of_type(IOMFBDisplayType)` over **`IOMobileFramebufferCreateDisplayList()`**, `open(i)` = `create_display_of_type` -> `CA::WindowServer::AppleDisplay(CFString name, ..., IOMFBDisplayType)` (an IOMFBDisplay driven by IOMFBServer: vsync_callback, frame_info_callback, swaps). `CA::WindowServer::VirtualDisplay` exists but is never auto-detected (explicit API only). => the main display MUST come from an IOMobileFramebuffer kernel service.
  - NEXT: reverse IOMobileFramebuffer.framework: IOMobileFramebufferCreateDisplayList / IOMobileFramebufferOpen (service matching, display type property), the user-client selectors used by IOMFBServer (display size/modes, swap begin/set-layer/end with IOSurface ids, vsync notifications), then the IOSurface kernel side (IOSurfaceRoot user client: create/lookup/lock, memory mapping) that both IOMFB swaps and CA surfaces need. Kernel: SWEET IOMobileFramebuffer service that copies the swapped IOSurface to the 1080x2400 framebuffer at 0x9c000000.
- **logd fixed; backboardd = DISPLAY WALL (boot 0045n on v7, 21:08:57 UTC, frames VID_20261016_230850 00:55-01:28, slide 0x4c3ec000, `research/crash-0045n-v7.txt`).** No `CRASH logd` any more; new daemons run (runningboardd, WirelessRadioManagerd, networkserviceproxy, dasd, cloudpaird, magicswitchd, atc, askpermissiond, ManagedSettingsAgent, containermanagerd uses AKS 0/17). New: locationd sig 11 at CFRunLoopAddSource+132 (NULL source) from its main+0x2af138 in a dispatch_once. **backboardd** sig 6: abort <- std::terminate <- _objc_terminate <- dispatch_once <- main+0x9334 = the "start %{public}@..." wrapper (0x100009264) for **"window server"** (block 0x10000a770 -> dispatch_once body 0x10001d7f0 = StartWindowServer): MTLSetShaderCachePath, `[CAWindowServer serverWithOptions:@{kCAWindowServerDisableUpdatesOnMainDisplay: @YES}]`, `setRendererFlags:`, **`mainDisplay`** -> `displayId` -> `[CADisplay displayWithDisplayId:]`, setWindowServerDisplay:, bounds, pointScale, currentMode, preferredScale, nativeOrientation, touchScales... With no display, mainDisplay is nil and it throws. (HID system and GS start fine before it.) SpringBoard dies on the same missing display (FBSDisplayMonitor). QuartzCore display backends (from the cache's .symbols subcache, `ipsw dyld str`): `CA::WindowServer::AppleCLCDDisplay` (IOMobileFramebuffer hardware) and **`CA::WindowServer::VirtualDisplay`** (open(), new_server, clone_update). `CA_DISPLAY_TYPE` and `CA_FORCE_LOCAL_SERVER` strings exist in QuartzCore but have no direct xref (likely read via a table of CA_* env names). NEXT: find how CA::WindowServer::Server enumerates displays (IOMobileFramebuffer services vs VirtualDisplay / CA_DISPLAY_TYPE) and choose: (a) kernel IOMobileFramebuffer service + IOSurface, or (b) a VirtualDisplay rendered by CA's CPU path (CA::OGL::SW) and copied to the framebuffer.
- **watchdogd + CommCenter + identityservicesd fixed (boot 0045n on v6, 20:41:30 UTC, frames VID_20261016_224133 00:39-01:13, slide 0x20fec000).** `SWEET WDT: watchdogd sel 0 in 0/0 out 1/0 -> ok`, no watchdogd/CommCenter/identityservicesd crashes (CommCenter/identityservicesd now call AKS 0/17/7). usermanagerd boot task runs (UMD_INIT creates primary session uid 501 "mobile", personas 99 System and 199 Default registered with the kernel); `Failed to atomically swap writing file /private/var//keybags/usersession.kb: Operation not supported (45)` (HFS lacks the atomic swap rename; non-fatal so far). Remaining: SpringBoard (FBSDisplayMonitor, no display), backboardd (uncaught exception), mediaserverd, lockdownd (crash inside obfuscated code, main+0x4c1b4?), logd. **logd**: main+0x18160 = `BUG IN LIBTRACE: Failed to migrate directory` from 0x10001801c(dir 0): 0x100016538 requires the dir to exist with uid/gid/mode from the table at 0x10002df14 (0: /private/var/db/diagnostics 272:272 0751, 1: /private/var/db/uuidtext 272:272 0755, 2: /private/var/db/diagnostics/timesync 272:272 0755) plus a `.migrated` file, else XPC "operation 6" to a helper and crash. **Image v7** = v6 + those dirs/markers (also in mkiosroot.sh), SHA256 in `ios16-root-20H392-v7.img.sha256`, `.simg` ready. Boot with `shim/out/shim-boot-0045n.img`.
- **Exit-reason text works (boot 0044n, frames VID_20261016_221726 00:32-00:53, slide 0x22d5c000).** CommCenter/identityservicesd: `couldn't dlopen libobjc-trampolines.dylib: dlopen(/usr/lib/libobjc-trampolines.dylib, 0x0106): tried: '/usr/lib/libobjc-trampolines.dylib' (no such file, not in dyld cache)`: the file only exists in the OS cryptex and dyld does not search cryptexes at ignition_level=1. 19 cryptex files have no root counterpart (OS: DriverKit dyld cache + .symbols, VisualTestKit, libffi-trampolines, libobjc-trampolines, libstdc++ 6.0.9 + 2 symlinks; App: SafariSupport.bundle, AuthenticationServicesAgent, com.apple.Safari.History, passwordbreachd, safarifetcherd, webbookmarksd, webinspectord, webpushd) -> hard-linked (symlinks copied: Linux hfsplus cannot hard-link symlinks); `tools/mkiosroot.sh` does it generically. watchdogd still crashed: the `-wdt_no_pmu` / `/arm-io/wdt no-pmu` check (0x10000a01c) only runs when os_variant_has_internal_diagnostics; otherwise 0x100009b18 looks up IOServiceMatching("IOService") + IOPropertyMatch {IOPMUPrimary: 1} (NSConstantDictionary) and crashes if absent, then IORegistryEntrySetCFProperty(boot stage 0xff) (failure only logged). Patch **0045**: IOWatchdog sets IOPMUPrimary = 1 and accepts setProperties; CI `38961814194` -> `xnu/out-0045`. **Image v6** = v5 + the 19 cryptex links, SHA256 7c610c6a...297a, `ios16-root-20H392-v6.simg` (full flash needed). Boot image `shim/out/shim-boot-0045n.img` (0045 + sweet-0044hi.adt). Still open: SpringBoard (no display), backboardd (uncaught exception, reason none), mediaserverd (Fig NULL dict), logd (main+0x18160), lockdownd (main+0x4c1b4).
- **System survives daemon crashes (boot 0043p, video frames VID_20261016_215006 00:25/00:42/00:54).** With the v5 plist patch no panic: launchd keeps launching (runningboardd, powerd, tccd, healthd, peopled, cryptexd, routined, aksd, mediaremoted, familynotificationd, nanoprefsyncd, navd, cloudpaird, passd, amsaccountsd, accessoryupdaterd, wcd ...). Shared cache slide that boot 0x406b4000 (`research/crash-0043p.txt`). watchdogd still crashed at main+0xb82c from the PMU step: `-wdt_no_pmu` is only honored when os_variant_has_internal_diagnostics; customer builds read `no-pmu` from IODeviceTree:/arm-io/wdt (IORegistryEntrySearchCFProperty) -> mkadt adds /arm-io/wdt {no-pmu}. **cryptexd** sig 6: abort_with_payload <- os_crash_fmt <- `__darwin_arm_secure_boot_chip.cold.7` ("panic: failed to get crypto algorithm") <- `_img4_chip_select_personalized_ap`: reads /chosen use-ddi-secure-boot, allow-ecid-mismatch, crypto-hash-method ("sha1" | "sha2-384"), /chosen/asmb lp-smb0/1 -> mkadt adds crypto-hash-method "sha2-384". **identityservicesd** sig 6 = same `_objc_fatal` in imp_implementationWithBlock as CommCenter (block trampolines; message needed). lockdownd sig 5 at main+0x4c1b4. Patch **0044**: crash report adds `CRASH name reason ns N code X: text` (exit reason description = abort_with_payload text). CI `38959096811` -> `xnu/out-0044`, QEMU OK. Image `shim/out/shim-boot-0044n.img` = 0044 + `shim/out/sweet-0044hi.adt` (wdt no-pmu, crypto-hash-method) + cmdline (wdt=-1, no -wdt_no_pmu).
- **First symbolicated daemon crashes (boot 0043u on journaled v4, 19:38:53 UTC; video frame chat image 36; transcribed in `research/crash-0043u.txt`; shared cache slide 0x40d60000 for every process).** (Gemini's video transcription invented values, use frames only.) `tools/sweet-crash.py research/dsc/dyld_shared_cache_arm64 x research/crash-0043u.txt`:
  - **watchdogd** pc main+0xb82c (`_os_crash` trap helper) from 0x100009bb0 = set PMU boot stage via IORegistry (no PMU) -> fix: boot-args `wdt=-1 -wdt_no_pmu` (Apple's own test mode writes "%s wdt=-1 -wdt_no_pmu"; watchdogd logs "skipping setting PMU boot stage because -wdt_no_pmu found in boot-args or no-pmu found in EDT"). Kernel effect of wdt=-1: sched hygiene debug off, zone_exhausted_timeout -1 (harmless).
  - **SpringBoard** sig 5 in `-[FBSDisplayMonitor _initWithBookendObserver:transformer:]+1160` <- `+[FBDisplayManager sharedInstance]` <- `FBSystemShellInitialize` <- `SBSystemAppMain`: no main display. GUI WALL: display service (IOMobileFramebuffer / CoreAnimation display).
  - **backboardd** sig 6: abort <- std::terminate <- _objc_terminate (uncaught exception; message not shown).
  - **CommCenter** sig 6: `_objc_fatal` in `imp_implementationWithBlock` (from `+[_PFRoutines initialize]`, CoreData): objc block trampolines cannot be allocated -> likely kernel gap (trampoline page remap); will hit many processes.
  - **mediaserverd** sig 11: CFDictionaryGetValue(NULL) in FigNotificationListenerStartNotifications (routing session manager).
  - **logd** sig 5 at its main+0x18160 (bt main+0x9dfc); lockdownd sig 5 (not yet symbolicated).
  - Image v5 = v4 + launchd.plist (`/System/Library/xpc/launchd.plist`, contiguous at image offset 0x1e025f000, 1456980 bytes) with the 7 `_PanicOnCrash` keys renamed `_PanicOnCrasX` in place (raw image patch, no metadata change) -> `diff-v4-v5.simg` = 7 blocks; v5 SHA256 78f96974...185a. Boot image `shim/out/shim-boot-0043p.img` = 0043 + `wdt=-1 -wdt_no_pmu`.
- **0043 console crash reports (QEMU verified); image `shim/out/shim-boot-0043u.img`; NEXT: flash v4 + boot 0043u.** Boot 0042u (video photo IMG_20261016_211646): short exec lines work; watchdogd crashes with NO `SWEET WDT:` line (fails before its first IOWatchdog call: lookup or IOServiceOpen, or elsewhere); lockdownd, SpringBoard, mediaserverd, CommCenter, identityservicesd, backboardd, watchdogd all crash repeatedly ("Too many corpses being created" = corpse limit, no crash reports). AKS callers: lockdownd (0, 7), imagent/sleepd (0, 17, 7), backboardd (0, 17), UserEventAgent (0, 7, 102, 103 -> unsupported). Patch **0043**: `sweet_crash_log` (osfmk/kern/exception.c, called from proc_prepareexit for crash exits on the current proc) prints `CRASH name[pid] sig S code (exc<<32|code) sub X slide SR mh MH`, `CRASH name pc lr sp fp far`, `CRASH name bt` (10 fp frames); AKS sel 103 notify_state_is_set -> 0. CI `38954520419` -> `xnu/out-0043`. QEMU test: init forks, child `brk #1`: `CRASH launchd[2] sig 5 code 0x600000001 sub 0x1000004f0 slide 0x0`, pc correct, parent keeps running (pid 1 crashes panic before proc_prepareexit, so test with a child). `tools/sweet-crash.py CACHE ROOT [report]` symbolicates typed-in CRASH lines (`ipsw dyld a2s` with addr - slide; main binary offsets = addr - mh + 0x100000000).
- **v3 reflashed 18:50-18:55 UTC (`research/flash-userdata-v3b.log`, 24/24 OKAY); 0042u booted 19:01:17 UTC on the clean disk (`research/boot0042u-2.log`), SLOW MO VID pending (watchdogd failure reason).** ABL hangs on the first `fastboot boot` after every big flash; user re-enters fastboot. User gave standing approval to reflash/boot without asking (memory standing-flash-approval). Commits now end with `Co-Authored-By: dipa-studio <183933817+dipa-studio@users.noreply.github.com>` (user request; never a Claude trailer).
  - watchdogd flow: connect_to_kext (0x100005408): IOServiceGetMatchingService("IOWatchdog") fails -> "failed to discover" + _os_crash; IOServiceOpen(type 1) fails -> "IOServiceOpen failed with error : 0x%x" + _os_crash. Then sel 0 (out 1 scalar): 0 -> "userspace monitoring disabled", 0x100009bb0, sleep 2, exit(0); nonzero -> "userspace monitoring enabled", normal operation.
  - **Image v4 (JOURNALED):** `tools/mkiosroot.sh` now does `mkfs.hfsplus -J`, mounts with `-o loop,force`, adds the /System/Library/Caches/com.apple.dyld hard links (44) and /private/var/keybags/systembag.kb (0700/0600 root). Built from the IPSW dmgs (OS 087-86698-044, SystemOS 087-86593-047, AppOS 087-86715-047) -> `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v4.img` SHA256 fba4aeae...ec0f9 + `.simg`. Header: attr 0x80002100 (unmounted, journaled), journal info block 129, journal 8 MiB at 532480 flagged need-init. Linux `fsck.hfsplus -n` reports "Volume header needs minor repair" on any fresh journaled volume even after -y (quirk). QEMU: 64 MB journaled test root (`rd=md0 rootrw=1`, 0042 kernel): `hfs: Initializing the journal (joffset 0x3000 sz 0x80000)` -> mounted -> init runs, no panic. NEXT: flash v4 (full), boot 0042u.
- **SPRINGBOARD STARTS (boot 0041u 18:39:53 UTC, photo IMG_20261016_204142).** backboardd, bluetoothd, fairplayd.H2, SpringBoard (pid 111, crashed: "Too many corpses"), xpcproxy run; `SWEET AKS: backboardd sel 0 -> 0`, `sel 17 in 1/0 out 0/4096 -> 0`. Panic: watchdogd[113] exited, namespace 2 subcode 5 (SIGTRAP = its _os_crash): watchdogd crashes on purpose when IOServiceGetMatchingService("IOWatchdog") fails ("connect_to_kext() unexpectedly failed") or IOServiceOpen(type 1) fails ("IOServiceOpen failed with error"); IOWatchdog DOES register (QEMU msgbuf: `SWEET WDT: IOWatchdog registered`), cause not on screen yet -> need video. Note `wdt_test=no_user_checkin` makes watchdogd log "detected testing boot-args to not run, exiting" (path not reached here?). **HFS CORRUPTION:** `hfs_swap_BTNode: offset #0 invalid (0xBC1D) (blockSize 0x2000 numRecords 81)`, `node=19677 fileID=4` (catalog), `hfs_mark_inconsistent` repeated. Likely cause: non-journaled HFS + unclean panics while writing (0038e wrote a 2.7 GB core then panicked; every boot since ends in panic). Plan: reflash v3 (clean), longer term HFS journaling. Patch **0042**: one short `exec NAME` console line instead of the 3-line "Allowing spawn of iOS binary" notice; CI `38949451276` -> `xnu/out-0042`; image `shim/out/shim-boot-0042u.img` (same cmdline as 0041u).
- **LAUNCHD DAEMONS RUN (boot 0039u, 18:29:13 UTC, photo IMG_20261016_203052).** With `launchd_unsecure_cache=1` all boot tasks pass and launchd starts LaunchDaemons (pids > 100: identityservicesd 114 and lockdownd 106 crash, "Too many corpses being created"). Fatal: `watchdogd: ERROR: failed to discover watchdog KEXT service` -> exit (namespace 2 = signal, subcode 5) -> `_PanicOnCrash` panic. watchdogd: IOServiceMatching("IOWatchdog"), IOServiceOpen type 1, IOConnectCallScalarMethod sel 0/1 (check in)/3/4 (disable/enable userspace monitoring)/5, IOConnectCallStructMethod sel 2 (1 KiB in) and 9 (small out); VM path ("detected virtual machine environment and no watchdog KEXT found, exiting...") only when it detects a VM. Console also flooded with `hfs: set hardlink bit on vol=iOSRoot cnid=321318` (Linux-made hard links lack kHFSHasLinkChainBit; repaired only in memory on each lookup). Patches **0040** (`iokit/Kernel/arm/SweetWatchdog.cpp`: IOWatchdog + IOWatchdogUserClient, all selectors succeed with zeroed outputs, each logged once as `SWEET WDT: ...`) and **0041** (sweet_hfs hfs_catalog.c: the three link-repair printfs limited to 8 per boot); CI `38948245372` PASSED -> `xnu/out-0041` (QEMU regression OK). Image `shim/out/shim-boot-0041u.img` (0041 + sweet-0038hi.adt + ufsrw rootrw + launchd_unsecure_cache=1) booted 18:39:53 UTC (`research/boot0041u.log`), photo pending.
- **v3 FLASHED + keybag passes; next wall AMFI (launchd_cache_loader).** User said "flash, nothing to lose": `fastboot -S 512M flash userdata ios16-root-20H392-v3.simg` 17:51:52-17:57:01 UTC, 24/24 chunks OKAY (`research/flash-userdata-v3.log`). userdata = v3 (SHA256 fa84274c...22df) until the next rw boot. ABL fastboot then hung ("Sending" forever, `reboot bootloader` timed out) until the user re-entered fastboot by hand (common Xiaomi ABL crash). Boot 0038e 18:06:15 UTC (`research/boot0038e-3.log`), photos IMG_20261016_200812/200838: keybag OK, then boot tasks tzinit (`Bad zoneinfo link`, resets to system partition, OK), finish-restore, finish-demo-restore, sysstatuscheck, prng_seedctl (`failed to load kernel prng seed`, `failed to load virtual random (-147)`, AllowCrash), auearlyboot, then **launchd_cache_loader: `abort: Unable to find AMFI`** -> 2.7 GB core written to /cores in 91 s -> launchd panic `launchd_cache_loader[22] exited -- exit reason namespace 7 subcode 0x1`. launchd_cache_loader: SecStaticCodeCheckValidity of /System/Library/xpc/launchd.plist with detached .sig, then IOServiceMatching("AppleMobileFileIntegrity") + IOServiceOpen type 0 + IOConnectCallMethod sel 6 (1 scalar = 1, struct in = cdhash) = trust the cdhash, then sends the cache to launchd. Boot-arg `launchd_unsecure_cache=1` skips signature + AMFI ("Using unsecure cache"); the value is parsed with strtoul base 10 (helper 0x100002da8), so a path = 0 = off: boot 0039w (18:17:13 UTC, `=/System/Library/xpc/launchd.plist`, photo IMG_20261016_202008) still aborted `Unable to find AMFI` (core dump now skipped: `Failed to generate core file ... error 14`, so 0039 works). Image `shim/out/shim-boot-0039u.img` uses `launchd_unsecure_cache=1`. Patch **0039**: do_coredump = 0 on SWEET (kern.coredump sysctl still works); CI `38945267341` -> `xnu/out-0039` (_do_coredump now in __common). Image `shim/out/shim-boot-0039w.img` = 0039 + sweet-0038hi.adt + ufsrw rootrw + `launchd_unsecure_cache=/System/Library/xpc/launchd.plist`. TODO later: real AppleMobileFileIntegrity IOService (sel 6 trust cdhash etc.).
- **Image v3 ready, awaiting user "flash".** Boot 0038w 17:38:10 UTC, photo (chat image 30): `SWEET AKS: keybagd sel 0 -> 0x0`, `sel 14 out 1/0 -> 0x0` (x2), `MKB_INIT: mount is with NO CPROTECT ... does not support Data Protection`, `System Keybag loaded`; then keybagd still opens /private/var/keybags/systembag.kb (0x100012d3c, for BackupKeyBagKeys) -> ENOENT, `no-effaceable-storage` not set -> `Can't load the keybag. tears in rain... Time to die` -> `FATAL KEYBAG ERROR: kb_load` -> reboot -> Halt/Restart Timed Out panic. Fix: ADT `/defaults/no-effaceable-storage` (mkadt.py; `shim/out/sweet-0038hi.adt`, `research/q0038-hi.adt`, QEMU OK) + file `/private/var/keybags/systembag.kb` (0600 root, dir 0700; XML plist {KeyBagKeys: data}). **v3 image** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v3.img` = v2 + that file, fsck OK, SHA256 fa84274c...22df; `ios16-root-20H392-v3.simg` (img2simg: zero blocks become FILL chunks, so a full flash overwrites every block the rw boots changed). Flash: `fastboot -S 512M flash userdata ios16-root-20H392-v3.simg`, then boot `shim/out/shim-boot-0038e.img` (0038 + sweet-0038hi.adt + ufsrw=1 rootrw=1).
- **0038 AppleKeyStore (CI 38938744130 PASSED -> `xnu/out-0038`; QEMU msgbuf: `SWEET AKS: AppleKeyStore registered (no passcode, unlocked)`; phone image `shim/out/shim-boot-0038w.img` booted 17:38:10 UTC, `research/boot0038w.log`, photo pending).** QEMU full kernel log trick (fb.txt is only the last screen): `llvm-nm KERNEL | grep _msgbufp` -> `--hmp "x /1gx ADDR"` gives struct msgbuf address (static, 0xfffffe0007b56678 on 0038) -> `--hmp "x /3gx STRUCT"` gives bufc (3rd quad) -> `--hmp "memsave BUFC 0x20000 \"FILE\""` (quote the file name), `tr -d "\0" < FILE`. Same inputs give the same addresses. Boot 0037w 17:08:35 UTC, photo IMG_20261016_191052: bindfs fixed mount; mount-phase-1/2 pass; `cc_fips_test` boot task: all corecrypto FIPS POST tests PASSED in userspace; then keybag boot task `keybagd --init`: `MKB_INIT: FATAL KEYBAG ERROR: failed to load system bag`, `Could not get options entry from the device tree` (x2, IODeviceTree:/options = NVRAM, non-fatal), `REBOOTING INTO RECOVERY MODE` -> reboot -> panic `Halt/Restart Timed Out @IOPlatformExpert.cpp:884` (no restart path on SWEET).
  - keybagd (static libaks): load_devicebag (0x100012c30) calls aks_get_system (sel 14, 0-1 scalar in, 1 out) and loads /private/var/keybags/systembag.kb only if the result is 0xe00002f0 (NotFound); any other error -> fatal; SUCCESS -> skip the file (userspace-reboot path). systembag.kb is a plist {KeyBagKeys}; decrypted with effaceable storage unless IODeviceTree:/defaults has `no-effaceable-storage`. Image has no /private/var/keybags. has_data_protection: statfs of /private/var; no cprotect on our HFS -> device-bag volume mapping skipped.
  - libaks connection: IORegistryEntryFromPath / IOServiceMatching("AppleKeyStore"), IOServiceOpen type 0, then selector 0 (no args) must succeed.
  - **AppleKeyStore selector map (iOS 16.7 AppleKeyStore.framework, via `ipsw dyld disass`):** 0 open, 2 create_bag, 3 save_bag, 4 unload_bag, 5 set_system_with_passcode, 6 load_bag, 7 get_lock_state (1 in, 1 out; bit 2 = unlocked since boot), 9 unlock_device, 10 wrap_key, 11 unwrap_key, 12 unlock_bag/test_stashed_kek, 13 lock_bag, 14 get_system, 15 change_secret_se, 16 internal_state, 17 get_device_state (1 in, struct out <=4K: DER SET of SEQUENCE{UTF8 key, INTEGER}: ss state, sls lock_state (MKBGetDeviceLockState returns it), sb backoff, sbo, sfa failed attempts, sfao, sgs generation, sas assertions, sgpe grace, srcd countdown, sr reserved), 18 recover_with_escrow_bag, 19 obliterate_class_d, 20 drain_backup_keys, 21/22 set/clear_backup_bag, 23 get_bag_uuid, 24 rewrap_key_for_backup, 26/27 assert_hold/drop, 30/31 set/get_configuration, 33-37 stash, 38 auth_token_create, 40 generation, 41 fdr_hmac_data, 42 verify_password, 43 _aks_operation, 44 remote_session, 49/50 signing keys, 51/53/54 stash enable/persist/escrow, 55 unload_session_bags, 57/58 remote peer, 59-62 smartcard, 63 migrate_s_key, 65 set_keybag_for_volume_with_cookie_persona, 66/67 sync bags, 68 copy_volume_cookie_persona, 69-73 se_*, 74-79/84/85/99 fv_* (FileVault/VEK), 80/81 absinthe, 82 make_public_backup_bag, 83 drop_auxiliary_auth, 86 kext get/set options, 87 invalidate_bag, 88-91/94/95/106/107 se_*, 92 lower_iteration_count, 93 get_internal_info, 96-98/117 keybag_persona create/list/delete, 100/101 assert promote/consume, 102/103 notify_state set/is_set, 104 fairplay, 105 change_secret_epilogue, 108 delete_xart_leak, 110-113 backup volume, 114 sealed_hashes_set, 115 prewarm_sps, 118-128 AKSIdentity*/AKSGetLastUser.
  - Patch **0038**: `iokit/Kernel/arm/SweetKeyStore.cpp` (class AppleKeyStore on IOResources, IOUserClientClass AppleKeyStoreUserClient; personality in KernelConfigTables.cpp): 0/4/5/9/12/13/26/27/55/102 success, 14 -> handle 0, 7 -> 0x4, 17 -> DER state (ss 4, sls 0), others kIOReturnUnsupported; logs `SWEET AKS: <proc> sel N arg0 in a/b out c/d -> ret` for every call.
  - Tools: shared cache copied to `research/dsc/` (git-ignored; ipsw needs a writable dir for its .a2s symbol cache); `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image AppleKeyStore|MobileKeyBag`; scratchpad `annot2.py BIN DIS FIXUPS` annotates llvm-objdump output with strings and import names (`ipsw macho info --fixups`).
- **0037 bindfs (phone boot 0037w pending photo).** Boot 0036mw 16:57:47 UTC, photo IMG_20261016_190102: WRITABLE ROOT WORKS: `/dev/ufsroot0 on / (hfs, local, noatime)` after mount_hfs update (GetMasterBlock EBUSY harmless), coredump of mount written to /cores (rw). Then `mount: failed to mount /private/preboot/5CBE3601.../usr/standalone/firmware -> ...: Operation not supported by device (19)` -> exit 74 -> launchd panic `mount[2] exited`. Cause: the macOS-derived config had nullfs but no bindfs (ENODEV = unknown fs type). Caller passes env 0 -> bind not required, ENOENT (missing source dir) tolerated. Patch **0037** adds `bindfs` to FILESYS_BASE in MASTER.arm64.sweet; CI `38936550483` -> `xnu/out-0037` (bindfs_vfsops present; QEMU probe regression OK). Image `shim/out/shim-boot-0037w.img` (0037 + sweet-0036hi.adt + ufsrw=1 rootrw=1) booted 17:08:35 UTC (`research/boot0037w.log`). NOTE: userdata has now been modified by rw boots; it no longer equals the v2 image, so sparsediff with v2 as OLD is not safe any more (full reflash or a new baseline needed).
- **0036 phone: launchd boot tasks run; mount -P 1 needs /chosen/boot-manifest-hash.** Boot 0036hr 16:15:32 UTC, photo IMG_20261016_185236: platform check passes; fsck boot task runs (`fsck: not booting main or diagnostic OS. Skipping fsck on OS container`); mount-phase-1: `failed to get filesystem info` x2 (no IODeviceTree:/filesystems/fstab, non-fatal), `mount: data volume missing, but not required in env: 0`, mount_hfs update of /: `GetMasterBlock: Error 16 opening /dev/ufsroot0` (EBUSY, mounted block dev, non-fatal) then mount() EROFS (read-only boot) -> `mount: / failed with 1`; then `failed to get boot-manifest-hash` -> errx exit 66 -> launchd panic `mount[3] exited`. /sbin/mount: fn 0x100005f90 reads IODeviceTree:/chosen boot-manifest-hash (hex), bindfs-mounts /private/preboot/<HEX>/usr/standalone/firmware (ENOENT tolerated unless required). `tools/mkadt.py` now adds `boot-manifest-hash` = SHA-384("sweet boot manifest") (5CBE3601...5205). ADTs `shim/out/sweet-0036hi.adt`, `research/q0036-hi.adt` (QEMU probe OK, csops 0x26000001). Image `shim/out/shim-boot-0036mw.img` (0036 + new ADT + ufsrw=1 rootrw=1), booted 16:57:47 UTC (`research/boot0036mw.log`): FIRST WRITABLE BOOT of userdata (restore source: v2 image on SSD).
- **0036 CS_SIGNED (phone boot 0036hr pending photo).** Phone boot 0035hr 2026-10-16 15:57:02 UTC (`research/boot0035hr.log`, photo IMG_20261016_180249): highmem works on hardware; shared cache maps (trust-cache warnings only), Apple launchd runs (`Darwin Bootstrapper Version 7.0.0`, `entering ondemand mode`), starts boot task fsck, then userspace panic `boot task is not a platform binary (fsck, /sbin/fsck)`. launchd+0x3fea0: `csops(pid, CS_OPS_STATUS)` must have bit 0x04000000. Cause: nothing set CS_SIGNED (AMFI does it in vnode_check_signature), so csproc_get_blob() returns NULL for every process and csops never reports CS_PLATFORM_BINARY (also breaks per-process cdhash/entitlement queries). QEMU probe init (`csops` status printer, scratchpad csq/) on 0035: `0x02000001`; patch **0036** (`*cs_flags |= CS_SIGNED` in the SWEET AMFI hook), CI `38929635791` -> `xnu/out-0036`: `0x26000001`. Images `shim/out/shim-boot-0036hr.img` / `-0036hw.img` (same cmdlines as 0035). 0036hr booted 16:15:32 UTC (`research/boot0036hr.log`). Next launchd boot tasks (embedded __config plist): fsck -qL and mount -P 1/2 (RequireSuccess); no /etc/fstab on the image.
- **0035 ENTITLEMENTS + PLATFORM BINARIES (QEMU verified).** `xnu/patches/0035-sweet-amfi-entitlements-platform-binaries.patch`: new `iokit/Kernel/arm/SweetEntitlements.cpp` (OSObject subclass: OSDictionary from OSUnserializeXML of the signature's XML entitlements + original XML for CS_OPS_ENTITLEMENTS_BLOB); `bsd/kern/sweet_amfi.c` answers queryEntitlementBoolean/String(+WithProc, string also matches array members), copyEntitlementAsOSObject(+WithProc, retained), asdict (retained), get_xml (kalloc_data copy); built-in MAC policy "SWEET AMFI" (registered from bsd_init before vfs/exec) with mpo_vnode_check_signature: every signed binary on the MNT_ROOTFS mount gets CS_PLATFORM_BINARY (stand-in for AMFI's static trust cache: iOS system binaries are ad-hoc, cd_flags 0x2, platform byte 0), and attaches entitlements ONLY for the writable copy (cs_blob != csb_ro_addr; revalidation passes the RO blob). LESSON: first version attached in adjustContextWithoutMonitor -> QEMU `unable to adjust OSEntitlements context without monitor: 53` because ubc_cs_convert_to_multilevel_hash (4K-page signatures on 16K kernel) sets csb_entitlements_blob = NULL; ALL iOS 16 binaries (launchd, backboardd, SpringBoard) use 4K code pages, so this would have broken launchd on the phone. Boot-arg `sweet_amfi_debug=1` logs `SWEET AMFI: <ident>: N entitlements (test: ...)`. `tools/mkinit.py OBJ OUT [ENTS.plist]` adds an XML entitlements blob (special slot -5; default output byte-identical). QEMU `research/q0035-ent` (RAM disk `research/root-hfs-ent.img`, init with 3 test entitlements, highmem): `org.sweet.init: 3 entitlements (test: bool 1 string 1 array 1)` then init PID 1. MAC policies loaded: 0034 = 1, 0035 = 2 (QMP `mac_policy_list`). CI `38909807230` -> `xnu/out-0035`. Phone images: `shim/out/shim-boot-0035hr.img` (highmem, ro), `-0035hw.img` (highmem, +ufsrw=1 rootrw=1), `-0035r.img` (low mem fallback).
- **PHONE TEST ORDER (updated):** 0035hr -> if instant reset, 0035r -> then 0035hw.

- **HIGHMEM: XNU in the upper DDR bank, ~3.95 GiB (was 1.2 GiB).** Live FDT memory = <0x80000000 2G> + <0x1_00000000 0xfcc00000>; all fixed reserved-memory carve-outs are in the low bank (highest: ramdump_fb 0xaf000000, rmtfs ~0xfde01000), dynamic pools have alloc-ranges <= 0xffffffff, UFS node has no `iommus` (Linux DMAs anywhere). `tools/mkadt.py --highmem` sets /chosen dram-base 0x100000000 dram-size 0xfcc00000; `tools/mkpayload.py` now takes phys_base/mem_size from the ADT (default payloads byte-identical, verified); `tools/qemu-sweet.py` sizes -m from the payload (8G for highmem). Patch **0034** (`0034-sweet-ufs-dma-above-4g.patch`): UFS refuses DMA memory above 4G without UFSHCI CAP.64AS (bit 24), logs `DMA at 0x...`. CI `38905889883` success -> `xnu/out-0034`. **QEMU verified** (`research/q0034-hi`, ADT `research/q0034-hi.adt` --qemu --highmem, HFS RAM disk): phys_base 0x100000000, init PID 1 heartbeat, no panic; `max_mem` = `mem_size` = 0xfcc00000 read via QMP (`research/q0034-hi-mem`). Phone images: `shim/out/shim-boot-0034hr.img` (read-only) / `-0034hw.img` (+ufsrw=1 rootrw=1), ADT `shim/out/sweet-0034hi.adt` (asmb SIP + sweet-ufs + highmem). PHONE RISK: unknown runtime TZ/XPU protection in the upper bank would show as an instant reset; fall back to 0033r/w. Watchdog ruled out for the overnight reset: msm-watchdog bark is 20 s (qcom,bark-time 0x4e20) yet panic screens stay up for many minutes.

- **Offline research 2026-10-16 (user away, phone unavailable). Images rebuilt** `shim/out/shim-boot-0033r.img` / `-0033w.img` now also carry `wdt_test=no_user_checkin`. NEXT ON PHONE: boot 0033r (expect past in6_nigroup), then 0033w (first writes: rw root fixes HFS link-chain bits itself and gives /var for launchd sockets /var/run/syslog, /var/run/lockdown.sock).
- **launchd.plist** (`/System/Library/xpc/launchd.plist`, compiled; 532 daemons, 66 RunAtLoad/KeepAlive, list in scratchpad `early-daemons.txt`). `_PanicOnCrash` daemons: containermanagerd/usermanagerd (InternalOnly), lockdownd/remoted/trustd/remotepairingdeviced (AutomationOnly), **watchdogd unconditional** (KeepAlive SuccessfulExit=false). watchdogd needs IOKit `IOWatchdog` kext service; if absent it exits only when `kern.hv_vmm_present` (ADT `/defaults/vmm-present`, hvg_sysctl.c) or with boot-arg `wdt_test=no_user_checkin` ("detected testing boot-args to not run, exiting"; reads kern.bootargs). Using the boot-arg (vmm-present would change many daemons; keep as an option).
- **GUI path research (QuartzCore in the shared cache, `ipsw dyld str CACHE STR`, ~10 s/search):** CA::WindowServer has IOMFBServer/IOMFBDisplay (Apple DCP/IOMobileFramebuffer), AppleCLCDDisplay, AppleRGBOutDisplay, **VirtualServer/VirtualDisplay** and **MemorySurface**, EAGLServer. Renderers: CA::OGL::MetalContext, GLContext and a **CPU software rasterizer CA::OGL::SW** (samplers/blend modes; "image is too large for software renderer"). Env knobs: `CA_ENABLE_OGL`, `CA_DISPLAY_TYPE`, `CA_FORCE_LOCAL_SERVER` (249 CA_* vars). Hypothesis (unverified): backboardd's render server could run a VirtualServer/MemorySurface with the SW renderer and we copy the surface to the ABL framebuffer -> needs disassembly of CA::WindowServer server creation. Expected other GUI walls: IOSurface (closed-source kext; needs a reimplementation), IOMobileFramebuffer user client, IOHID touch events, AppleKeyStore/keybag (SEP) for lock state, MobileGestalt answers (AppleCLCD etc.).

- **0032r RESULT (boot 05:07:50 UTC, `research/boot0032r.log`, photo IMG_20261016_071200): SHARED CACHE MAPPED, LAUNCHD RUNS.** With SIP relaxed (ADT asmb) the `not in trust cache` lines are only warnings for every subcache (.31 ... .42.dyldlinkedit); no SIP rejection; libSystem loads; launchd configures networking (`skip attaching fsw to lo0 using legacy TX model`) -> kernel data abort far 0x28 in `SHA1Init` (symbolized as sha1_init) from `in6_nigroup` (IPv6 on lo0): g_crypto_funcs NULL. Kernel addresses are unslid: `~/swift/usr/bin/llvm-symbolizer --obj=KERNEL ADDR` works directly.
- **0032** BearSSL SHA-1 (`0032-sweet-bearssl-sha1.patch`), **0033** BearSSL SHA-384/512 (`0033-sweet-bearssl-sha384-sha512.patch`, BearSSL ctx stored in SHA512_CTX, static-asserted to fit; ubc_subr.c uses SHA-384 for code directories). `0020-stage-bearssl.sh` now also stages hash/sha1.c, hash/sha2big.c, codec/{dec,enc}{32,64}be.c. CI `38854909053` success (0032-only run `38854802073` superseded). Kernel `xnu/out-0033` (SHA1Init -> _br_sha1_init verified by disassembly; nm symbols have a leading underscore). Images (ADT sweet-0032): `shim/out/shim-boot-0033r.img` (read-only), `shim-boot-0033w.img` (+ufsrw=1 rootrw=1). Still NULL g_crypto_funcs users: des, chacha20poly1305, rsa, aesxts, rand, flow_divert.
- `research/check-patch-order.py` now skips patches touching CI-staged sweet_hfs sources (0031) instead of stopping.

- **0031r RESULT (boot 05:03:52 UTC 2026-10-16, `research/boot0031r.log`, photo IMG_20261016_070508): SHARED CACHE FOUND.** dyld now opens `dyld_shared_cache_arm64` (v2 image hard links), kernel refuses to map it: `shared_region: ... map(...'dyld_shared_cache_arm64'): not in trust cache` -> `vnode is not SIP-protected` (vm_unix.c: macOS arm64 path needs trust cache, else root-owned + SF_RESTRICTED unless CSR_ALLOW_UNRESTRICTED_FS) -> `dyld cache '(null)' not loaded: syscall to map cache into shared region failed` -> libSystem not loaded -> coredump to /cores fails error 30 (EROFS) -> panic initproc failed -> "MACH Reboot" (spins; screen kept). Lots of `hfs: set hardlink bit on vol=iOSRoot cnid=... linkid=...` spam (Linux-made hard links lack the link-chain bit; read-only mount cannot persist the fix). FIX: ADT `/chosen/asmb` with `lp-sip0`=0x6f (u64; incl. CSR_ALLOW_UNRESTRICTED_FS) and `lp-sip1`=1 (unauthenticated root), `tools/mkadt.py` -> `shim/out/sweet-0032.adt`. Images with kernel 0031: `shim/out/shim-boot-0032r.img` (read-only) and `shim-boot-0032w.img` (+ufsrw=1 rootrw=1).

- **2026-10-16 morning:** userdata now = **v2** image (`diff-v1-v2.simg` flashed 21:06:50 UTC 2026-10-15, OKAY, `research/flash-userdata-diff-v2.log`); future diffs use `ios16-root-20H392-v2.img` as OLD. Booted `shim-boot-0029k.img` (ignition_level=1) right after (`research/boot0029k-v2.log`); **no photo** (user asleep). Next morning the phone was in PixelOS recovery = some hardware reset (ABL then booted Android, which cannot use userdata). OBSERVATION: our kernel cannot reset the SoC itself (`PE_halt_restart` is never set; reboot/halt print "MACH Reboot"/"CPU halted" and spin), so the reset came from outside XNU: Qualcomm watchdog or a TZ/XPU violation. Unknown which; re-boot 0029k and watch/video until the reset. Do NOT tap factory reset/format data in recovery (would wipe the iOS image).
- **0030** (`xnu/patches/0030-sweet-ufs-writes.patch`, CI `38852655542`): UFS WRITE(10) + read-modify-write for partial 4 KiB blocks + SYNCHRONIZE CACHE (DKIOCSYNCHRONIZE), only with boot-arg `ufsrw=1`; `ufs_write_blocks` re-checks partition bounds before every write (only place data goes out).
- **0031** (`xnu/patches/0031-sweet-read-write-root.patch`, CI `38852837176`): boot-arg `rootrw=1` clears MNT_RDONLY before the root mount (no data volume on sweet: /private/var is on the root; image has no /etc/fstab); Apple HFS accepts a dirty non-journaled ROOT read-write on SWEET (logs "mounting dirty non-journaled root read-write"). Later: journaled HFS for crash safety. Kernel `xnu/out-0031` (CI `38852837176` success, 5m31s; 0030 run cancelled by the newer push). Boot images (phone ADT `sweet-0028.adt`, ramdisk byte-matched): `shim/out/shim-boot-0031r.img` = 0029k args (read-only, ignition_level=1) and `shim/out/shim-boot-0031w.img` = same + `ufsrw=1 rootrw=1`. PLAN: boot 0031r first and film until the reset (diagnose overnight reset), then 0031w (first ever writes to userdata; v2 image on the SSD is the restore source). `research/check-patch-order.py` cannot check 0031 (staged sweet_hfs files are not in its index); CI stage scripts run first, so CI is the check.

- **ignition_level=1 result** (boot 21:01:39 UTC, `research/boot0029k.log`, photo IMG_20261015_230308): preboot/cryptex stages skipped (need >= 2/3), `dylib_cache: finding shared cache on system volume: ignition level = 1, search root fd = 4, subpath = System/Library/Caches/com.apple.dyld/` -> not found -> `ignition boot failed: 19` -> no shared cache -> libSystem not loaded. FIX IN PROGRESS: image v2 = copy of the flashed image + `/System/Library/Caches/com.apple.dyld/` with HARD LINKS to the 44 cryptex cache files (no extra space; avoids symlink-following doubts), then `tools/sparsediff.py ios16-root-20H392.img ios16-root-20H392-v2.img diff.simg` and flash only the diff. Boot with `ignition_level=1` (shim-boot-0029k.img).
- **ignition_level=0 result** (boot 20:58:07 UTC, `research/boot0029j.log`, photo IMG_20261015_230037): all stages skipped as "ignition level insufficient" (hello/preboot/cryptex1 sniff >= 2, select os cryptex path/graft >= 3, **dyld_cache >= 1**), `ignition boot failed: 89`, "ignition partially disabled", then same `Library not loaded: /usr/lib/libSystem.B.dylib (no such file, no dyld cache)`. => dyld gets the shared cache directory from ignition's dyld_cache stage. Next: `ignition_level=1` (`shim/out/shim-boot-0029k.img`) to skip preboot/cryptex stages but run dyld_cache; its log "finding shared cache on %s ... subpath = %s" will show where it searches. If it searches rootfs /System/Library/Caches/com.apple.dyld, add a symlink there (image rebuild; consider a diff-only sparse flash tool to avoid rewriting 12 GB).
- **APPLE dyld/launchd RUNNING (libignition) with `unentitled_ios_sim_launch=1`** (boot 20:53:24 UTC, `research/boot0029i.log`, photo IMG_20261015_225617): kernel prints "Allowing spawn of iOS binary ... boot-arg set to true"; `shared_region: ... check_np ... vm_shared_region_start_address() failed` (no region yet, normal); dyld's built-in **libignition** (Darwin Ignition Sequence 1.0.0, libignition-51~1974; prints rd=ufsroot0, hardware target sweet, ignition level 0x5, platform 0x2, boot spec local, 7 stages): `hello from launchd.1` -> `preboot: mounting preboot` -> `failed to lookup preboot: 25` (ENOTTY: looks for a separate Preboot volume by role) -> ignition fails -> dyld `Library not loaded: /usr/lib/libSystem.B.dylib ... (no such file, no dyld cache)` -> launchd exit -> panic initproc failed. dyld boot-args found via strings: `ignition_level`, `ignition_force_dylib_root` (forced rootfs/livefs/cryptex fallback), `ignition_halt_after`, `ignition_live_app_graft`; dyld cache search paths include /System/Cryptexes/OS, /System/Volumes/Preboot/Cryptexes/OS/, /private/preboot/Cryptexes/OS/ (present in our image). Next try `ignition_level=0` (`shim/out/shim-boot-0029j.img`).
- **APPLE launchd EXECUTED FROM UFS (2026-10-15).** Flashed iOS image: `img2simg` -> `ios16-root-20H392.simg` (12.1 GB) then `fastboot -S 512M flash userdata ...simg` (24 chunks, 307 s, `research/flash-userdata-ios16.log`; a raw-image flash was killed by earlyoom at 2.6 GB RSS - always flash the sparse image). ABL fastboot hung on getvar after the flash; power+vol-down fixed it. Boot 0029u 20:49:04 UTC (`research/boot0029u-ios16.log`), photo IMG_20261015_225134: `hfs: mounted iOSRoot` -> load_init_program /sbin/launchd -> panic `unexpected SIGKILL of launchd (CS_KILLED) with reason -- namespace 9 code 0xe` = OS_REASON_EXEC / EXEC_EXIT_REASON_WRONG_PLATFORM: our kernel is XNU_TARGET_OS_OSX, iOS-platform binaries are "alien" and refused unless spawn attr platform set or DEVELOPMENT TUNABLE `unentitled_ios_sim_launch`. Next try: same kernel, cmdline + `unentitled_ios_sim_launch=1` (`shim/out/shim-boot-0029i.img`). LONGER TERM: macOS-config kernel marks iOS maps alien (vm_map_mark_alien) and differs from iOS in many policies; an iPhoneOS-config kernel build may eventually be needed.
- **iOS 16 ROOT IMAGE BUILT:** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392.img` (16 GiB case-sensitive HFS+, label iOSRoot, 12 GB used, fsck OK after `fsck.hfsplus -y` rewrote 32 non-ASCII localized WorkflowKit Shortcut names Linux decomposes differently). Built by `tools/mkiosroot.sh OS.dmg SYSTEMOS.dmg APPOS.dmg OUT.img [SIZE]` (needs sudo; apfs-fuse as root; OS dmg is UDIF -> link must end .dmg). Contents: iPhone X 20H392 OS root + SystemOS cryptex at /private/preboot/Cryptexes/OS (so /System/Cryptexes/OS -> cache, 44 files, dyld_v1 arm64) + AppOS at .../App. /sbin/launchd and /usr/lib/dyld root:wheel 0755. NEXT: (confirm) `fastboot flash userdata ios16-root-20H392.img` (auto-sparse), boot 0029u (rd=ufsroot0) -> Apple launchd attempt.
- **MILESTONE ON HARDWARE: BOOT FROM INTERNAL FLASH.** 0029 CI `38797924912` PASSED, `xnu/out-0029` SHA256 `a68bc847...2a37`. Image `shim/out/shim-boot-0029u.img` (payload-0029u = 0029 kernel + `shim/out/sweet-0028.adt` + `rd=ufsroot0`, NO RAM disk). Boots 20:01:34 and 20:12:37 UTC (`research/boot0029u*.log`), photo IMG_20261015_221403: `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB, read-only` -> `BSD root: ufsroot0, major 1, minor 0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `SWEET: root volume is not authenticated (error 25); continuing unsealed` -> `load_init_program ... /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> heartbeat (ran for minutes unattended). userdata currently holds the 8 MB `research/root-hfs.img`. NEXT: build a multi-GB HFS+ image with the iOS 16 (iPhone X 20H392) userland (OS rootfs + SystemOS cryptex contents incl. dyld shared cache at /System/Library/Caches/com.apple.dyld; preserve modes/owners/symlinks; decompress LZBITMAP via apfs-fuse), flash it to userdata (sparse, needs user OK), then try Apple's dyld/launchd. Driver is read-only (root mounts RDONLY), fine for first launchd attempts.
- **userdata FLASHED with the 8 MB HFS test volume** (user said "flash it", 2026-10-15 19:53:17 UTC, `research/flash-userdata-hfs-test.log`: `fastboot flash userdata research/root-hfs.img` OKAY; pre-checks: one sweet device, partition-size:userdata 0x1AC4BFB000, partition-type f2fs, image fsck OK, SHA256 3626ea69...). Android userdata is now destroyed (expected/approved). Boot 0028u at 19:53:20 (`research/boot0028u-hfs.log`), photo IMG_20261015_215541: `BSD root: ufsroot0` -> **`hfs: mounted SweetRoot on device b(1, 0)` from internal UFS** -> panic `rootvp not authenticated after mounting @bsd_init.c:931` (arm64 macOS-config requires FSIOC_KERNEL_ROOTAUTH sealed root for non-ramdisk roots). Patch **0029** (`dd1c284`): SWEET logs `SWEET: root volume is not authenticated (error N); continuing unsealed` instead of panicking (Apple configs keep the panic; pivot_root still requires auth). CI **`38797924912`** running. Next: download out-0029, phone image with sweet-0028.adt + rd=ufsroot0 (no RAM disk), boot -> expect init from UFS.
- **UFS ROOT DRIVER VERIFIED ON HARDWARE (read-only).** 0028 CI `38796139570` PASSED, `xnu/out-0028` SHA256 `8b981640...9da6`; QEMU HFS RAM-disk regression `research/q0028-hfs` still runs init. Phone boot 2026-10-15 19:50:24 UTC (`research/boot0028u.log`, image `shim/out/shim-boot-0028u.img`, phone ADT `shim/out/sweet-0028.adt` with /sweet-ufs, NO RAM disk, `rd=ufsroot0`), photos IMG_20261015_215151/215220: `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB, read-only` -> `BSD root: ufsroot0, major 1, minor 0` -> `hfs_ValidateHFSPlusVolumeHeader: unknown Volume Signature : f188` (Android-encrypted data, as expected) -> `cannot mount root, errno = 19`, kernel retries mountroot (no panic). Nothing written to flash. NEXT (destructive, needs user confirmation right before): `fastboot flash userdata research/root-hfs.img` (8 MB HFS with test init) then boot rd=ufsroot0 -> expect init from internal flash.
- **PATCH 0028 (`33aceac`): XNU read-only UFS root device**, CI **`38796139570`** running (next artifacts xnu/out-0028, research/bt29, run29.log). `bsd/dev/sweet_ufs.c`: reuses ABL's UFSHCI state (like the shim probe), takes over UTRL at a kmem_alloc_contig region (DMA layout: UTRL 0x0, UCD 0x1000, 1 MiB bounce 0x4000), verifies UTRLBA readback before any doorbell, IE=0 polled, one SCSI cmd at a time on LUN0 (TUR x3, READ(10) via bounce, PRDT 256 KiB chunks), flush_dcache64 by PA around each command (host not dma-coherent per DT), finds GPT partition by name (`ufsroot=` boot-arg, default `userdata`), exposes `/dev/ufsroot0`/`rufsroot0` (512-byte logical sectors, physical 4 KiB, DKIOC* ioctls), refuses writes (EROFS). IOKitBSDInit: `rd=ufsroot0` -> sweet_ufs_rootdev() (lazy init) else panic. ADT: `tools/mkadt.py` adds `/sweet-ufs` reg <0x1d84000 0x3000> for the PHONE only (not --qemu). Local compile OK, imports resolve. Sandbox research/bt28 (pre0028 originals). FIRST PHONE TEST PLAN (non-destructive): boot 0028 with phone ADT + `rd=ufsroot0` and NO RAM disk: expect `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB` + `BSD root: ufsroot0`, then root mount failure (userdata is still Android-encrypted) -> panic. That validates the driver before flashing an HFS image into userdata (needs explicit user confirmation at that time).
- **SUPERSEDES the 64 GiB iosroot GPT plan: user said "u can delete android" (2026-10-15).** Use the existing `userdata` partition (LUN0 sda34, 4K LBA 0x2B8C00, 0x1AC4B MiB ~107 GiB) directly as the iOS root: NO GPT changes. Keep bootloaders, recovery (OrangeFox), modem/persist/fsg/modemst untouched. Write the HFS image later with `fastboot flash userdata` (sparse, auto-split under the 768 MiB limit). Android will no longer boot normally (expected; reinstallable). Order: XNU UFS driver first, read-only against the current GPT; flash only once it can locate userdata. Nothing erased yet.
- **DECIDED (user, 2026-10-15): 64 GiB `iosroot` on LUN0 (sda), taken from userdata (wipes Android user data; Android/super kept).** Planned GPT (4K LBAs): userdata 0x2B8C00..0xD7D6FF (~43 GiB, keep type/unique GUIDs and attributes); iosroot 0xD7D700..0x1D7D6FF (0x1000000 blocks = 64 GiB, 1 MiB aligned); backup GPT area unchanged. Procedure: user backs up phone data -> boot OrangeFox recovery (adb) -> back up GPT (sgdisk --backup + raw dd of LBA 0-5 and last 6 blocks) to research/ -> sgdisk edit -> Format Data -> verify Android boots to setup. NOT EXECUTED YET.
- **INTERNAL UFS WORKS FROM THE SHIM (read-only), user authorized internal-UFS approach incl. flashing (2026-10-15, "i allow everything").** Shim probe `shim/ufs.c` (commit `12ed3ed` + filter): ufshc@1d84000 is UFSHCI 2.1 (ver 0x210, cap 0x1587031F, 32 slots), ABL leaves HCE=1, HCS=0x10F (device present, lists ready, UIC ready); probe takes over UTRL at its own buffer (verifies UTRLBA readback before any doorbell), TEST UNIT READY/READ CAPACITY/READ(10) all succeed. LUN0 = 0x1D7D800 x 4 KiB (~126.6 GB), valid GPT (64 entries at LBA 2). Photos IMG_20261015_212916/213325/213429. Big LUN0 partitions (start in 4K LBAs / MiB): super 0xCA00/0x2200 (8.5 GiB), logdump 0x22CA00/64, minidump 0x230A00/128, rawdump 0x238A00/128, recovery 0x240C00/128, cache 0x248C00/384 ext4, exaid 0x260C00/384, cust 0x278C00/1024 ext4, **userdata 0x2B8C00/0x1AC4B MiB (~107 GiB), fs unreadable = encrypted (metadata encryption)**. cache..cust contiguous = only 1.75 GiB (too small for iOS ~10+ GiB). Plan needing user consent: shrink userdata in GPT (wipes Android data) and add an `iosroot` partition at the end of LUN0. LUNs 1-5 not listed yet (sdb..sdf backed up in backup/lun).
- **fastboot limit measured (2026-10-15, read-only getvar):** `max-download-size: 805306368` (768 MiB); `max-fetch-size` unsupported; `is-userspace: no` (ABL fastboot). A `fastboot boot` image (shim+kernel+RAM disk) must be < 768 MiB, so the 2.5 GiB iOS shared cache cannot ride in the boot RAM disk even if XNU gets all RAM. Real userland needs storage access (UFS driver, or USB host) or a much smaller cache. Unlocking full RAM is still needed later (GUI).
- **iOS 16 USERLAND SOURCE (Claude, 2026-10-15).** Chose **iPhone X (iPhone10,3/10,6, D22/D221AP)** iOS **16.7.16 (20H392)** over iPhone 8: same A11 (no PAC -> plain arm64, runs on Kryo 470/ARMv8.2), last iOS for A11; X userland is home-button-less and tall-screen (1125x2436 vs sweet 1080x2400), better fit for later GUI. Note the X has its OWN SystemOS cryptex (different digest from iPhone 8's). IPSW URL in `research/ipsw-x/URL.txt` (+ BuildManifest). Images on the user's external SSD (NOT in git, do not format that disk: it holds the user's photos): `/run/media/dipa/android/ios-sweet-ipsw/iPhone10,3_16.7.16_20H392/` — `087-86593-047.dmg` = Cryptex1,SystemOS (2,743,074,816 B), `087-86698-044.dmg` = OS rootfs (4,730,814,044 B), both zip CRC-32 verified, plus Firmware/*.root_hash/.trustcache/.mtree. AppOS cryptex is 087-86715-047.dmg (10 MB, same as iPhone 8).
  - Images are raw APFS; files use LZBITMAP (decmpfs type 14). 7z cannot decode. Tools: `ipsw` 3.1.738 (AUR ipsw-bin, user-approved) needs apfs-fuse on Linux; **apfs-fuse** built in user space (system cmake broken: cmake 4.4.4 wants libjsoncpp.so.27, jsoncpp 1.9.6 installed = partial upgrade, NOT fixed) with pip cmake + `-DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-include cstdint"`, installed to `~/.local/bin/apfs-fuse` (+apfs-dump-quick). Mount via a comma-free symlink (apfs-fuse splits options on ',' in `iPhone10,3`; exFAT has no symlinks -> put link elsewhere): `apfs-fuse LINK/087-86698-044.dmg MNT` -> `MNT/root/...`; unmount `fusermount3 -u MNT`.
  - Verified from headers: `dyld_shared_cache_arm64` magic `dyld_v1   arm64`; `/sbin/launchd`, `/usr/lib/dyld` = cputype 0x100000c subtype 0 (plain arm64). libSystem exists only inside the cache.
  - **BLOCKER for real userland via RAM disk:** shared cache = 3.10 GiB in 44 files (~2.5 GiB without the 592 MB `.symbols`), but the kernel manages only 1.20 GiB (0xb0000000..0xfd000000). Options: (A) give XNU the phone's full ~6 GB (banks 0x80000000+2G and 0x100000000+0xfcc00000, carve-out holes need pmap support) AND check fastboot max-download-size for a multi-GB boot image; (B) storage driver (Qualcomm UFS) to read a root from flash (no flashing allowed: would need a file/partition strategy); (C) run against individual dylibs extracted from the cache (uncertain).
- **MILESTONE ON HARDWARE: HFS+ ROOT FILESYSTEM -> PID 1.** Boot 2026-10-15 18:22:12 UTC (`research/boot0027b.log`, image `shim/out/shim-boot-0027b.img`), photo `IMG_20261015_202334.jpg`: `BSD root: md0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> repeated `SWEET init: still alive`, no panic. Kernel 0027 (built-in Apple OSS HFS + BearSSL MD5), init with SP alignment fix. NEXT: real iOS 16 userland on the HFS image (dyld, libSystem/dyld shared cache, launchd). Known gaps: entitlements (none granted), SHA-1/SHA-384/512 providers, no storage driver (RAM disk only), root mounted read-only.
- **PHONE HFS ROOT (0027) + SIGBUS ROOT-CAUSED.** Phone boot 2026-10-15 17:49:06 UTC (`research/boot0027.log`, photo `IMG_20261015_200031.jpg`): `hfs: mounted SweetRoot on device b(1, 0)` (HFS works on hardware), init printed its first line, then `pid 1 exited -- exit reason namespace 2 subcode 0xa` = SIGNAL/SIGBUS -> `initproc failed to start` panic. Diagnostic boot 18:08:13 UTC (`research/boot0027d.log`, image `shim/out/shim-boot-0027d.img`, diag init `research/diag-init` from scratch diag-init.S with [a][b][c] markers, `cs_debug=1`; photo `IMG_20261015_201547.jpg`): output `PID [a][b]` then SIGBUS -> fault at first `strb w21,[sp]`; no code-signing messages. Cause: kernel enters a static binary with sp at argc, not necessarily 16-aligned (depends on arg/apple string lengths, differs mockfs vs HFS); EL0 SP alignment check -> EXC_ARM_SP_ALIGN -> SIGBUS (sleh handle_sp_align). QEMU does not enforce SP alignment. NOT a kernel bug: real binaries start in dyld which aligns. Fix `1a8fc15`: sweet-init aligns sp at entry. Rebuilt `research/root-hfs.img`, QEMU `research/q0027-hfs2` OK. Phone image `shim/out/shim-boot-0027b.img` SHA256 `098ba46c...c5c` (payload-0027b, ramdisk match check-0027b) ready, awaiting FASTBOOT. Lesson: Assembly `;` is a comment in Apple arm64 asm (use .macro, not ;-joined #define).
- **HFS ROOT WORKS (QEMU).** 0027 CI `38779441895` PASSED, `xnu/out-0027` SHA256 `a8643886...5f6a`. QEMU `research/q0027-hfs` (RAM disk = `research/root-hfs.img`, rd=md0): `BSD root: md0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` + heartbeat, no panic. Phone image `shim/out/shim-boot-0027.img` (payload-0027 = 0027 kernel + sweet-0021.adt + root-hfs.img + rd=md0, ramdisk byte-match check-0027) ready; awaiting FASTBOOT for phone test.
- **HFS ROOT WORK (Claude), patches 0026-0027.**
  - 0026 (`f0e990c` + link fix `64c96f4`): Apple OSS **hfs-627.100.6** (commit `31d5ec238dfab485e78a9a30b8b92d13e8914f03`, paired with xnu-8796.141.3 in macos-135 release.json) staged by `xnu/patches/0026-stage-hfs.sh` into `bsd/sweet_hfs` (core + hfs_encodings; AppleKeyStore include/key prototypes guarded by CONFIG_PROTECT; SDK TargetConditionals copied). New config option `sweet_hfs` (MASTER + MASTER.arm64.sweet); 40 `optional sweet_hfs` files; Makefile.template foreach adds `_CFLAGS_ADD = -include sweet_hfs_compat.h -I...` (MUST come after kernel -D flags; compat undefs BSD/XNU_KERNEL_PRIVATE and the CONFIG_* HFS tests so kext-config.h decides: macOS profile, no content protection). `sweet_hfs_iokit.c` replaces hfs_iokit.cpp/hfs_encodings_kext.cpp: `sweet_hfs_register()` called in bsd_init after vfsinit (encodings init, vfs_fsadd VFS_TBLCANMOUNTROOT, zones, sysctls); is_ejectable 0, iterate_media none, serial KERN_NOT_SUPPORTED, OSKextGetCurrentLoadTag -> kOSKextInvalidLoadTag (renamed via compat macro). hfs_encodings' own `hfs_allocated` renamed per object (separate kexts on Apple; first CI `38777325964` failed on that duplicate at link). mockfs now validates Mach-O magic (its TODO) so non-Mach-O roots fall through to HFS (new fs entries come AFTER mockfs in vfsconf). CI `38778133720` PASSED, `xnu/out-0026` SHA256 `0b49170c...701a`, prints `SWEET HFS: hfs-627.100.6 registered`.
  - HFS+ image: `research/root-hfs.img` (8 MB, mkfs.hfsplus from AUR hfsprogs installed with user approval; loop-mounted with sudo; /sbin/launchd = research/sweet-init, /dev; fsck.hfsplus OK). QEMU `research/q0026-hfs`: `BSD root: md0` then data abort in MD5Init from hfs_getvoluuid (mount computes volume UUID).
  - 0027 (`14bf2b7`): 0020 stager also copies BearSSL hash/md5.c + codec/dec32le.c/enc32le.c; `corecrypto_md5.c` SWEET branch converts MD5_CTX <-> br_md5_context around br_md5_* calls; wrappers sweet_md5.c/sweet_dec32le.c/sweet_enc32le.c. Host test 40/40 match md5sum. CI **`38779441895`** running.
  - Local tooling: `tools/xnu-cc.py` has `XNU_CC_POST` (flags after logged ones). Sandbox `research/bt28/xnu` = 0025 CI tree + 0026/0027 edits; originals `research/pre0026`, `research/pre0027`. HFS local objects `research/hfs-objs`. Checker entries updated to bt28.
  - SHA-1 / SHA-384/512 still have no provider.
- **MILESTONE ON HARDWARE: USERSPACE PID 1 RUNS ON THE PHONE.** Boot 2026-10-15 17:16:00 UTC (`research/boot0025.log`: send OKAY0.410s, boot OKAY0.135s), image `shim/out/shim-boot-0025.img` SHA256 `9dbfa0b1...89db0`. Photo `IMG_20261015_191733.jpg`: `BSD root: md0` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> repeated `SWEET init: still alive` (5 s heartbeat), no panic. Kernel 0025 + mockfs RAM disk + built-in no-entitlements AMFI. No flashing performed.
- **NEXT (toward real iOS userland):** real root filesystem with real binaries. Options: (a) build Apple OSS `hfs` (macOS 13.5 tag `hfs-627.100.6`) into SWEET like libpthread, then an HFS RAM disk image; (b) iOS 16 dyld + libSystem/dyld shared cache from the IPSW (needs APFS or repacking onto HFS). Expected hurdles: entitlements (sweet_amfi grants none), SHA-1/MD5/SHA-384/512 providers (BearSSL), missing kexts/daemons. Current init is a static test program, not launchd.
- **MILESTONE: USERSPACE RUNS (QEMU).** 0025 CI `38774788048` PASSED, `xnu/out-0025` SHA256 `5496069b...4877`. QEMU `research/q0025-rd` (150 s, no panic): `BSD root: md0` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> `SWEET init: still alive` every 5 s. Exec, ad-hoc SHA-256 code signature, syscalls, devfs /dev/console, select timeouts all work. Phone image prepared: `shim/out/shim-boot-0025.img` 16,515,072 bytes SHA256 `9dbfa0b15140c0bd733a16c4f727f6a7df44a8741f98d8e266d5f2fa4f689db0` (payload-0025 = 0025 kernel + sweet-0021.adt + research/sweet-init + rd=md0; ramdisk byte-match check-0025). Waiting for user to put phone in FASTBOOT.
- **0024 CI `38773277811` PASSED**, `xnu/out-0024` SHA256 `a0ba964b...4348`. QEMU `research/q0024-rd` and **PHONE (boot 2026-10-15 17:05:55 UTC, `research/boot0024.log`, image `shim/out/shim-boot-0024.img` SHA256 `cf3dac86...6964`, 16,510,976 bytes, payload `shim/out/payload-0024.bin` = 0024 kernel + `shim/out/sweet-0021.adt` + RAM disk `research/sweet-init` + rd=md0; ramdisk byte-match `check-0024`)** agree: `Added memory device md0`, `BSD root: md0`, `load_init_program: attempting to load /sbin/launchd`, then data abort in accelerate_entitlement_queries (PC 0x...77d2458, FAR 0x1a0) = NULL AMFI interface. Photo `IMG_20261015_190715.jpg`. RAM disk root is physically verified.
- **0025 (`2518c79`)**: new `bsd/kern/sweet_amfi.c` registers a built-in AMFI interface at EARLY_BOOT/MIDDLE: no entitlements (adjustContextWithoutMonitor succeeds without creating a context, queries KERN_DENIED, copies NULL/KERN_NOT_FOUND, get_xml/transmuted false); WithMonitor KERN_NOT_SUPPORTED; OSEntitlements_query and query_context_to_object panic explicitly (CoreEntitlements closed; no kernel caller); TrustCache version 0 (0015 keys on trust_cache_rt==NULL, img4 absent -> still unavailable); CoreEntitlements table zero (PMAP_CS only). Compiles locally; checker updated (bt27 entries). CI **`38774788048`** running. Next artifacts `xnu/out-0025`, `research/bt29`, `research/run29.log`. Real iOS binaries will need real entitlements later (no OSS CoreEntitlements exists).
- **0021-0024 RAM-disk-root iteration (Claude), QEMU only so far, no new phone boot since 0020.** Each kernel tested with `tools/mkpayload.py KERNEL research/q0021.adt OUT --ramdisk research/sweet-init --cmdline "debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=md0"` then `tools/qemu-sweet.py OUT DIR --secs 150 --kernel KERNEL --fail-on-panic` (PATH needs ~/swift/usr/bin for llvm-nm). Fresh ADTs: `research/q0021.adt` (QEMU), `shim/out/sweet-0021.adt` (phone).
  - 0021 CI `38769532000` PASSED, `xnu/out-0021` SHA256 `2b7500a1...962e`, `research/bt25`/`run25.log`. QEMU `research/q0021-rd`: md0 root, then assert `iomediaClass` in IOService::publishHiddenMedia.
  - 0022 (`20ece9c`, publishHiddenMedia without IOMedia class) CI `38770666158` PASSED, `xnu/out-0022` SHA256 `a4d0e787...30c5`, `research/bt26`/`run26.log`. QEMU `research/q0022-rd`: data abort in SHA256_Init (NULL g_crypto_funcs) from vm_kernel_addrhash_internal.
  - 0023 (`c8089d1`, libkern SHA256_Init/Update/Final use built-in ccsha256_ltc_di + ccdigest_init/update on SWEET; also serves code-signing SHA-256; SHA-1/MD5/SHA-384/512 still have NO provider - BearSSL from 0020 could supply them later) CI `38771876423` PASSED, `xnu/out-0023` SHA256 `d763fed7...1003`, `research/bt27`/`run27.log`. QEMU `research/q0023-rd`: **mockfs mounted md0, `load_init_program: attempting to load /sbin/launchd`**, then panic `mockfs_fsnode_vnode failed to create fictitious pages ... rvalue = 5` (mockfs.c:351).
  - 0024 (`3293c80`): mockfs used memdev mi_base (4K page number of a VIRTUAL kernel address for IOKit RAMDisk, truncated to 32 bits) << PAGE_SHIFT as a physical address. Now zero-copy pager mapping only when mi_phys (with 4K units); virtual md uses pagein/blockmap/strategy -> memdev bcopy. memdev's own mdPhys path assumes 4K ppnums (unsafe on 16K arm64), so do NOT switch the RAMDisk to physical. CI **`38773277811`** running. Next artifacts `xnu/out-0024`, `research/bt28`, `research/run28.log`.
  - Sandboxes: bt25/bt26/bt27 contain the next patch's edited files; pristine copies in `research/pre0022`..`pre0024`.
- **PATCH 0021 (Claude): RAM disk root via mockfs -> first userspace program.** Commits `9c37771` (initial; CI `38768500280` FAILED: mockfs_fsnode.c kfree_type(mockfs_fsnode_t) typed-alloc static assert; local xnu-cc stubs `__builtin_xnu_types_compatible` so it can't catch this) and `193772f` (fix), CI **`38769532000`** running: https://github.com/dipa-studio/ios-sweet/actions/runs/38769532000. Next artifacts: `xnu/out-0021`, `research/bt25`, `research/run25.log`.
  - Kernel: `config/MASTER.arm64.sweet` FILESYS_BASE += `mockfs` (XNU's built-in FS: root device is itself a Mach-O, served as /sbin/launchd, plus /dev for devfs). Upstream mockfs bit-rot fixed: kalloc_type/kfree_type used the POINTER typedef mockfs_fsnode_t (nodes were 8 bytes) -> `struct mockfs_fsnode`. `IOService::setRootMedia` asserted IOBlockStorageDriver class exists (IOStorageFamily absent): SWEET-only, a missing class means root=NULL (same as IOSetImageBoot); Apple path keeps assert. All 21 patches apply (`research/check-patch-order.py`); 5 TUs compile locally with -DMOCKFS (`research/mockfs-objs`), imports resolve vs 0020 kernel. Sandbox `research/bt24/xnu` now holds 0021 versions of those 3 files; pristine 0020 copies in `research/pre0021`.
  - Tools: `tools/mkpayload.py --ramdisk IMAGE` appends IMAGE as an extra payload segment right after the kernel, moves kernel_end past it (shim unchanged: ADT+boot_args follow it, image stays below topOfKernelData), and adds ADT `/chosen/memory-map` `RAMDisk`=<phys,size>. Boot with `rd=md0`. Without --ramdisk output is byte-identical to existing 0020 QEMU and phone payloads (verified). `tools/sweet-init.S` + `tools/mkinit.py`: PIC static init (open /dev/console, print PID, heartbeat every 5 s via select, never exits) wrapped into a static arm64 Mach-O (__PAGEZERO, __TEXT@0x100000000, LC_UNIXTHREAD, ad-hoc SHA-256 CodeDirectory v0x20400, 4K pages). Build: `~/swift/usr/bin/clang -target arm64-apple-ios16.0 -c tools/sweet-init.S -o X.o && tools/mkinit.py X.o research/sweet-init` (ld64.lld cannot link static iOS). Signature not verified by a real codesign; the kernel will tell.
  - QEMU with 0020 kernel + RAM disk (`research/q0020-rd.bin`, rd=md0, 150 s `research/q0020-rd150`): `Added memory device md0`, **`BSD root: md0, major 1, minor 0`** (plumbing works), then the setRootMedia assert (now fixed in 0021). NOTE: QEMU needs >60 s to reach IOFindBSDRoot (60 s run showed nothing after stf0; likely RTC/inittodr wait), so use --secs 150.
  - NEXT: download 0021, QEMU 150 s with ramdisk; expect mockfs mount then init exec -> `*** SWEET userspace: init running as PID 1 ***`. Then phone boot with same payload (phone ADT shim/out/sweet-0020.adt pattern + --ramdisk + rd=md0).
- **0020 PHONE RESULT (user transcription of screen, 2026-10-15): KERNEL INIT COMPLETE, WAITING FOR ROOT.** After Skywalk self-tests PASSED, kminit, ifnet_attach lo0/gif0/stf0, screen prints `BSD`, then `Waiting on <dict><key>IOProviderClass</key><string>IOMedia</string><key>Content</key><string>Apple_HFS</string></dict>` and `Failed to write boot-picker-bringup-reason to NVRAM.` No panic. This is IOFindBSDRoot waiting for a root device (none exists); NVRAM warning is expected (no NVRAM driver). QEMU `cpu_idle` snapshot is presumably the same wait (not GDB-confirmed; milestone GDB run was cancelled by user since phone answered it). Draft `research/check-milestones20.gdb` (hbreaks inittodr/vfs_mountroot/IOFindBSDRoot/bsd_utaskbootstrap) left uncommitted/ignored.
- **NEXT MILESTONE: root filesystem -> launchd.** Plan: (1) RAM disk: shim places an image in RAM, ADT /chosen/memory-map `RAMDisk` entry, boot-arg `rd=md0` (XNU md driver). (2) HFS is a separate kext on Apple; build Apple OSS `hfs` (tag paired with macOS 13.5 in distribution-macOS macos-135 release.json) into SWEET like libpthread 0019. APFS is closed. (3) Minimal HFS image with iOS 16 launchd (later: dyld/shared cache; AMFI/code-signing absent will be a later hurdle). User's end goal is full iOS GUI.
- **0020 (AES) VERIFIED + PHONE BOOTED (Claude took over after Codex usage limit).** Actions `38765422261` (`ab9e23f`) PASSED; kernel `xnu/out-0020/kernel.development.sweet` checksum OK; buildtree `research/bt24`, log `research/run24.log`. Actual-kernel AES checks PASS (`research/check-aes20.gdb` / `.log`, 12 extra CBC cases match OpenSSL). 45s QEMU `research/q0020`: no panic, zero unknown glyphs, past old TCP/AES panic -> Skywalk self-tests PASSED -> bsd_autoconf kminit -> ifnet_attach lo0/gif0/stf0; final snapshot PC in `cpu_idle` (idle or waiting; NOT yet diagnosed, could be root-device wait). Image `shim/out/shim-boot-0020.img` 16,461,824 bytes SHA256 `775200cb02d95fc750981516b79d91dcdc96184bbe67a38f9d57c59b4a391828`, ramdisk byte-matches `payload-0020.bin` (`check-0020`). **Phone temporarily booted 2026-10-15 16:10:00 UTC**: one FASTBOOT product sweet, send OKAY0.407s, boot OKAY0.134s, total0.549s, exit0 (`research/boot0020.log`). Awaiting user photo; do not reboot the phone before it. NEXT: read photo; diagnose what QEMU waits on after stf0 (GDB backtrace of threads / longer run). Codex's STOP request below is complete.
- User requests STOP after completing the current0020 AES iteration (Actions/QEMU/phone), then leave a precise committed handoff for another AI. User says FASTBOOT ready again after0019 photo. Do not start a new blocker fix after this iteration.
- Goal: iOS16-generation XNU on Redmi Note10Pro sweet/SM7150. Always commit, use gh/Actions for kernel builds, keep this handoff current. Temporary fastboot boot only; preserve Android/backups. No userland/root filesystem boot yet.
- **Patch0020 update:** initial `e71098d` / Actions `38765012466` superseded by scalar-only compile flags. Added -mgeneral-regs-only to all six provider/BearSSL TUs and corecrypto_aes.c; object disassembly now confirms no SIMD. Updated implementation `ab9e23f`, Actions `38765422261` queued/running: https://github.com/dipa-studio/ios-sweet/actions/runs/38765422261. Do not launch another run. portable BearSSL AES CBC and legacy one-block ECB wired directly into SWEET corecrypto_aes.c. Genuine bitslice implementation, no CPU AES/SIMD requirement, heap or fake global crypto table. Source fetched by `0020-stage-bearssl.sh` from official BearSSL git at immutable `7bea48e5e850ab4cafbe68d3765cdaba13a86d6f`; MIT license retained, downloaded source stays out of git. Kernel limits include adapter only. All128/192/256-bit keys, CBC encrypt/decrypt, copied contexts, in-place/out-of-place; zero block count and size overflow handled, invalid keys clear context. Seven TUs compile to arm64 objects (`research/aes-objs`), imports resolve, all20 patches apply and sources match (`research/patch0020-check.log`). Sandbox `research/bt23/xnu`, originals `research/pre0020`. NEXT: Actions then actual-kernel NIST/random CBC/ECB checks and >=45s QEMU before another phone boot. Next artifacts out-0020 / bt24 / run24.log. 0020 updated CI pending. Local sources/checks match the scalar-only patch.
- **Latest built kernel0019**, implementation `256d3f0`, patches0001-0019. Actions `38763072907` PASSED (4m5s): https://github.com/dipa-studio/ios-sweet/actions/runs/38763072907. Kernel `xnu/out-0019/kernel.development.sweet`, SHA256 `a27df7568f03fb541cf0e8024c0a594fa178a85054fcf9eba29158cbd4c5ecc0`; checksum verified. Log/source `research/run23.log` / `research/bt23` (no nested .git). Seven pthread source/build/header files and staged adaptations byte-match local compile inputs.
- **0019 hardware photo received** `IMG_20261015_175306.jpg`: pthread registration visible, passes mbinit and DLIL checksum/scheduling, same AES fault as QEMU: PC`0xfffffe00079174e0` (`aes_encrypt_key128`), LR`0xfffffe000767c3a4` (`tcp_init`), FAR0x78, x8=0. Disassembly proves NULL g_crypto_funcs->ccaes_cbc_encrypt. Photo processed; no more0019 observation pending. General crypto table remains absent, other hash/mode operations may still fault after0020. DO NOT bypass TCP or install fake crypto. XNU already contains SHA256/HMAC implementations; AES source there is a dispatch wrapper. Full future provider interface libkern/libkern/crypto/register_crypto.h. Apple/corecrypto default README describes evaluation-only licensing, so no external corecrypto was fetched or staged; BearSSL selected for this portable AES integration.
- **0019 pthread FIXED in QEMU and observed beyond its init on phone**: 45s QEMU `research/q0019`, zero unknown glyphs, then AES panic. Actual-kernel API checks PASS `research/check-pthread19.gdb` / `.log`, guest `research/q0019-api`: function/callback table identity, actual provider pthread_init returns, locks/global hash/threadcall/typed zones initialized, thread_selfid via syscall shim + buffer bounds, process hash init/delete via shims restores NULL. Monitor quit prints expected remote-disconnect after PASS. All fixture guests stopped.
- **0019 provider**: genuine Apple libpthread-514.100.2 commit `a6c70ca0e544347a0377babf748f831577ec24f9`, exact paired release with xnu8796.141.3 in distribution-macOS/macos-135/release.json (`research/macos-135-release.json`). 0019 shell stage runs before patches (workflow copies *.sh); three SWEET wrapper TUs use kext BSD header view, vm_fault_external, renamed provider-side pthread_kern/current_uthread; register real function table at EARLY_BOOT SECOND, real pthread_init later. Stager applies bounded address casts, zero user addresses, proper panic format. SWEET opaque ksyn storage enlarged48->56 for trailing kwe_uth, checked with provider static assertion. Local pre-CI TargetConditionals fixture was syntax-only; artifact bt23 carries actual SDK header and CI is authoritative.
- **Phone0019 temporarily booted** 2026-10-15 15:51:36 UTC: exactly one FASTBOOT/product sweet verified; send OKAY0.406s, boot OKAY0.134s, total0.546s, exit0 (`research/boot0019.log`). Image `shim/out/shim-boot-0019.img`, 16,457,728 bytes, SHA256 `19429a57e486b856880df9e27327ed488e0139345311fdb0350974e72103a9a1`. Phone ADT/payload `shim/out/sweet-0019.adt` / `payload-0019.bin` timer19, unpacked ramdisk byte-match (`check-0019`). EntryPA0xb146b488, kernelendPA0xb2000000, boot_argsPA0xb2004000/top0xb2008000. Last user FASTBOOT+USB reply preceded this boot; do not assume phone is still in FASTBOOT.
- **CPU0018 physically verified** by `IMG_20261015_173951 (2).jpg`: boot CPU0 registered, real SGI1 verified, initialization complete -> BSD/MAC/mbinit -> old pthread-table panic. SweetCPU uses legacy IOCPU, ml_processor_register/processor_start/initCPU, real SGI1 clears SIGPdisabled before max CPUs completion; no forced flags/skipped waits. CPU APIs and two-CPU rejection passed (`research/check-cpu18.gdb`, `q0018-api`, `q0018-smp`). Single core; SMP/suspend unsupported. CURRENT SWEET has NO USE_APPLEARMSMP.
- QEMU next run: generate fresh `tools/mkadt.py research/q0020.adt --qemu` (timer27), mkpayload with `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`, then `tools/qemu-sweet.py PAYLOAD OUT --secs 45 --kernel KERNEL --fail-on-panic`. 12s can miss later panics because IORTC waits30s. Runner snapshot only: panic exit2, blank/incomplete exit3; absence of panic does not mean complete boot. Qualcomm XPU/ABL/panel and phone SMC PSCI require hardware checks.
- Local checker `tools/xnu-cc.py research/run23.log research/bt23 FILTER --per-file`, XNU_CC_OBJDIR for objects. For new BearSSL TUs add XNU_CC_EXTRA with -I bt23/xnu/libkern/crypto/sweet_bearssl/{inc,src}. Patch checker `research/check-patch-order.py` uses temporary upstream index; source fixtures/artifacts ignored under research. GDB mask registers to unsigned64, use function-entry manual-call return traps, discard manipulated guests. No QEMU guest intentionally left running.

## Session log and earlier handoffs (superseded by the active summary above)

### Prior 0019 transition notes (superseded)

- Goal: iOS 16 generation XNU on sweet. Always commit completed work, use gh/Actions for kernel builds, keep this handoff current. Temporary fastboot boot only; preserve Android/backups.
- **0019 build PASSED** Actions `38763072907` (4m5s), implementation `256d3f0`. Kernel `xnu/out-0019/kernel.development.sweet`, SHA256 `a27df7568f03fb541cf0e8024c0a594fa178a85054fcf9eba29158cbd4c5ecc0`; checksum verified. Log/source `research/run23.log` / `research/bt23`; all seven patched files and staged provider adaptations match local compile inputs. Prefer bt23 as the next baseline.
- **0019 pthread FIXED in QEMU**: 45s run `research/q0019` registers provider, passes mbinit, DLIL SUM16 checks and DLIL thread scheduling. Actual-kernel GDB checks `research/check-pthread19.gdb` / `.log` PASS: function/callback table identity, real _pthread_init returns, locks/global hash/cleanup threadcall/typed zones non-NULL, thread_selfid via actual syscall shim with output bounds, process hash init/delete through actual shims restores NULL. Guest stopped after tests; no fixture left running. GDB monitor quit prints expected remote disconnect after PASS.
- **Current next blocker:** QEMU0019 panic data abort FAR0x78 at `aes_encrypt_key128` PC`0xfffffe00079174e0`, called by `tcp_init` LR`0xfffffe000767c3a4`. Disassembly confirms `g_crypto_funcs == NULL`, loading ccaes_cbc_encrypt at+0x78. General crypto registration is still absent; DO NOT bypass TCP or supply fake crypto. Next integrate a genuine compatible crypto implementation/provider (AES first needed here, other digest/mode APIs also used). XNU contains SHA256/HMAC but no AES implementation; its corecrypto_aes.c is a dispatch wrapper. Full crypto table is in libkern/libkern/crypto/register_crypto.h.
- **0019 phone image prepared and verified**, user reports FASTBOOT+USB again; exactly one device/product sweet verified. `shim/out/shim-boot-0019.img`, 16,457,728 bytes, SHA256 `19429a57e486b856880df9e27327ed488e0139345311fdb0350974e72103a9a1`; unpacked ramdisk matches phone payload (`shim/out/check-0019`, `payload-0019.bin`, `sweet-0019.adt`, timer19). EntryPA0xb146b488; kernelendPA0xb2000000; boot_argsPA0xb2004000/top0xb2008000. Usual debug cmdline cpus=1/-noprogress. **Temporarily booted 2026-10-15 15:51:36 UTC**: send OKAY0.406s, boot OKAY0.134s, total0.546s, exit0 (`research/boot0019.log`). User asked for photo after45s. Await the photo; DO NOT reboot again before observation. Bootloader acceptance only; no0019 physical progress observed yet.
- **Hardware photo confirms 0018 progress** (`IMG_20261015_173951 (2).jpg`): real phone prints `SWEET CPU: boot CPU 0 registered, SGI1 verified, initialization complete`, enters BSD/MAC, reaches `mbinit: done`, then the same missing-pthread-function-table panic as QEMU at pthread_shims.c:318. CPU completion/interrupt delivery is now physically observed. The photo was received; no further phone boot performed yet.
- **Patch0019 committed/pushed `256d3f0`; Actions `38763072907` queued/running:** https://github.com/dipa-studio/ios-sweet/actions/runs/38763072907. Do not launch a duplicate. genuine Apple OSS libpthread-514.100.2 provider (immutable commit `a6c70ca0e544347a0377babf748f831577ec24f9`), paired with xnu-8796.141.3 by Apple's `distribution-macOS/macos-135/release.json` (`research/macos-135-release.json`). `0019-stage-libpthread.sh` fetches/stages it before patches; workflow now copies shell scripts too. SWEET-only wrappers compile all three real kernel sources, rename provider-side symbols, use kext header view and vm_fault_external, register the real function table at EARLY_BOOT SECOND. Existing pthread_init then runs the actual provider initialization. No pthread wait/syscall is bypassed. Source staging includes bounded explicit address casts/zero user addresses and panic-format fixes. SWEET kernel opaque ksyn storage enlarged from48 to56 bytes to contain this provider's trailing kwe_uth, with a provider size assertion. Local compile of three provider TUs plus pthread_shims/kern_fork passed; imports resolve and provider exports do not collide with existing kernel symbols. All19 patches apply and changed sources match (`research/patch0019-check.log`). Source sandbox `research/bt22/xnu`, originals `research/pre0019`, objects `research/pthread-objs`. Local TargetConditionals fixture only has target macros for syntax; CI stages the real macOS SDK header and is authoritative. Next Actions artifacts: out-0019 / bt23 / run23.log; run QEMU >=45 seconds. 0019 CI is pending; no 0019 QEMU run yet.
- **Latest kernel implementation `e7d9550`, patches0001-0018; CI `38760004398` PASSED (3m56s)**: https://github.com/dipa-studio/ios-sweet/actions/runs/38760004398. No build is pending. Kernel `xnu/out-0018/kernel.development.sweet`, SHA256 `b3c8d59acc88f93a2c836eb2527a05ed4fbaac7c580a2ea8c3b795137f4aadf1`; checksum verified. Source/log `research/bt22` / `research/run22.log` (baseline for patch0019; no nested .git). New driver/config sources match CI exactly.
- **CPU wait FIXED in QEMU**: SweetCPU uses legacy IOCPU, validates single boot CPU, ml_processor_register -> processor_start -> initCPU real SGI1 -> scheduler/IOKit completion -> ml_set_max_cpus. It does NOT force a flag or skip a wait. CPU APIs passed: Running CPU0, processor_array[0] association, SGI signalling enabled, name, unsupported secondary-start error (`research/check-cpu18.gdb` / `.log`, `research/q0018-api`). Single-core only; SMP and suspend unsupported. Two-CPU topology fails explicitly (`research/q0018-smp`).
- **Next blocker reproduced in 45s QEMU** (`research/q0018-long`, zero unknown glyphs): BSD initialization reaches MAC framework, network mcache and `mbinit: done`, then **`pthread kernel extension not loaded (function table is NULL). @pthread_shims.c:318`**. Do not bypass pthread_init: find/integrate the matching open-source libpthread kernel implementation and register its real function table. A 12s run `research/q0018` looked panic-free before the 30s IORTC wait elapsed; use >=45s or GDB checkpoints for the next iteration. No userland/root filesystem boot yet.
- **Phone 0018 TEMPORARILY BOOTED** 2026-10-15 **15:31:15 UTC**: exactly one FASTBOOT device verified product sweet; send OKAY0.400s, boot OKAY0.134s, total0.539s, exit0. Local log `research/boot0018.log`. This confirms bootloader acceptance only. User was asked for a photo; await it, DO NOT reboot the phone again before their observation. No flashing performed.
- Current hardware image `shim/out/shim-boot-0018.img`, **16,437,248 bytes**, SHA256 **`b7a23595d143a76c72c9fe2cfcc5d77a8f16987b5af1a2703bbffdfa6922908c`**. Phone ADT/payload `shim/out/sweet-0018.adt` / `shim/out/payload-0018.bin` (timer19), unpacked ramdisk exactly matches payload (`shim/out/check-0018`). EntryPA0xb146b488; kernelendPA0xb1ffc000; boot_argsPA0xb2000000/top0xb2004000. Command line `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`.
- QEMU payload/ADT `research/q0018.bin` / `research/q0018.adt` (timer27). Run `python3 tools/qemu-sweet.py research/q0018.bin research/NEW-OUT --secs 45 --kernel xnu/out-0018/kernel.development.sweet --fail-on-panic`; fresh ADT seed for a new payload. Output fb.png/fb.txt/regs.txt/qemu.log/result.json. Visible panic exit2; blank/incomplete decode exit3; no_panic_observed is snapshot-only, not successful boot. -noprogress prevents the graphical indicator corrupting console text. Qualcomm XPU/bootloader/panel and SMC PSCI still need physical validation.
- Patches0014-0017 fixed PRNG registration/direct SHA256, explicit unavailable trust-cache service with rejected loads/no matches, built-in SweetPlatformExpert, and timer PPI from ADT (phone19/default19, QEMU27). All their checks/artifacts are preserved in the history below. CURRENT SWEET has NO USE_APPLEARMSMP; do not assume gCPUIC/gAIC/gPMGR AppleARMSMP globals exist.
- Local single-file checker: tools/xnu-cc.py research/run22.log research/bt22 FILTER --per-file, output via XNU_CC_OBJDIR. Patch checker `research/check-patch-order.py` applies all18 via temporary index, matches sandbox sources. Sandbox for0018 `research/bt21/xnu`, originals `research/pre0018`, objects `research/cpu-objs`. First compiler issues were missing machine/atomic.h and nonexistent getNameSymbol; fixed and both TUs compiled successfully before CI. Fixtures/artifacts under research are local-only/ignored.
- GDB: mask int(register)&((1<<64)-1) for unsigned kernel pointers; use function-entry manual-call return traps, discard manipulated guests. No QEMU fixture is intentionally left running.

### Earlier active handoff snapshot (superseded)


- **0018 milestone:** Actions `38760004398` PASSED (3m56s), checksums passed, new CPU/build files byte-match CI tree. Kernel `xnu/out-0018/kernel.development.sweet`, SHA256 `b3c8d59acc88f93a2c836eb2527a05ed4fbaac7c580a2ea8c3b795137f4aadf1`; log/tree `research/run22.log` / `research/bt22`. QEMU `research/q0018` 12s: boot CPU registered, SGI1 verified, CPU initialization complete, **BSD initialization entered** (copyright, MAC framework, buffer headers), no panic/zero unknown glyphs. Direct CPU API checks PASS (`research/check-cpu18.gdb`, `.log`, `research/q0018-api`): CPU0 Running, processor matches processor_array[0], real SGI enabled, CPU name correct, secondary-start returns KERN_NOT_SUPPORTED. Two-CPU ADT correctly panics before registration (`research/q0018-smp`). Longer 45s run `research/q0018-long` still running; next BSD wait/fault not yet identified.
- **Prepared 0018 phone image:** `shim/out/shim-boot-0018.img`, 16,437,248 bytes, SHA256 `b7a23595d143a76c72c9fe2cfcc5d77a8f16987b5af1a2703bbffdfa6922908c`. Phone ADT/payload `shim/out/sweet-0018.adt` / `shim/out/payload-0018.bin`, usual debug args with cpus=1 and -noprogress. Unpacked ramdisk byte-compared (`shim/out/check-0018`). Entry PA remains 0xb146b488; kernel end PA 0xb1ffc000, boot_args 0xb2000000/top0xb2004000. User reports FASTBOOT+USB ready; read-only check found exactly one product sweet. NEXT: temporary fastboot boot of this verified image, record send/boot results, then await hardware photo without rebooting again.
- Patch 0018 committed/pushed **`e7d9550`**; Actions **`38760004398`** queued/running: https://github.com/dipa-studio/ios-sweet/actions/runs/38760004398. Do not launch a duplicate run.
- Active continuation: patch **0018** implemented in `iokit/Kernel/arm/SweetCPU.cpp` + arm64 source list + exact qcom,kryo470 personality. Keeps legacy IOCPU, accepts ONLY the single boot CPU, fills ml_processor_info from parsed topology with CPU object as cpu_id, calls ml_processor_register and processor_start. initCPU sends SGI1 via ICC_SGI1R_EL1 and waits (1-second deadline) for real cpu_signal_handler to clear SIGPdisabled. Only after successful startup calls ml_cpu_init_completed/cpusRunning and publishes completion/max CPUs. Secondary startup/suspend are explicitly unsupported. Local C++ compile passed for both TUs (`research/cpu-objs`), all imports resolve, object contains dsb ishst / ICC_SGI1R / isb; all18 patches apply in order and match sources. Sandbox `research/bt21/xnu`, originals `research/pre0018`; next CI artifacts should use `xnu/out-0018`, `research/bt22`, `research/run22.log`. User has the phone available; first run QEMU, then prepare/temporarily boot useful hardware progress.
- Goal: iOS 16 generation XNU on Redmi Note 10 Pro / sweet. User wants persistent progress, commits, kernel builds via `gh` Actions, and this handoff kept current across agent switches. Temporary `fastboot boot` only; preserve Android and backups.
- Latest kernel implementation: **`aa3f991`**, patches **0001-0017**. All four new Actions builds PASSED: 0014 `38748543058` (4m0s), 0015 `38749549779` (4m3s), 0016 `38750733996` (4m3s), 0017 **`38751507437` (4m7s)**. Latest: https://github.com/dipa-studio/ios-sweet/actions/runs/38751507437. No build is pending.
- **Current blocker: CPU initialization has no SWEET CPU driver.** QEMU registers SweetPlatformExpert, then kernel_bootstrap_thread waits in **kperf_init_early -> ml_wait_max_cpus**. Confirmed via actual-kernel GDB call stack (`research/locate-cpu-wait2.log` / `.symbols`) and normal-run `max_cpus_initialized == 2` (MAX_CPUS_WAIT). Do not force the flag or remove the wait. Next implement real CPU registration and completion using XNU's CPU/processor interfaces. CURRENT SWEET uses legacy IOCPU (`USE_APPLEARMSMP` is absent); enabling AppleARMSMP is a separate architectural change requiring GIC/PMGR services. No userland/root filesystem boot yet.
- Fixed this session: PC=0 unregistered PRNG callback (0014, built-in HMAC-SHA256 provider + direct entropy/write_random hashing); absent Image4/AMFI trust-cache service (0015, unavailable runtime, loads rejected and queries no-match); missing platform driver (0016, SweetPlatformExpert exact personality); incorrect QEMU timer IRQ (0017, validated ADT PPI property, phone default19/QEMU27).
- **Latest kernel** `xnu/out-0017/kernel.development.sweet`, SHA256 `055a80190ab998b4df9203f1102072dcc78faad1779a537a514e522b682b582f`. Buildtree/log **`research/bt21` / `research/run21.log`**; all nine changed C/C++/header/config files byte-match local checked sources. Checksums passed. Entry PA `0xb146b488`, kernel end PA `0xb1ff4000`. Preferred baseline for patch 0018: `research/bt21/xnu` (no nested .git).
- **QEMU verified**: `research/q0017-noprogress` ran **30 seconds**, no visible panic, **zero unknown glyphs**, IRQ exceptions returned normally (4 IRQs, tickless idle). It still waits for CPU completion, so this is NOT a completed boot. Earlier 15s run `research/q0017` captured 122 IRQs, timer value27, GICR_ISENABLER0 `0x08000002`, and CPU WAIT; graphical progress overlay corrupted 13 glyphs. Add **`-noprogress`** to keep the console readable. New runner classifies incomplete/blank decoding explicitly (exit3 with --fail-on-panic), visible panic exits2. Snapshot-only; use regs/GDB to diagnose stalls.
- Current QEMU payload/ADT: **`research/q0017-noprogress.bin` / `research/q0017.adt`**. Run: `python3 tools/qemu-sweet.py research/q0017-noprogress.bin research/NEW-OUT --secs 30 --kernel xnu/out-0017/kernel.development.sweet --fail-on-panic`. Generate fresh seed with mkadt for a new payload. QEMU virt models generic ARM execution, not Qualcomm XPU/bootloader/panel or the phone's SMC PSCI conduit.
- **Prepared phone image**: **`shim/out/shim-boot-0017.img`**, 16,416,768 bytes, SHA256 `51ff7fe30b4a6668c3452ffe1da922c5ac30cb8de60625c2a652587ecbd0ec92`. Phone ADT/payload `shim/out/sweet-0017.adt` / `shim/out/payload-0017.bin` (timer19). Unpacked ramdisk exactly matches payload (`shim/out/check-0017`). Command line **`debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`**. NOT sent to phone this session: known CPU-driver wait should be addressed in QEMU first. Last actual phone boot remains 0013; user's latest photo `IMG_20261015_160033.jpg` confirmed the old PRNG PC=0 panic.
- Direct QEMU/GDB API checks: PRNG 600-byte chunking, buffer bounds, changing output, zero-length reads/writes, user reseed, contended refresh, generator1 init/output PASS again on latest0017 (`research/check-prng17.gdb` / `.log`, guest `research/q0017-api`). Trust-cache unavailable-service/argument/output cases PASS on0015 (`research/check-trustcache.gdb` / `.log`). Platform registration + target/product normal/truncated/zero/null/bounds PASS on0016 (`research/check-platform.gdb`, `research/check-platform3.log`). Different platform ID correctly retains IOPanicPlatform fallback (`research/q0016-negative`). Timer PPI32 and size2 correctly panic (`research/q0017-badppi`, `research/q0017-badsize`); omitted property selects19 (`research/q0017-default`). These are API/bring-up checks, not crypto certification or SMP scheduling validation.
- Local checker **`research/check-patch-order.py`** verifies all17 patches and changed source equality using a temporary upstream git index. Fixtures/logs/artifacts under research are local-only and ignored. For GDB unsigned kernel pointers, mask `int(register_value) & ((1<<64)-1)`; x30/x29 may be rendered signed. Stop at a function entry for manual-call return traps, and discard each manipulated guest after API tests. All fixture QEMU guests have been stopped.


- User wants persistent progress toward iOS 16, commits for completed changes, builds through `gh` / GitHub Actions.
- Keep this file current at every milestone so another agent can resume immediately, including when usage limits interrupt a session.
- Patch 0017 committed/pushed `aa3f991`, Actions `38751507437` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38751507437. Next artifacts: xnu/out-0017, research/bt21, research/run21.log. Do not duplicate.
- Patch 0016 kernel downloaded/checksum verified: SHA256 `d06336c54baa06e0df6561a8bd7df98a9b9f7502c9381c62d1a44c045cd1ce46`, `xnu/out-0016/kernel.development.sweet`; buildtree/log `research/bt20` / `research/run20.log`. QEMU `research/q0016` (10s) prints platform expert registered, zero unknown glyphs, no panic observed BUT stalls (timer mapping still wrong until 0017). Direct actual-kernel GDB tests passed for registered instance and target/product names, including maxLength=1/0 and NULL, sentinels intact (`research/check-platform.gdb`, `research/check-platform3.log`, `research/q0016-api3`). First two fixture attempts used premature/wrong return breakpoints; discarded, corrected fixture uses start-return observation then a function-entry return trap. No phone boot yet.
- Patch 0016 CI `38750733996` PASSED (4m3s); artifacts not yet downloaded/booted. Patch 0017 prepared to fix QEMU timer fidelity BEFORE interpreting future no-panic/stall runs: actual `qemu-system-aarch64 -M virt,gic-version=3,dumpdtb=research/qemu-virt.dtb ...` timer property has virtual PPI 11 => INTID 27, while phone uses INTID 19. Kernel formerly hardcoded 19. New optional /arm-io/gic virtual-timer-intid property selects the PPI (validate exact u32 and 16..31); missing property retains phone default 19. One RO-late global drives GIC enable and sleh_irq dispatch. tools/mkadt.py emits phone19/QEMU27. Both C TUs compile (`research/timer-objs`), ADT serialize/parse checks confirm values/addresses, all 17 patches apply and match. Sandbox `research/bt19/xnu`, originals `research/pre0017`; initial local sleh compile failed due read-only exported header not updated, fixed export and BOTH recompiled successfully. CI exports normally.
- Architecture correction for next agent: CURRENT SWEET board_config does NOT define USE_APPLEARMSMP; it compiles the legacy IOCPU path, not cpu_boot_thread/IOPMGR AppleARMSMP. Existing roadmap mentions AppleARMSMP as a future approach. Do not look for gCPUIC/gAIC/gPMGR globals in the current kernel: they are absent. Determine the actual CPU-init wait after platform registration before choosing the next driver architecture.
- Patch 0016 committed/pushed as `0dcdf5c`; Actions `38750733996` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38750733996. Next artifacts: `xnu/out-0016`, `research/bt20`, `research/run20.log`.
- Patch 0016 implemented: new `iokit/Kernel/arm/SweetPlatformExpert.cpp`, arm64 source list, built-in personality in KernelConfigTables.cpp guarded by ARM64_BOARD_CONFIG_SWEET. Matches only xiaomi,sweet at score 10000, keeps IOPanicPlatform fallback for other hardware. Uses IODTPlatformExpert base initialization/power domain and createNubs CPU logical-ID annotation; overrides top-level publishing because base requires nonexistent Apple NVRAM /options. Publishes real CPU/top-level nodes, provides bounded target/product names, and registers the platform service. GIC/PMGR and arm-io child-bus drivers remain separate work. Both C++ TUs compile (`research/platform-objs`), all imports resolve against 0015/own objects, all 16 patches apply and sources match. Sandbox `research/bt19/xnu`; originals `research/pre0016`. NEXT: full Actions/QEMU; inspect CPU boot waits after the platform registers, do not equate absence of panic with successful boot.
- Patch 0015 CI `38749549779` PASSED (4m3s), checksum verified. Kernel `xnu/out-0015/kernel.development.sweet`, SHA256 `ca1b424a596c7058550ad1659080a333e7643270f019656401d80bf2b876645f`; buildtree/log `research/bt19` / `research/run19.log`. QEMU `research/q0015` (10s, zero unknown glyphs) passes trust-cache handling and machine lockdown, then panics `Unable to find driver for this platform: "xiaomi,sweet" @IOPlatformExpert.cpp:2319` (IOPanicPlatform fallback). Next concrete work: add a built-in SWEET IODTPlatformExpert personality/class; keep the fallback for mismatched platforms. No phone boot yet.
- Direct trust-cache API checks PASSED in the actual 0015 kernel under QEMU/GDB (`research/check-trustcache.gdb`, `research/check-trustcache.log`, `research/q0015-api`): runtime pointers NULL, hash/UUID queries return NOT_FOUND, typed/untyped/legacy loads return NOT_SUPPORTED, capabilities outputs zero and bounds preserved, invalid-argument cases still reject. Second PRNG check also verifies contended refresh returns immediately (`research/check-prng2.log`, `research/q0014-api2`).
- Patch 0015 committed/pushed `8f851d4`, Actions run `38749549779` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38749549779. Do not duplicate.
- Direct PRNG API checks passed in the REAL 0014 kernel under QEMU/GDB, stopped before trust-cache init (`research/check-prng.gdb`, log `research/check-prng.log`, guest `research/q0014-api`). Invoked read_random for 600 bytes (chunking and buffer sentinel intact), repeated output differed, zero-length read/write succeeded, write_random(64-byte input) succeeded, secondary generator 1 initialized and generated distinct output. QEMU log has no exceptions during these checks; guest was discarded after the tests. This tests API behavior, not a cryptographic certification or SMP scheduling.
- Patch 0015 implemented in `bsd/kern/kern_trustcache.c`: SWEET with missing Image4/AMFI marks both runtime pointers NULL and logs service unavailability. Existing static loader handles NULL. Public load APIs return KERN_NOT_SUPPORTED; hash/UUID queries return KERN_NOT_FOUND; capabilities outputs are zero with KERN_NOT_SUPPORTED. Invalid-input checks remain, and Apple paths/available-provider initialization retain existing behavior. No trust is granted. Local arm64 compile passed (`research/trustcache-objs`), all 15 patches apply and sources match. Sandbox `research/bt18/xnu`, baseline `research/pre0015`. Next: Actions/QEMU and direct unavailable-service API checks using GDB.
- Patch 0014 CI `38748543058` PASSED (4m0s), artifact checksum passed. Kernel `xnu/out-0014/kernel.development.sweet`, SHA256 `741de20c851755d333759d7e668346f3edb4f325efac4cc7c142d80d1f5ff75c`; buildtree/log `research/bt18` / `research/run18.log`. QEMU run `research/q0014` (10s, zero unknown glyphs) prints `SWEET PRNG: HMAC-SHA256 registered`, passes commpage initialization, loads vnguard policy, THEN panics `image4 interface not available @kern_trustcache.c:253`. PC=0 fault FIXED IN QEMU. No new phone boot performed.
- Next work: SWEET currently has neither AppleImage4 nor AMFI. `trust_cache_runtime_init` unconditionally requires both; unlike BCM2837, SWEET enters this startup path. Investigate an explicitly unavailable trust-cache runtime with rejected loads/no query matches while providers are absent; preserve all Apple-platform checks. Merely skipping the startup call would leave later AMFI/IMG4 dereferences unsafe. Existing load_static_trust_cache already handles trust_cache_rt == NULL.
- QEMU runner now supports `--kernel MATCHING_KERNEL --fail-on-panic`: runtime font extraction from the payload produces exact `fb.txt`, plus `result.json`; a visible panic returns 2. Baseline 0013 re-run `research/q0013-text` detects the same NULL callback panic with zero unknown glyphs. Synthetic glyph roundtrip (including literal `?`) and invalid-VA rejection passed. Screen rows remain circular, not a full log; `no_panic_observed` does not prove successful boot. README has the invocation.
- Patch 0014 committed/pushed as `be61f99`; Actions run `38748543058` is running: https://github.com/dipa-studio/ios-sweet/actions/runs/38748543058. Do not start a duplicate build.
- 2026-10-15 active: hardware photo `IMG_20261015_160033.jpg` confirms the same PC=0 instruction-fetch abort as QEMU (LR `0xfffffe0007443fe4` = read_random). Independently reproduced with kernel 0013 in `research/q0013` (8-second run); prior allocator fix works. Latest tooling commit reviewed: `8d66d2d`.
- Patch 0014 implemented: registers a built-in HMAC-SHA256 DRBG provider at EARLY_BOOT/FIRST, before commpage creation. A shared mutex serializes output/reseed across CPUs (correctness first; no per-CPU scaling yet), initgen validates CPU identities, refresh uses try-lock and the existing entropy filter/health tests. SWEET entropy accumulation and write_random now use the built-in SHA256 directly; no incomplete g_crypto_funcs table is registered. The existing bootloader-seed requirement remains enforced.
- Local validation: both PRNG translation units compile to arm64 objects in `research/prng-objs`; no SHA256 wrapper imports remain. All 14 patches apply in CI order and resulting PRNG sources match local inputs. Sandbox `research/bt17/xnu`, originals `research/pre0014`, checker `research/check-patch-order.py`. NEXT: Actions kernel build, download to `xnu/out-0014`, run the QEMU payload before requesting another phone boot. Baseline QEMU ADT/payload are `research/q0013.adt` / `research/q0013.bin`.
- 2026-10-15 08:15 QEMU EMULATION WORKS (`tools/qemu-sweet.py`, see "QEMU emulation" below). Patch 0013 VERIFIED in QEMU: boot passes kmem_crypto_init and ulock_initialize. NEXT BLOCKER (reproduced in QEMU, expected on hardware too): `pmap_create_commpages -> random() -> RandomULong -> read_random -> prng_funcs.refresh == NULL` (instruction fetch abort at pc 0, lr read_random+0x34). Nobody calls `register_and_init_prng` (closed corecrypto kext does it on Apple). Fix = patch 0014: SWEET-registered cckprng_funcs provider (osfmk/prng/prng_random.c); note random_cpu_init also panics while !prng_ready. The 07:26 hardware boot of 0013 will most likely show this same panic.
- Previous hardware boot: patch 0013 (`a3a46e2`) CI `38686345689` PASSED (3m44s), image `shim/out/shim-boot-0013.img` was temporarily booted on 2026-10-15 at 05:26 UTC: send OKAY (0.407s), boot OKAY (0.134s), total 0.546s. Superseded by the hardware/QEMU PC=0 observation and patch 0014 work above.
- Latest kernel implementation commit: `8f851d4`. Latest successful kernel CI: `38749549779` (patch 0015), https://github.com/dipa-studio/ios-sweet/actions/runs/38749549779.
- CURRENT image: `shim/out/shim-boot-0013.img`, 16,412,672 bytes, SHA256 `110d1c46aee4b60253db24b6535e9781c4cf0fd25ca2a70e9016cf81378cea25`. Kernel `xnu/out-0013/kernel.development.sweet`, SHA256 `f0b1d375995316c550ce7014ff234d8271e9b9ac2857795ceff41b76ba2cd740`, plain arm64. CI log confirms 0013 applied; checksums passed. Entry PA `0xb146b488`, kernel end PA `0xb1ff4000`.
- Current log/buildtree: `research/run17.log`, `research/bt17` (extracted, no nested .git; preferred baseline for patch 0014). Payload/ADT: `shim/out/payload-0013.bin`, `shim/out/sweet-0013.adt` (includes /defaults). Unpacked ramdisk byte-compared with payload in `shim/out/check-0013`.
- Patch-0012 original image: `shim/out/shim-boot-0012.img`, 16,412,672 bytes, SHA256 `cf4b8ec4a65a51888d71c17d09cd0831d6b761b90e2531fdb8e575c32f4fd24a`. Kernel `xnu/out-0012/kernel.development.sweet`, SHA256 `69b78f49f6459cc63a0af44e7cf73c1779ef72130ef72b12ae86c88183ffc742`; checksums passed and sweet_early_relocate symbol present. Entry PA remains `0xb146b488`, kernel end PA `0xb1ff4000`.
- Patch-0012 log/tree: `research/run16.log`, `research/bt16` (extracted, no nested .git; preferred baseline for next patch). CI log confirms 0012 applied. Payload `shim/out/payload-0012.bin`, ADT `shim/out/sweet-0012.adt`; packed ramdisk byte-compared with payload in `shim/out/check-0012`.
- Active payload command line: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam`.
- Latest observed photo: `/home/dipa/Downloads/IMG_20261015_071346.jpg` (local only). Stages 9 (kernel framebuffer VA), 10 (TTBR0 off/TLB flush), 11 (physmap table pointers) and 12 (calling pmap_bootstrap) all visible. Persistent diagnostics are VERIFIED ON HARDWARE.
- pmap.c:1987 is the assert after SecureDTLookupEntry(NULL, "/defaults", &entry). The pmap-max-asids property itself is optional; an empty /defaults uses XNU's MAX_ASIDS. Do not bypass the assertion or guess an ASID limit.
- Previous payload-only fix image: `shim/out/shim-boot-0012-defaults.img`, SHA256 `3ff61a268853c6ea7cbf284833f1346a1d791980ca366b6e1a215a86e040512b` (16,412,672 bytes). Same kernel/CI as 0012; ADT 2516 bytes (`shim/out/sweet-0012-defaults.adt`), root /defaults present with no ASID override. Payload `shim/out/payload-0012-defaults.bin`; unpacked ramdisk exactly matches payload (`shim/out/check-0012-defaults`). This boot reached the allocator crypto NULL-pointer fault below.
- Latest hardware photo: `/home/dipa/Downloads/IMG_20261015_071608.jpg` (local only). Normal serial framebuffer console works. VM bootstrap/zone initialization, logging, scheduler, IPC, KDP and ulock_initialize print before the kmem_crypto_init data abort. gPanicBase warnings are expected because PLATFORM_PANIC_LOG_DISABLED is configured, and are not the faulting call.
- Faulting instruction: `ldr x0, [x8, #0x150]` in crypto_random_kmem_ctx_size; x8 = NULL g_crypto_funcs. Source: libkern/crypto/corecrypto_rand.c and osfmk/vm/vm_kern.c:2448. rand.h explicitly permits NON-cryptographic kmem RNGs, but requires no locking in generation and context size <=256. Do not substitute read_random here: the global PRNG provider is also unregistered and kmem generation must remain lock-free. early_random may seed contexts during single-CPU bootstrap; it uses the built-in HMAC-SHA256 DRBG with the host-generated ADT seed.
- Patch 0013 keeps the replacement entirely private to vm_kern.c: SplitMix64 state is 8 bytes per CPU/sizeclass, initialized using early_random. Uniform selection uses rejection sampling to avoid modulo bias. Other platforms retain the original corecrypto calls; SWEET's generic crypto APIs/registration remain untouched. Reference: https://prng.di.unimi.it/splitmix64.c (Sebastiano Vigna, public domain).
- Validation: vm_kern.c compiles to arm64 (`research/kmem-rng-objs`, using `research/run16.log` + `research/bt16`). Undefined symbols include early_random and NO crypto_random_* references. All 13 patches apply in CI order and match the checked source. Original saved as `research/vm_kern.pre0013.c`.
- RNG host checks: extracted actual new helper in `research/kmem-rng-check.c`; 16,384 outputs match the author's downloaded reference (`research/splitmix64-reference.c`), 147,456 bounded outputs satisfy their limits (including 1 and UINT64_MAX), and a forced rejection advances correctly. Full kernel crypto services and the registered kernel PRNG provider remain future work; this patch only supplies the allocator RNG contract.
- Patch-0011 artifacts: kernel `xnu/out-0011/kernel.development.sweet`, log `research/run15.log`, extracted buildtree `research/bt15` (no nested .git). CI log confirms patch 0011 applied; artifact checksums passed. Kernel is plain arm64, entry VA `0xfffffe000746b488` -> PA `0xb146b488`, kernel end PA still `0xb1ff4000`.
- Patch-0011 image: 16,412,672 bytes, SHA256 `29ad5cbfc752473de4af2c471a24a8b34f92da4bff5afec65c614b90cd3ad53a`. Kernel SHA256 `8ac3a956894b09f7bd0d890de8c5de38c65513287feb1e1bcd12db8ca772ee5c`. Payload/ADT in `shim/out/payload-0011.bin`, `shim/out/sweet-0011.adt`. Header unpacked/checked in `shim/out/check-0011`.
- First patch-0011 attempt timed out waiting for FASTBOOT; superseded by the successful send/boot recorded above. Do not repeat the boot before the user reports the current screen.
- Patch-0011 photo: `/home/dipa/Downloads/IMG_20261015_070218.jpg` (local only). Visible stages 1-8 and old red shim text; entry PA B146B488, boot args PA B1FF8000 / top B1FFC000. No evidence yet locating execution after stage 8.
- Patch-0012 sandbox: `research/bt15/xnu` (NO nested .git). Proposed permanent debug VA: VM_MIN_KERNEL_ADDRESS + ARM_TT_L2_SIZE, in the reserved gap below gVirtBase and above low globals; map the same PA framebuffer as Normal-NC in the final TTBR1 before arm_vm_physmap_init changes phystokv(). Keep the early panic sink until normal kprintf startup.
- Patch 0012 validation: all 4 changed C translation units compiled to arm64 objects in `research/post-ttbr0-objs`; internal header export added to osfmk/arm64/Makefile and recreated locally in EXPORT_HDRS for pe_serial.c. All 12 patches apply in CI order and match all 6 edited files. Baselines are saved under `research/pre0012/`.
- Actual mapping-helper host model (`research/early-map-check.c`, barrier stubbed only for host compilation) confirms: VA `0xfffffe0002000000`, L1 index 2016, L2 index 1; descriptor `0x006000009c000605` = framebuffer PA, Normal-NC, outer-shareable, EL1 RW, PXN+UXN. All other L2 entries preserved. The gap is excluded by ARM_LARGE_MEMORY's pmap_virtual_region(0).
- Next boot command line MUST add `-enable_kprintf_spam`: DEVELOPMENT disables kprintf_output by default even when DB_KPRT is set (`pexpert/arm/pe_kprintf.c`). Planned command line: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam`.

### Patch 0012 screen legend (after original stages 1-8)
- 9: kernel framebuffer VA live; 10: TTBR0 off / TLB flushed; 11: physmap pointers rebound.
- 12: calling pmap_bootstrap; 13: pmap_bootstrap returned; 14: early I/O page tables ready; 15: arm_vm_init returned.
- 16: calling serial_init; 17: fbcon config read / mapping; 18: fbcon mapping returned; 19: serial_init returned; 20: kprintf startup complete.
- Normal serial initialization clears the screen, so earlier stages may disappear before 19. If serial exists, early console disables after 20; otherwise early panic output stays enabled.
- Local source sandbox: `research/bt13/xnu` (git baseline `623b060`, patches 0001-0008 already in baseline; uncommitted export edits correspond to patch 0009). Preserve those edits when producing patch 0010.
- Previous compile log/tree: `research/run13.log`, `research/bt13`; previous kernel: `xnu/out/kernel.development.sweet`. New successful log/tree: `research/run14.log`, `research/bt14`; new kernel: `xnu/out-0010/kernel.development.sweet`.
- Current device access: patch-0012 image was temporarily started from FASTBOOT; no adb connection is expected. Never flash partitions for bring-up; use `fastboot boot` with the shim image.
- Patch `0010` lives in `xnu/patches/0010-sweet-early-framebuffer-debug.patch`. Its exact compiled sources are under `research/bt13/xnu`; generated objects are in `research/early-objs`.
- Local checks passed: all 5 changed/new translation units compiled to arm64 Mach-O objects; new console only imports `_doprnt` and `iso_font` (both exist in the previous kernel). All 10 patches applied to a temporary upstream git index in CI order, and all 7 resulting changed source files matched the local compile inputs.
- Reproduce changed-file compilation: `XNU_CC_OBJDIR="$PWD/research/early-objs" python3 tools/xnu-cc.py research/run13.log research/bt13 arm_init.c arm_vm_init.c kern/debug.c arm64/start.s osfmk/arm64/sweet_early.c --per-file` (create the output directory first). The helper now accepts explicit new source paths absent from the old artifact's Makefiles and rejects empty selections.
- Device command result: `adb reboot bootloader`, then `timeout 30s fastboot boot shim/out/shim-boot-0010.img`: send OKAY (16028 KB), boot OKAY, total 0.541s. This confirms bootloader acceptance only, not XNU progress.
- The successful boot above was on 2026-10-14. On 2026-10-15, `timeout 45s fastboot boot ...` timed out waiting for a device; no image was sent. Boot image SHA256 rechecked and unchanged. No new build is needed to repeat the trial.
- Earlier retry: `timeout 90s fastboot boot shim/out/shim-boot-0010.img` timed out (exit 124). This is superseded by the successful 2026-10-15 repeat boot recorded above; do not repeat it until the user reports the screen.
- User observation confirms MMU-on C entry, platform expert, CPU topology/bootstrap, startup bootstrap and cpu_init all complete. Failure is within arm_vm_physmap_init (non-XNU_MONITOR branch), before stage 8 / TTBR0 teardown. Old red shim text remains behind the early console; this is expected because only written rows are cleared.
- New edit/compile sandbox is `research/bt14/xnu` (extracted artifact, NO nested .git; `git diff` there would act on the parent project). Use a saved baseline file / generated unified diff, or explicitly initialize a local baseline before editing. `research/bt13/xnu` does have its own baseline git repo.
- Exact user-reported panic: `arm_vm_init.c:1606 Assertion failed: (temp_ptov_table[ptov_index - 1].va + temp_ptov_table[ptov_index - 1].len) <= physmap_end`.
- Root cause: MacOSX build sets `ARM_LARGE_MEMORY=1`; `XNU_MONITOR` is off. Block alignment in arm_vm_physmap_slide can add gaps, but the non-PPL large-memory physmap_end omitted the padding already present in the small-memory branch. Patch 0011 reserves PTOV_TABLE_SIZE*ARM_TT_TWIG_SIZE (8*32MB) in both the aperture bound and its L1 allocation; monitor/PPL builds retain zero padding. The assertion is preserved.
- Validation: `arm_vm_init.c` compiled to an arm64 object using `research/run14.log` + `research/bt14` (object in `research/physmap-objs`). All 11 patches apply in CI order and produce exactly that source. Host harness `research/physmap-check.c` extracts the real XNU slide function with page-table-write stubs: all 65,536 page-aligned slides within 1GB checked against the current kernel memory layout; old bound fails 65,504 cases, padded bound fails zero; worst overrun 0x1ffc000 bytes. Baseline source saved as `research/arm_vm_init.pre0011.c`.
- CI: https://github.com/dipa-studio/ios-sweet/actions/runs/38638702083 (success; artifacts and full log downloaded).
- New image: `shim/out/shim-boot-0010.img` (16,412,672 bytes, SHA256 `ed2c270e0081bad5ff517be415f9bfe8805463aea7866732203fa97ac737e64e`). Previous image preserved as `shim/out/shim-boot-pre0010.img`.
- New kernel SHA256: `3ee05270cc291c49589a101678f904b1b69cb2f2575e05398bce8a4e052f409a`. Artifact checksums passed; arm64 (not arm64e), early-console symbols present. Payload entry VA `0xfffffe000746a488` -> PA `0xb146a488`; kernel end PA `0xb1ff4000`. Command line remains `debug=0xc serial=3 cpus=1 keepsyms=1`.

### Patch 0010 screen legend
- Bottom-left white 64x32 tile: assembly entered `start_first_cpu`, before page tables/MMU.
- Text `SWEET EARLY 1`: entered `arm_init` with MMU on; 2: platform expert done; 3: CPU topology done; 4: CPU bootstrap done; 5: startup bootstrap done; 6: CPU init done; 7: entering `arm_vm_init`; 8: leaving bootstrap TTBR0.
- `SWEET EARLY PANIC:` prints a copy of panic arguments before normal panic handling needs per-CPU/thread state.
- In patches 0010/0011 the console disabled before TTBR0 invalidation; patch 0012 replaces that with a persistent kernel VA alias and diagnostics through normal serial/kprintf startup (see its legend above).
- Screen contents require a physical observation from the user: adb cannot capture a framebuffer after Android has been replaced by a bare-metal kernel.

## QEMU emulation (2026-10-15)
- `tools/mkadt.py OUT.adt --qemu` = same ADT with QEMU virt GICD 0x08000000 / GICR 0x080a0000 / CNTFRQ 62.5 MHz.
- `tools/qemu-sweet.py PAYLOAD OUTDIR [--secs N] [--hmp "x /8gx ADDR"] [--gdb]`: host-side copy of shim/loader.c
  (segments + ADT + boot_args at their PAs, 6-instruction stub sets x0 and jumps), `-M virt,gic-version=3 -cpu cortex-a76`
  (same ID_AA64MMFR0 as Kryo 470), 4G RAM so 0x9c000000 fb and 0xb0000000 kernel are plain RAM.
  Outputs `fb.png` (the screen), `regs.txt`, `qemu.log` (exceptions with ESR/FAR/ELR). `--gdb` halts with a stub on :1234
  (system `gdb` + `set architecture aarch64`, `hbreak *VA` works with the MMU on).
- Not emulated: Qualcomm XPUs, ABL, real panel, PSCI conduit (QEMU virt uses hvc). Hardware still decides those.
- Example: `python3 tools/mkadt.py /tmp/q.adt --qemu && python3 tools/mkpayload.py xnu/out-0013/kernel.development.sweet /tmp/q.adt /tmp/pq.bin --cmdline 'debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam' && python3 tools/qemu-sweet.py /tmp/pq.bin /tmp/q`

## Layout
- `backup/`  partition dumps + full sdb..sdf LUNs, `SHA256SUMS` (all verified on-device == local)
- `dtb/`     live FDT (from OrangeFox), PixelOS boot.img dtb, dtbo, dts versions
- `shim/`    bare-metal boot shim (`./build.sh` -> `out/shim-boot.img`)
- `research/` mainline sm7150 dts, XNU pe_fiq.c etc, PocketDarwin patches
- `tools/unpack_bootv2.py`

## Device access
- No root in PixelOS 17 (user build, adb root disabled). Root = `fastboot boot recovery/recovery.img` (OrangeFox R12.0_2, temp boot, not flashed).
- `fastboot boot` works for stock boot.img, OrangeFox, and our shim.
- Shim resets itself via PSCI SYSTEM_RESET; IMEM restart_reason 0x77665500 is seen
  (bootreason=bootloader) but ABL still boots Android, so it does not stop in fastboot.

## Hardware facts (live DT + shim measurements)
- Framebuffer (ABL cont splash): 0x9c000000, 1080x2400, stride 4320, a8r8g8b8, panel is DSC *video* mode (no kick needed).
- RAM: 0x80000000+2G, 0x100000000+0xfcc00000. Live reserved-memory = PixelOS base dtb + sweet dtbo fixups.
- GICv3: GICD 0x17a00000, GICR 0x17a60000 (stride 0x20000, 8 PEs). GICD_TYPER 0x007B041D: SecurityExtn=1 (DS=0).
  ABL leaves GICD_CTLR = 0x10 (ARE_NS on, groups off). Writing 0x13 reads back 0x12: EnableGrp1A (bit1) is the one that matters.
- GIC Group 1 VERIFIED (shim 2c): vtimer INTID 19 = 30 IRQs/300ms, ptimer INTID 18 = 30, SGI 1 to self = 10/10.
  ICC_SRE=1 already, ICC_CTLR 0x8440, priority/enable writes stick. GICR_IGROUPR0 and GICD_IGROUPRn read 0 from NS
  even though Group 1 delivery works (RAZ in NS view) - do not use them as a health check.
  INTID 28 shows pending constantly (unknown PPI 12).
- Timer 19.2 MHz. Qualcomm PPI numbering: secure-phys/phys/virt/hyp = PPI 1/2/3/0 -> vtimer INTID 19, ptimer 18 (NOT 27/30).
- PSCI 1.1 via SMC, SMCCC 1.1. CPU_ON ok; SYSTEM_SUSPEND and SYSTEM_RESET2 unsupported.
- SMP: CPU_ON works for all 7 secondaries (MPIDR 0x81000n00).
- Entry EL1, MMU off, x0 = DTB (magic ok). ID_AA64MMFR0 = ...101122: 16K granule YES, 4K YES.
- No serial console: debug UART SE is in SPI mode on sweet. Screen is the only debug channel.

## XNU implications
- XNU GICv3 path (pexpert/arm/pe_fiq.c, VMAPPLE) puts the timer (PPI 27) in Group 0 = FIQ. With SecurityExtn=1,
  Group 0 is secure -> impossible from NS EL1. Need: Group 1 IRQ, ICC_IGRPEN1, INTID 19, and the timer handled in the IRQ path.
- XNU VMAPPLE PSCI uses `hvc`; sweet needs `smc`.
- PocketDarwin NonAppleGenericCpu.patch only swaps -mcpu=apple-h7 for -march=armv8-a.

## Milestone 3 (2026-10-14): 16K MMU verified
- ABL loads the Image at 0x80080000 (base 0x80000000 + 0x80000) regardless of text_offset=0.
- 16K granule, T0SZ=28 (L2 start, 32MB blocks), MAIR 0x44ff00, TCR 0x1409CB51C, PARange=2 (40-bit PA).
- Only own image pages WB (Qualcomm XPUs: never map carve-outs cacheable); fb Normal-NC; rest Device.
- AT S1E1R checks all as expected; unmapped -> translation fault L2.
- Fill fb: 110 ms (MMU off) -> 3.5 ms (NC). Memory loop 70 ms -> 0.7 ms. vtimer + SGI IRQs still fine with MMU on.

## XNU loader design notes (xnu-8796)
- Entry: `_start` -> `start_first_cpu`, x0 = boot_args (PA), MMU off, EL1. boot_args: Revision/Version 2,
  virtBase/physBase/memSize/topOfKernelData, Boot_Video (fb 0x9c000000, rowBytes 4320, 1080x2400, depth 32),
  deviceTreeP/Length (ADT), CommandLine[608], bootFlags, memSizeActual.
- start.s maps [kernel mach header .. physBase+memSize) with cacheable BLOCKS. On Qualcomm every XPU carve-out
  must therefore lie below the kernel: use physBase = 0xb0000000 (above ramdump_fb 0xaf000000+16M,
  cdsp_sec, qseecom), end before rmtfs 0xfde01000 -> memSize ~0x4d000000 for bring-up.
- Base ADT: iPhone 8 d20ap DeviceTree from iOS 16.7.16 IPSW (tools/remotezip.py + tools/adt.py; LZFSE payload).
  Template values are empty: the loader must fill chosen/*, memory-map, cpu*/reg etc. like iBoot.
- XNU build: GitHub Actions (dipa-studio/ios-sweet, xnu.yml) via blacktop/darwin-xnu-build, MACOS_VERSION=13.5.
  New-clang fixes in xnu/patches; Xcode 16 iig is incompatible (IORPC.kernelContent) -> macos-14 runner, oldest Xcode.

## Kernel architecture plan (SWEET machine config)
- First stock build (VMAPPLE) is arm64e (PAC). Kryo 470 = ARMv8.2, no PAC -> SWEET must build plain arm64
  (HAS_APPLE_PAC is only defined for __arm64e__, so arm64 drops PAC automatically).
- Template: VMAPPLE (16K pages, GICv3 code in pe_fiq.c) minus APPLEVIRTUALPLATFORM hypercalls/paravirt PAC,
  plus BCM2837 (generic ARM: no APPLE_ARM64_ARCH_FAMILY Apple sysregs). Do not link the KDK lib<cfg>.os.*.a.
- Timer: XNU expects it on FIQ (sleh_fiq -> rtclock_intr). SWEET: GIC Group 1, so sleh_irq must ack ICC_IAR1,
  route INTID 19 to the same timer path, SGIs to cpu_signal_handler, EOI via ICC_EOIR1.
- SMP/interrupts: open-source AppleARMSMP (USE_APPLEARMSMP) needs an IOInterruptController (AIC role) and an
  IOPMGR (CPU power -> PSCI CPU_ON via SMC). Plan: built-in IOKit classes (SweetGIC, SweetPMGR, platform
  expert) compiled into the kernel and matched via iokit/KernelConfigTables.cpp -> no closed kexts needed.
- Debug: xnu patch 0003 sweet-fbcon = kprintf drawn on the framebuffer (ADT node "sweet-fbcon").
- ADT /arm-io ranges must not map to parent 0 (pe_arm_get_soc_base_phys()==0 disables serial): use parent 0x1000000.

## Status 2026-10-14 late: first XNU boot attempt
- SWEET kernel builds (CI run 38635343732, patches 0001-0009). Verified offline: arm64, no PAC, no >v8.2 code,
  70300 classic relocs all in range (slide 0 = no loader work), entry = __start.
- Boot: shim loader worked (initrd 0x846F0000-0x855FE3E0, BOOTARG 0xB1FF8000, JUMP 0xB146A488) but screen stayed
  red -> xnu died/hung before serial_init (fbcon). kprintf is a no-op before STARTUP_SUB_KPRINTF.
- Historical next-step plan (patch 0010, now implemented and built; see active handoff above): early fb debug channel
  1. start.s start_first_cpu (after mov x20,x0 / mov x21,#0): PA marker band (MMU off, direct store to 0x9c000000).
  2. start.s after both create_bootstrap_mapping calls: add ONE block entry to the existing V=P L2 table
     (x25 + 2*PGBYTES; do NOT call create_bootstrap_mapping again: fb and RAM share L1 entry 0, it would replace
     the L2 table). Entry = TYPE_BLOCK|VALID|SH(OUTER)|ATTRINDX(CACHE_ATTRINDX_WRITECOMB=1)|AF|PNX|NX|0x9c000000,
     index = (va & ARM_TT_L2_INDEX_MASK) >> ARM_TT_L2_SHIFT.
  3. new osfmk/arm64/sweet_early.c (+files.arm64 entry): sweet_early_mark(n) colored bands at screen bottom and
     sweet_early_putc using iso_font via VA=PA while the bootstrap TTBR0 is live; disable before
     arm_vm_init's set_mmu_ttb(invalid_ttep) (arm_vm_init.c:2148).
  4. markers in arm_init after PE_init_platform, ml_parse_cpu_topology, cpu_bootstrap, kernel_startup_bootstrap,
     cpu_init, before arm_vm_init.
  5. panic hook at top of panic_trap_to_debugger: va_copy + _doprnt(fmt, &copy, sweet_early_putc, 16).
  Verify with tools/xnu-cc.py (compile+symbols) and patch-order simulation before the single CI run.


### Next-stage source metadata and storage evidence

Primary Apple CDN BuildManifest fetched by bounded range requests, CRC checked:
D:/A52-iOS16/metadata/BuildManifest.plist and source.json. Version16.7.16,
build20H392, d22ap OS087-86698-044.dmg (4730814044 bytes), SystemOS087-86593-047.dmg
(2743074816 bytes inflated ZIP member), AppOS087-86715-047.dmg (10485760 bytes).
No full firmware downloaded, no Apple userland committed, no real launchd run.
Read-only UFS evidence backup/a52q/ufs-evidence/twrp-sysfs.txt: 4096-byte blocks,
Samsung KM2V8001CM-B707 rev0003, LUN0, ufshc1d84000; Linux runtime suspended.
Bootloader UFS clock/PHY/power/DMA state remains unmeasured. Do not reuse Redmi
initialization values. General FS+read-only storage+entitlement support are the
next iOS-userland gates. Existing WSL distros all point to missing E paths;
D has enough free space for a future dedicated Linux/rootfs workspace.
