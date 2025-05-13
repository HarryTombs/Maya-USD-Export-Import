import maya.standalone
maya.standalone.initialize(name='Test')

import unittest
import os
import maya.cmds as cmds

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

sys.path.append(src_path)

cmds.file(new=True, force=True)

cmds.file(rn="test.ma")
cmds.file(save=True, type="mayaAscii")
cmds.polyCube(name='testCube', sx=5, sy=5, sz=5)
cmds.polySphere(name='testSphere')
import Export


class TestExporter(unittest.TestCase):

    def setUp(self):
        print("Saving")       

    def test_select_all_but_cameras(self):
        selected = Export.SelectAllButCameras()
        self.assertEqual(selected, ['|testCube','|testSphere'])

    def test_select_Current(self):
        cmds.select('testSphere')
        selected = Export.SelectCurrent()
        self.assertEqual(selected,['|testSphere'])

    def test_create_USDA(self):
        USDA_Export = Export.CreateUSDA("Export")
        self.assertEqual(os.path.basename(USDA_Export.GetRootLayer().identifier),'Export.usda')

if __name__ == '__main__':
    unittest.main()