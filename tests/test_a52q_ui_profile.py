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
        self.assertEqual(result['display_scale'],3)
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
        cfg['abort_reason']=True
        with self.assertRaisesRegex(ValueError,'abort-reason'):check()
        oldcmd=cmd;cmd+=b' a52qscan=backboardd'
        data[0x48:0x2a8]=cmd+bytes(608-len(cmd));check()
        del cfg['abort_reason']
        with self.assertRaisesRegex(ValueError,'abort-reason'):check()
        cmd=oldcmd;data[0x48:0x2a8]=cmd+bytes(608-len(cmd));check()
        cfg['display_scale']=3
        with self.assertRaisesRegex(ValueError,'display scale'):check()
        chosen=next(n for n in tree.children if n.name=='chosen')
        chosen.props.append(('display-scale',0,struct.pack('<I',3)))
        check()
        chosen.props[-1]=('display-scale',0,struct.pack('<I',0))
        with self.assertRaisesRegex(ValueError,'display scale'):check()
        chosen.props.pop()
        del cfg['display_scale']
        for key,value in [('environment','QEMU virt ONLY; never flash'),('kernel_sha256','e'*64),
                          ('live_dtb_sha256','c'*64),('ios_exec_development',False)]:
            old=manifest[key];manifest[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):check()
            manifest[key]=old
        defaults.props[-1]=('no-effaceable-storage',0,struct.pack('<I',0))
        with self.assertRaises(ValueError):check()
        defaults.props[-1]=('no-effaceable-storage',0,struct.pack('<I',1))
        from test_a52q_persistent_data import PersistentDataTests
        from a52q_persistent_data import adt_node as var_node,write_adt_node
        var=PersistentDataTests();var.setUp();cfg['var_plan']=var.plan
        vn=var_node(var.plan,base.config,base.ufs['nonce']);tree.children.append(vn)
        check()  # Existing RO data-node behavior is unchanged.
        cfg['var_write_development']=True
        with self.assertRaisesRegex(ValueError,'var-write'):check()
        readonly_cmd=cmd;cmd+=b' a52qvarwrite=1'
        data[0x48:0x2a8]=cmd+bytes(608-len(cmd))
        with self.assertRaisesRegex(ValueError,'var-write'):check()
        wn=write_adt_node(var.plan,base.config,base.ufs['nonce']);tree.children.append(wn)
        check();self.assertFalse(var.plan['write_approved'])  # A package is not phone approval.
        original=wn.props[1];wn.props[1]=('ufs-nonce',0,struct.pack('<Q',82))
        with self.assertRaisesRegex(ValueError,'var-write'):check()
        wn.props[1]=original;check()
        del cfg['var_write_development']
        with self.assertRaisesRegex(ValueError,'undeclared development var writes'):check()
        tree.children.remove(wn);cmd=readonly_cmd
        data[0x48:0x2a8]=cmd+bytes(608-len(cmd));check()
        tree.children.remove(vn);del cfg['var_plan'];check()
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
        self.assertEqual(ui.decode_console(detail(6,1,1),cfg)['rejections'][0]['reason'],'start-completion-timeout')
        for args in ((6,1,0),(6,6,1),(6,1,2)):
            with self.assertRaises(ValueError):ui.decode_console(detail(*args),cfg)
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
                    export=out[out.index('case kSweetFBGetLayerDefaultSurface:'):]
                    self.assertLess(export.index('fFB->handoffConsole()'),export.index('sweet_surface_port_in_task'))
                    self.check_surface_handoff(out)

    def check_surface_handoff(self, source):
        """Execute the transformed action against a workloop-gate concurrency model."""
        cc='C:/winlibs/mingw64/bin/g++.exe' if os.name=='nt' else shutil.which('c++')
        if not cc:self.skipTest('native C++ compiler unavailable')
        action=source[source.index('static IOReturn\na52q_console_handoff_action'):]
        action=action[:action.index('\n#endif')]
        code=r'''
#include <cassert>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <thread>
using IOReturn=int;
const int kIOReturnSuccess=0,kIOReturnNotReady=1;
struct OSObject {};
struct IOWorkLoop {
 std::recursive_mutex gate;
 using Action=IOReturn (*)(OSObject *,void *,void *,void *,void *);
 IOReturn runAction(Action a,OSObject *o) {
  std::lock_guard<std::recursive_mutex> guard(gate);return a(o,nullptr,nullptr,nullptr,nullptr);
 }
};
static bool drawing=false,owned=true;
static bool a52q_fb_console_handoff() {assert(!drawing);owned=false;return true;}
struct AppleCLCD:OSObject {IOWorkLoop *fWorkLoop;bool handoffConsole();};
''' + action + r'''
int main() {
 IOWorkLoop loop;AppleCLCD fb;fb.fWorkLoop=&loop;
 std::mutex mutex;std::condition_variable cv;bool started=false,release=false;
 std::atomic<bool> attempting(false),exported(false);
 std::thread renderer([&] {
  std::lock_guard<std::recursive_mutex> gate(loop.gate);drawing=true;
  std::unique_lock<std::mutex> lock(mutex);started=true;cv.notify_all();
  cv.wait(lock,[&]{return release;});assert(owned);drawing=false;
 });
 {std::unique_lock<std::mutex> lock(mutex);cv.wait(lock,[&]{return started;});}
 std::thread client([&] {attempting=true;assert(fb.handoffConsole());exported=true;});
 while(!attempting.load())std::this_thread::yield();
 assert(!exported.load());
 {std::lock_guard<std::mutex> lock(mutex);release=true;}cv.notify_all();
 renderer.join();client.join();assert(exported && !owned);
 assert(fb.handoffConsole());fb.fWorkLoop=nullptr;assert(!fb.handoffConsole());
}
'''
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'handoff.cpp';p.write_text(code);exe=Path(d)/('handoff.exe' if os.name=='nt' else 'handoff')
            args=[cc,'-std=c++11','-Wall','-Wextra','-Werror','-pthread']
            if os.name=='nt':args.append('-static')
            v=subprocess.run([*args,str(p),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(v.returncode,0,v.stderr)
            v=subprocess.run([str(exe)],capture_output=True,text=True,timeout=15)
            self.assertEqual(v.returncode,0,v.stderr)

if __name__=='__main__':unittest.main()
