import os
import subprocess
import maya.cmds as cmds
import maya.api.OpenMaya as om
from pxr import Usd, UsdGeom, Gf, Vt, Sdf, UsdSkel

useSelected = True

startFrame = cmds.playbackOptions(q=True, min=True)
endFrame = cmds.playbackOptions(q=True, max=True)
frameTimeCode = 24.0


def SelectAllButCameras():
    exclude = {"|front","|persp","|side","|top"}
    selected = cmds.ls(assemblies=True, l=True)
    return [obj for obj in selected if obj not in exclude]
    #thanks Jon

def SelectCurrent():
    selectedName = cmds.ls(l=True, sl=True)
    if not selectedName:
        print("Selection is empty")
    return selectedName

def CreateUSDA(name):

    scenePath = cmds.file(query=True, sceneName=True)

    if not scenePath:
        raise RuntimeError("Scene must be saved before determining save location.")

    sceneDir = os.path.dirname(scenePath)
    usdOutputPath = os.path.join(sceneDir, f"{name}.usda")
    if os.path.isfile(usdOutputPath) == True:
        stage = Usd.Stage.Open(usdOutputPath)
        print(f"USD file found at: {usdOutputPath}")
    else:
        stage = Usd.Stage.CreateNew(usdOutputPath)
        print(f"USD file created at: {usdOutputPath}")
    return stage 
    
def checkXform(xform, transType):
    for op in xform.GetOrderedXformOps():
        if op.GetOpType() == transType:
            return op
    return xform.AddXformOp(transType)
        
def setXform(obj,xform):

    cmds.currentTime(1, edit= True)

    t_xform = checkXform(xform,UsdGeom.XformOp.TypeTranslate)
    r_xform = checkXform(xform,UsdGeom.XformOp.TypeRotateXYZ)

    if cmds.keyframe(obj,q =True,kc =True)>1:
        for frame in range(int(startFrame), int(endFrame) + 1):
            cmds.currentTime(frame, edit= True)
            time = Usd.TimeCode(frame)
            pos = cmds.xform(obj, query=True, ws=True, t=True)
            rot = cmds.xform(obj, query=True, ws=True, ro=True)
            t_xform.Set(Gf.Vec3f(*pos),time)
            r_xform.Set(Gf.Vec3f(*rot),time)

    else: 
        pos = cmds.xform(obj, query=True, ws=True, t=True)
        rot = cmds.xform(obj, query=True, ws=True, ro=True)
        t_xform.Set(Gf.Vec3f(*pos))
        r_xform.Set(Gf.Vec3f(*rot))


def writeMesh(obj,stage,path):
    
    select = om.MSelectionList()
    select.add(obj)
    dagPath = select.getDagPath(0)
    meshFN = om.MFnMesh(dagPath)
    usdMesh = UsdGeom.Mesh.Define(stage,path)  
    array = meshFN.getPoints(om.MSpace.kTransform)
    points = []
    for pt in array:
        currentpoint = [*pt]
        Vec3list = [Gf.Vec3f(currentpoint[:-1])]
        points = points + Vec3list
    usdMesh.GetPointsAttr().Set(points)
    counts, indices = meshFN.getVertices()
    usdMesh.GetFaceVertexCountsAttr().Set(counts)
    usdMesh.GetFaceVertexIndicesAttr().Set(indices)
    
    xform = UsdGeom.Xform(stage.GetPrimAtPath(path))

    setXform(obj,xform)

    
def writeCam(obj, stage,path):
    
    usdCam = UsdGeom.Camera.Define(stage, f"{path}")
    
    shape = cmds.listRelatives(obj, shapes=True)[0]
    focalLength = cmds.getAttr(f"{shape}.focalLength")
    
    horiAperture = cmds.getAttr(f"{shape}.horizontalFilmAperture")
    vertAperture = cmds.getAttr(f"{shape}.verticalFilmAperture")    

    xform = UsdGeom.Xform(stage.GetPrimAtPath(path))
    
    setXform(obj,xform)
    
    usdCam.GetFocalLengthAttr().Set(focalLength)
    
    usdCam.GetHorizontalApertureAttr().Set(horiAperture)
    usdCam.GetVerticalApertureAttr().Set(vertAperture)
    
    
    
