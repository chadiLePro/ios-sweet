"""Persistent data plans must preserve the root and bind captured geometry."""
import copy
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import a52q_persistent_data as data


class PersistentDataTests(unittest.TestCase):
    def setUp(self):
        self.root = dict(layout_kind=2, partition_index=31, partition_name='userdata',
            bytes=16<<30, sha256='a'*64, window=[3165696,27911647,3165696,4194304],
            gpt_crc32=[123,456],gpt_capture_sha256=hashlib.sha256(b'capture').hexdigest())
        self.image = dict(bytes=4<<30,sha256='b'*64,header_crc32=83,
            source_root_sha256='a'*64,volume=dict(bytes=4<<30,journaled=False))
        self.capture=MagicMock()
        self.capture.__truediv__.return_value.read_bytes.return_value=b'capture'
        self.report=dict(block_bytes=4096,disk_bytes=31077376*4096,
            partitions=[dict(index=31,name='userdata',first_lba=3165696,
                             block_count=27911647,bytes=27911647*4096)])
        with patch.object(data,'from_capture',return_value=self.report):
            self.plan=data.configuration(self.capture,self.root,self.image)

    def test_exact_extent_does_not_overlap_root_or_other_partitions(self):
        self.assertEqual(self.plan['window'],[3165696,27911647,7359999+1,1048576])
        self.assertEqual(self.plan['offset_in_partition_bytes'],17179869184)
        self.assertFalse(self.plan['runtime_implemented'])
        self.assertFalse(self.plan['write_approved'])
        for key,value in [('window',[3165696,27911647,3165696,1048576]),
                          ('window',[3165696,4194304,7360000,1048576]),
                          ('window',[3165696,27911647,7360001,1048576]),
                          ('window',[3165696,27911647,7360000,1048577]),
                          ('offset_in_partition_bytes',0),('partition_index',19),
                          ('partition_name','boot'),('root_sha256','c'*64),
                          ('source_root_sha256','c'*64),('sha256','x'),
                          ('bytes',96<<20),('volume',dict(bytes=4<<30,journaled=True)),
                          ('gpt_crc32',[123,457]),('gpt_capture_sha256','0'*64),
                          ('mount_target','/'),('runtime_implemented',True),('write_approved',True)]:
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):
                data.validate_config(dict(self.plan,**{key:value}),self.root)

    def test_rejects_changed_capture_or_geometry(self):
        for mutate in ('block_bytes','partition','capacity','capture'):
            report=copy.deepcopy(self.report)
            if mutate=='block_bytes':report['block_bytes']=512
            if mutate=='partition':report['partitions'][0]['first_lba']+=1
            if mutate=='capacity':report['disk_bytes']=1000
            if mutate=='capture':self.capture.__truediv__.return_value.read_bytes.return_value=b'changed'
            with self.subTest(mutate=mutate),patch.object(data,'from_capture',return_value=report),self.assertRaises(ValueError):
                data.configuration(self.capture,self.root,self.image)

    def test_rejects_unverified_or_wrong_master_before_reading(self):
        path=MagicMock();path.stat.return_value.st_mode=0o100644
        path.stat.return_value.st_size=4<<30
        for proof in ({},dict(bytes=4<<30,fsck_passed=True,
                             rsync_checksum_comparison_passed=True,source_subtree='/private/var',
                             source_master_sha256='c'*64)):
            with self.assertRaises(ValueError):data.inspect_data(path,proof,'a'*64)
        path.open.assert_not_called()
        path.stat.return_value.st_size=16<<30
        with self.assertRaises(ValueError):data.inspect_data(path,{},'a'*64)
        path.open.assert_not_called()


if __name__=='__main__':unittest.main()
