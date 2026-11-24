"""Native rejection checks for the exact measured persona Boolean."""
from pathlib import Path
import os,shutil,subprocess,tempfile,unittest
R=Path(__file__).resolve().parents[1]
class PersonaCapabilityTests(unittest.TestCase):
 def test_exact_identity_key_and_validated_catalog_required(self):
  cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
  if not cc:self.skipTest('C compiler unavailable')
  text=(R/'xnu/a52q/a52q_amfi.c').read_text();body=text.split('static int a52q_persona_task',1)[1].split('static kern_return_t a52q_bool_proc',1)[0]
  harness=r"""
#include <assert.h>
#include <stdint.h>
#include <string.h>
#define CS_CDHASH_LEN 20
#define CS_SIGNED 1
#define CS_VALID 2
#define CS_PLATFORM_BINARY 4
struct cs_blob {uint8_t csb_cdhash[20];int csb_platform_binary,csb_flags;};
typedef struct cs_blob *proc_t;
static int catalog=1,flags=3;
static int proc_getcsflags(proc_t p){(void)p;return flags;}
static struct cs_blob *csproc_get_blob(proc_t p){return p;}
static int a52q_verified_catalog_blob(struct cs_blob *b){(void)b;return catalog?0:-1;}
"""
  checks=r"""
int main(void){
struct cs_blob b={{0xfe,0x4f,0x08,0x91,0x91,0x73,0xd0,0x3d,0xb9,0x8b,0x98,0xce,0x55,0x57,0xb1,0xc9,0x9c,0x47,0x41,0x9e},1,5};
const char *k="com.apple.private.persona-mgmt";
assert(a52q_persona_task(&b,k));assert(!a52q_persona_task(0,k));
assert(!a52q_persona_task(&b,0));assert(!a52q_persona_task(&b,"com.apple.private.persona.modify"));
b.csb_cdhash[0]^=1;assert(!a52q_persona_task(&b,k));b.csb_cdhash[0]^=1;
catalog=0;assert(!a52q_persona_task(&b,k));catalog=1;
flags=1;assert(!a52q_persona_task(&b,k));flags=3;
b.csb_platform_binary=0;assert(!a52q_persona_task(&b,k));b.csb_platform_binary=1;
b.csb_flags=1;assert(!a52q_persona_task(&b,k));return 0;}
"""
  with tempfile.TemporaryDirectory() as d:
   c=Path(d)/'persona.c';exe=Path(d)/('persona.exe' if os.name=='nt' else 'persona');c.write_text(harness+'static int a52q_persona_task'+body+checks)
   x=subprocess.run([cc,'-Wall','-Wextra','-Werror',str(c),'-o',str(exe)],capture_output=True,text=True);self.assertEqual(x.returncode,0,x.stderr)
   x=subprocess.run([str(exe)],capture_output=True,text=True);self.assertEqual(x.returncode,0,x.stderr)
