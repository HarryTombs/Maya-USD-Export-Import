import subprocess
import json
from pathlib import Path
import os

try:
    with open("C:\\ProgramData\\Epic\\UnrealEngineLauncher\\LauncherInstalled.dat","r") as f:
        data = json.load(f)
except:
    print("Couldn't find Unreal Directory")

for installation in data["InstallationList"]:
    if((installation['AppName'][:2]) == 'UE'):
        Unrealinstall = installation['InstallLocation']

Projpath = os.path.dirname(__file__)
Unrealinstall = str(Path(Unrealinstall) / "Engine" / "Binaries" / "Win64" / "UnrealEditor.exe")
Scriptpath = str(Path(Projpath) / "Import.py")
Scriptpath = Scriptpath.replace("\\","/")
powershellScript = str(Path(Projpath) / "unrealRun.ps1")

def launchUnreal(unrealProject: str):
    """
    Launches Unreal Editor with the specified project and runs the import script.
    """
    subprocess.run([
        "powershell",
        "-File", powershellScript,
        "-engine", Unrealinstall,
        "-project", unrealProject,
        "-script", Scriptpath
    ], check=True)
