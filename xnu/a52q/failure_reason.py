"""Reuse the upstream checked-copy heap observer for an opt-in backboardd probe."""
RECORDER = r'''
#if defined(ARM64_BOARD_CONFIG_A52Q)
#include <arm64/a52q_fb_console.h>
static unsigned a52q_reason_rank(const char *text)
{
    const char *needles[]={"NSInvalidArgumentException","Error getting shared system container","nil string parameter"};
    unsigned rank=0;size_t length=strlen(text);
    for (unsigned n=0;n<3;n++) {
        size_t size=strlen(needles[n]);
        for (size_t i=0;i+size<=length;i++)
            if (!memcmp(text+i,needles[n],size)) {rank=n+1;break;}
    }
    return rank;
}
static void a52q_reason_record(int pid,unsigned rank,const char *text)
{
    char body[208],line[240];
    int n=snprintf(body,sizeof(body),"%d/backboardd/%u/%.159s",pid,rank,text);
    if (n<=0 || (unsigned)n>=sizeof(body)) return;
    uint32_t crc=0xffffffffU;
    for (int i=0;i<n;i++) {
        crc^=(uint8_t)body[i];
        for (unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320U&(0U-(crc&1)));
    }
    n=snprintf(line,sizeof(line),"A52EX1 %s %08x\n",body,crc^0xffffffffU);
    if (n<=0 || (unsigned)n>=sizeof(line)) return;
    a52q_early_critical(line,(unsigned)n,7);
    for (unsigned i=0;i<3;i++) printf("%s",line);
}
'''


def helper(source):
    begin=source.index('static void\nsweet_crash_strings(const char *name)\n{')
    end=source.index('\n/*\n * SWEET process sampler',begin)
    code=source[begin:end]
    def replace(old,new):
        nonlocal code
        if code.count(old)!=1:raise ValueError('upstream exception observer anchor changed')
        code=code.replace(old,new,1)
    replace('sweet_crash_strings(const char *name)','a52q_crash_strings(const char *name, int pid)')
    start=code.index('\tif (!PE_parse_boot_argn(')
    stop=code.index('\tbuf = kalloc_data',start)
    code=code[:start]+'''    if (strcmp(name,"backboardd") ||
        !PE_parse_boot_argn("a52qscan",names,sizeof(names))) return;
    names[sizeof(names)-1]=0;
    if (strcmp(names,"backboardd")) return;
    unsigned best=0,regions=0;
'''+code[stop:]
    replace('while (lines < 700 && scanned < (96ull << 20))',
        'while (lines < 3 && scanned < (16ull << 20) && regions++ < 1024)')
    replace('\t\taddr += size;', '\t\tif (!size || addr > UINT64_MAX-size) break;\n\t\taddr += size;')
    replace('off < size && lines < 700;', 'off < size && lines < 3 && scanned < (16ull << 20);')
    replace('\t\t\tif (copyin(', '\t\t\tscanned += len; /* Bound attempted reads, including faults. */\n\t\t\tif (copyin(')
    replace('\t\t\tscanned += len; /* Bound attempted reads, including faults. */',
        '\t\t\tif (len > (16ull << 20)-scanned) len=(size_t)((16ull << 20)-scanned);\n\t\t\tscanned += len; /* Bound attempted reads, including faults. */')
    replace('\t\t\tscanned += len;\n','')
    replace('if (strncmp(text, last, sizeof(last) - 1) != 0) {',
        'unsigned rank=a52q_reason_rank(text);\n\t\t\t\t\tif (rank>best && strncmp(text, last, sizeof(last) - 1) != 0) {\n\t\t\t\t\t\tbest=rank;')
    replace('printf("STR %s\\n", text);','a52q_reason_record(pid,rank,text);')
    code=code.replace('STR scan of %s heap','A52Q exception-text probe of %s heap')
    code=code.replace('STR done:','A52Q exception-text probe done:')
    return RECORDER+code+'\n#endif\n'
