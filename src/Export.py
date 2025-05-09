import os
import maya.cmds as cmds
from pxr import Usd, UsdGeom, Gf, Vt, Sdf, UsdSkel

useSelected = True

startFrame = cmds.playbackOptions(q=True, min=True)
endFrame = cmds.playbackOptions(q=True, max=True)
frameTimeCode = 24.0


def SelectAllButCameras():
    exclude = {"|front","|persp","|side","|top"}
    selected = cmds.ls(tr=True, lt=True, l=True)
    return [obj for obj in selected if obj not in exclude]
    #thanks Jon

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
    
    
    
def WriteRig(obj,stage):
    
    skelRootPath = cmds.ls(obj,sn=True)
    SkelRoot = UsdSkel.Root.Define(stage,f"/World/{skelRootPath[0]}")
    skelPath = (f"/World/{skelRootPath[0]}/Skel")
    skeleton = UsdSkel.Skeleton.Define(stage,skelPath)
    skelAnimPath = (f"/World/{skelRootPath[0]}/Anim")
    skelAnim = UsdSkel.Animation.Define(stage,skelAnimPath)
    skelPrim = stage.GetPrimAtPath(skelPath)
    binding = UsdSkel.BindingAPI.Apply(skelPrim)
    binding.CreateAnimationSourceRel().SetTargets([Sdf.Path(skelAnimPath)])

    
    attr = skelAnim.CreateRotationsAttr()
    
    joints = cmds.listRelatives(obj,ad=True,type='joint')
    bindPoseMat4 = []
    restPoseMat4 = []
    jointOrder = []
    allRotations = []
    cmds.currentTime(1, edit= True)
    for J in joints:
        jointOrder.append(J)
        bindPose = cmds.getAttr(f"{J}.bindPose")
        restPose = cmds.getAttr(f"{J}.matrix")
        if bindPose != None:
            bindPoseMat4.append(Gf.Matrix4d(bindPose[0],bindPose[1],bindPose[2],bindPose[3],bindPose[4],bindPose[5],bindPose[6],bindPose[7],bindPose[8],bindPose[9],bindPose[10],bindPose[11],bindPose[12],bindPose[13],bindPose[14],bindPose[15]))
        else:
            bindPoseMat4.append(Gf.Matrix4d()) # some of them were none so they're getting an identity matrix
        restPoseMat4.append(Gf.Matrix4d(restPose[0],restPose[1],restPose[2],restPose[3],restPose[4],restPose[5],restPose[6],restPose[7],restPose[8],restPose[9],restPose[10],restPose[11],restPose[12],restPose[13],restPose[14],restPose[15]))
    
    num = 0
    for frame in range(int(startFrame), int(endFrame) + 1):
        

        cmds.currentTime(frame, edit= True)
        frameQuats = []
        for joints in jointOrder:
            matrix = cmds.xform(joints, q=True, matrix=True,ws=True)
            gfMatrix = Gf.Matrix4d(*matrix)
            rotationQuat = gfMatrix.ExtractRotationQuat()
            imagine = rotationQuat.GetImaginary()
            quat = Gf.Quatf(rotationQuat.GetReal(),imagine[0],imagine[1],imagine[2])
            frameQuats.append(quat)
        allRotations.append(Vt.QuatfArray(frameQuats))
        
        
    skeleton.CreateJointsAttr(jointOrder)
    skeleton.CreateBindTransformsAttr().Set(bindPoseMat4)
    skeleton.CreateRestTransformsAttr().Set(restPoseMat4)
    skelAnim.CreateJointsAttr().Set(jointOrder)
    rotAttr = skelAnim.CreateRotationsAttr()
    
    for frame, rotList in enumerate(allRotations, start=1):
        vt_quats = Vt.QuatfArray(rotList)
        rotAttr.Set(vt_quats, time=frame)

        ##FIXME I don't think this works maybe once you add the skinclusters?
        ## Rig doesn't move when its imported despite having differen quat values over time

    

    
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

print(stage)

worldPrim = stage.DefinePrim("/World", "Xform")

stage.SetStartTimeCode(int(startFrame))
stage.SetEndTimeCode(int(endFrame))
stage.SetTimeCodesPerSecond(int(frameTimeCode))
 
if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SeelctAll()



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
    
    
    
    
    

 