"""Prepare capacity + one RECOVERY-block read, only after a checked NOP success."""
import hashlib
from a52q_handoff import decode
from a52q_ufs_nop import configuration as nop_configuration


def configuration(evidence, sources, capture_build, console, cpu_log,
                  nop_build, nop_console, geometry):
    config = nop_configuration(evidence, sources, capture_build, console, cpu_log)
    if hashlib.sha256((sources / 'scsi_proto.h').read_bytes()).hexdigest() != 'e603dc7790d9f540b6f9fc2b6c781c817f4c2cbedd730dd55ba5367fffe2c523':
        raise ValueError('SCSI opcode source mismatch')
    checked = decode(nop_console, nop_build['handoff_probe'])
    if (checked.get('stage') != 0xa4 or checked.get('esr') != 0 or
            checked.get('ufs_nop') != {'ocs': 0, 'response_header': 0x20000000, 'doorbell': 0}):
        raise ValueError('need CRC-checked completed NOP/restore from this device')
    if (nop_build.get('ufs_nop') != config):
        raise ValueError('NOP success used different memory/source configuration')
    disk, block = int(geometry['disk_bytes']), int(geometry['logical_block_bytes'])
    start = int(geometry['recovery_start_512_sectors']) * 512
    length = int(geometry['recovery_size_512_sectors']) * 512
    if (geometry.get('phone_writes') is not False or block != 4096 or disk % block or
            not 0 < disk // block <= 0xffffffff or start % block or length < block or
            not 0 < start < start + length <= disk or
            not geometry['scsi_device_path'].endswith('/0:0:0:0')):
        raise ValueError('need bounded LUN0/RECOVERY geometry from TWRP')
    expected_crc = geometry['recovery_first4096_crc32']
    if not isinstance(expected_crc, int) or not 0 <= expected_crc <= 0xffffffff:
        raise ValueError('invalid expected recovery block CRC')
    config.update(scope='READ CAPACITY(10) then one READ(10) of unchanged RECOVERY first block; no write opcode',
                  prior_nop_console_sha256=hashlib.sha256(nop_console).hexdigest(),
                  read_lba=start // block, expected_last_lba=disk // block - 1,
                  expected_block_size=block, expected_read_crc32=expected_crc,
                  baseline_read_sha256=geometry['recovery_first4096_sha256'],
                  data_pool_offset=8192, command_whitelist=[0x25, 0x28],
                  status='prepared read-only experiment; no data sector I/O verified yet')
    return config


def header(config):
    return ''.join(f'#define A52Q_UFS_{name.upper()} {config[name]}U\n' for name in
                   ('read_lba', 'expected_last_lba', 'expected_block_size', 'expected_read_crc32'))
