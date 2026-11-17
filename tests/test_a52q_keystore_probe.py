"""Run the actual empty KeyStore probe against hostile requests and task transfer."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from a52q_keybag_trace import decode


class EmptyKeyStoreTests(unittest.TestCase):
    def test_no_bag_success_no_crypto_and_owned_connection_lifecycle(self):
        root = Path(__file__).resolve().parents[1]
        compiler = shutil.which('g++')
        if os.name == 'nt' and Path('C:/winlibs/mingw64/bin/g++.exe').exists():
            compiler = 'C:/winlibs/mingw64/bin/g++.exe'
        if not compiler: self.skipTest('native C++ compiler unavailable')
        text = (root / 'xnu/a52q/A52PlatformExpert.cpp').read_text()
        begin = text.index('/* A52Q_EMPTY_KEYSTORE_BEGIN')
        end = text.index('/* A52Q_EMPTY_KEYSTORE_END */')
        actual = text[begin:end]
        prefix = r"""
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cstdarg>
#include <initializer_list>
#define __unused __attribute__((unused))
#define APPLE_KEXT_OVERRIDE override
#define OSDeclareDefaultStructors(T) public: T() = default;
#define OSDefineMetaClassAndStructors(T,B)
using UInt32 = uint32_t;
using IOReturn = int32_t;
using task_t = void *;
#define TASK_NULL nullptr
#define MACH_PORT_NULL 0
#define kIOExternalMethodArgumentsCurrentVersion 2
#define kIOReturnSuccess 0
#define kIOReturnNoMemory ((IOReturn)0xe00002bdU)
#define kIOReturnNoResources ((IOReturn)0xe00002beU)
#define kIOReturnNotPrivileged ((IOReturn)0xe00002c1U)
#define kIOReturnBadArgument ((IOReturn)0xe00002c2U)
#define kIOReturnUnsupported ((IOReturn)0xe00002c7U)
#define kIOReturnNotOpen ((IOReturn)0xe00002cdU)
#define kIOReturnNotFound ((IOReturn)0xe00002f0U)
static int task_object, other_object, task_refs;
static task_t current = &task_object;
static task_t current_task() { return current; }
static void task_reference(task_t) { ++task_refs; }
static void task_deallocate(task_t) { --task_refs; }
static void proc_selfname(char *p, size_t n) { snprintf(p,n,"keybagd"); }
static const char *boot_root = "a52ios0";
static bool PE_parse_boot_argn(const char *key, void *p, size_t n) {
 if (!strcmp(key,"a52q_dev_keybag")) { assert(n==sizeof(int)); *static_cast<int *>(p)=0; return true; }
 assert(!strcmp(key,"rd"));
 if (!boot_root) return false;
 snprintf(static_cast<char *>(p),n,"%s",boot_root); return true;
}
static int registrations, live_clients;
static bool fail_init, fail_attach, fail_start;
static void IOLog(const char *fmt, ...) {
 va_list ap; va_start(ap,fmt); vprintf(fmt,ap); va_end(ap);
}
struct OSObject { virtual ~OSObject() = default; };
struct OSDictionary : OSObject {};
static OSObject boolean;
static OSObject *kOSBooleanTrue = &boolean;
struct IOExternalMethodDispatch {};
struct IOExternalMethodArguments {
 uint32_t version = 2, selector = 0, asyncWakePort = 0;
 void *asyncReference = nullptr;
 uint32_t asyncReferenceCount = 0;
 const uint64_t *scalarInput = nullptr;
 uint32_t scalarInputCount = 0;
 const void *structureInput = nullptr;
 uint32_t structureInputSize = 0;
 void *structureInputDescriptor = nullptr;
 uint64_t *scalarOutput = nullptr;
 uint32_t scalarOutputCount = 0;
 void *structureOutput = nullptr;
 uint32_t structureOutputSize = 0;
 void *structureOutputDescriptor = nullptr;
 uint32_t structureOutputDescriptorSize = 0;
 OSObject **structureVariableOutputData = nullptr;
};
class IOUserClient;
class IOService : public OSObject {
public:
 virtual bool init() { return !fail_init; }
 virtual bool attach(IOService *) { return !fail_attach; }
 virtual bool start(IOService *) { return !fail_start; }
 virtual void free() {}
 virtual IOReturn newUserClient(task_t,void *,UInt32,OSDictionary *,IOUserClient **) { return -1; }
 virtual IOReturn newUserClient(task_t,void *,UInt32,IOUserClient **) { return -1; }
 void detach(IOService *) {}
 void setProperty(const char *,OSObject *) {}
 void registerService() { ++registrations; }
 void release() { free(); delete this; }
};
class IOUserClient : public IOService {
public:
 IOUserClient() { ++live_clients; }
 ~IOUserClient() override { --live_clients; }
 virtual bool initWithTask(task_t,void *,UInt32) { return !fail_init; }
 virtual bool initWithTask(task_t,void *,UInt32,OSDictionary *) { return false; }
 virtual IOReturn clientClose() { return -1; }
 virtual IOReturn externalMethod(uint32_t,IOExternalMethodArguments *,IOExternalMethodDispatch *,OSObject *,void *) { return -1; }
 void terminate() {}
};
"""
        body = r"""
