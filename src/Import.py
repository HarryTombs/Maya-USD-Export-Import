import unreal

fileName = fr"EXPORT.usda"
fileDir = fr"C:\Users\ht-23\Documents\PythonProjects\USDMayaAnimImporter\{filename}"

usd_import_options = unreal.UsdStageImportOptions()
for attr in dir(usd_import_options):
    if not attr.startswith('_'):
        print(attr)

i = 0
while i < 100:
    print(i)
    i += 1