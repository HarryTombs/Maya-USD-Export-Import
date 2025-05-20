import maya.standalone
maya.standalone.initialize(name='Test')

import unittest
import maya.cmds as cmds
import maya.api.OpenMaya as om
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
cam = cmds.camera(name='testCamera1')
import Export

stage = Export.create_usda("Export")
worldPrim = stage.DefinePrim("/World", "Xform")

usdPath = "/World/Prim"
usdMesh = UsdGeom.Mesh.Define(stage,usdPath)  
xform = UsdGeom.Xform(stage.GetPrimAtPath(usdPath))


class TestExporter(unittest.TestCase):

    def setUp(self):
        return super().setUp()    

    def test_select_all_but_cameras(self):
        selected = Export.select_all_but_cameras()
        self.assertEqual(selected, ['|testCube','|testSphere','|testCamera1'])
        self.assertNotIn('|persp',selected)

    def test_select_Current(self):
        cmds.select('testSphere')
        selected = Export.select_current()
        self.assertEqual(selected,['|testSphere'])

    def test_create_USDA(self):
        USDA_Export = Export.create_usda("Export")
        self.assertEqual(os.path.basename(USDA_Export.GetRootLayer().identifier),'Export.usda')
    
    def test_check_xform(self):
        checkedXform = Export.check_xform(xform, UsdGeom.XformOp.TypeTranslate)
        self.assertIsInstance(checkedXform, UsdGeom.XformOp)

    def test_set_xform(self):
        Export.set_xform(sphere,xform)
        pos = cmds.xform(sphere, query=True, ws=True, t=True)
        rot = cmds.xform(sphere, query=True, ws=True, ro=True)
        Ops = xform.GetOrderedXformOps()
        transValue = Ops[0].Get()
        rotValue = Ops[1].Get()
        self.assertEqual(transValue,pos)
        self.assertEqual(rotValue,rot)

    def test_write_mesh(self):
        cmds.select('testSphere')
        useSphere = Export.select_current()
        Export.write_mesh(useSphere[0],stage,usdPath)
        pos = cmds.xform(sphere, query=True, ws=True, t=True)
        rot = cmds.xform(sphere, query=True, ws=True, ro=True)
        Ops = xform.GetOrderedXformOps()
        transValue = Ops[0].Get()
        rotValue = Ops[1].Get()
        self.assertEqual(transValue,pos)
        self.assertEqual(rotValue,rot)


    def test_write_cam(self):
        Export.write_cam(cam,stage,usdPath)
        pos = cmds.xform(cam, query=True, ws=True, t=True)
        rot = cmds.xform(cam, query=True, ws=True, ro=True)
        Ops = xform.GetOrderedXformOps()
        transValue = Ops[0].Get()
        rotValue = Ops[1].Get()
        self.assertEqual(transValue,pos)
        self.assertEqual(rotValue,rot)

    def test_execute_export_all(self):
        Export.execute_export(
            name="ExportTestAll",
            unreal_project="DummyProject",
            use_selected=False,
            start_frame=1,
            end_frame=1,
            frame_time_code=24.0
        )
        scene_path = cmds.file(query=True, sceneName=True)
        scene_dir = os.path.dirname(scene_path)
        usd_output_path = os.path.join(scene_dir, "ExportTestAll.usda")
        self.assertTrue(os.path.isfile(usd_output_path))




class TestImporter(unittest.TestCase):
    def setUp(self):
        print("importing")
        return super().setUp()

if __name__ == '__main__':
    unittest.main()