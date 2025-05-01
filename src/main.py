import os
import maya.cmds as cmds
from pxr import Usd, UsdGeom, Gf, UsdLux, UsdSkel

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
    usdOutputPath = os.path.join(sceneDir, "my_export5.usda")
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
    usdPath = "/" + obj.replace("|","/").strip("/")
    usdMesh = UsdGeom.Mesh.Define(stage,f"/World{usdPath}")  
    array = meshFN.getPoints(om.MSpace.kTransform)
    points = []
    if cmds.keyframe(obj,q =True,kc =True)>1:
        print("keyframes")
    if cmds.keyframe(obj,q =True,kc =True)<1:
        print("no keyframes")
#    for frame in rannge
    for pt in array:
        currentpoint = [*pt]
        Vec3list = [Gf.Vec3f(currentpoint[:-1])]
        points = points + Vec3list
    usdMesh.GetPointsAttr().Set(points)
    counts, indices = meshFN.getVertices()
    usdMesh.GetFaceVertexCountsAttr().Set(counts)
    usdMesh.GetFaceVertexIndicesAttr().Set(indices)
    
    
def writeCam(obj, stage):
    
    camPath = "/" + obj.replace("|", "/").strip("/")
    usdCam = UsdGeom.Camera.Define(stage, f"/World{camPath}")
    
    translate = cmds.xform(obj, q=True, ws=True, t=True)
    rotate = cmds.xform(obj, q=True, ws=True, ro=True)
    
    shape = cmds.listRelatives(obj, shapes=True)[0]
    focalLength = cmds.getAttr(f"{shape}.focalLength")
    
    horiAperture = cmds.getAttr(f"{shape}.horizontalFilmAperture")
    vertAperture = cmds.getAttr(f"{shape}.verticalFilmAperture")    
    
    
    #FIXME if already written to file don't use Add.Set
    
    usdCam.AddTranslateOp().Set(Gf.Vec3d(*translate))
    usdCam.AddRotateXYZOp().Set(Gf.Vec3f(*rotate))
    

    usdCam.GetFocalLengthAttr().Set(focalLength)
    
    usdCam.GetHorizontalApertureAttr().Set(horiAperture)
    usdCam.GetVerticalApertureAttr().Set(vertAperture)
    
    #If frame number > 0 then it'll be animated
    #I probably don't need to check for this
    
def WriteRig(obj,stage):
    
    skelRootPath = cmds.ls(obj,sn=True)
    UsdSkel.Root.Define(stage,f"/World/{skelRootPath[0]}")
    skelPath = (f"/World/{skelRootPath[0]}/Skel")
    skeleton = UsdSkel.Skeleton.Define(stage,skelPath)
    
    joints = cmds.listRelatives(obj,ad=True,type='joint')
    bindPoseMat4 = []
    restPoseMat4 = []
    jointOrder = []
    for J in joints:
        jointOrder.append(J)
        bindPose = cmds.getAttr(f"{J}.bindPose")
        restPose = cmds.getAttr(f"{J}.matrix")
        #print(bindPose)
        if bindPose != None:
            bindPoseMat4.append(Gf.Matrix4d(bindPose[0],bindPose[1],bindPose[2],bindPose[3],bindPose[4],bindPose[5],bindPose[6],bindPose[7],bindPose[8],bindPose[9],bindPose[10],bindPose[11],bindPose[12],bindPose[13],bindPose[14],bindPose[15]))
        else:
            bindPoseMat4.append(Gf.Matrix4d()) # some of them were none so they're getting an identity matrix
        restPoseMat4.append(Gf.Matrix4d(restPose[0],restPose[1],restPose[2],restPose[3],restPose[4],restPose[5],restPose[6],restPose[7],restPose[8],restPose[9],restPose[10],restPose[11],restPose[12],restPose[13],restPose[14],restPose[15]))
    #print(bindPoseMat4)
    skeleton.CreateJointsAttr(jointOrder)
    skeleton.CreateBindTransformsAttr().Set(bindPoseMat4)
    skeleton.CreateRestTransformsAttr().Set(restPoseMat4)

    
    shapes = cmds.listRelatives(obj, ad =True, fullPath=True) or []
    for shape in shapes:
        history = cmds.listHistory(shape)
        skinClusters = cmds.ls(history, type='skinCluster')
        for sc in skinClusters:
            geometry = cmds.skinCluster(sc, q=True, g=True)
            # Get the joints influencing the skinCluster
            joints = cmds.skinCluster(sc, q=True, inf=True)
            #print(sc)
            #print(geometry)
            #print(joints)
            
stage = CreateUSDA()

worldPrim = stage.DefinePrim("/World", "Xform")

stage.SetStartTimeCode(int(cmds.playbackOptions(q=True, min=True)))
stage.SetEndTimeCode(int(cmds.playbackOptions(q=True, max=True)))
stage.SetTimeCodesPerSecond(int(cmds.playbackOptions(q=True, fps=True)))
 
if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SeelctAll()

#write world base xform

for obj in objList:
    #keys = cmds.keyframe(obj,q =True,kc =True)
    #print(keys)

    if cmds.listRelatives(obj, s=True, typ="mesh"):
        print("mesh")
        #writeXform(obj,stage)
        #writeMesh(obj,stage)
        
    elif cmds.listRelatives(obj, s=True, typ="camera"):  
        print("Camera")  
        writeCam(obj,stage)
        #writeXform(obj,stage)
    elif cmds.listRelatives(obj,ad=True,type='joint'): #we're assuming this is a rigged mesh
        print("Joints")
        WriteRig(obj,stage)
               
        
        
stage.GetRootLayer().Save()
    
    
    
    
    

 