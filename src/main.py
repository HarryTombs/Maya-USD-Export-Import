import sys

path = os.path.abspath(os.getcwd())
sys.path.append(fr"{path}\src")

import Export
import LaunchUnreal

UsdFilename = "ExportTester"
UnrealPath = r"D:\UnrealProjects\ImporterProject2\ImporterProject2.uproject"
UserSelected = True

startFrame = cmds.playbackOptions(q=True, min=True)
endFrame = cmds.playbackOptions(q=True, max=True)
frameTimeCode = 24.0   

Export.ExecuteExport(UsdFilename,UnrealPath,UserSelected,startFrame,endFrame,frameTimeCode)
# LaunchUnreal.launchUnreal(UnrealPath)