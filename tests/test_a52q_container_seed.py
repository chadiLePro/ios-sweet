import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from a52q_persistent_data import CONTAINER_DIRECTORIES,validate_container_directories


class ContainerSeedTests(unittest.TestCase):
    def test_exact_scaffold_and_reject_unreviewed_permissions_or_paths(self):
        validate_container_directories(copy.deepcopy(CONTAINER_DIRECTORIES))
        for value in ({},dict(CONTAINER_DIRECTORIES,unexpected={}),None,[]):
            with self.assertRaises(ValueError):validate_container_directories(value)
        for key,value in (('uid',501),('gid',501),('mode','0777'),('uid',False),('gid',0.0)):
            changed=copy.deepcopy(CONTAINER_DIRECTORIES)
            changed['containers'][key]=value
            with self.assertRaises(ValueError):validate_container_directories(changed)
