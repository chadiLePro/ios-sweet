/* A52Q command-mode splash profile: derived from the CRC-verified physical
 * display-v2 capture, not Redmi constants. Live DT SHA256:
 * 8175ef1d0443676475ea94773484d4fece3a24f8df9cedae71ffabf90e9ab0c8.
 * Only this reserved frame and these already-running register values qualify.
 */
#ifndef A52Q_UI_PROFILE_H
#define A52Q_UI_PROFILE_H
#include <stdint.h>
#include <stddef.h>
struct a52q_ui_guard { uint64_t address; uint32_t value, reserved; };
static const struct a52q_ui_guard a52q_ui_expected[13] = {
    {0xae02014ULL,0x20000U,0},
    {0xae0201cULL,0x0U,0},
    {0xae020f4ULL,0x2U,0},
    {0xae022f4ULL,0x0U,0},
    {0xae024f4ULL,0x0U,0},
    {0xae94004ULL,0x1f5U,0},
    {0xae94008ULL,0x5U,0},
    {0xae05000ULL,0x9600438U,0},
    {0xae05014ULL,0x9c000000U,0},
    {0xae05024ULL,0x10e0U,0},
    {0xae05030ULL,0x237ffU,0},
    {0xae05034ULL,0x3020001U,0},
    {0xae05038ULL,0x80000000U,0},
};
#define A52Q_UI_PHYS 0x9c000000ULL
#define A52Q_UI_BYTES 0x9e4000ULL
#define A52Q_UI_WIDTH 1080U
#define A52Q_UI_HEIGHT 2400U
#define A52Q_UI_STRIDE 4320U
/* DSI_STATUS is transient, not configuration: the pinned Samsung
 * dsi_ctrl_hw_cmn_wait_for_cmd_mode_mdp_idle() waits for bit 2 to clear.
 * V25 observed idle0; the visible RGB test accepted busy5 before START.
 * V27's added idle-wait fails after the first START. Keep both observed states
 * without imposing a clock-change idle precondition on unchanged refreshes.
 * Every other configuration register still matches its captured value.
 */
static inline int a52q_ui_guard_value_matches(unsigned index,uint32_t value)
{
    if (index>=13) return 0;
    return index==6 ? (value==0 || value==5) : value==a52q_ui_expected[index].value;
}
static inline int a52q_ui_profile_matches(const uint64_t reg[2],
    const uint32_t geometry[3], const struct a52q_ui_guard guards[13],
    uint64_t start, uint64_t ram_base, uint64_t ram_size)
{
    if (!reg || !geometry || !guards || reg[0]!=A52Q_UI_PHYS || reg[1]!=A52Q_UI_BYTES ||
        geometry[0]!=A52Q_UI_WIDTH || geometry[1]!=A52Q_UI_HEIGHT || geometry[2]!=A52Q_UI_STRIDE ||
        start!=a52q_ui_expected[1].address || !ram_size || ram_base>UINT64_MAX-ram_size ||
        (reg[0]<ram_base+ram_size && ram_base<reg[0]+reg[1])) return 0;
    for (unsigned i=0;i<13;i++)
        if (guards[i].address!=a52q_ui_expected[i].address ||
            guards[i].value!=a52q_ui_expected[i].value || guards[i].reserved) return 0;
    return 1;
}
#endif
