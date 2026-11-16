/* A52Q CPU bootstrap and measured-cache software query; no Apple hardware. */
#include <IOKit/IOPlatformExpert.h>
#include <IOKit/IODeviceTreeSupport.h>
#include <IOKit/IOLib.h>
#include <libkern/c++/OSBoolean.h>
#include <IOKit/IOUserClient.h>
#include <kern/task.h>
#include <kern/task_ref.h>
#include <kern/thread.h>
#include <sys/proc.h>
#include <pexpert/pexpert.h>
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

/* A52Q_EMPTY_KEYSTORE_BEGIN
 * V22: keybagd cannot discover AppleKeyStore. This empty discovery probe lets
 * its real no-bag path run. It is NOT an unlocked bag, keychain or SEP emulator.
 * No file, key, bag handle, lock state or crypto operation is implemented.
 */
static IOReturn
a52q_aks_probe_request(uint32_t selector, IOExternalMethodArguments *a,
    bool owner, unsigned *state)
{
    if (!owner) return kIOReturnNotPrivileged;
    if (selector != 0 && selector != 14) return kIOReturnUnsupported;
    if (!a || a->version != kIOExternalMethodArgumentsCurrentVersion ||
        a->asyncWakePort != MACH_PORT_NULL || a->asyncReferenceCount ||
        a->structureInputSize || a->structureOutputSize ||
        a->structureInputDescriptor || a->structureOutputDescriptor ||
        a->structureOutputDescriptorSize || a->structureVariableOutputData ||
        a->scalarInputCount) return kIOReturnBadArgument;
    if (selector == 0) {
        if (a->scalarOutputCount) return kIOReturnBadArgument;
        unsigned expected = 0;
        if (!__atomic_compare_exchange_n(state, &expected, 1U, false,
            __ATOMIC_ACQ_REL, __ATOMIC_ACQUIRE)) return kIOReturnNotOpen;
        return kIOReturnSuccess; /* Only an actual per-connection handshake. */
    }
    if (a->scalarOutputCount != 1 || !a->scalarOutput) return kIOReturnBadArgument;
    if (__atomic_load_n(state, __ATOMIC_ACQUIRE) != 1) return kIOReturnNotOpen;
    /* Leave output handle untouched: no bag exists and none was loaded. */
    return kIOReturnNotFound;
}

static void
a52q_aks_probe_trace(uint32_t selector, IOReturn result)
{
    char name[32];
    proc_selfname(name, sizeof(name));
    if (strcmp(name, "keybagd")) return;
    static unsigned events;
    unsigned sequence = __atomic_fetch_add(&events, 1U, __ATOMIC_RELAXED) + 1U;
    if (sequence > 80) return;
    char body[120];
    snprintf(body, sizeof(body), "aks/%u selector=%u result=0x%08x bag=absent",
        sequence, selector, (unsigned)result);
    uint32_t crc = 0xffffffffU;
    for (unsigned i = 0; body[i]; i++) {
        crc ^= (uint8_t)body[i];
        for (unsigned bit = 0; bit < 8; bit++)
            crc = (crc >> 1) ^ (0xedb88320U & (0U - (crc & 1)));
    }
    for (unsigned copy = 0; copy < 3; copy++)
        IOLog("A52KB1 %s %08x\n", body, crc ^ 0xffffffffU);
}

class A52EmptyKeyStoreUserClient : public IOUserClient {
    OSDeclareDefaultStructors(A52EmptyKeyStoreUserClient);
    task_t ownerTask = TASK_NULL;
    unsigned sessionState = 0; /* fresh/open/closed; never a bag handle */
public:
    using IOUserClient::initWithTask;
    bool initWithTask(task_t, void *, UInt32, OSDictionary *) APPLE_KEXT_OVERRIDE;
    void free(void) APPLE_KEXT_OVERRIDE;
    IOReturn clientClose(void) APPLE_KEXT_OVERRIDE;
    IOReturn externalMethod(uint32_t, IOExternalMethodArguments *,
        IOExternalMethodDispatch *, OSObject *, void *) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(A52EmptyKeyStoreUserClient, IOUserClient);

bool A52EmptyKeyStoreUserClient::initWithTask(task_t task, void *security,
    UInt32 type, OSDictionary *properties __unused)
{
    if (type || task == TASK_NULL || task != current_task()) return false;
    if (!IOUserClient::initWithTask(task, security, type)) return false;
    ownerTask = task;
    task_reference(ownerTask);
    return true;
}

void A52EmptyKeyStoreUserClient::free(void)
{
    if (ownerTask != TASK_NULL) {
        task_deallocate(ownerTask);
        ownerTask = TASK_NULL;
    }
    IOUserClient::free();
}

IOReturn A52EmptyKeyStoreUserClient::clientClose(void)
{
    __atomic_store_n(&sessionState, 2U, __ATOMIC_RELEASE);
    terminate();
    return kIOReturnSuccess;
}

IOReturn A52EmptyKeyStoreUserClient::externalMethod(uint32_t selector,
    IOExternalMethodArguments *a, IOExternalMethodDispatch *dispatch __unused,
    OSObject *target __unused, void *reference __unused)
{
    IOReturn result = a52q_aks_probe_request(selector, a,
        ownerTask != TASK_NULL && current_task() == ownerTask, &sessionState);
    a52q_aks_probe_trace(selector, result);
    return result;
}

/* Matching compatibility name only. No Apple hardware is claimed. */
class AppleKeyStore : public IOService {
    OSDeclareDefaultStructors(AppleKeyStore);
public:
    IOReturn newUserClient(task_t, void *, UInt32, OSDictionary *, IOUserClient **) APPLE_KEXT_OVERRIDE;
    IOReturn newUserClient(task_t, void *, UInt32, IOUserClient **) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(AppleKeyStore, IOService);

IOReturn AppleKeyStore::newUserClient(task_t task, void *security,
    UInt32 type, IOUserClient **handler)
{
    return newUserClient(task, security, type, nullptr, handler);
}

IOReturn AppleKeyStore::newUserClient(task_t task, void *security,
    UInt32 type, OSDictionary *properties, IOUserClient **handler)
{
    if (!handler) return kIOReturnBadArgument;
    *handler = nullptr;
    if (type) return kIOReturnUnsupported;
    if (task == TASK_NULL || task != current_task()) return kIOReturnNotPrivileged;
    A52EmptyKeyStoreUserClient *client = new A52EmptyKeyStoreUserClient;
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
    return kIOReturnSuccess;
}

static void
a52q_aks_probe_register(IOService *platform)
{
    char root[32] = {0};
    if (!PE_parse_boot_argn("rd", root, sizeof(root))) return;
    root[sizeof(root) - 1] = '\0';
    if (strcmp(root, "a52ios0")) return; /* No provider for diagnostic RAM roots. */
    AppleKeyStore *probe = new AppleKeyStore;
    if (!probe) return;
    bool attached = false;
    if (probe->init() && (attached = probe->attach(platform)) && probe->start(platform)) {
        probe->setProperty("A52QEmptyKeyStoreProbe", kOSBooleanTrue);
        probe->registerService();
        IOLog("A52Q KeyStore: empty discovery probe registered; no keybags or crypto\n");
    } else {
        if (attached) probe->detach(platform);
        IOLog("A52Q KeyStore: empty discovery probe registration failed\n");
    }
    probe->release();
}
/* A52Q_EMPTY_KEYSTORE_END */

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
    a52q_aks_probe_register(this);
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
