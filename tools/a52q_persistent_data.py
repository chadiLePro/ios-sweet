"""Plan a separate persistent var extent. Host-only; no runtime/write approval.

Checks an existing data image against its fsck/copy proof, the preserved root
identity, and captured userdata geometry. Does not create keybags, change GPT,
install an image, enable writes, or claim a kernel mount implementation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import zlib
from a52q_gpt import from_capture
from a52q_hfs_root import validate_volume_headers
from a52q_persistent_root import ROOT_BYTES

DATA_BYTES = 4 << 30
BLOCK_BYTES = 4096
TIMEZONE_SYMLINKS = {
    'db/timezone/zoneinfo': '/usr/share/zoneinfo.default',
}


def validate_timezone_symlinks(links):
    if not isinstance(links, dict) or set(links) != set(TIMEZONE_SYMLINKS):
        raise ValueError('unreviewed timezone seed paths')
    for path, target in TIMEZONE_SYMLINKS.items():
        if links[path] != dict(target=target, uid=0, gid=0):
            raise ValueError('invalid system timezone symlink seed')


def digest_valid(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def inspect_data(path, proof, root_sha256):
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size != DATA_BYTES:
        raise ValueError('data image must be a regular 4 GiB file')
    if (not digest_valid(root_sha256) or proof.get('bytes') != DATA_BYTES or
            proof.get('fsck_passed') is not True or
            proof.get('rsync_checksum_comparison_passed') is not True or
            proof.get('source_subtree') != '/private/var' or
            proof.get('source_master_sha256') != root_sha256):
        raise ValueError('data image needs matching master, completed fsck and copy proof')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        first = stream.read(4096)
        digest.update(first)
        while data := stream.read(1 << 20):
            digest.update(data)
        if stream.tell() != DATA_BYTES:
            raise ValueError('data image changed size while reading')
        stream.seek(DATA_BYTES - 1024)
        alt = stream.read(512)
    if digest.hexdigest() != proof.get('sha256'):
        raise ValueError('data image differs from checked copy')
    volume = validate_volume_headers(first[1024:1536], alt, DATA_BYTES)
    if volume['journaled']:
        raise ValueError('initial data image must be clean and non-journaled')
    result=dict(bytes=DATA_BYTES, sha256=digest.hexdigest(), volume=volume,
                header_crc32=zlib.crc32(first), source_root_sha256=root_sha256)
    if proof.get('seed_files'):
        files=proof['seed_files']
        if set(files)!={'keybags/systembag.kb'}:
            raise ValueError('unreviewed development data seed paths')
        seed=files['keybags/systembag.kb']
        if (not digest_valid(seed.get('sha256')) or not 0<seed.get('bytes',0)<=8192 or
                seed.get('uid')!=0 or seed.get('gid')!=0 or seed.get('mode')!='0600'):
            raise ValueError('invalid development keybag metadata seed')
        result['seed_files']=files
    if 'seed_symlinks' in proof:
        validate_timezone_symlinks(proof['seed_symlinks'])
        result['seed_symlinks']=proof['seed_symlinks']
    return result


def validate_config(config, root):
    parent, parent_count, first, count = config['window']
    rparent, rparent_count, rfirst, rcount = root['window']
    if (config.get('layout_kind') != 'persistent-var-plan-v1' or
            root.get('layout_kind') != 2 or root.get('bytes') != ROOT_BYTES or
            root.get('partition_index') != 31 or root.get('partition_name') != 'userdata' or
            (parent, parent_count) != (rparent, rparent_count) or rfirst != parent or
            rcount != ROOT_BYTES // BLOCK_BYTES or parent < 2 or
            first != parent + rcount or count != DATA_BYTES // BLOCK_BYTES or
            parent_count < rcount + count or first + count > parent + parent_count or
            parent + parent_count > 1 << 32 or config.get('bytes') != DATA_BYTES or
            config.get('offset_in_partition_bytes') != ROOT_BYTES or
            config.get('partition_index') != 31 or config.get('partition_name') != 'userdata' or
            config.get('root_sha256') != root.get('sha256') or
            config.get('source_root_sha256') != root.get('sha256') or
            not digest_valid(config.get('sha256')) or not digest_valid(root.get('sha256')) or
            config.get('gpt_crc32') != root.get('gpt_crc32') or
            config.get('gpt_capture_sha256') != root.get('gpt_capture_sha256') or
            config.get('volume', {}).get('bytes') != DATA_BYTES or
            config.get('volume', {}).get('journaled') is not False or
            config.get('mount_target') != '/private/var' or
            config.get('runtime_implemented') is not False or
            config.get('write_approved') is not False):
        raise ValueError('invalid or overlapping persistent-data plan')
    if 'seed_symlinks' in config:
        validate_timezone_symlinks(config['seed_symlinks'])


def configuration(capture, root, data):
    report = from_capture(capture)
    matches = [p for p in report['partitions'] if p['index'] == 31 and p['name'] == 'userdata']
    if len(matches) != 1 or report['block_bytes'] != BLOCK_BYTES:
        raise ValueError('need the captured 4 KiB userdata partition')
    part = matches[0]
    if (root['window'][:2] != [part['first_lba'], part['block_count']] or
            part['bytes'] != part['block_count'] * BLOCK_BYTES or
            part['first_lba'] + part['block_count'] > report['disk_bytes'] // BLOCK_BYTES or
            hashlib.sha256((capture / 'capture.json').read_bytes()).hexdigest() != root['gpt_capture_sha256']):
        raise ValueError('root and captured partition geometry differ')
    result = dict(data, layout_kind='persistent-var-plan-v1', partition_index=31,
        partition_name='userdata', window=[part['first_lba'], part['block_count'],
            part['first_lba'] + ROOT_BYTES // BLOCK_BYTES, DATA_BYTES // BLOCK_BYTES],
        offset_in_partition_bytes=ROOT_BYTES, root_sha256=root['sha256'],
        gpt_crc32=root['gpt_crc32'], gpt_capture_sha256=root['gpt_capture_sha256'],
        mount_target='/private/var', runtime_implemented=False, write_approved=False,
        scope='host-only layout; no device writes, kernel writable support, keybag or UI claim')
    validate_config(result, root)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('image', 'validation', 'root-plan', 'gpt-capture', 'out'):
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    try:
        if a.out.exists():
            raise ValueError('refuse to replace a prior plan')
        root = json.loads(a.root_plan.read_text())
        data = inspect_data(a.image, json.loads(a.validation.read_text()), root['sha256'])
        plan = configuration(a.gpt_capture, root, data)
        with a.out.open('x', encoding='utf-8') as output:
            output.write(json.dumps(plan, indent=2) + '\n')
        print(json.dumps(plan, indent=2))
    except (OSError, KeyError, TypeError, ValueError) as error:
        p.exit(1, f'Data planning rejected: {error}\n')


def adt_node(config, root, nonce):
    """Bind a planned RO data proxy to the existing candidate UFS nonce."""
    validate_config(config, root)
    if not isinstance(nonce, int) or not 0 < nonce < 1 << 64:
        raise ValueError('invalid data-proxy UFS nonce')
    from mkadt import node, u32, u64
    return node('a52q-ufs-var',[('window',u64(*config['window'])),
        ('ufs-nonce',u64(nonce)),('header-crc32',u32(config['header_crc32']))])


if __name__ == '__main__':
    main()
