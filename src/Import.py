import unreal

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level("/Game/ThirdPerson/Maps/ThirdPersonMap.umap")

unreal.log("Headlessly Running file")

destination = r"/Game/UsdImport"

assetName = "Usd"  ## Get file name later

usdFilePath = r"C:\Users\ht-23\Documents\PythonProjects\USDMayaAnimImporter\EXPORT3.usda" ## again get this later

task = unreal.AssetImportTask()
task.filename = usdFilePath
task.destination_path = destination
task.destination_name = assetName
task.replace_existing = True
task.automated = True
task.save = True


if not unreal.EditorAssetLibrary.does_directory_exist(destination):
    unreal.EditorAssetLibrary.make_directory(destination)
    unreal.log(f"Created Folder: {destination}")
else:
    unreal.log(f"Folder Already exists: {destination}")

usd_options = unreal.UsdStageImportOptions()
usd_options.import_actors = True
usd_options.kinds_to_collapse = 1 | 4
task.options = usd_options

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
