import unreal
import math
from pxr import Usd

def findActorRecursive(parent_Actor, class_filter=None):
        """Recursively find all children of parent_actor. Optionally filter by class."""
        found = []
        children = parent_Actor.get_attached_actors()

        for child in children:
                if not class_filter or isinstance(child,class_filter):
                        found.append(child)
                found.extend(findActorRecursive(child,class_filter))
        return found


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

camera = (findActorRecursive(actor,unreal.CameraActor))[0]

unreal.log(f"Actors are{camera}")

stage = Usd.Stage.Open(usdFilePath)

# UsdCam = stage.GetPrimAtPath(CamPath)

# FOV = 2 * math.atan((sensor_width / (2 * focal_length))) * (180 / math.pi)

# camera.set_editor_property("field_of_view",FOV)

unreal.EditorLevelLibrary.save_current_level()

