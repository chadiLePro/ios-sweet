/* A52Q bootstrap platform: CPU nub only; no Apple NVRAM or peripheral claims. */
#include <IOKit/IOPlatformExpert.h>
#include <IOKit/IODeviceTreeSupport.h>
#include <IOKit/IOLib.h>

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
    IOLog("A52Q platform: starting CPU-only platform expert\n");
    if (!IODTPlatformExpert::start(provider)) {
        return false;
    }
    registerService();
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
