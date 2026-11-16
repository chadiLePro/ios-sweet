"""Diagnostic guards and actual helper behavior; no Apple key material."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'xnu/a52q'))
import keybag_trace
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_keybag_trace import decode


def other_board(text):
    lines, mode = [], None
    for line in text.splitlines():
        if line == '#if defined(ARM64_BOARD_CONFIG_A52Q)':
            assert mode is None
            mode = False
        elif mode is not None and line == '#else':
            mode = True
        elif mode is not None and line == '#endif':
            mode = None
        elif mode is not False and line.strip():
            lines.append(line)
    return '\n'.join(lines)


class KeybagTraceTests(unittest.TestCase):
    def test_crc_rejects_corruption_and_conflicting_valid_copies(self):
        body = b'match/1 class=AppleKeyStore result=0xe00002c0 found=none'
        def frame(value): return b'A52KB1 ' + value + b' %08x\n' % zlib.crc32(value)
        good = frame(body)
        self.assertEqual(decode(good * 3)['records'][0]['valid_copies'], 3)
        self.assertEqual(decode(good.replace(b'02c0', b'02c1'))['records'], [])
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            decode(good + frame(body.replace(b'02c0', b'02c1')))
    def test_transforms_preserve_other_board_code_and_return_paths(self):
        source = ('int\nopen1(void)\n{\n' + keybag_trace.OPEN_LOCALS +
                  ''.join('\tif (x) {\n\t\treturn ' + str(n) + ';\n\t}\n' for n in range(7)) +
                  '}\n' + keybag_trace.OPEN_END + '\n remainder */\n')
        changed = keybag_trace.vfs(source)
        self.assertEqual(other_board(changed), other_board(source))
        self.assertEqual(changed.count('return a52q_keybag_open_result('), 7)
        with self.assertRaises(ValueError): keybag_trace.vfs(changed)
        with self.assertRaises(ValueError): keybag_trace.vfs(source.replace('return 6;', 'goto end;'))
        source = (keybag_trace.IO_ANCHOR + '\n */\nold_helper();\n#endif\n' +
                  '\t\tkr = *service ? kIOReturnSuccess : kIOReturnNotFound;\n')
        changed = keybag_trace.iokit(source)
        self.assertEqual(other_board(changed), other_board(source))
        with self.assertRaises(ValueError): keybag_trace.iokit(changed)
        with self.assertRaises(ValueError): keybag_trace.iokit(source + source)

    def test_open_helper_is_bounded_and_preserves_errors(self):
        compiler = shutil.which('gcc')
        if os.name == 'nt' and Path('C:/winlibs/mingw64/bin/gcc.exe').exists():
            compiler = 'C:/winlibs/mingw64/bin/gcc.exe'
        if not compiler: self.skipTest('native compiler unavailable')
        prefix = r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <errno.h>
#define ARM64_BOARD_CONFIG_A52Q 1
#define UIO_SEG_IS_USER_SPACE(v) (v)
#define CAST_DOWN(t,v) ((t)(v))
typedef uintptr_t user_addr_t;
typedef char *caddr_t;
struct nameidata { int ni_segflg; user_addr_t ni_dirp; };
static const char *process_name="keybagd";
static int failed_copy;
static void proc_selfname(char *out, size_t size) { snprintf(out,size,"%s",process_name); }
static int copyinstr(user_addr_t address, char *out, size_t size, size_t *copied) {
 if(failed_copy) return EFAULT;
 const char *p=(const char *)address;size_t n=strlen(p);
 if(n>=size) {memcpy(out,p,size-1);*copied=size-1;return ENAMETOOLONG;}
 memcpy(out,p,n+1);*copied=n+1;return 0;
}
static int copystr(caddr_t p,char *out,size_t size,size_t *copied) {
 return copyinstr((user_addr_t)p,out,size,copied);
}
'''
        body = r'''
int main(void) {
 char path[160];struct nameidata nd={1,(user_addr_t)"/private/var/keybags/systembag.kb"};
 a52q_keybag_open_path(&nd,path,sizeof(path));assert(!strcmp(path,(char *)nd.ni_dirp));
 const int results[]={-1,0,2,30,53};
 for(unsigned i=0;i<sizeof(results)/sizeof(results[0]);i++)
  assert(a52q_keybag_open_result(path,0,results[i])==results[i]);
 failed_copy=1;a52q_keybag_open_path(&nd,path,sizeof(path));assert(!path[0]);failed_copy=0;
 process_name="other";a52q_keybag_open_path(&nd,path,sizeof(path));assert(!path[0]);
 process_name="keybagd";char longpath[300];memset(longpath,'x',sizeof(longpath));longpath[299]=0;
 nd.ni_dirp=(user_addr_t)longpath;a52q_keybag_open_path(&nd,path,sizeof(path));assert(strlen(path)==159);
 nd.ni_segflg=0;a52q_keybag_open_path(&nd,path,sizeof(path));assert(strlen(path)==159);
 for(unsigned i=0;i<100;i++) assert(a52q_keybag_open_result(path,0,30)==30);
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'trace.c'; p.write_text(prefix + keybag_trace.VFS_HELPERS + body)
            exe = Path(directory) / ('trace.exe' if os.name == 'nt' else 'trace')
            result = subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', str(p), '-o', str(exe)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run([str(exe)], capture_output=True, text=True, check=True)
            records = decode(result.stdout.encode())['records']
            self.assertEqual(len(records), 80)
            self.assertTrue(all(row['valid_copies'] == 3 for row in records))


if __name__ == '__main__': unittest.main()
