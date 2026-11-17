/* Software-only bring-up power profile: never reads Samsung PMIC/SPMI.
 * All values are explicitly synthetic. This does not measure battery safety.
 */
#include <IOKit/pwr_mgt/IOPMPowerSource.h>
#include <IOKit/IOLib.h>
#include <libkern/c++/OSBoolean.h>
#include <libkern/c++/OSSymbol.h>
#include <pexpert/pexpert.h>
class A52DevelopmentPower : public IOPMPowerSource {
    OSDeclareDefaultStructors(A52DevelopmentPower);
public:
    bool start(IOService *provider) APPLE_KEXT_OVERRIDE;
};
OSDefineMetaClassAndStructors(A52DevelopmentPower,IOPMPowerSource);
bool A52DevelopmentPower::start(IOService *provider)
{
    if (!IOPMPowerSource::start(provider)) return false;
    setBatteryInstalled(true);
    setCurrentCapacity(100);setMaxCapacity(100);
    setExternalConnected(true);setExternalChargeCapable(true);
    setIsCharging(false);setAtWarnLevel(false);setAtCriticalLevel(false);
    setTimeRemaining(-1);setCycleCount(0);
    const OSSymbol *full=OSSymbol::withCString("FullyCharged");
    if (full) { setPSProperty(full,kOSBooleanTrue);full->release(); }
    setProperty("A52QDevelopmentPower",kOSBooleanTrue);
    updateStatus();registerService();
    IOLog("A52Q development power: synthetic 100 percent AC profile; no battery measurement\n");
    return true;
}
static void a52q_register_development_power(IOService *platform)
{
    int enabled=0;
    if (!PE_parse_boot_argn("a52q_ui",&enabled,sizeof(enabled)) || enabled!=1) return;
    A52DevelopmentPower *power=new A52DevelopmentPower;
    if (!power) return;
    bool attached=false;
    if (!power->init() || !(attached=power->attach(platform)) || !power->start(platform)) {
        if (attached) power->detach(platform);
        IOLog("A52Q development power: profile registration failed\n");
    }
    power->release();
}
