"""Add A52-only software graphics guards to the fully patched upstream units.

Original Redmi paths and cached surface-lookup fix remain intact. No DSI,
clock, reset or allocator reservation changes occur in these transforms.
"""
import hashlib

PINS = {'SweetSurface.h': '3a3efd984200566285009001ca114aff39c3e6ee597a7ace9511ebdc75137425', 'SweetSurface.cpp': '2a4e100968439a0a72012b008d40d6ec4723515a9952f4ce1f4d178814b02dba', 'SweetFramebuffer.cpp': 'aa561c09542267087427deee903fb7afacb20e2265044a8e1b12586b5337565f', 'SweetWatchdog.cpp': '21df34ee7be7c60f9f9866d4e659ca610385e21007b4a7a61ab99afaeb9fb9e1'}


def transform(name, source):
    if name not in PINS or hashlib.sha256(source.encode()).hexdigest()!=PINS[name]:
        raise ValueError('unexpected patched software source: '+name)
    def change(old,new):
        nonlocal source
        if source.count(old)!=1:raise ValueError(name+': software ABI anchor changed')
        source=source.replace(old,new)
    change('#if defined(SWEET)', '#if defined(SWEET) || defined(A52Q)')
    if name=='SweetSurface.h': return source
    if name=='SweetSurface.cpp':
        change('#define SWEET_SURFACE_MAX_ALLOC         (256u << 20)',
            '#if defined(A52Q)\n#define SWEET_SURFACE_MAX_ALLOC (32u << 20)\n#else\n#define SWEET_SURFACE_MAX_ALLOC         (256u << 20)\n#endif')
        change('#define SWEET_SURFACE_WIRED_MAX         (1536ull << 20)',
            '#if defined(A52Q)\n#define SWEET_SURFACE_WIRED_MAX (96ull << 20)\n#else\n#define SWEET_SURFACE_WIRED_MAX         (1536ull << 20)\n#endif')
        change('#include "SweetSurface.h"','#include "SweetSurface.h"\n#if defined(A52Q)\n#include "a52q_ui_bridge.h"\n#include <pexpert/pexpert.h>\n#endif')
        change('\tIOLockLock(sweet_surface_lock);\n\tif (kernelMap == NULL && memory != NULL)',
            '#if defined(A52Q)\n\treturn a52q_ui_pixels();\n#endif\n\tIOLockLock(sweet_surface_lock);\n\tif (kernelMap == NULL && memory != NULL)')
        change('\tSweetSurface *s = sweet_surface_alloc();\n\tif (s == NULL) {\n\t\treturn NULL;',
            '#if defined(A52Q)\n\tif (!a52q_ui_physical_allowed(phys,width,height,bytesPerRow)) return NULL;\n#endif\n\tSweetSurface *s = sweet_surface_alloc();\n\tif (s == NULL) {\n\t\treturn NULL;')
        change('\ts->mapCache = kIOMapWriteCombineCache;',
            '#if defined(A52Q)\n\ts->mapCache = kIOMapInhibitCache; /* Match the clean physical RGB probe. */\n#else\n\ts->mapCache = kIOMapWriteCombineCache;\n#endif')
        change('IOCoreSurfaceRoot::start(IOService *provider)\n{',
            'IOCoreSurfaceRoot::start(IOService *provider)\n{\n#if defined(A52Q)\n\tint ui=0;\n\tif (!PE_parse_boot_argn("a52q_ui",&ui,sizeof(ui)) || ui!=1) return false;\n#endif')
    elif name=='SweetFramebuffer.cpp':
        change('#include "SweetSurface.h"', '#include "SweetSurface.h"\n#if defined(A52Q)\n#include "a52q_ui_bridge.h"\n#include "a52q_ui_copy.h"\n#endif')
        change('#include "a52q_ui_copy.h"','#include "a52q_ui_copy.h"\n#include "a52q_fb_console.h"')
        change('\tvoid present(const uint8_t *rec);',
            '\tvoid present(const uint8_t *rec);\n#if defined(A52Q)\n\tbool handoffConsole();\n#endif')
        change('OSDefineMetaClassAndStructors(AppleCLCD, IOMobileFramebuffer);',
            'OSDefineMetaClassAndStructors(AppleCLCD, IOMobileFramebuffer);\n'
            '#if defined(A52Q)\n'
            'static IOReturn\na52q_console_handoff_action(OSObject *, void *, void *, void *, void *)\n{\n'
            '\treturn a52q_fb_console_handoff() ? kIOReturnSuccess : kIOReturnNotReady;\n}\n'
            'bool\nAppleCLCD::handoffConsole()\n{\n'
            '\t/* Timer rendering and surface export share the recursive workloop gate. */\n'
            '\treturn fWorkLoop && fWorkLoop->runAction(a52q_console_handoff_action, this)==kIOReturnSuccess;\n}\n#endif')
        change('\t\tout[0] = sweet_surface_port_in_task(fFB->fSurface, fTask);',
            '#if defined(A52Q)\n\t\tif (!fFB->handoffConsole()) return kIOReturnNotReady;\n#endif\n'
            '\t\tout[0] = sweet_surface_port_in_task(fFB->fSurface, fTask);')
        change('AppleCLCD::present(const uint8_t *rec)\n{',
            'AppleCLCD::present(const uint8_t *rec)\n{\n#if defined(A52Q)\n\tif (!a52q_fb_console_handoff()) { swap(rec); return; }\n#endif')
        change('AppleCLCD::vsyncFired(OSObject *owner, IOTimerEventSource *sender)\n{',
            'AppleCLCD::vsyncFired(OSObject *owner, IOTimerEventSource *sender)\n{\n#if defined(A52Q)\n\ta52q_fb_console_tick(0);\n#endif')
        change('\tAppleCLCD *fb = (AppleCLCD *)owner;',
            '\tAppleCLCD *fb = (AppleCLCD *)owner;\n#if defined(A52Q)\n'
            '\tIOLockLock(fb->fLock);\n\tunsigned a52off=fb->fPowerOff;\n\tIOLockUnlock(fb->fLock);\n'
            '\ta52q_ui_heartbeat(a52off);\n#endif')
        change('\t\t    args->scalarOutputCount, args->structureOutputSize, ret);',
            '\t\t    args->scalarOutputCount, args->structureOutputSize, ret);\n#if defined(A52Q)\n'
            '\t\tstatic unsigned a52logged;\n'
            '\t\tif (__atomic_fetch_add(&a52logged,1U,__ATOMIC_RELAXED)<64) {\n'
            '\t\t\tchar body[168];\n'
            '\t\t\tsnprintf(body,sizeof(body),"call proc=%.16s pid=%d sel=%u ret=%08x out=%u/%llx/%llx in=%u/%u",\n'
            '\t\t\t    name,proc_selfpid(),selector,ret,outCount,(unsigned long long)out[0],(unsigned long long)out[1],\n'
            '\t\t\t    args->scalarInputCount,args->structureInputSize);\n'
            '\t\t\ta52q_ui_observe(5,body);\n\t\t}\n#endif')
        change('extern "C" int sweet_console_muted;     /* osfmk/console/serial_console.c */',
            '#if defined(SWEET)\nextern "C" int sweet_console_muted;     /* osfmk/console/serial_console.c */\n#endif')
        change('\tPE_Video video;', '#if defined(SWEET)\n\tPE_Video video;\n#endif')
        change('\tPE_current_console(&video);\n\tfPhys = video.v_baseAddr;\n\tfWidth = (uint32_t)video.v_width;\n\tfHeight = (uint32_t)video.v_height;\n\tfRowBytes = (uint32_t)video.v_rowBytes;',
            '#if defined(A52Q)\n\tif (!a52q_ui_framebuffer(&fPhys,&fWidth,&fHeight,&fRowBytes)) return false;\n#else\n\tPE_current_console(&video);\n\tfPhys = video.v_baseAddr;\n\tfWidth = (uint32_t)video.v_width;\n\tfHeight = (uint32_t)video.v_height;\n\tfRowBytes = (uint32_t)video.v_rowBytes;\n#endif')
        change('\tPE_parse_boot_argn("sweetfb_native", &native, sizeof(native));',
            '\tPE_parse_boot_argn("sweetfb_native", &native, sizeof(native));\n#if defined(A52Q)\n\tnative=1;\n#endif')
        change('\tfFlushTicks = (hz == 0 || hz >= 60) ? 1 : 60 / hz;',
            '\tfFlushTicks = (hz == 0 || hz >= 60) ? 1 : 60 / hz;\n#if defined(A52Q)\n\tfFlushTicks=1; /* software timer 16667us; physical panel Hz unproven */\n#endif')
        change('\t\t\tsweet_console_muted = 1;', '#if defined(SWEET)\n\t\t\tsweet_console_muted = 1;\n#endif')
        old='\t\t\t\tmemcpy((void *)(fPixels + (uint64_t)(dy + y) * fRowBytes + (uint64_t)dx * 4),\n\t\t\t\t    (const void *)(src + s->offset + (uint64_t)(sy + y) * s->bytesPerRow + (uint64_t)sx * 4),\n\t\t\t\t    (size_t)w * 4);'
        a52copy='\t\t\t(void)a52q_ui_copy_rect((volatile uint32_t *)fPixels,(uint64_t)fRowBytes*fHeight,fWidth,fHeight,fRowBytes,\n\t\t\t    (const uint8_t *)src,s->memory->getLength(),s->width,s->height,s->bytesPerRow,s->offset,sx,sy,dx,dy,w,h);'
        oldloop='\t\t\tfor (int32_t y = 0; y < h; y++) {\n'+old+'\n\t\t\t}'
        new='#if defined(A52Q)\n'+a52copy+'\n#else\n'+oldloop+'\n#endif'
        old=oldloop
        change(old,new)
        change('\t\tif (src != 0 && bpe == 4) {', '#if defined(A52Q)\n\t\tif (s->pixelFormat!=SWEET_FB_FORMAT_BGRA) src=0;\n#endif\n\t\tif (src != 0 && bpe == 4) {')
        change('\t\ts->release();\n\t}\n}\n\nbool\nIOMobileFramebufferUserClient::initWithTask',
            '\t\ts->release();\n\t}\n#if defined(A52Q)\n\t(void)a52q_ui_flush();\n#endif\n}\n\nbool\nIOMobileFramebufferUserClient::initWithTask')
        change('\t\tsender->setTimeoutUS(SWEET_FB_VSYNC_US);\n\t\treturn;',
            '#if defined(A52Q)\n\t\tif (step<=6) (void)a52q_ui_flush();\n#endif\n\t\tsender->setTimeoutUS(SWEET_FB_VSYNC_US);\n\t\treturn;')
    elif name=='SweetWatchdog.cpp':
        change('#include <sys/proc.h>', '#include <sys/proc.h>\n#if defined(A52Q)\n#include <pexpert/pexpert.h>\n#endif')
        change('IOWatchdog::start(IOService *provider)\n{',
            'IOWatchdog::start(IOService *provider)\n{\n#if defined(A52Q)\n\tint ui=0;\n\tif (!PE_parse_boot_argn("a52q_ui",&ui,sizeof(ui)) || ui!=1) return false;\n#endif')
    return source
