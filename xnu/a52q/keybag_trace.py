"""Bounded A52 keybag diagnostics; no service, storage or return-value changes."""
import re

VFS = 'bsd/vfs/vfs_syscalls.c'
IOKIT = 'iokit/Kernel/IOUserClient.cpp'
OPEN_BEGIN = 'int\nopen1('
OPEN_END = '\n/*\n * While most of the *at'
OPEN_LOCALS = '\tvnode_t authvp = NULLVP;\n'
IO_ANCHOR = 'static \n#if defined(ARM64_BOARD_CONFIG_SWEET)\n/*\n * SWEET IOKit trace:'


def record_helper(output):
    return r'''
/* CRC-protected triplicates survive the observed unprotected-text damage. */
static void
a52q_keybag_record(const char *body)
{
    uint32_t crc = 0xffffffffU;
    unsigned length = (unsigned)strlen(body);
    if (!length || length >= 240) return;
    for (unsigned i = 0; i < length; i++) {
        crc ^= (uint8_t)body[i];
        for (unsigned bit = 0; bit < 8; bit++)
            crc = (crc >> 1) ^ (0xedb88320U & (0U - (crc & 1)));
    }
    for (unsigned copy = 0; copy < 3; copy++)
        OUTPUT("A52KB1 %s %08x\n", body, crc ^ 0xffffffffU);
}
'''.replace('OUTPUT', output)

VFS_HELPERS = r'''#if defined(ARM64_BOARD_CONFIG_A52Q)
/* Observe names/errors only: never read keybag contents or modify an open. */
static void
a52q_keybag_open_path(struct nameidata *ndp, char *path, size_t size)
{
    char name[32];
    size_t copied = 0;
    int error;
    path[0] = '\0';
    proc_selfname(name, sizeof(name));
    if (strcmp(name, "keybagd")) return;
    if (UIO_SEG_IS_USER_SPACE(ndp->ni_segflg)) {
        error = copyinstr(ndp->ni_dirp, path, size, &copied);
    } else {
        error = copystr(CAST_DOWN(caddr_t, ndp->ni_dirp), path, size, &copied);
    }
    if (error && error != ENAMETOOLONG) path[0] = '\0';
    path[size - 1] = '\0';
}

static int
a52q_keybag_open_result(const char *path, int flags, int result)
{
    static unsigned lines;
    if (path[0] && (path[0] != '/' ||
        !strncmp(path, "/private/var/", 13) || !strncmp(path, "/var/", 5))) {
        char body[240];
        unsigned sequence = __atomic_fetch_add(&lines, 1U, __ATOMIC_RELAXED) + 1U;
        if (sequence > 80) return result;
        snprintf(body, sizeof(body), "open/%u flags=0x%x errno=%d path=%.159s", sequence, flags, result, path);
        a52q_keybag_record(body);
    }
    return result;
}
#endif

'''
VFS_HELPERS = VFS_HELPERS.replace('/* Observe names/errors only:', record_helper('printf') + '\n/* Observe names/errors only:', 1)

IO_HELPER = r'''#if defined(ARM64_BOARD_CONFIG_A52Q)
/* Class names and match outcomes only; no properties or key material. */
static void
a52q_keybag_match(OSDictionary *dict, kern_return_t result, const char *found)
{
    static unsigned lines;
    char name[32];
    proc_selfname(name, sizeof(name));
    if (strcmp(name, "keybagd")) return;
    unsigned sequence = __atomic_fetch_add(&lines, 1U, __ATOMIC_RELAXED) + 1U;
    if (sequence > 80) return;
    OSString *className = OSDynamicCast(OSString, dict->getObject("IOProviderClass"));
    char body[240];
    snprintf(body, sizeof(body), "match/%u class=%.80s result=0x%x found=%.64s", sequence,
        className ? className->getCStringNoCopy() : "(other match)", result, found);
    a52q_keybag_record(body);
}
#endif

'''
IO_HELPER = IO_HELPER.replace('/* Class names and match outcomes only;', record_helper('IOLog') + '\n/* Class names and match outcomes only;', 1)


def vfs(text):
    if 'a52q_keybag_open_result' in text or text.count(OPEN_BEGIN) != 1:
        raise ValueError('unexpected or already traced open1')
    begin = text.index(OPEN_BEGIN)
    end = text.index(OPEN_END, begin)
    function = text[begin:end]
    if function.count(OPEN_LOCALS) != 1:
        raise ValueError('open1 local anchor changed')
    function = function.replace(OPEN_LOCALS, OPEN_LOCALS + '''#if defined(ARM64_BOARD_CONFIG_A52Q)
\tchar a52q_open_path[160];
\ta52q_keybag_open_path(ndp, a52q_open_path, sizeof(a52q_open_path));
#endif
''')
    def replace(match):
        indent, value = match.groups()
        return (f'#if defined(ARM64_BOARD_CONFIG_A52Q)\n'
                f'{indent}return a52q_keybag_open_result(a52q_open_path, uflags, {value});\n'
                f'#else\n{match[0]}\n#endif')
    function, count = re.subn(r'^(\t+)return ([^;\n]+);', replace, function, flags=re.M)
    if count != 7:
        raise ValueError('open1 return paths changed')
    return text[:begin] + VFS_HELPERS + function + text[end:]


def iokit(text):
    if 'a52q_keybag_match' in text or text.count(IO_ANCHOR) != 1:
        raise ValueError('unexpected or already traced matching implementation')
    text = text.replace(IO_ANCHOR, IO_HELPER + IO_ANCHOR)
    anchor = '\t\tkr = *service ? kIOReturnSuccess : kIOReturnNotFound;\n'
    if text.count(anchor) != 1:
        raise ValueError('single-service matching anchor changed')
    return text.replace(anchor, anchor + '''#if defined(ARM64_BOARD_CONFIG_A52Q)
\t\ta52q_keybag_match(dict, kr,
\t\t    *service ? (*service)->getMetaClass()->getClassName() : "none");
#endif
''')
