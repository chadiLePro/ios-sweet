# Guarded A52 bitmap console

The saved idle-status/zoneinfo candidate completed full HFS compilation, a
90-file source-archive check, diagnostic QEMU, preserved-master rehash and BOOT
packaging. It was not installed. The combined console build now also passed:
HFS run44916663730, hostCI44916653849 (147tests),95 archived source hashes,
exact-kernel diagnostic QEMU (3 entry records,13 diagnostic PID1 heartbeats),
preserved-master rehash and independently checked BOOT packaging. The QEMU
fixture does not exercise Samsung display/UFS hardware or Apple userland.
V26 installed and verified the timezone seed, then temporarily booted the
combined BOOT. Original BOOT was restored and independently hash-verified.
The operator saw no text. CRC records show adapter preparation, one completed
START submission, then a runtime flush failure. These are separate observations.
The timezone task progressed to EarlyBootComplete; the retained 256 KiB log then
captured SpringBoard SIGTRAP and UserEventAgent's low-space IO policy abort.
The complete five-minute userland run was not retained because the log filled.

The follow-up adds a CRC guard index/value or START timeout reason on runtime
flush failure, preserving every guard and the quiet panic path. Saved PC/LR and
shared-cache slide are recorded with CRC for SpringBoard, logd and mediaserverd;
no user stack is dereferenced and termination behavior stays intact.
The register helper lives in the Mach exception translation unit, where task
and shared-region private definitions are available. BSD calls a typed name/PID
entry; it does not dereference those opaque types.
UserEventAgent's exact original signed low-space Boolean is exposed through the
existing AMFI query callbacks only after catalog/platform checks and a full
84,016-byte SHA-256 of its read-only root vnode. All 15 code pages and signed
XML/DER hashes were checked against the pristine master. This capability affects
an IO policy bit; storage stays read-only. Other keys and binaries remain denied.
The 2,786-entry catalog is unchanged. A new phone trial is needed to establish
the display failure and crash callers.

The opt-in `--text-console` payload flag requires the guarded hardware UI profile,
a compiled renderer marker, and the exact `a52q_text_console=1` boot argument.
The physical buffer remains 0x9c000000/0x9e4000, 1080x2400, stride 4320, BGRA.
No new early framebuffer mapping, panel commands, clock writes, RAM exclusions,
UFS code, code-catalog entries or KeyStore behavior are introduced.

The existing XNU `iso_font` supplies 8x16 glyphs, drawn at 2x in 16x32 cells:
67 columns, one banner row and 74 scrolling body rows. Text is white on black.
The right eight pixels stay black. The viewport scrolls with a circular text
grid; no unbounded string parsing or frame allocation is needed.

Every original pstore byte is written first. A transform appends a mirror call
after that write and does not alter the persistent-buffer implementation.
The mirror queues up to 16 KiB using a try-lock, with no allocation, printing,
waiting or MMIO. Early text is replayed only after the existing display adapter
has checked the captured registers and mapped the reserved frame. Overflow
replaces oldest queued characters; a reentrant producer drops its mirror byte.
Those losses do not suppress the original pstore output.

The existing framebuffer workloop drains the queue and refreshes dirty text at
at most 10 Hz, using the already bounded guarded START operation. This is a text
refresh rate, not a new assertion about physical panel Hz. A panic requests a
bounded best-effort drain if the console owns a valid mapping. Panic refresh
uses a quiet path with no logging, avoiding printf/console locks. It never waits
for a preempted renderer or reclaims a GUI-owned display; pstore remains the
recovery channel when direct drawing is unsafe or unavailable.

Exporting the default physical surface requests permanent console handoff before
its port is exposed to userland. `IOWorkLoop::runAction` serializes this with the
timer renderer, so a process cannot write through the shared mapping during a
console draw. Presentation checks ownership too; if a concurrent panic draw is
busy, the presenter requeues its existing frame. Kernel and console logging keeps
reaching pstore after handoff. Handoff is not proof of backboardd, a composed
frame, or a visible SpringBoard lock screen.

Only the existing console stream is mirrored. This includes the launchd output
already observed in pstore. Logs emitted exclusively to files or private Apple
os_log buffers need their own functioning collection services; this renderer
does not synthesize them or bypass daemon startup.

Files changed for this feature:

- `xnu/a52q/a52q_fb_console.c`, `.h`: bounded queue, refresh and ownership.
- `xnu/a52q/a52q_text_grid.h`: scrolling grid and checked bitmap renderer.
- `xnu/a52q/text_console.py`: preserves the pstore body, appends mirror/panic hooks.
- `xnu/a52q/apply.py`: source/header staging and build integration.
- `xnu/a52q/a52q_ui_bridge.c`: starts text only after guarded mapping succeeds.
- `xnu/a52q/software_ui.py`: timer consumption and presentation handoff.
- `tools/a52q_payload.py`, `a52q_ui_profile.py`: explicit opt-in/binding checks.
- `tools/relink_a52q_console.py`: rejects stale single-leaf archive reuse.
- `tests/test_a52q_fb_console.py`, `test_a52q_ui_guard_runtime.py`,
  `test_a52q_ui_profile.py`: native bounds, backpressure, handoff and payload checks.

Host tests, kernel compile/link, diagnostic emulation, visible boot text, actual
Apple service startup and a rendered lock screen are separate milestones.

V27 host validation completed on source18c6d78: full HFS build44939199104,
hostCI44939190163 (150tests),96 archived source hashes, exact-kernel diagnostic
QEMU (3 entry records and13 diagnostic PID1 heartbeats), preserved master rehash
and independent BOOT validation. BOOT SHA256 is
203155dbee765f9ae80d4596924f79547e11e00ad3d5027259d83e2ecc6da009.
The candidate is unflashed. UserEventAgent behavior, the display runtime failure
and SpringBoard remain subject to the next physical trial. The optional noisy
cs_debug=2 argument is omitted; signature enforcement and console logging remain.

V27 was subsequently tested and restored. No text was visible. Its new failure
record proves the extra DSI-idle wait stalled with status5 after the first START.
The next correction follows the already visible RGB diagnostic's unchanged
refresh operation: validate the observed0/5 states, then bound START completion,
without a clock-change idle wait. All configuration pins remain enforced.
The saved crash registers locate SpringBoard's FrontBoardServices assertion
about an unavailable main CADisplay. Its assertion and the GUI result remain
unmodified and subject to the next hardware test. See the detailed evidence in
`A52Q-DEVELOPMENT-UI.md`.
