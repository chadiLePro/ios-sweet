/* A52Q CPU bootstrap and measured-cache software query; no Apple hardware. */
#include <IOKit/IOPlatformExpert.h>
#include <IOKit/IODeviceTreeSupport.h>
#include <IOKit/IOLib.h>
#include <libkern/c++/OSBoolean.h>
#include <IOKit/IOUserClient.h>
#include <kern/task.h>
#include <kern/task_ref.h>
#include <kern/thread.h>
#include "a52q_boot_cache_policy.h"

extern "C" int a52q_boot_cache_client_allowed(void);
extern "C" int a52q_boot_cache_query(const uint8_t *, size_t);

/* Compatibility name requested by the measured 20H392 loader. This is not
 * Apple's AMFI implementation: only its observed local cache query exists. */
class AppleMobileFileIntegrityUserClient : public IOUserClient {
    OSDeclareDefaultStructors(AppleMobileFileIntegrityUserClient);
    task_t ownerTask = TASK_NULL;
public:
    using IOUserClient::initWithTask;
    bool initWithTask(task_t, void *, UInt32, OSDictionary *) APPLE_KEXT_OVERRIDE;
    void free(void) APPLE_KEXT_OVERRIDE;
    IOReturn clientClose(void) APPLE_KEXT_OVERRIDE;
    IOReturn externalMethod(uint32_t, IOExternalMethodArguments *,
        IOExternalMethodDispatch *, OSObject *, void *) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(AppleMobileFileIntegrityUserClient, IOUserClient);

bool AppleMobileFileIntegrityUserClient::initWithTask(task_t task, void *security,
    UInt32 type, OSDictionary *properties __unused)
{
    if (type != 0 || task == TASK_NULL || task != current_task() ||
        !a52q_boot_cache_client_allowed()) return false;
    /* Ignore caller-supplied properties; no user-controlled dispatch/entitlements. */
    if (!IOUserClient::initWithTask(task, security, type)) return false;
    ownerTask = task;
    task_reference(ownerTask);
    return true;
}

void AppleMobileFileIntegrityUserClient::free(void)
{
    if (ownerTask != TASK_NULL) {
        task_deallocate(ownerTask);
        ownerTask = TASK_NULL;
    }
    IOUserClient::free();
}

IOReturn AppleMobileFileIntegrityUserClient::clientClose(void)
{
    terminate();
    return kIOReturnSuccess;
}

IOReturn AppleMobileFileIntegrityUserClient::externalMethod(uint32_t selector,
    IOExternalMethodArguments *arguments, IOExternalMethodDispatch *dispatch __unused,
    OSObject *target __unused, void *reference __unused)
{
    if (current_task() != ownerTask || !a52q_boot_cache_client_allowed())
        return kIOReturnNotPrivileged;
    if (selector != A52Q_BOOT_CACHE_SELECTOR) return kIOReturnUnsupported;
    if (!arguments || arguments->scalarInputCount != 1 || !arguments->scalarInput ||
        !arguments->structureInput) return kIOReturnBadArgument;
    if (!a52q_boot_cache_request_valid(selector, arguments->scalarInputCount,
        arguments->scalarInput[0], arguments->structureInputSize,
        arguments->scalarOutputCount, arguments->structureOutputSize,
        arguments->structureInputDescriptor != nullptr ||
        arguments->structureOutputDescriptor != nullptr || arguments->structureOutputDescriptorSize != 0,
        arguments->asyncWakePort != MACH_PORT_NULL || arguments->asyncReferenceCount != 0))
        return kIOReturnBadArgument;
    return a52q_boot_cache_query((const uint8_t *)arguments->structureInput,
        arguments->structureInputSize) ? kIOReturnSuccess : kIOReturnNotFound;
}

class AppleMobileFileIntegrity : public IOService {
    OSDeclareDefaultStructors(AppleMobileFileIntegrity);
public:
    IOReturn newUserClient(task_t, void *, UInt32, OSDictionary *, IOUserClient **) APPLE_KEXT_OVERRIDE;
    IOReturn newUserClient(task_t, void *, UInt32, IOUserClient **) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(AppleMobileFileIntegrity, IOService);

IOReturn AppleMobileFileIntegrity::newUserClient(task_t task, void *security,
    UInt32 type, IOUserClient **handler)
{
    return newUserClient(task, security, type, nullptr, handler);
}

IOReturn AppleMobileFileIntegrity::newUserClient(task_t task, void *security,
    UInt32 type, OSDictionary *properties, IOUserClient **handler)
{
    if (!handler) return kIOReturnBadArgument;
    *handler = nullptr;
    if (type != 0) return kIOReturnUnsupported;
    if (task != current_task() || !a52q_boot_cache_client_allowed()) {
        IOLog("A52Q local AMFI: connection identity/owner rejected\n");
        return kIOReturnNotPrivileged;
    }
    AppleMobileFileIntegrityUserClient *client = new AppleMobileFileIntegrityUserClient;
    if (!client) return kIOReturnNoMemory;
    if (!client->initWithTask(task, security, type, properties) || !client->attach(this)) {
        client->release();
        return kIOReturnNotPrivileged;
    }
    if (!client->start(this)) {
        client->detach(this);
        client->release();
        return kIOReturnNoResources;
    }
    *handler = client;
    IOLog("A52Q local AMFI: exact cache-loader connection opened\n");
    return kIOReturnSuccess;
}

/* C AMFI callback bridge. OSBoolean's public singleton API preserves the
 * ownership/type expected by IOUserClient::copyClientEntitlement. This
 * function makes no policy decision; the C caller checks the exact signed
 * mount process, key and actual read-only root before calling it. */
extern "C" void *a52q_copy_bindfs_true(void);
extern "C" void *a52q_copy_bindfs_true(void)
{
    if (!kOSBooleanTrue) return nullptr;
    kOSBooleanTrue->retain();
    return kOSBooleanTrue;
}

class A52PlatformExpert : public IODTPlatformExpert {
    OSDeclareDefaultStructors(A52PlatformExpert);
public:
    bool start(IOService *provider) APPLE_KEXT_OVERRIDE;
    void processTopLevel(IORegistryEntry *root) APPLE_KEXT_OVERRIDE;
    const char *deleteList(void) APPLE_KEXT_OVERRIDE;
    const char *excludeList(void) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(A52PlatformExpert, IODTPlatformExpert);

bool A52PlatformExpert::start(IOService *provider)
{
    IOLog("A52Q platform: starting CPU bootstrap and local cache query\n");
    if (!IODTPlatformExpert::start(provider)) {
        return false;
    }
    registerService();
    AppleMobileFileIntegrity *cacheService = new AppleMobileFileIntegrity;
    if (cacheService) {
        bool attached = false;
        if (cacheService->init() && (attached = cacheService->attach(this)) && cacheService->start(this)) {
            cacheService->setProperty("A52QLocalDevelopment", kOSBooleanTrue);
            cacheService->registerService();
            IOLog("A52Q local AMFI: registered measured boot-cache query only; no Apple validation claim\n");
        } else {
            if (attached) cacheService->detach(this);
            IOLog("A52Q local AMFI: software provider initialization failed\n");
        }
        cacheService->release();
    }
    IOLog("A52Q platform: registered\n");
    return true;
}

const char *A52PlatformExpert::deleteList(void) { return "()"; }
const char *A52PlatformExpert::excludeList(void) { return "('chosen', 'defaults', 'cpus', 'options', 'arm-io', 'pram')"; }

void A52PlatformExpert::processTopLevel(IORegistryEntry *root)
{
    /* createNubs assigns the logical CPU IDs from the parsed topology.
     * GIC/timer are owned by pexpert; publish no unimplemented I/O devices. */
    IORegistryEntry *cpus = root->childFromPath("cpus", gIODTPlane);
    if (cpus == NULL) {
        panic("A52Q platform: missing bootstrap CPU node");
    }
    createNubs(this, IODTFindMatchingEntries(cpus, kIODTExclusive, NULL));
    cpus->release();
}
