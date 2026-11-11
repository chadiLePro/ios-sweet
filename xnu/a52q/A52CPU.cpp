/* One already-running CPU. No PSCI, secondary entry, suspend or power writes. */
#include <IOKit/IOCPU.h>
#include <IOKit/IOLib.h>
#include <libkern/c++/OSData.h>
#include <libkern/c++/OSNumber.h>
#include <arm64/proc_reg.h>
#include <kern/clock.h>
#include <kern/processor.h>
#include <kern/thread.h>
#include <mach/mach_time.h>
#include <pexpert/pexpert.h>

extern "C" boolean_t sweet_cpu_signal_is_enabled(unsigned int cpu);

class A52CPU : public IOCPU {
    OSDeclareDefaultStructors(A52CPU);
    const OSSymbol *cpuName = NULL;
    uint32_t initialized = 0;
public:
    static void activate(void *arg, wait_result_t result);
    bool start(IOService *provider) APPLE_KEXT_OVERRIDE;
    void free(void) APPLE_KEXT_OVERRIDE;
    void initCPU(bool boot) APPLE_KEXT_OVERRIDE;
    void quiesceCPU(void) APPLE_KEXT_OVERRIDE;
    kern_return_t startCPU(vm_offset_t start_paddr, vm_offset_t arg_paddr) APPLE_KEXT_OVERRIDE;
    void haltCPU(void) APPLE_KEXT_OVERRIDE;
    void signalCPU(IOCPU *target) APPLE_KEXT_OVERRIDE;
    const OSSymbol *getCPUName(void) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(A52CPU, IOCPU);

bool A52CPU::start(IOService *provider)
{
    const ml_topology_info_t *topology = ml_get_topology_info();
    OSNumber *logical = OSDynamicCast(OSNumber, provider->getProperty("logical-cpu-id"));
    OSData *reg = OSDynamicCast(OSData, provider->getProperty("reg"));
    if (topology->num_cpus != 1 || topology->boot_cpu != &topology->cpus[0] ||
        logical == NULL || logical->unsigned32BitValue() != 0 || reg == NULL ||
        reg->getLength() != sizeof(uint32_t)) {
        return false;
    }
    const ml_topology_cpu_t *cpu = topology->boot_cpu;
    if (cpu->cpu_id != 0 || *(const uint32_t *)reg->getBytesNoCopy() != cpu->phys_id ||
        cpu->phys_id != (__builtin_arm_rsr64("MPIDR_EL1") & 0xffff)) {
        panic("A52Q CPU: bootstrap topology disagrees with running CPU");
    }
    if (!IOCPU::start(provider)) {
        return false;
    }
    cpuName = OSSymbol::withCStringNoCopy("A52Q boot CPU");
    if (cpuName == NULL) {
        return false;
    }
    setCPUNumber(0);
    ml_processor_info_t info = {};
    info.cpu_id = reinterpret_cast<cpu_id_t>(this);
    info.phys_id = cpu->phys_id;
    info.log_id = cpu->cpu_id;
    info.cluster_id = cpu->cluster_id;
    info.cluster_type = cpu->cluster_type;
    info.l2_cache_id = cpu->l2_cache_id;
    info.l2_cache_size = cpu->l2_cache_size;
    info.l3_cache_id = cpu->l3_cache_id;
    info.l3_cache_size = cpu->l3_cache_size;
    perfmon_interrupt_handler_func pmi_handler = NULL;
    kern_return_t kr = ml_processor_register(&info, &machProcessor, &ipi_handler, &pmi_handler);
    if (kr != KERN_SUCCESS || pmi_handler != NULL) {
        panic("A52Q CPU: registration failed (%d), or unsupported PMI handler", kr);
    }
    registerService();
    /* Matching must return without waiting for the startup thread. */
    retain();
    thread_t thread;
    kr = kernel_thread_start(&A52CPU::activate, this, &thread);
    if (kr != KERN_SUCCESS) {
        release();
        panic("A52Q CPU: startup thread failed: %d", kr);
    }
    thread_deallocate(thread);
    return true;
}

void A52CPU::activate(void *arg, wait_result_t result __unused)
{
    A52CPU *cpu = static_cast<A52CPU *>(arg);
    kern_return_t kr = processor_start(cpu->machProcessor);
    if (kr != KERN_SUCCESS) {
        panic("A52Q CPU: processor_start failed: %d", kr);
    }
    uint64_t deadline;
    nanoseconds_to_deadline(5 * NSEC_PER_SEC, &deadline);
    while (__atomic_load_n(&cpu->initialized, __ATOMIC_ACQUIRE) == 0 ||
        !sweet_cpu_signal_is_enabled(0)) {
        if (mach_absolute_time() > deadline) {
            panic("A52Q CPU: boot CPU did not receive its self-SGI");
        }
        IOSleep(1);
    }
    ml_cpu_init_completed();
    cpu->cpusRunning();
    IOService::publishResource(gIOAllCPUInitializedKey, kOSBooleanTrue);
    ml_set_max_cpus(1);
    IOLog("A52Q CPU: single boot CPU initialized; self-SGI delivered\n");
    cpu->release();
    thread_terminate(current_thread());
}

void A52CPU::initCPU(bool boot)
{
    if (!boot || cpu_number() != 0) {
        panic("A52Q CPU: unsupported resume or secondary CPU");
    }
    ml_broadcast_cpu_event(CPU_BOOTED, 0);
    signalCPU(this);
    setCPUState(kIOCPUStateRunning);
    __atomic_store_n(&initialized, 1, __ATOMIC_RELEASE);
}

void A52CPU::signalCPU(IOCPU *target)
{
    if (target != this || target->getCPUNumber() != 0 || cpu_number() != 0) {
        panic("A52Q CPU: only self-SGI is implemented");
    }
    /* Architected GICv3 affinity fields, read from this running CPU. */
    uint64_t mpidr = __builtin_arm_rsr64("MPIDR_EL1");
    unsigned int aff0 = mpidr & 0xff;
    if (aff0 >= 16) {
        panic("A52Q CPU: unsupported SGI range selector");
    }
    uint64_t sgi = (((mpidr >> 32) & 0xff) << 48) |
        (((mpidr >> 16) & 0xff) << 32) | (((mpidr >> 8) & 0xff) << 16) |
        ((uint64_t)SWEET_IPI_SGI << 24) | (1ULL << aff0);
    __builtin_arm_dsb(DSB_ISHST);
    __builtin_arm_wsr64("ICC_SGI1R_EL1", sgi);
    __builtin_arm_isb(ISB_SY);
}

kern_return_t A52CPU::startCPU(vm_offset_t start_paddr __unused, vm_offset_t arg_paddr __unused)
{
    panic("A52Q CPU: CPU power-on/restart is not implemented");
}
void A52CPU::quiesceCPU(void) { panic("A52Q CPU: quiesce is not implemented"); }
void A52CPU::haltCPU(void) { panic("A52Q CPU: halt/suspend is not implemented"); }
const OSSymbol *A52CPU::getCPUName(void) { return cpuName; }
void A52CPU::free(void)
{
    OSSafeReleaseNULL(cpuName);
    IOCPU::free();
}
