import sys,unittest
from pathlib import Path
from unittest.mock import MagicMock
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
import a52q_persistent_data as data
import test_a52q_persistent_data as fixtures


class RuntimeVarTests(unittest.TestCase):
    def setUp(self):
        self.base=fixtures.PersistentDataTests();self.base.setUp()
        self.snapshot=dict(format='a52q-runtime-var-v1',target='/dev/block/sda31',
            offset_bytes=16<<30,bytes=4<<30,sha256='c'*64,root_sha256='a'*64,
            source_boot_sha256='d'*64,source_kernel_sha256='e'*64,
            root_preserved=True,original_boot_restored=True,other_file_data_preserved=True,repair_changed_files={})

    def test_captured_var_requires_exact_source_extent_and_preservation_proof(self):
        data.validate_runtime_snapshot(self.snapshot,'a'*64)
        plan=dict(self.base.plan,runtime_snapshot=self.snapshot)
        data.validate_config(plan,self.base.root)
        self.assertFalse(plan['write_approved']);self.assertFalse(plan['runtime_implemented'])
        for key,value in [('target','/dev/block/sda19'),('offset_bytes',0),('bytes',16<<30),
                          ('root_sha256','b'*64),('source_boot_sha256','unknown'),
                          ('source_kernel_sha256','unknown'),('root_preserved',False),
                          ('original_boot_restored',False),('other_file_data_preserved',False),
                          ('bytes',True),('root_preserved',1)]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                data.validate_config(dict(plan,runtime_snapshot=dict(self.snapshot,**{key:value})),self.base.root)
        extra=dict(self.snapshot,unreviewed=True)
        with self.assertRaises(ValueError):data.validate_runtime_snapshot(extra,'a'*64)

    def test_invalid_or_ambiguous_runtime_proof_rejected_before_image_read(self):
        path=MagicMock();path.stat.return_value.st_mode=0o100644;path.stat.return_value.st_size=4<<30
        proof=dict(bytes=4<<30,fsck_passed=True,source_subtree='/private/var',
            source_master_sha256='a'*64,runtime_snapshot=self.snapshot,
            rsync_checksum_comparison_passed=True)
        with self.assertRaisesRegex(ValueError,'unchanged master'):data.inspect_data(path,proof,'a'*64)
        path.open.assert_not_called()
        proof['rsync_checksum_comparison_passed']=False
        proof['runtime_snapshot']=dict(self.snapshot,other_file_data_preserved=False)
        with self.assertRaises(ValueError):data.inspect_data(path,proof,'a'*64)
        path.open.assert_not_called()

    def test_only_observed_active_log_may_differ_after_repair(self):
        change=dict(before_sha256='1'*64,after_sha256='2'*64)
        snap=dict(self.snapshot,repair_changed_files={'log/com.apple.xpc.launchd/launchd.log':change})
        data.validate_runtime_snapshot(snap,'a'*64)
        for value in ({'keybags/systembag.kb':change},
                      {'log/com.apple.xpc.launchd/launchd.log':dict(change,after_sha256='invalid')},
                      {'log/com.apple.xpc.launchd/launchd.log':dict(change,after_sha256='1'*64)}):
            with self.assertRaises(ValueError):
                data.validate_runtime_snapshot(dict(snap,repair_changed_files=value),'a'*64)
