"""Observe fatal A52 process exits; preserve termination and other targets."""

TARGET = 'bsd/kern/kern_exit.c'
REGISTER_TARGET = 'osfmk/kern/exception.c'
REGISTER_ANCHOR = '#if defined(ARM64_BOARD_CONFIG_SWEET)\n#include <vm/vm_shared_region.h>'
REGISTERS = '''
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <arm/thread.h>
#include <vm/vm_shared_region.h>
#include <arm64/a52q_fb_console.h>
/* A short checked-copy frame walk follows the upstream SWEET crash mechanism.
 * Only backboardd needs the caller chain beyond pthread_kill. */
static void a52q_backboard_stack(arm_saved_state_t *ss, uint64_t slide,
    uint64_t main_header, int pid)
{
    uint64_t pcs[16], frame[2];
    unsigned count=2;
    pcs[0]=get_saved_state_pc(ss);pcs[1]=get_saved_state_lr(ss);
    uint64_t sp=get_saved_state_sp(ss),fp=get_saved_state_fp(ss);
    while (count<16 && fp>=sp && fp-sp<=65536-sizeof(frame) && !(fp&15)) {
        if (copyin((user_addr_t)fp,frame,sizeof(frame))) break;
        pcs[count++]=frame[1];
        if (frame[0]<=fp) break;
        fp=frame[0];
    }
    char body[208],line[240];
    int n=snprintf(body,sizeof(body),"%d/backboardd/%llx/%llx",pid,
        (unsigned long long)slide,(unsigned long long)main_header);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    for (unsigned i=0;i<count;i++) {
        int added=snprintf(body+n,sizeof(body)-(unsigned)n,"/%llx",(unsigned long long)pcs[i]);
        if (added<=0 || (unsigned)added>=sizeof(body)-(unsigned)n) {body[n]=0;break;}
        n+=added;
    }
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    n=snprintf(line,sizeof(line),"A52BT1 %s %08x\\n",body,crc^0xffffffffU);
    if (n<=0 || (unsigned)n>=sizeof(line)) return;
    a52q_early_critical(line,(unsigned)n,7);
    for (unsigned i=0;i<3;i++) printf("%s",line);
}
void a52q_crash_registers(const char *name, int pid);
void a52q_crash_registers(const char *name, int pid)
{
    if (!name || (strcmp(name,"SpringBoard") && strcmp(name,"backboardd") && strcmp(name,"logd") &&
        strcmp(name,"mediaserverd"))) return;
    arm_saved_state_t *ss=find_user_regs(current_thread());
    if (!ss || !is_saved_state64(ss)) return;
    task_t task=current_task();uint64_t slide=0;
    vm_shared_region_t sr=vm_shared_region_get(task);
    if (sr) {slide=sr->sr_slide;vm_shared_region_deallocate(sr);}
    char body[240];
    int n=snprintf(body,sizeof(body),"%d/%.16s/%016llx/%016llx/%016llx/%016llx/%016llx/%016llx",
        pid,name,(unsigned long long)slide,
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
    char line[240];
    n=snprintf(line,sizeof(line),"A52CR1 %s %08x\\n",body,crc^0xffffffffU);
    if (n>0 && (unsigned)n<sizeof(line) &&
        (!strcmp(name,"SpringBoard") || !strcmp(name,"backboardd")))
        a52q_early_critical(line,(unsigned)n,!strcmp(name,"SpringBoard") ? 6 : 7);
    if (!strcmp(name,"backboardd"))
        a52q_backboard_stack(ss,slide,task->mach_header_vm_address,pid);
}
#endif
'''
ANCHOR = '''#if defined(ARM64_BOARD_CONFIG_SWEET)
		if (p == current_proc()) {
			extern void sweet_crash_log(const char *, int, int, uint64_t, uint64_t);'''
TRACE = '''#if defined(ARM64_BOARD_CONFIG_A52Q)
		/* V17: the required cache-loader child aborts, but var/crash logs are
		 * unavailable on the read-only root. Observe the existing fatal-exit
		 * context before corpse notification; do not change the exit reason,
		 * signal, code-signing status or crash-report decision. Three bounded
		 * copies improve retention in the existing unprotected text stream. */
		if (p == current_proc()) {
			extern void a52q_crash_registers(const char *, int);
			a52q_crash_registers(p->p_comm, proc_getpid(p));
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
    if text.count(ANCHOR) != 1 or TRACE in text:
        raise ValueError('unexpected fatal-exit source or trace already applied')
    return text.replace(ANCHOR, TRACE + ANCHOR, 1)

def exception(text):
    if text.count(REGISTER_ANCHOR)!=1 or REGISTERS in text:
        raise ValueError('unexpected Mach exception source or trace already applied')
    return text.replace(REGISTER_ANCHOR,REGISTERS+REGISTER_ANCHOR,1)