int main() {
 unsigned state = 0;
 IOExternalMethodArguments a;
 assert(a52q_aks_probe_request(0,&a,false,&state)==kIOReturnNotPrivileged);
 assert(state==0);
 assert(a52q_aks_probe_request(0,nullptr,true,&state)==kIOReturnBadArgument);
 for (unsigned n=1;n<=110;n++) if(n!=14)
  assert(a52q_aks_probe_request(n,&a,true,&state)==kIOReturnUnsupported);
 for(unsigned n=0;n<11;n++) {
  auto bad=a;
  switch(n) {
   case 0:bad.version=1;break;
   case 1:bad.asyncWakePort=1;break;
   case 2:bad.asyncReferenceCount=1;break;
   case 3:bad.structureInputSize=1;break;
   case 4:bad.structureOutputSize=1;break;
   case 5:bad.structureInputDescriptor=&state;break;
   case 6:bad.structureOutputDescriptor=&state;break;
   case 7:bad.structureOutputDescriptorSize=1;break;
   case 8:bad.structureVariableOutputData=&kOSBooleanTrue;break;
   case 9:bad.scalarInputCount=1;break;
   case 10:bad.scalarOutputCount=1;break;
  }
  assert(a52q_aks_probe_request(0,&bad,true,&state)==kIOReturnBadArgument);
  assert(state==0);
 }
 // New profile stays explicit; default discovery behavior below is unchanged.
 unsigned devstate=1;uint64_t devhandle=99;auto dev=a;
 dev.scalarOutput=&devhandle;dev.scalarOutputCount=1;
 assert(a52q_aks_probe_request(14,&dev,true,&devstate,true)==kIOReturnSuccess && devhandle==0);
 assert(a52q_aks_probe_request(7,&dev,true,&devstate,true)==kIOReturnSuccess && devhandle==4);
 devhandle=99;
 assert(a52q_aks_probe_request(14,&dev,false,&devstate,true)==kIOReturnNotPrivileged && devhandle==99);
 uint64_t other=123;dev.scalarInput=&other;dev.scalarInputCount=1;
 assert(a52q_aks_probe_request(14,&dev,true,&devstate,true)==kIOReturnBadArgument && devhandle==99);
 uint8_t der[128];memset(der,0xaa,sizeof(der));dev=a;
 dev.structureOutput=der;dev.structureOutputSize=1;
 assert(a52q_aks_probe_request(17,&dev,true,&devstate,true)==kIOReturnBadArgument && der[0]==0xaa);
 dev.structureOutputSize=sizeof(der);
 assert(a52q_aks_probe_request(17,&dev,true,&devstate,true)==kIOReturnSuccess);
 assert(der[0]==0x31 && (unsigned)der[1]+2U==dev.structureOutputSize && der[dev.structureOutputSize]==0xaa);
 for(unsigned sel : {3U,6U,10U,11U,999U})
  assert(a52q_aks_probe_request(sel,&a,true,&devstate,true)==kIOReturnUnsupported);
 devstate=2;dev=a;dev.scalarOutput=&devhandle;dev.scalarOutputCount=1;
 assert(a52q_aks_probe_request(14,&dev,true,&devstate,true)==kIOReturnNotOpen);
 uint64_t handle=0x1122334455667788ULL;
 auto query=a;query.scalarOutput=&handle;query.scalarOutputCount=1;
 assert(a52q_aks_probe_request(14,&query,true,&state)==kIOReturnNotOpen);
 assert(a52q_aks_probe_request(0,&a,true,&state)==kIOReturnSuccess);
 assert(a52q_aks_probe_request(0,&a,true,&state)==kIOReturnNotOpen);
 assert(a52q_aks_probe_request(14,&query,true,&state)==kIOReturnNotFound);
 assert(handle==0x1122334455667788ULL);
 for(unsigned count=0;count<17;count++) if(count!=1) {
  query.scalarOutputCount=count;
  assert(a52q_aks_probe_request(14,&query,true,&state)==kIOReturnBadArgument);
 }
 query.scalarOutputCount=1;query.scalarOutput=nullptr;
 assert(a52q_aks_probe_request(14,&query,true,&state)==kIOReturnBadArgument);
 query.scalarOutput=&handle;
 state=2;
 assert(a52q_aks_probe_request(0,&a,true,&state)==kIOReturnNotOpen);
 assert(a52q_aks_probe_request(14,&query,true,&state)==kIOReturnNotOpen);
 assert(handle==0x1122334455667788ULL);
 IOService platform;
 boot_root=nullptr;a52q_aks_probe_register(&platform);assert(registrations==0);
 boot_root="a52root0";a52q_aks_probe_register(&platform);assert(registrations==0);
 boot_root="a52ios0evil";a52q_aks_probe_register(&platform);assert(registrations==0);
 boot_root="a52ios0";
 for(unsigned n=0;n<3;n++) {
  fail_init=(n==0);fail_attach=(n==1);fail_start=(n==2);
  a52q_aks_probe_register(&platform);assert(registrations==0);
 }
 fail_init=fail_attach=fail_start=false;
 a52q_aks_probe_register(&platform);assert(registrations==1);
 AppleKeyStore service;
 IOUserClient *client=nullptr;
 assert(service.newUserClient(current,nullptr,0,nullptr)==kIOReturnBadArgument);
 assert(service.newUserClient(current,nullptr,1,&client)==kIOReturnUnsupported && !client);
 assert(service.newUserClient(nullptr,nullptr,0,&client)==kIOReturnNotPrivileged && !client);
 assert(service.newUserClient(&other_object,nullptr,0,&client)==kIOReturnNotPrivileged && !client);
 for(unsigned n=0;n<3;n++) {
  fail_init=(n==0);fail_attach=(n==1);fail_start=(n==2);
  assert(service.newUserClient(current,nullptr,0,&client)!=kIOReturnSuccess);
  assert(!client && task_refs==0 && live_clients==0);
 }
 fail_init=fail_attach=fail_start=false;
 assert(service.newUserClient(current,nullptr,0,&client)==kIOReturnSuccess);
 assert(client && task_refs==1 && live_clients==1);
 assert(client->externalMethod(0,&a,nullptr,nullptr,nullptr)==kIOReturnSuccess);
 current=&other_object;
 assert(client->externalMethod(14,&query,nullptr,nullptr,nullptr)==kIOReturnNotPrivileged);
 current=&task_object;
 assert(client->externalMethod(14,&query,nullptr,nullptr,nullptr)==kIOReturnNotFound);
 assert(handle==0x1122334455667788ULL);
 assert(client->clientClose()==kIOReturnSuccess);
 assert(client->externalMethod(0,&a,nullptr,nullptr,nullptr)==kIOReturnNotOpen);
 client->release();assert(task_refs==0 && live_clients==0);
 // Logging stays bounded and contains statuses only, never payload/handles.
 for(unsigned n=0;n<100;n++) a52q_aks_probe_trace(14,kIOReturnNotFound);
 return 0;
}
"""
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'probe.cpp'; p.write_text(prefix + actual + body)
            exe = Path(directory) / ('probe.exe' if os.name == 'nt' else 'probe')
            link = ['-static'] if os.name == 'nt' else []
            result = subprocess.run([compiler, *link, '-std=c++17', '-Wall', '-Wextra', '-Werror',
                                     str(p), '-o', str(exe)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            run = subprocess.run([str(exe)], capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr.decode(errors='replace'))
            records = decode(run.stdout)['records']
            self.assertEqual(len(records), 80)
            self.assertTrue(all(x['kind']=='aks' and x['valid_copies']==3 for x in records))
            self.assertTrue(any('result=0xe00002f0' in x['body'] for x in records))


if __name__ == '__main__': unittest.main()
