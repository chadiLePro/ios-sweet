/* Only these two read-only CDBs can be constructed; no arbitrary command API. */
static int ufs_read_packet(volatile uint32_t *list, volatile uint8_t *request,
    volatile uint32_t *prdt, uint64_t command, uint64_t data,
    unsigned opcode, uint32_t lba, unsigned bytes)
{
    if (!((opcode == 0x25 && lba == 0 && bytes == 8) ||
          (opcode == 0x28 && bytes == 4096)))
        return 0;
    ufs_nop_descriptor(list, command);
    list[0] |= 0x04000000U; /* DEVICE_TO_HOST, never HOST_TO_DEVICE. */
    list[7] |= 1U;
    prdt[0] = (uint32_t)data;
    prdt[1] = (uint32_t)(data >> 32);
    prdt[2] = 0;
    prdt[3] = bytes - 1;
    /* Request area was zeroed: LUN0, tag0, simple task, SCSI command set. */
    request[0] = 1;
    request[1] = 0x40; /* UPIU_CMD_FLAGS_READ. */
    request[12] = (uint8_t)(bytes >> 24);
    request[13] = (uint8_t)(bytes >> 16);
    request[14] = (uint8_t)(bytes >> 8);
    request[15] = (uint8_t)bytes;
    request[16] = (uint8_t)opcode;
    if (opcode == 0x28) {
        request[18] = (uint8_t)(lba >> 24);
        request[19] = (uint8_t)(lba >> 16);
        request[20] = (uint8_t)(lba >> 8);
        request[21] = (uint8_t)lba;
        request[24] = 1; /* Exactly one logical block. */
    }
    return 1;
}
static uint32_t ufs_be32(volatile const uint8_t *p)
{
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
        ((uint32_t)p[2] << 8) | p[3];
}
static uint32_t ufs_data_crc32(volatile const uint8_t *p, unsigned bytes)
{
    uint32_t crc = 0xffffffffU;
    for (unsigned i = 0; i < bytes; i++) {
        crc ^= p[i];
        for (unsigned bit = 0; bit < 8; bit++)
            crc = (crc >> 1) ^ (0xedb88320U & (0U - (crc & 1)));
    }
    return crc ^ 0xffffffffU;
}
