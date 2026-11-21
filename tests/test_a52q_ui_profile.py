"""Exercise exact hardware pins, pixel-copy bounds and patched software inputs."""
import copy,os,shutil,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'));sys.path.insert(0,str(R/'xnu/a52q'))
import a52q_ui_profile as ui
import software_ui

class UIProfileTests(unittest.TestCase):
    def test_profile_and_crc_prerequisite(self):
        cfg=dict(copy.deepcopy(ui.EXPECTED),nonce=81,kernel_sha256='b'*64,root_sha256='a'*64,
                 physical_kernel_console_sha256='d'*64,software_vsync_us=16667,physical_panel_hz=None)
        ui.validate_config(cfg)
        for k,v in [('reg',[0x9c004000,0x9e4000]),('geometry',[1080,2400,4400]),('software_vsync_us',8333),('physical_panel_hz',60),('root_sha256','x')]:
            with self.subTest(k=k),self.assertRaises(ValueError):ui.validate_config(dict(cfg,**{k:v}))
        build=dict(embedded_payload=dict(display_selftest=cfg))
        with self.assertRaises(ValueError):ui.configuration(build,b'','b'*64,'a'*64)
        frames=[]
        for phase in (0x10,0x20,0x30):
            body=f'{81:016x}/{phase:02x}/{0:08x}'.encode()
            frames.append(b'A52D1 '+body+b' %08x\n'%zlib.crc32(body))
        result=ui.configuration(build,b''.join(frames),'b'*64,'a'*64)
        self.assertEqual(result['geometry'],[1080,2400,4320]);self.assertIsNone(result['physical_panel_hz'])

    def test_payload_requires_exact_full_root_flags_and_nodes(self):
        import hashlib,struct,adt
        from test_a52q_payload import fixture
        from test_a52q_persistent_root import PersistentRootTests
        from a52q_ufs_selftest import adt_node as unode
        from a52q_persistent_root import adt_node as rnode
        from a52q_payload import validate_payload
        base=PersistentRootTests();base.setUp()
        cfg=dict(copy.deepcopy(ui.EXPECTED),nonce=81,kernel_sha256='b'*64,root_sha256='a'*64,
                 physical_kernel_console_sha256='d'*64,software_vsync_us=16667,physical_panel_hz=None)
        data,manifest=fixture();off,size=struct.unpack_from('<2Q',data,0x20)
        tree,_=adt.parse(data[off:off+size]);tree.children.extend([unode(base.ufs),rnode(base.config),ui.adt_node(cfg)])
        next(n for n in tree.children if n.name=='arm-io').children.append(ui.display_node())
        defaults=next(n for n in tree.children if n.name=='defaults')
        defaults.props.append(('no-effaceable-storage',0,struct.pack('<I',1)))
        cmd=b'rd=a52ios0 unentitled_ios_sim_launch=1 a52q_dev_keybag=1 a52q_ui=1'
        data[0x48:0x2a8]=cmd+bytes(608-len(cmd))
        manifest.update(environment='SM-A525F/DS hardware candidate',ufs_selftest=base.ufs,
            ufs_ios_root=base.config,kernel_sha256='b'*64,ios_exec_development=True,
            live_dtb_sha256=ui.EXPECTED['live_dtb_sha256'],development_ui_profile=cfg)
        def check():
            b=adt.serialize(tree);data[off:]=b;struct.pack_into('<Q',data,0x28,len(b))
            manifest['payload_sha256']=hashlib.sha256(data).hexdigest();validate_payload(data,manifest)
        check()
        for key,value in [('environment','QEMU virt ONLY; never flash'),('kernel_sha256','e'*64),
                          ('live_dtb_sha256','c'*64),('ios_exec_development',False)]:
            old=manifest[key];manifest[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):check()
            manifest[key]=old
        defaults.props[-1]=('no-effaceable-storage',0,struct.pack('<I',0))
        with self.assertRaises(ValueError):check()
        defaults.props[-1]=('no-effaceable-storage',0,struct.pack('<I',1))
        cfg['text_console']=True
        with self.assertRaises(ValueError):check()
        cmd+=b' a52q_text_console=1';data[0x48:0x2a8]=cmd+bytes(608-len(cmd));check()
        del cfg['text_console']
        with self.assertRaises(ValueError):check()

    def test_adapter_decode_rejects_corruption_and_wrong_nonce(self):
        cfg=dict(copy.deepcopy(ui.EXPECTED),nonce=81,kernel_sha256='b'*64,root_sha256='a'*64,
                 physical_kernel_console_sha256='d'*64,software_vsync_us=16667,physical_panel_hz=None)
        def frame(phase,count,nonce=81):
            body=f'{nonce:016x}/{phase:02x}/{count:08x}'.encode()
            return b'A52G1 '+body+b' %08x\n'%zlib.crc32(body)
        good=frame(0x10,0)*3+frame(0x30,1)*2
        report=ui.decode_console(good,cfg)
        self.assertTrue(report['adapter_prepared'] and report['guarded_submit_observed'])
        self.assertFalse(report['physical_visible_ui_verified'])
        self.assertEqual(ui.decode_console(good.replace(b'/30/',b'/31/'),cfg)['records'][0]['phase'],0x10)
        self.assertFalse(ui.decode_console(frame(0x30,1,82),cfg)['guarded_submit_observed'])
        self.assertTrue(ui.decode_console(good+frame(0xe1,20),cfg)['error_record_observed'])
        with self.assertRaises(ValueError):ui.decode_console(frame(0x30,4),cfg)

    def test_rejection_detail_crc_nonce_and_guard_index(self):
        cfg=dict(copy.deepcopy(ui.EXPECTED),nonce=81,kernel_sha256='b'*64,root_sha256='a'*64,
                 physical_kernel_console_sha256='d'*64,software_vsync_us=16667,physical_panel_hz=None)
        def detail(reason,index,value,nonce=81):
            body=f'{nonce:016x}/{reason:02x}/{index:02x}/{value:08x}'.encode()
            return b'A52G2 '+body+b' %08x\n'%zlib.crc32(body)
        good=detail(3,6,4)*3
        row=ui.decode_console(good,cfg)['rejections'][0]
        self.assertEqual((row['register_index'],row['expected'],row['observed'],row['valid_copies']),(6,5,4,3))
        self.assertFalse(ui.decode_console(good,cfg)['adapter_prepared'])
        self.assertEqual(ui.decode_console(good.replace(b'/03/',b'/02/'),cfg)['rejections'],[])
        self.assertEqual(ui.decode_console(detail(3,6,4,82),cfg)['rejections'],[])
        self.assertEqual(ui.decode_console(detail(5,6,5),cfg)['rejections'][0]['reason'],'dsi-busy-timeout')
        for args in ((3,13,4),(3,6,5),(2,6,4),(1,0,0),(4,255,1),(5,6,0),(5,5,5)):
            with self.subTest(args=args),self.assertRaises(ValueError):ui.decode_console(detail(*args),cfg)

    def test_native_profile_pins_and_cpu_copy_canaries(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        code=r"""
#include <assert.h>
#include <string.h>
#include <limits.h>
#include "a52q_ui_profile.h"
#include "a52q_ui_copy.h"
int main(void) {
 uint64_t reg[2]={A52Q_UI_PHYS,A52Q_UI_BYTES};uint32_t geo[3]={1080,2400,4320};
 struct a52q_ui_guard g[13];memcpy(g,a52q_ui_expected,sizeof(g));
 assert(a52q_ui_profile_matches(reg,geo,g,g[1].address,0x106000000ULL,0xff00000));
 for(unsigned i=0;i<13;i++) {
  g[i].value^=1;assert(!a52q_ui_profile_matches(reg,geo,g,g[1].address,0x106000000ULL,0xff00000));g[i].value^=1;
  g[i].address^=4;assert(!a52q_ui_profile_matches(reg,geo,g,g[1].address,0x106000000ULL,0xff00000));g[i].address^=4;
 }
 assert(!a52q_ui_profile_matches(reg,geo,g,g[1].address,A52Q_UI_PHYS,A52Q_UI_BYTES));
 assert(!a52q_ui_profile_matches(reg,geo,g,g[1].address,UINT64_MAX,2));
 uint32_t dst[10],src[12];for(unsigned i=0;i<12;i++)src[i]=i+1;
 for(unsigned i=0;i<10;i++)dst[i]=0xdeadbeef;
 assert(a52q_ui_copy_rect(dst+1,32,3,2,16,(uint8_t *)src,sizeof(src),3,2,20,4,1,1,1,1,2,1));
 assert(dst[6]==8 && dst[7]==9 && dst[0]==0xdeadbeef && dst[9]==0xdeadbeef && dst[5]==0xdeadbeef && dst[8]==0xdeadbeef);
 uint32_t saved[10];memcpy(saved,dst,sizeof(dst));
 for(unsigned mode=0;mode<9;mode++) {
  int sx=0,dx=0,w=3,h=2;uint64_t len=sizeof(src),dlen=32;unsigned offset=0;
  if(mode==0)sx=INT_MAX;
  if(mode==1)dx=-1;
  if(mode==2)w=INT_MAX;
  if(mode==3)h=INT_MAX;
  if(mode==4)len=1;
  if(mode==5)dlen=31;
  if(mode==6)offset=UINT_MAX;
  if(mode==7)w=0;
  if(mode==8)h=-1;
  assert(!a52q_ui_copy_rect(dst+1,dlen,3,2,16,(uint8_t *)src,len,3,2,20,offset,sx,0,dx,0,w,h));
  assert(!memcmp(saved,dst,sizeof(dst)));
 }
 return 0;
}
"""
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ui.c';p.write_text(code);exe=Path(d)/('ui.exe' if os.name=='nt' else 'ui')
            v=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-I',str(R/'xnu/a52q'),str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True,text=True);self.assertEqual(v.returncode,0,v.stderr)

    def test_transform_actual_upstream_and_keep_cached_lookup_fix(self):
        if not shutil.which('git'):self.skipTest('git unavailable')
        with tempfile.TemporaryDirectory() as d:
            for p in sorted((R/'xnu/patches').glob('*.patch')):
                if not any(('/'+n).encode() in p.read_bytes() for n in software_ui.PINS):continue
                v=subprocess.run(['git','apply','--allow-empty',*['--include=iokit/Kernel/arm/'+n for n in software_ui.PINS],str(p)],cwd=d,capture_output=True,text=True)
                self.assertEqual(v.returncode,0,v.stderr)
            for name in software_ui.PINS:
                original=(Path(d)/'iokit/Kernel/arm'/name).read_text();out=software_ui.transform(name,original)
                with self.assertRaises(ValueError):software_ui.transform(name,out)
                if name=='SweetSurface.cpp':
                    self.assertIn('*existing = true;',out);self.assertIn('if (ret != kIOReturnSuccess && !existing)',out)
                    self.assertIn('a52q_ui_physical_allowed',out)
                if name=='SweetFramebuffer.cpp':
                    self.assertIn('a52q_ui_copy_rect',out);self.assertIn('16667',out);self.assertIn('(void)a52q_ui_flush()',out)

if __name__=='__main__':unittest.main()
