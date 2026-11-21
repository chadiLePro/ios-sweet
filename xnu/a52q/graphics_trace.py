"""Read-only A52 graphics IOKit observations, without changing any result."""
import re

ANCHOR = '/* Routine io_iterator_next */'
HELPER = r'''#if defined(ARM64_BOARD_CONFIG_A52Q)
#include "arm/a52q_ui_bridge.h"
/* Observe class names and result codes only, not arbitrary properties.
 * In particular do not consume/reset a matching iterator to count it. */
static bool a52q_graphics_process(char *name, unsigned size)
{
    proc_selfname(name,size);
    return !strcmp(name,"SpringBoard") || !strcmp(name,"backboardd");
}
static unsigned a52q_graphics_class(const char *name)
{
    if (!name) return 0;
    if (strstr(name,"Surface")) return 2;
    if (strstr(name,"Framebuffer") || strstr(name,"CLCD")) return 1;
    return 0;
}
static void a52q_graphics_match(OSDictionary *dict,kern_return_t result,
    const char *found,const char *operation)
{
    char name[32],body[168];
    if (!a52q_graphics_process(name,sizeof(name))) return;
    OSString *cls=OSDynamicCast(OSString,dict->getObject("IOProviderClass"));
    OSString *key=OSDynamicCast(OSString,dict->getObject("IONameMatch"));
    const char *requested=cls ? cls->getCStringNoCopy() : key ? key->getCStringNoCopy() : "(other)";
    unsigned slot=a52q_graphics_class(requested);
    if (!slot) slot=1; /* A graphics process may ask for an unsupported class. */
    snprintf(body,sizeof(body),"%s proc=%.16s pid=%d class=%.56s ret=%08x found=%.40s",
        operation,name,proc_selfpid(),requested,result,found);
    a52q_ui_observe(slot,body);
}
static void a52q_graphics_next(OSObject *obj)
{
    IOService *service=OSDynamicCast(IOService,obj);
    if (!service) return;
    const char *cls=service->getMetaClass()->getClassName();
    unsigned slot=a52q_graphics_class(cls);char name[32],body[168];
    if (!slot || !a52q_graphics_process(name,sizeof(name))) return;
    snprintf(body,sizeof(body),"next proc=%.16s pid=%d class=%.80s",name,proc_selfpid(),cls);
    a52q_ui_observe(slot,body);
}
static void a52q_graphics_open(IOService *service,unsigned type,
    kern_return_t rpc,IOReturn result,bool result_valid)
{
    const char *cls=service->getMetaClass()->getClassName();
    unsigned slot=a52q_graphics_class(cls);char name[32],body[168];
    if (!slot || !a52q_graphics_process(name,sizeof(name))) return;
    snprintf(body,sizeof(body),"open proc=%.16s pid=%d class=%.56s type=%u rpc=%08x io=%08x valid=%u",
        name,proc_selfpid(),cls,type,rpc,result,(unsigned)result_valid);
    a52q_ui_observe(slot+2,body);
}
#endif

'''


def block(code):
    return '\n#if defined(ARM64_BOARD_CONFIG_A52Q)\n'+code+'\n#endif\n'


def iokit(text):
    if text.count(ANCHOR)!=1 or 'a52q_graphics_process' in text:
        raise ValueError('unexpected graphics trace source or already applied')
    def change(old,new):
        nonlocal text
        if text.count(old)!=1:raise ValueError('graphics trace anchor changed: '+old[:80])
        text=text.replace(old,new,1)
    change(ANCHOR,HELPER+ANCHOR)
    change('\t\tkr = *service ? kIOReturnSuccess : kIOReturnNotFound;',
        '\t\tkr = *service ? kIOReturnSuccess : kIOReturnNotFound;'+block(
            '\t\ta52q_graphics_match(dict,kr,*service ? (*service)->getMetaClass()->getClassName() : "none","match");'))
    change('\t\t*existing = IOUserIterator::withIterator(found);\n\t\tkr = kIOReturnSuccess;',
        '\t\t*existing = IOUserIterator::withIterator(found);\n\t\tkr = kIOReturnSuccess;'+block(
            '\t\ta52q_graphics_match(dict,kr,*existing ? "iterator-created" : "no-iterator","match-many");'))
    begin=text.index('is_io_iterator_next(');end=text.index('/* Routine io_iterator_reset */',begin)
    part=text[begin:end];old='\t\t*object = obj;'
    if part.count(old)!=1:raise ValueError('graphics iterator anchor changed')
    text=text[:begin]+part.replace(old,old+block('\t\ta52q_graphics_next(obj);'))+text[end:]
    begin=text.index('is_io_service_open_extended(');end=text.index('/* Routine io_service_close */',begin)
    part=text[begin:end]
    # Ignore a disabled #if0 block but retain it byte-for-byte. Every active
    # explicit return is observed; CHECK's invalid-object return is unchanged.
    inactive=re.findall(r'#if 0\n.*?\n#endif',part,re.S)
    if len(inactive)!=1:raise ValueError('unexpected open disabled block')
    part=part.replace(inactive[0],'A52Q_INACTIVE_BLOCK')
    returns=list(re.finditer(r'(?m)^(\s*)return ([^;]+);',part))
    if [m[2] for m in returns]!=['kIOReturnBadArgument','kIOReturnBadArgument','kIOReturnNotPermitted','kIOReturnUnsupported','err']:
        raise ValueError('graphics open return paths changed')
    part=re.sub(r'(?m)^(\s*)return ([^;]+);',lambda m:
        block('\t\ta52q_graphics_open(service,connect_type,'+m[2]+',res,'+('true' if m[2]=='err' else 'false')+');')+m[0],part)
    part=part.replace('A52Q_INACTIVE_BLOCK',inactive[0])
    return text[:begin]+part+text[end:]
