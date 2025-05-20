import unreal
import math
import json
import os
from pxr import Usd, UsdGeom, Sdf

def find_actor_recursive(parent_actor, class_filter=None):
    """Recursively find all children of parent_actor. Optionally filter by class."""
    found = []
    children = parent_actor.get_attached_actors()

    for child in children:
        if not class_filter or isinstance(child, class_filter):
            found.append(child)
        found.extend(find_actor_recursive(child, class_filter))
    return found

proj_path = os.path.dirname(os.path.dirname(__file__) )

with open(fr"{proj_path}\Temp\Usd_info.json") as f:
    data = json.load(f)

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level("/Game/ThirdPerson/Maps/ThirdPersonMap")

unreal.log("Headlessly Running file")

for info in data["Scene_Data"]:
    asset_name = info["WorldName"]
    usd_file_path = info["FilePath"]

usd_file_path = fr"{usd_file_path}"

spawn_location = unreal.Vector(0,0,0)
spawn_rotation = unreal.Rotator(0,0,0)

cache_name = "USDCahce"
cache_path = r"/Game/USD"

if (unreal.EditorAssetLibrary.does_asset_exist(f"{cache_path}/{cache_name}") != True):
    usd_asset_cache = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        cache_name,
        cache_path,
        unreal.UsdAssetCache,
        unreal.UsdAssetCacheFactory()
    )
else:
    usd_asset_cache = unreal.EditorAssetLibrary.load_asset(f"{cache_path}/{cache_name}")

unreal.EditorAssetLibrary.save_loaded_asset(usd_asset_cache)

actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.UsdStageActor,
    spawn_location,
    spawn_rotation
)

unreal_usd_file = unreal.FilePath(usd_file_path)

actor.set_editor_property("root_layer", unreal_usd_file)

actor.set_editor_property("initial_load_set", unreal.UsdInitialLoadSet.LOAD_ALL)

usd_asset_cache.add_asset_reference(actor,actor)
usd_asset_cache.refresh_storage()
unreal.EditorAssetLibrary.save_loaded_asset(usd_asset_cache)


# camera = (find_actor_recursive(actor,unreal.CameraActor))[0]


# for info in data["Exported_Data"]:
#     if info['asset_type'] == "Camera":
#         cam_path = info["usd_path"]

# unreal.log(f"Actors are{camera}")

# stage = Usd.Stage.Open(usd_file_path)


# focal_length = None
# sensor_width = None
# sensor_height = None

# if cam_path != None:
#     usd_camera: UsdGeom.Camera = UsdGeom.Camera.Get(stage, Sdf.Path(cam_path))
#     focal_length = usd_camera.GetFocalLengthAttr().Get()
#     sensor_width = usd_camera.GetHorizontalApertureAttr().Get()
#     sensor_height = usd_camera.GetVerticalApertureAttr().Get()
    

# if camera.get_class().get_name() == "CineCameraActor":
#     camera_component = camera.get_cine_camera_component()
#     print("Camera component:", camera_component)
# else:
#     unreal.log_warning(f"Actor is not a CineCameraActor: {camera.get_class().get_name()}")


unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
