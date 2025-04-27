import os
import maya.cmds as cmds
from pxr import Usd, UsdGeom, Gf, UsdLux

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

    if not scenePath:
        raise RuntimeError("Scene must be saved before determining save location.")

    sceneDir = os.path.dirname(scenePath)
    usdOutputPath = os.path.join(sceneDir, "my_export1.usda")
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

def writeMesh(obj, stage):
    
    import maya.api.OpenMaya as om
    
    select = om.MSelectionList()
    select.add(obj)
    dagPath = select.getDagPath(0)
    
    meshFN = om.MFnMesh(dagPath)
    
  #  print(meshFN)
    
    usdPath = "/" + obj.replace("|","/").strip("/")
    
   # print(usdPath)
    
    usdMesh = UsdGeom.Mesh.Define(stage,usdPath)
    
   # print(usdMesh)
    
    
    array = meshFN.getPoints(om.MSpace.kWorld)
    
    #print(array)
    
    points = []
    
    count = 0
    
    for pt in array:
        count += 1
        currentpoint = [*pt]
        Vec3list = [Gf.Vec3f(currentpoint[:-1])]
        points = points + Vec3list
    usdMesh.GetPointsAttr().Set(points)
    
    counts, indices = meshFN.getVertices()
    
    usdMesh.GetFaceVertexCountsAttr().Set(counts)
    usdMesh.GetFaceVertexIndicesAttr().Set(indices)

    
stage = CreateUSDA()


if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SeelctAll()
   

for obj in objList:
    if cmds.listRelatives(obj, s=True, typ="mesh"):
        print("mesh")
        writeXform(obj,stage)
        writeMesh(obj,stage)
    elif cmds.listRelatives(obj, s=True, typ="camera"):  
        print("Camera")  
        #writeCam(obj,stage)
   # writeXform(obj,stage)
        
stage.GetRootLayer().Save()
    
    
    
    
    

