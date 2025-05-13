import maya.standalone
maya.standalone.initialize(name='Test')

import unittest
import os
import maya.cmds as cmds
from pxr import UsdGeom

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

sys.path.append(src_path)

cmds.file(new=True, force=True)

cmds.file(rn="test.ma")
cmds.file(save=True, type="mayaAscii")
cube = cmds.polyCube(name='testCube', sx=5, sy=5, sz=5)
sphere = cmds.polySphere(name='testSphere')
import Export

stage = Export.CreateUSDA("Export")
worldPrim = stage.DefinePrim("/World", "Xform")

usdPath = "/World/Prim"
usdMesh = UsdGeom.Mesh.Define(stage,usdPath)  
xform = UsdGeom.Xform(stage.GetPrimAtPath(usdPath))




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
    
    def test_check_xform(self):
        checkedXform = Export.checkXform(xform, UsdGeom.XformOp.TypeTranslate)
        self.assertIsInstance(checkedXform, UsdGeom.XformOp)
    def test_set_xform(self):
        Export.setXform(sphere,xform)
        pos = cmds.xform(sphere, query=True, ws=True, t=True)
        rot = cmds.xform(sphere, query=True, ws=True, ro=True)
        Ops = xform.GetOrderedXformOps()
        transValue = Ops[0].Get()
        rotValue = Ops[1].Get()
        self.assertEqual(transValue,pos)
        self.assertEqual(rotValue,rot)




class TestImporter(unittest.TestCase):
    def setUp(self):
        print("importing")
        return super().setUp()

if __name__ == '__main__':
    unittest.main()