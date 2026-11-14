/* Minimal bring-up interface for XNU's unconditional AMFI query callers.
 * No entitlements, platform binaries, trust caches or Apple validation service.
 * Diagnostic mode permits only our exact entitlement-free ad-hoc init.
 * The separate full UFS root may also attempt the two audited 20H392 launch
 * executables below. Their entitlements remain unavailable and queries fail;
 * this is an experimental hash allowlist, not Apple's AMFI/trust service.
 * Core XNU signature structure and executable-page hashes remain checked.
 */
#include <kern/debug.h>
#include <kern/startup.h>
#include <libkern/amfi/amfi.h>
#include <mach/kern_return.h>
#include <sys/codesign.h>
#include <sys/proc.h>
#include <sys/systm.h>
#include <sys/ubc_internal.h>

static void a52q_ent_invalidate(void *ent)
{
    if (ent != NULL) {
        panic("A52Q diagnostic AMFI: unexpected entitlements object");
    }
}
static void *a52q_ent_dict(void *ent __unused) { return NULL; }
static CEError_t a52q_ent_query(void *ent __unused, uint8_t hash[CS_CDHASH_LEN] __unused,
    CEQuery_t query __unused, size_t length __unused)
{
    panic("A52Q diagnostic AMFI: CoreEntitlements queries unsupported");
}
static bool a52q_ent_blob(void *ent __unused, const CS_GenericBlob **blob)
{
    if (blob != NULL) {
        *blob = NULL;
    }
    return false;
}
static bool a52q_ent_xml(void *ent __unused, CS_GenericBlob **blob)
{
    if (blob != NULL) {
        *blob = NULL;
    }
    return false;
}
static bool a52q_no_profile(const uint8_t **profile __unused, size_t *length __unused) { return false; }
static bool a52q_no_udid(const uint8_t **udid __unused, size_t *length __unused) { return false; }
static void *a52q_no_context(CEQueryContext_t context __unused)
{
    panic("A52Q diagnostic AMFI: query contexts unsupported");
}
static kern_return_t a52q_with_monitor(void *ent __unused, const CEQueryContext_t context __unused,
    const void *object __unused, const char *identity __unused, uint32_t flags __unused)
{
    return KERN_NOT_SUPPORTED;
}
static kern_return_t a52q_without_monitor(void *ent, struct cs_blob *blob)
{
    extern int a52q_ufs_root_named(const char *name);
    /* SHA256 CodeDirectory cdhash20, extracted from the validated full master.
     * launchd file SHA256 12370e5e...cac61c; dyld 58068345...33757.
     * Host audit verified every executable-page hash. CMS trust is NOT claimed.
     * Core XNU continues checking CodeDirectory structure, special slots and
     * executable pages. No global CS_VALID/platform/entitlement bypass. */
    static const uint8_t apple_pins[2][CS_CDHASH_LEN] = {
        {0xb6,0x5c,0x36,0xc9,0xf5,0xb2,0x87,0xa6,0xa8,0xf5,
         0xca,0x83,0xd9,0x42,0x7f,0xb5,0x5e,0xf0,0x4f,0x4e},
        {0x68,0x4d,0x84,0x7c,0x40,0xe6,0xe8,0x73,0xee,0xae,
         0xc6,0x93,0x01,0x1d,0x4d,0x99,0x7a,0x86,0x9d,0x2a}
    };
    if (blob && !ent && a52q_ufs_root_named("a52ios0")) {
        for (unsigned i = 0; i < 2; i++) {
            if (!memcmp(blob->csb_cdhash, apple_pins[i], CS_CDHASH_LEN)) {
                printf("A52Q exec policy: pinned 20H392 %s accepted; entitlements UNAVAILABLE, not an execution proof\n",
                    i ? "dyld" : "launchd");
                return KERN_SUCCESS;
            }
        }
    }
    static const uint8_t pin[CS_CDHASH_LEN] = {
        0xa8, 0xa6, 0xba, 0x5e, 0x16, 0x2a, 0x5c, 0x73, 0x96, 0x6e,
        0x22, 0x70, 0x0c, 0x1b, 0xa0, 0xa7, 0x38, 0x6b, 0x35, 0xa2
    };
    if (blob == NULL || ent != NULL || !(blob->csb_flags & CS_ADHOC) ||
        blob->csb_entitlements || blob->csb_entitlements_blob || blob->csb_der_entitlements_blob ||
        memcmp(blob->csb_cdhash, pin, sizeof(pin))) {
        return KERN_DENIED;
    }
    printf("A52Q AMFI diagnostic: pinned init signature, no entitlements\n");
    return KERN_SUCCESS;
}
static kern_return_t a52q_bool(const void *ent __unused, const char *name __unused) { return KERN_DENIED; }
static kern_return_t a52q_bool_proc(proc_t proc __unused, const char *name __unused) { return KERN_DENIED; }
static kern_return_t a52q_string(const void *ent __unused, const char *name __unused,
    const char *value __unused) { return KERN_DENIED; }
static kern_return_t a52q_string_proc(proc_t proc __unused, const char *name __unused,
    const char *value __unused) { return KERN_DENIED; }
static kern_return_t a52q_object(const void *ent __unused, const char *name __unused, void **object)
{
    if (object != NULL) {
        *object = NULL;
    }
    return KERN_NOT_FOUND;
}
static kern_return_t a52q_object_proc(proc_t proc __unused, const char *name, void **object)
{
    return a52q_object(NULL, name, object);
}
static const amfi_t a52q_diagnostic_amfi = {
    .OSEntitlements_invalidate = a52q_ent_invalidate,
    .OSEntitlements_asdict = a52q_ent_dict,
    .OSEntitlements_query = a52q_ent_query,
    .OSEntitlements_get_transmuted = a52q_ent_blob,
    .OSEntitlements_get_xml = a52q_ent_xml,
    .get_legacy_profile_exemptions = a52q_no_profile,
    .get_udid = a52q_no_udid,
    .query_context_to_object = a52q_no_context,
    .OSEntitlements = {
        .version = OSENTITLEMENTS_INTERFACE_VERSION,
        .adjustContextWithMonitor = a52q_with_monitor,
        .adjustContextWithoutMonitor = a52q_without_monitor,
        .queryEntitlementBoolean = a52q_bool,
        .queryEntitlementBooleanWithProc = a52q_bool_proc,
        .queryEntitlementString = a52q_string,
        .queryEntitlementStringWithProc = a52q_string_proc,
        .copyEntitlementAsOSObject = a52q_object,
        .copyEntitlementAsOSObjectWithProc = a52q_object_proc,
    },
};
__startup_func static void a52q_register_diagnostic_amfi(void)
{
    amfi_interface_register(&a52q_diagnostic_amfi);
    printf("A52Q AMFI diagnostic interface registered: no entitlements or platform status\n");
}
STARTUP(EARLY_BOOT, STARTUP_RANK_MIDDLE, a52q_register_diagnostic_amfi);
