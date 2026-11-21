"""Observe fatal A52 process exits; preserve termination and other targets."""

TARGET = 'bsd/kern/kern_exit.c'
HEADER = '#include <kern/thread_call.h>'
REGISTERS = '''
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <arm/thread.h>
#include <vm/vm_shared_region.h>
/* V26: actual SpringBoard SIGTRAP needs the cache slide and return PC.
 * Read saved state only, never walk/dereference user stacks during exit. */
static void a52q_crash_registers(proc_t p)
{
    if (strcmp(p->p_comm,"SpringBoard") && strcmp(p->p_comm,"logd") &&
        strcmp(p->p_comm,"mediaserverd")) return;
    arm_saved_state_t *ss=find_user_regs(current_thread());
    if (!ss || !is_saved_state64(ss)) return;
    task_t task=current_task();uint64_t slide=0;
    vm_shared_region_t sr=vm_shared_region_get(task);
    if (sr) {slide=sr->sr_slide;vm_shared_region_deallocate(sr);}
    char body[240];
    int n=snprintf(body,sizeof(body),"%d/%.16s/%016llx/%016llx/%016llx/%016llx/%016llx/%016llx",
        proc_getpid(p),p->p_comm,(unsigned long long)slide,
        (unsigned long long)task->mach_header_vm_address,
        (unsigned long long)get_saved_state_pc(ss),(unsigned long long)get_saved_state_lr(ss),
        (unsigned long long)get_saved_state_sp(ss),(unsigned long long)get_saved_state_fp(ss));
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    for (unsigned i=0;i<3;i++) printf("A52CR1 %s %08x\\n",body,crc^0xffffffffU);
}
#endif
'''
ANCHOR = '''#if defined(ARM64_BOARD_CONFIG_SWEET)
		if (p == current_proc()) {
			a52q_crash_registers(p);
			extern void sweet_crash_log(const char *, int, int, uint64_t, uint64_t);'''
TRACE = '''#if defined(ARM64_BOARD_CONFIG_A52Q)
		/* V17: the required cache-loader child aborts, but var/crash logs are
		 * unavailable on the read-only root. Observe the existing fatal-exit
		 * context before corpse notification; do not change the exit reason,
		 * signal, code-signing status or crash-report decision. Three bounded
		 * copies improve retention in the existing unprotected text stream. */
		if (p == current_proc()) {
			for (unsigned copy = 1; copy <= 3; copy++) {
				printf("A52Q crash[%u]: pid=%d comm=%.16s signal=%d exception=%u code=0x%llx subcode=0x%llx\\n",
				    copy, proc_getpid(p), p->p_comm, WTERMSIG(rv),
				    (unsigned)ut->uu_exception, (unsigned long long)ut->uu_code,
				    (unsigned long long)ut->uu_subcode);
				if (PROC_HAS_EXITREASON(p)) {
					const char *desc = exit_reason_get_string_desc(p->p_exit_reason);
					printf("A52Q crash reason[%u]: ns=%u code=0x%llx desc=%.192s\\n",
					    copy, p->p_exit_reason->osr_namespace,
					    (unsigned long long)p->p_exit_reason->osr_code,
					    desc != NULL ? desc : "(none)");
				} else {
					printf("A52Q crash reason[%u]: unavailable\\n", copy);
				}
			}
		}
#endif
'''


def transform(text):
    if text.count(ANCHOR) != 1 or text.count(HEADER)!=1 or TRACE in text:
        raise ValueError('unexpected fatal-exit source or trace already applied')
    return text.replace(HEADER,HEADER+REGISTERS,1).replace(ANCHOR, TRACE + ANCHOR, 1)