def WriteRig(obj,stage):
    
    skelRootPath = cmds.ls(obj,sn=True)
    SkelRoot = UsdSkel.Root.Define(stage,f"/World/{skelRootPath[0]}")
    rootPrim = stage.GetPrimAtPath(f"/World/{skelRootPath[0]}")
    bindingRoot = UsdSkel.BindingAPI.Apply(rootPrim)

    skelPath = (f"/World/{skelRootPath[0]}/Skel")
    skeleton = UsdSkel.Skeleton.Define(stage,skelPath)
    skelAnimPath = (f"/World/{skelRootPath[0]}/Anim")
    skelAnim = UsdSkel.Animation.Define(stage,skelAnimPath)
    skelPrim = stage.GetPrimAtPath(skelPath)

    bindingSkel = UsdSkel.BindingAPI.Apply(skelPrim)
    bindingSkel.CreateAnimationSourceRel().SetTargets([Sdf.Path(skelAnimPath)])

    meshPath = (f"/World/{skelRootPath[0]}/SkelMesh")
    usdMesh = UsdGeom.Mesh.Define(stage,meshPath)
    meshPrim = stage.GetPrimAtPath(meshPath)
    meshBinding = UsdSkel.BindingAPI.Apply(meshPrim)
    meshBinding.CreateSkeletonRel().SetTargets([skelPath])
    

    
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
    #print(shapes)
    for shape in shapes:
        history = cmds.listHistory(shape)
        skinClusters = cmds.ls(history, type='skinCluster')
        for sc in skinClusters:
            
            # Get the joints influencing the skinCluster
            joints = cmds.skinCluster(sc, q=True, inf=True)
            select = om.MSelectionList()
            #select.add(geometry)
            #dagPath = select.getDagPath(0)
            #meshFN = om.MFnMesh(dagPath)
            #usdMesh = UsdGeom.Mesh.Define(stage,path)  
            #array = meshFN.getPoints(om.MSpace.kTransform)
            #print(array)
            # print(sc)

            # print(joints)
        #geometry = cmds.skinCluster(shape, q=True, g=True)    
        #print(geometry)
   
name = "EXPORT"         
            
stage = CreateUSDA(name)


worldPrim = stage.DefinePrim("/World", "Xform")

stage.SetStartTimeCode(int(startFrame))
stage.SetEndTimeCode(int(endFrame))
stage.SetTimeCodesPerSecond(int(frameTimeCode))
 
if useSelected == True:
    objList = SelectCurrent()

if useSelected == False:
    objList = SelectAllButCameras()


for obj in objList:

    if cmds.listRelatives(obj, s=True, typ="mesh"):
        print("mesh")
        usdMeshPath = "/World/" + obj.replace("|","/").strip("/")
        writeMesh(obj,stage,usdMeshPath)
        
    elif cmds.listRelatives(obj, s=True, typ="camera"):  
        print("Camera")  
        usdCamPath = "/World/" + obj.replace("|","/").strip("/")
        writeCam(obj,stage,usdCamPath)
    elif cmds.listRelatives(obj,ad=True,type='joint'): #we're assuming this is a rigged mesh
        print("Joints")
        WriteRig(obj,stage)
        
        
stage.GetRootLayer().Save()

### You can use this to run a headerless version of the unreal project and run the import script :)

# unrealProjLocation = fr'"C:\Users\ht-23\Documents\Unreal Projects\MyProject\MyProject.uproject"'

# ImportScript = fr'"./Import.py"' 
 
# command = fr'> UnrealEditor-Cmd.exe {unrealProjLocation} -run=pythonscript -script=ImportScript'

# subprocess.run(command, shell=True)

    


 ## Get the skin clusters out of there so the mesh exists

 ## Get a script to import into unreal

 ## you need to manually apply the animation data yourself :(

