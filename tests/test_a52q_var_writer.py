import os,shutil,subprocess,tempfile,unittest,sys,zlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]


class VarWriterTests(unittest.TestCase):
    def test_probe_decoder_rejects_modified_or_unrelated_records(self):
        sys.path.insert(0,str(R/'tools'));from a52q_var_write_trace import decode
        body=b'0000000000000051/10/00000000/00000000/21000000'
        line=b'A52W1 '+body+b' %08x\n'%zlib.crc32(body)
        result=decode(line*3,81)
        self.assertTrue(result['identical_block_probe_passed'])
        self.assertEqual(result['records'][0]['valid_copies'],3)
        self.assertFalse(decode(line,82)['identical_block_probe_passed'])
        self.assertFalse(decode(line.replace(b'/10/',b'/11/'),81)['identical_block_probe_passed'])
        body=body.replace(b'/00000000/',b'/00000005/',1)
        with self.assertRaises(ValueError):decode(b'A52W1 '+body+b' %08x\n'%zlib.crc32(body),81)

    def test_native_packets_boundaries_rmw_and_failures(self):
        cc='C:/winlibs/mingw64/bin/gcc.exe' if os.name=='nt' else shutil.which('cc')
        if not cc:self.skipTest('native compiler unavailable')
        code=r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include "ufs_nop_protocol.h"
#include "a52q_ufs_bounds.h"
#include "a52q_var_bounds.h"
#include "a52q_var_write_protocol.h"
#include "a52q_var_write_plan.h"
static uint64_t root[4]={100,6000000,100,4194304};
static uint64_t var[4]={100,6000000,4194404,1048576};
static uint8_t blocks[3][4096],bounce[4096],source[8192];
static unsigned reads,writes,fail_read,fail_write;
static int index_for(uint32_t lba){
 assert(lba>=var[2] && lba<var[2]+var[3]);
 if(lba==var[2])return 0;
 if(lba==var[2]+1)return 1;
 assert(lba==var[2]+var[3]-1);return 2;
}
static int read_block(void *ctx,uint32_t lba,uint8_t *out){
 assert(!ctx);++reads;if(fail_read==reads)return 5;
 memcpy(out,blocks[index_for(lba)],4096);return 0;
}
static int write_block(void *ctx,uint32_t lba,const uint8_t *in){
 assert(!ctx);++writes;if(fail_write==writes)return 6;
 memcpy(blocks[index_for(lba)],in,4096);return 0;
}
static int run(uint64_t offset,uint32_t bytes,uint32_t *done){
 return a52q_var_write_bytes(root,var,7000000,offset,source,bytes,bounce,
  read_block,write_block,0,done,22);
}
int main(void){
 uint32_t list[8]={0},prdt[4]={0};uint8_t request[3072]={0};
 a52q_var_write_packet(list,request,prdt,0x12345678000ULL,0x23456789000ULL,0x12345678);
 assert(list[0]==0x13000000 && (list[7]&0xffff)==1);
 assert(prdt[0]==0x56789000 && prdt[1]==0x234 && prdt[3]==4095);
 assert(request[0]==1 && request[1]==0x20 && !request[2] && !request[3]);
 assert(request[12]==0 && request[13]==0 && request[14]==0x10 && request[15]==0);
 assert(request[16]==0x2a && request[17]==0 && request[18]==0x12 && request[19]==0x34);
 assert(request[20]==0x56 && request[21]==0x78 && request[24]==1);
 memset(list,0,sizeof(list));memset(request,0,sizeof(request));
 a52q_var_sync_packet(list,request,0x12345678000ULL);
 assert(list[0]==0x11000000 && !(list[7]&0xffff));
 assert(request[0]==1 && request[16]==0x35);
 for(unsigned i=0;i<32;i++)if(i!=0 && i!=16)assert(!request[i]);
 uint32_t lba=0xdeadbeef,done=99;
 assert(a52q_var_write_lba(root,var,7000000,0,4096,&lba) && lba==var[2]);
 assert(a52q_var_write_lba(root,var,7000000,(4ULL<<30)-4096,4096,&lba) && lba==var[2]+var[3]-1);
 assert(!a52q_var_write_lba(root,var,7000000,4ULL<<30,4096,&lba));
 assert(!a52q_var_write_lba(root,var,7000000,1,4096,&lba));
 assert(!a52q_var_write_lba(root,var,7000000,UINT64_MAX-4095,4096,&lba));
 assert(!a52q_var_write_lba(root,var,(uint32_t)var[2],0,4096,&lba));
 memset(blocks,0x44,sizeof(blocks));memset(source,0xaa,sizeof(source));
 assert(!run(4090,20,&done) && done==20 && reads==2 && writes==2);
 for(unsigned i=0;i<4090;i++)assert(blocks[0][i]==0x44);
 for(unsigned i=4090;i<4096;i++)assert(blocks[0][i]==0xaa);
 for(unsigned i=0;i<14;i++)assert(blocks[1][i]==0xaa);
 for(unsigned i=14;i<4096;i++)assert(blocks[1][i]==0x44);
 assert(!run((4ULL<<30)-512,512,&done) && done==512);
 assert(blocks[2][3583]==0x44 && blocks[2][3584]==0xaa);
 unsigned old=reads+writes;
 assert(run((4ULL<<30)-1,2,&done)==22 && !done && reads+writes==old);
 assert(run(UINT64_MAX,1,&done)==22 && !done && reads+writes==old);
 assert(!run(4ULL<<30,0,&done) && !done && reads+writes==old);
 var[2]--;assert(run(0,1,&done)==22 && !done && reads+writes==old);var[2]++;
 fail_read=reads+1;assert(run(1,1,&done)==5 && !done);fail_read=0;
 fail_write=writes+1;assert(run(0,4096,&done)==6 && !done);fail_write=0;
 /* Full-block writes skip reads; partial completion remains exact on error. */
 fail_write=writes+2;unsigned before=reads;
 assert(run(0,8192,&done)==6 && done==4096 && reads==before);
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'writer.c';path.write_text(code)
            exe=Path(directory)/('writer.exe' if os.name=='nt' else 'writer')
            result=subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror',
                '-I',str(R/'shim/a52q'),'-I',str(R/'xnu/a52q'),str(path),'-o',str(exe)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            result=subprocess.run([str(exe)],capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
