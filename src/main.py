import os
import maya.cmds as cmds
from pxr import Usd, UsdGeom, Gf

useSelected = False
stage = CreateUSDA()
print(cmds.ls(st=True))

def SeelctAll():
    selectedName = cmds.ls(tr=True, lt=True, l=True)
    if "|front" in selectedName:
        selectedName.remove("|front")
    if "|persp" in selectedName:
        selectedName.remove("|persp")
    if "|side" in selectedName:
        selectedName.remove("|side")
    if "|top" in selectedName:
        selectedName.remove("|top")
    # Im sure theres a way better way to do this
    return selectedName

def SelectCurrent():
    selectedName = cmds.ls(l=True, sl=True)
    print(selectedName)
    if not selectedName:
        print("Selection is empty")
    return selectedName

def CreateUSDA():

    scenePath = cmds.file(query=True, sceneName=True)

    if not scenePath:
        raise RuntimeError("Scene must be saved before determining save location.")

    sceneDir = os.path.dirname(scenePath)

    usd_output_path = os.path.join(sceneDir, "my_export2.usda")
    if os.path.isfile(usd_output_path) == True:
        stage = Usd.Stage.Open(usd_output_path)
        print(f"USD file found at: {usd_output_path}")
    else:
        stage = Usd.Stage.CreateNew(usd_output_path)
        print(f"USD file created at: {usd_output_path}")
    return stage 
    
def checkXform(xform, transType):
    for op in xform.GetOrderedXformOps():
        if op.GetOpType() == transType:
            return op    
    return xform.AddXformOp(transType)
        
def writeXform(obj,stage):
    xform = UsdGeom.Xform.Define(stage, f"/{obj.strip('|').replace('|', '/')}")
    
    pos = cmds.xform(obj, query=True, ws=True, t=True)
    rot = cmds.xform(obj, query=True, ws=True, ro=True)
    
    t_xform = checkXform(xform,UsdGeom.XformOp.TypeTranslate)
    r_xform = checkXform(xform,UsdGeom.XformOp.TypeRotateXYZ)



if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SeelctAll()
   

for obj in objList:
    print(cmds.objectType(obj,tt=True))
    #writeXform(obj,stage)
        
stage.GetRootLayer().Save()
    
    
    
    
    

