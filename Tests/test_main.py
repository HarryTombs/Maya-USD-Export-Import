import maya.standalone
maya.standalone.initialize(name='Test')

import unittest
import maya.cmds as cmds

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

sys.path.append(src_path)

cmds.file(new=True, force=True)
cmds.polyCube(name='testCube', sx=5, sy=5, sz=5)
cmds.file(rn="test.ma")
cmds.file(save=True, type="mayaAscii")

import Export


class TestExporter(unittest.TestCase):

    def setUp(self):
        print("Saving")

        

    def test_select_all_but_cameras(self):
        selected = Export.SelectAllButCameras()
        self.assertEqual(selected, ['|testCube'])

if __name__ == '__main__':
    unittest.main()