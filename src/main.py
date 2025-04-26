import os
import maya.cmds as cmds
from pxr import Usd, UsdGeom, Gf, UsdLux

useSelected = True

## FIX THE SET ISSUE, you can't rewrite over with sets
## for each type: mesh, cam, light, etc make an array of details
## the using the list relatives do the shape. something something
## for each attrib in attributes[] shape.attrib
## so would be end up with shape.horizontalaperture and bing bang boom
## then you've got a vairable that can be check in a for loop with checkXform()

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
    if not selectedName:
        print("Selection is empty")
    return selectedName

def CreateUSDA():

    scenePath = cmds.file(query=True, sceneName=True)

    if not scenePath:
        raise RuntimeError("Scene must be saved before determining save location.")

    sceneDir = os.path.dirname(scenePath)
    usdOutputPath = os.path.join(sceneDir, "my_export7.usda")
    if os.path.isfile(usdOutputPath) == True:
        stage = Usd.Stage.Open(usdOutputPath)
        print(f"USD file found at: {usdOutputPath}")
    else:
        stage = Usd.Stage.CreateNew(usdOutputPath)
        print(f"USD file created at: {usdOutputPath}")
    return stage 
    
def checkXform(xform, transType,input):
    for op in xform.GetOrderedXformOps():
        if op.GetOpType() == transType:
            return op
    return xform.AddXformOp(transType)

        
def writeXform(obj,stage):
    xform = UsdGeom.Xform.Define(stage, f"/{obj.strip('|').replace('|', '/')}")
    
    pos = cmds.xform(obj, query=True, ws=True, t=True)
    rot = cmds.xform(obj, query=True, ws=True, ro=True)
    
    t_xform = checkXform(xform,UsdGeom.XformOp.TypeTranslate,pos)
    r_xform = checkXform(xform,UsdGeom.XformOp.TypeRotateXYZ,rot)
    t_xform.Set(Gf.Vec3f(pos[0],pos[1],pos[2]))
    r_xform.Set(Gf.Vec3f(rot[0],rot[1],rot[2]))


    
stage = CreateUSDA()


if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SeelctAll()
   

for obj in objList:
    if cmds.listRelatives(obj, s=True, typ="mesh"):
        print("mesh")
        writeXform(obj,stage)
        #writeMesh(obj,stage)
    elif cmds.listRelatives(obj, s=True, typ="camera"):  
        print("Camera")  
        #writeCam(obj,stage)
   # writeXform(obj,stage)
        
stage.GetRootLayer().Save()
    
    
    
    
    

