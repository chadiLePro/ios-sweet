"""Observe fatal A52 process exits; preserve termination and other targets."""

TARGET = 'bsd/kern/kern_exit.c'
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
