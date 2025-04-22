import os
import maya.cmds as cmds
from pxr import Usd, UsdGeom, Gf

useSelected = True

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
    print(scenePath)

    if not scenePath:
        raise RuntimeError("Scene must be saved before determining save location.")

    sceneDir = os.path.dirname(scenePath)
    print(sceneDir)

    usd_output_path = os.path.join(sceneDir, "my_export.usda")
    if os.path.isfile(usd_output_path) == True:
        stage = Usd.Stage.Open(usd_output_path)
    else:
        stage = Usd.Stage.CreateNew(usd_output_path)
        print(f"USD file created at: {usd_output_path}")
    return stage 


if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SeelctAll()
    
stage = CreateUSDA()

print(objList)
    

for obj in objList:
    pos = cmds.getAttr(obj+".translate")
    rot = cmds.getAttr(obj+".rotate")
    scale = cmds.getAttr(obj+".scale")  
    print(pos,rot,scale)  
    
    usdPath = obj.replace("|","/")
    usdPath = "/" + usdPath.strip("/")
    xform = UsdGeom.Xform.Define(stage, usdPath)
    
    #xform.AddTranslateOp().Set(Gf.Vec3d(*pos))
    #xform.AddRotateXYZOp().Set(Gf.Vec3d(*rot))
    #xform.AddScaleOp().Set(Gf.Vec3d(*scale))
    
stage.GetRootLayer().Save()
    
    
    
    
    

