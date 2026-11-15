/* Local measured boot-cache policy; not Apple CMS or general AMFI trust. */
#ifndef A52Q_BOOT_CACHE_POLICY_H
#define A52Q_BOOT_CACHE_POLICY_H
#include <stdint.h>
#include <stddef.h>
#define A52Q_BOOT_CACHE_BYTES 1456980U
#define A52Q_BOOT_CACHE_SIGNATURE_BYTES 19006U
#define A52Q_BOOT_CACHE_HASH_BYTES 20U
#define A52Q_BOOT_CACHE_SELECTOR 6U
static inline int a52q_boot_cache_hash_index(const uint8_t *hash, size_t bytes)
{
    static const uint8_t pins[2][20] = {
        {0x58,0xec,0x4f,0x1a,0x22,0x52,0x06,0x8d,0x88,0x4c,0x5d,0x82,0x30,0x13,0xd6,0xcf,0x73,0xf6,0xac,0x27},
        {0x17,0xf4,0xf2,0xe7,0x48,0x70,0x1d,0x9e,0x2d,0x79,0xec,0x16,0xfd,0xfd,0x96,0xa7,0x6e,0x52,0x8b,0xc2}
    };
    if (!hash || bytes != 20) return -1;
    for (unsigned i=0;i<2;i++) {
        unsigned difference=0;
        for (unsigned j=0;j<20;j++) difference |= hash[j]^pins[i][j];
        if (!difference) return (int)i;
    }
    return -1;
}
static inline int a52q_boot_cache_measurements_match(const uint8_t *code,
    size_t code_bytes, const uint8_t *signature, size_t signature_bytes)
{
    static const uint8_t expected_code[32] = {0x81,0x00,0x70,0x30,0x2b,0x5c,0x4d,0x7c,0x5f,0x00,0xbd,0xc8,0xdf,0x20,0xaa,0xea,0x2d,0xd3,0x3c,0xd8,0x34,0x2d,0x24,0x02,0xfc,0xdf,0x7f,0xf6,0x39,0x7d,0x37,0x4c};
    static const uint8_t expected_signature[32] = {0xd2,0x0a,0x1d,0x31,0x3a,0x2d,0xd8,0xe7,0x79,0x99,0x5c,0xfb,0x9a,0x4e,0x70,0xc6,0x86,0x3d,0xc4,0xce,0xa0,0xee,0x07,0x20,0xc8,0x98,0x7b,0x6b,0xeb,0xcd,0x1e,0x5a};
    if (!code || !signature || code_bytes != A52Q_BOOT_CACHE_BYTES ||
        signature_bytes != A52Q_BOOT_CACHE_SIGNATURE_BYTES) return 0;
    unsigned difference=0;
    for (unsigned i=0;i<32;i++) {
        difference |= code[i]^expected_code[i];
        difference |= signature[i]^expected_signature[i];
    }
    return !difference;
}
static inline int a52q_boot_cache_request_valid(uint32_t selector,
    uint32_t scalar_count, uint64_t scalar, size_t hash_bytes,
    uint32_t output_scalars, size_t output_bytes, int descriptors, int asynchronous)
{
    return selector == A52Q_BOOT_CACHE_SELECTOR && scalar_count == 1 &&
        scalar == 1 && hash_bytes == 20 && !output_scalars && !output_bytes &&
        !descriptors && !asynchronous;
}
#endif
