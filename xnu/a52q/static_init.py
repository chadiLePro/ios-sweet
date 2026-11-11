"""Permit only the pinned entitlement-free diagnostic when AMFI is absent.

This is not an AMFI implementation or an Apple-userland compatibility claim.
Core XNU signature-structure and executable-page hash checks remain in place.
The hash is the SHA256 CodeDirectory cdhash20 of the CI-built A52 diagnostic
from tools/sweet-init.S (-DA52Q_INIT), wrapped without entitlements by mkinit.py.
Changing that executable deliberately requires updating this diagnostic pin.
"""
import hashlib

TARGET = 'bsd/kern/ubc_subr.c'
SOURCE_SHA256 = 'd68ac24f84336aba8f5ee57adc2a40a2614626f1c6bbc9990f3c396a121b499c'
ANCHOR = 'accelerate_entitlement_queries(\n\tstruct cs_blob *cs_blob)\n{\n'
GUARD = '''#if defined(ARM64_BOARD_CONFIG_A52Q)
    if (amfi == NULL) {
        static const unsigned char diagnostic_cdhash[20] = {
            0xa8, 0xa6, 0xba, 0x5e, 0x16, 0x2a, 0x5c, 0x73, 0x96, 0x6e,
            0x22, 0x70, 0x0c, 0x1b, 0xa0, 0xa7, 0x38, 0x6b, 0x35, 0xa2
        };
        /* No entitlements are granted, and no binary is marked platform.
         * This permits only our diagnostic; all other no-AMFI execs fail. */
        if (!(cs_blob->csb_flags & CS_ADHOC) || cs_blob->csb_entitlements ||
            cs_blob->csb_entitlements_blob || cs_blob->csb_der_entitlements_blob ||
            memcmp(cs_blob->csb_cdhash, diagnostic_cdhash, sizeof(diagnostic_cdhash))) {
            printf("A52Q exec: AMFI absent; refusing non-diagnostic or entitled executable\\n");
            return ENOTSUP;
        }
        printf("A52Q exec: pinned entitlement-free diagnostic; no AMFI service\\n");
        return 0;
    }
#endif
'''


def transform(text):
    if hashlib.sha256(text.encode('utf-8')).hexdigest() != SOURCE_SHA256 or text.count(ANCHOR) != 1:
        raise ValueError('static-init source anchor differs')
    return text.replace(ANCHOR, ANCHOR + GUARD)
