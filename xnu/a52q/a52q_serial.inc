/* Poll-only RAM console; uses the verified reserved-region mapping maintained
 * by a52q_early.c. This has no UART, input, interrupt or framebuffer accesses. */
static void a52q_ram_init(void) {}
static unsigned int a52q_ram_tx_ready(void) { return 1; }
static void a52q_ram_tx(uint8_t c) { sweet_early_putc((char)c); }
static unsigned int a52q_ram_rx_ready(void) { return 0; }
static uint8_t a52q_ram_rx(void) { return 0; }
SECURITY_READ_ONLY_LATE(static struct pe_serial_functions) a52q_ram_functions = {
    .init = a52q_ram_init,
    .transmit_ready = a52q_ram_tx_ready,
    .transmit_data = a52q_ram_tx,
    .receive_ready = a52q_ram_rx_ready,
    .receive_data = a52q_ram_rx,
    .has_irq = false,
    .device = (serial_device_t)0x40
};
