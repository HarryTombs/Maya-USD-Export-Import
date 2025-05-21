
import unreal
import json
import os


proj_path = os.path.dirname(__file__)

with open(proj_path + r"/Temp/Usd_info.json") as f:
    data = json.load(f)

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level("/Game/ThirdPerson/Maps/ThirdPersonMap")

unreal.log("Headlessly Running file")

for info in data["Scene_Data"]:
    asset_name = info["WorldName"]
    usd_file_path = info["FilePath"]

usd_file_path = str(usd_file_path)

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

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
