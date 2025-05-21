from pathlib import Path
import os 
import json
import maya.cmds as cmds
import maya.api.OpenMaya as om
from pxr import Usd, UsdGeom, Gf


start_frame = cmds.playbackOptions(q=True, min=True)
end_frame = cmds.playbackOptions(q=True, max=True)
frame_time_code = 24.0   

scene_data = []

json_file = (os.path.dirname(__file__) + r"\Temp\Usd_info.json")
Path(json_file).parent.mkdir(parents=True, exist_ok=True)
Path(json_file).write_text("")



def select_all_but_cameras() -> list:
    """
    Returns a list of all top-level objects in the scene except default cameras.
    """
    exclude = {"|front","|persp","|side","|top"}
    selected = cmds.ls(assemblies=True, l=True)
    return [obj for obj in selected if obj not in exclude]
    #thanks Jon

def select_current() -> list:
    """
    Returns the currently selected objects in the scene.
    Exits if nothing is selected.
    """
    selected_name = cmds.ls(l=True, sl=True)
    if not selected_name:
        open(json_file, 'w').close()
        exit("Selection is empty")
    return selected_name

def create_usda(name: str) -> Usd.Stage:
    """
    Creates or opens a .usda for the scene and returns the stage.
    """
    scene_data.clear()
    scene_path = cmds.file(query=True, sceneName=True)
    if not scene_path:
        raise RuntimeError("Scene must be saved before determining save location.")

    scene_dir = str(Path(scene_path).parent)
    usd_output_path = str(Path(scene_dir) / f"{name}.usda")
    if Path(usd_output_path).is_file():
        stage = Usd.Stage.Open(usd_output_path)
        print(f"USD file found at: {usd_output_path}")
    else:
        stage = Usd.Stage.CreateNew(usd_output_path)
        print(f"USD file created at: {usd_output_path}")

    scene_names = [{

        "WorldName": name,
        "FilePath": usd_output_path
        }]
    scene_data.append(scene_names[0])
    
    return stage 
    
def check_xform(xform, trans_type) -> UsdGeom.XformOp:
    """
    Checks if a specific transform operation exists on the xform, adds it if not, and returns it.
    """
    for op in xform.GetOrderedXformOps():
        if op.GetOpType() == trans_type:
            return op
    return xform.AddXformOp(trans_type)
        
def set_xform(obj: str, xform: UsdGeom.Xform) -> None:
    """
    Sets the transform (translate, rotate, scale) for the given object on the USD xform, including animation if present.
    """

    cmds.currentTime(1, edit= True)

    t_xform = check_xform(xform,UsdGeom.XformOp.TypeTranslate)
    r_xform = check_xform(xform,UsdGeom.XformOp.TypeRotateXYZ)
    s_xform = check_xform(xform,UsdGeom.XformOp.TypeScale)

    if cmds.keyframe(obj,q =True,kc =True)>1:
        for frame in range(int(start_frame), int(end_frame) + 1):
            cmds.currentTime(frame, edit= True)
            time = Usd.TimeCode(frame)
            pos = cmds.xform(obj, query=True, ws=True, t=True)
            rot = cmds.xform(obj, query=True, ws=True, ro=True)
            scale = cmds.xform(obj, query=True, ws=True, s=True)
            t_xform.Set(Gf.Vec3f(*pos),time)
            r_xform.Set(Gf.Vec3f(*rot),time)
            s_xform.Set(Gf.Vec3f(*scale),time)
            

    else: 
        pos = cmds.xform(obj, query=True, ws=True, t=True)
        rot = cmds.xform(obj, query=True, ws=True, ro=True)
        scale = cmds.xform(obj, query=True, ws=True, s=True)
        t_xform.Set(Gf.Vec3f(*pos))
        r_xform.Set(Gf.Vec3f(*rot))
        s_xform.Set(Gf.Vec3f(*scale))



def write_mesh(obj: str, stage: Usd.Stage, path: str) -> None:
    """
    Writes mesh data from the Maya object to the USD stage at the specified path.
    """
    
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

    set_xform(obj,xform)

    
def write_cam(obj: str, stage: Usd.Stage, path: str) -> None:
    """
    Writes camera data from the Maya object to the USD stage at the specified path.
    """
    
    usdCam = UsdGeom.Camera.Define(stage, f"{path}")
    
    shape = cmds.listRelatives(obj, shapes=True)[0]
    focalLength = cmds.getAttr(f"{shape}.focalLength")
    
    horiAperture = cmds.getAttr(f"{shape}.horizontalFilmAperture")
    vertAperture = cmds.getAttr(f"{shape}.verticalFilmAperture")    

    horiAperture = (horiAperture*25.4)*0.01
    vertAperture = (vertAperture*25.4)*0.01
    focalLength = focalLength*0.01

    xform = UsdGeom.Xform(stage.GetPrimAtPath(path))
    
    set_xform(obj,xform)
    
    usdCam.GetFocalLengthAttr().Set(focalLength)
    
    usdCam.GetHorizontalApertureAttr().Set(horiAperture)
    usdCam.GetVerticalApertureAttr().Set(vertAperture)
    

def execute_export(
    name: str,
    unreal_project: str,
    use_selected: bool,
    start_frame: float,
    end_frame: float,
    frame_time_code: float
) -> None:   
    """
    Main export function. Exports selected or all objects to USD and writes export info to JSON.
    """
                
    stage = create_usda(name)

    worldPrim = stage.DefinePrim("/World", "Xform")

    Path(json_file).parent.mkdir(parents=True, exist_ok=True)
    Path(json_file).write_text("")

    stage.SetStartTimeCode(int(start_frame))
    stage.SetEndTimeCode(int(end_frame))
    stage.SetTimeCodesPerSecond(int(frame_time_code))
    UsdGeom.SetStageMetersPerUnit(stage,1.0)
    
    if use_selected == True:
        objList = select_current()

    if use_selected == False:
        objList = select_all_but_cameras()

    export_data = []

    for obj in objList:

        if cmds.listRelatives(obj, s=True, typ="mesh"):
            print("mesh")
            usdMeshPath = "/World/" + obj.replace("|","/").strip("/")
            objName = obj.replace("|","")            
            write_mesh(obj,stage,usdMeshPath)
            mesh_data = {
                "usd_path": usdMeshPath,
                "asset_name": objName,
                "asset_type":"Mesh"
            }
            export_data.append(mesh_data)
        elif cmds.listRelatives(obj, s=True, typ="camera"):  
            print("Camera")  
            usdCamPath = "/World/" + obj.replace("|","/").strip("/")
            objName = obj.replace("|","")
            write_cam(obj,stage,usdCamPath)
            cam_data = {
                "usd_path": usdCamPath,
                "asset_name": objName,
                "asset_type": "Camera"
            }
            export_data.append(cam_data)

        elif cmds.listRelatives(obj,ad=True,type='joint'): 
            print("Joints")
            write_rig(obj,stage)
    
    data = {
        "Exported_Data": export_data,
        "Scene_Data": scene_data
    }
    with open(json_file,"a") as f:
        json.dump((data),f, indent=4) 
    stage.GetRootLayer().Save()

    print(f"Sent to Unreal project: {unreal_project}")



 ## Get the skin clusters out of there so the mesh exists

 ## you need to manually apply the animation data yourself :(

