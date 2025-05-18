import unreal

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level("/Game/ThirdPerson/Maps/ThirdPersonMap")

unreal.log("Headlessly Running file")


destination = r"/Game/UsdImported"

assetName = "Usd"  ## Get file name later

usdFilePath = r"C:\Users\ht-23\Documents\PythonProjects\USDMayaAnimImporter\EXPORT333.usda" ## again get this later

# level_actors = unreal.EditorLevelLibrary.get_all_level_actors()

spawn_location = unreal.Vector(0,0,0)
spawn_rotation = unreal.Rotator(0,0,0)

# for currentActor in level_actors:
#     if currentActor.get_class().get_name() == "USDStageActor":
#         unreal.EditorLevelLibrary.destroy_actor(currentActor)


actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.UsdStageActor,
    spawn_location,
    spawn_rotation
)

# actor.reload_stage()

unrealusdFile = unreal.FilePath(usdFilePath)

actor.set_editor_property("root_layer", unrealusdFile)

actor.set_editor_property("initial_load_set", unreal.UsdInitialLoadSet.LOAD_ALL)

unreal.EditorLevelLibrary.save_current_level()



