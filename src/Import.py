import unreal

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level("/Game/ThirdPerson/Maps/ThirdPersonMap.umap")


unreal.log("runningScript")

unreal.log("Headlessly Running file")

destination = r"/Game/TestFolder"

if not unreal.EditorAssetLibrary.does_directory_exist(destination):
    unreal.EditorAssetLibrary.make_directory(destination)
    unreal.log(f"Created Folder: {destination}")
else:
    unreal.log(f"Folder Already exists: {destination}")