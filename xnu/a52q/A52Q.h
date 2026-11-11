/* SM-A525F/DS single-core XNU bootstrap. Values supported by r4 CPU evidence.
 * This is not the Redmi board config: no SWEET macro, SMP, display or storage.
 */
#ifndef _PEXPERT_ARM64_A52Q_H
#define _PEXPERT_ARM64_A52Q_H
#define A52Q 1
#define NO_MONITOR 1
#define NO_ECORE 1
#define ARM_ARCH_TIMER
#define __ARM_ARCH__ 8
#define __ARM_VMSA__ 8
#define __ARM_VFP__ 4
#define __ARM_COHERENT_CACHE__ 1
#define __ARM_DEBUG__ 7
#define __ARM_ENABLE_SWAP__ 1
#define __ARM_V8_CRYPTO_EXTENSIONS__ 1
#define __ARM_PAN_AVAILABLE__ 1
#define __ARM_16K_PG__ 1
#define HAS_GIC_V3 1
#ifndef ASSEMBLER
#define PLATFORM_PANIC_LOG_DISABLED
#endif
/* DT virtual timer: PPI 3 -> INTID 19. These names are shared timer code ABI. */
#define SWEET_VTIMER_INTID 19
#define SWEET_IPI_SGI 1
#define GIC_SPURIOUS_IRQ 1023
#define GICR_PE_SIZE 0x20000
#define GICD_CTLR 0x0
#define GICD_CTLR_ENABLEGRP1 0x1
#define GICD_CTLR_ENABLEGRP1A 0x2
#define GICD_CTLR_ARE_NS 0x10
#define GICD_CTLR_RWP 0x80000000
#define GICR_TYPER 0x08
#define GICR_WAKER 0x14
#define GICR_IGROUPR0 0x10080
#define GICR_ISENABLER0 0x10100
#define GICR_IPRIORITYR0 0x10400
#define GICR_TYPER_AFFINITY_VALUE_SHIFT 32
#define GICR_TYPER_LAST 0x10
#define GICR_WAKER_PROCESSORSLEEP 0x2
#define GICR_WAKER_CHILDRENASLEEP 0x4
#define ICC_CTLR_EOIMODE 0x2
#define ICC_SRE_SRE 0x1
/* Live DT + runtime ramoops + matching board-06 DTBO, documented in A52Q.md. */
#define A52Q_RAMLOG_BASE 0xb4640000
#define A52Q_RAMLOG_SIZE 0x40000
#endif
