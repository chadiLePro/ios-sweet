/* Filesystem-table compatibility for the unchanged 20H392 Libinfo consumer.
 * Despite the sysctl namespace, this describes HFS; it implements no APFS API.
 * See docs/A52Q-BOOT-FILESYSTEM.md for the measured wire offsets and guards.
 */
#include <sys/sysctl.h>
#include <sys/mount.h>
#include <sys/vnode.h>
#include <sys/systm.h>
#include <stddef.h>
#include <stdint.h>

struct a52q_edt_fstab_wire {
    char spec[32], file[64], vfstype[32], mntops[64], type[32];
    int32_t freq, passno;
    /* Four final bytes are not read by the measured consumer. Keep zero. */
    uint8_t unused[4];
};
_Static_assert(sizeof(struct a52q_edt_fstab_wire) == 0xec, "Libinfo entry stride");
_Static_assert(offsetof(struct a52q_edt_fstab_wire, file) == 0x20, "mount path offset");
_Static_assert(offsetof(struct a52q_edt_fstab_wire, vfstype) == 0x60, "filesystem offset");
_Static_assert(offsetof(struct a52q_edt_fstab_wire, mntops) == 0x80, "options offset");
_Static_assert(offsetof(struct a52q_edt_fstab_wire, type) == 0xc0, "type offset");
_Static_assert(offsetof(struct a52q_edt_fstab_wire, freq) == 0xe0, "frequency offset");
_Static_assert(offsetof(struct a52q_edt_fstab_wire, passno) == 0xe4, "pass offset");

static int a52q_sysctl_edt_fstab SYSCTL_HANDLER_ARGS
{
    extern vnode_t rootvnode;
    extern dev_t rootdev;
    if (req->newptr) return EPERM;
    dev_t device;
    if (!a52q_ufs_root_named("a52ios0") || a52q_ufs_rootdev(&device) ||
        device != rootdev || rootvnode == NULL) return ENOENT;
    mount_t mp = vnode_mount(rootvnode);
    if (mp == NULL || (vfs_flags(mp) & (MNT_RDONLY | MNT_ROOTFS)) !=
        (MNT_RDONLY | MNT_ROOTFS) || strcmp(vfs_statfs(mp)->f_fstypename, "hfs")) return ENOENT;
    static const struct a52q_edt_fstab_wire entry = {
        .spec = "/dev/a52ios0", .file = "/", .vfstype = "hfs",
        .mntops = "ro", .type = "ro", .freq = 0, .passno = 1
    };
    printf("A52Q boot filesystem: publishing mounted read-only UFS HFS root, no data volume\n");
    return SYSCTL_OUT(req, &entry, sizeof(entry));
}

SYSCTL_DECL(_vfs_generic);
SYSCTL_NODE(_vfs_generic, OID_AUTO, apfs, CTLFLAG_RD | CTLFLAG_LOCKED,
    NULL, "A52 development filesystem-table compatibility only; no APFS filesystem");
SYSCTL_PROC(_vfs_generic_apfs, OID_AUTO, edt_fstab,
    CTLTYPE_OPAQUE | CTLFLAG_RD | CTLFLAG_LOCKED, NULL, 0,
    a52q_sysctl_edt_fstab, "S,a52q_edt_fstab_wire", "Mounted A52 read-only root entry");
