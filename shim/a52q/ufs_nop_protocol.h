/* Samsung pinned ufshci.h/ufs.h and ufshcd_memory_configure()/NOP preparation.
 * Little-endian UTRD, big-endian UPIU. The all-zero request is NOP OUT/tag0.
 * ALIGNED_UPIU_SIZE is 1024 in this Samsung tree, not a borrowed board value.
 * No PRDT and no SCSI CDB exist in this experiment.
 */
static void ufs_nop_descriptor(volatile uint32_t *list, uint64_t command)
{
    list[0] = 0x11000000U; /* UFS storage command type + interrupt-request flag. */
    list[1] = 0;
    list[2] = 15;          /* OCS_INVALID_COMMAND_STATUS before submission. */
    list[3] = 0;
    list[4] = (uint32_t)command;
    list[5] = (uint32_t)(command >> 32);
    list[6] = (256U << 16) | 256U; /* response: offset1024/4, length1024/4 */
    list[7] = 512U << 16;          /* PRDT offset2048/4; length ZERO. */
}
