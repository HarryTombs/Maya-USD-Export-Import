import subprocess
import json
from pathlib import Path

try:
    with open("C:\\ProgramData\\Epic\\UnrealEngineLauncher\\LauncherInstalled.dat","r") as f:
        data = json.load(f)
except:
    print("Couldn't find Unreal Directory")

for installation in data["InstallationList"]:
    if((installation['AppName'][:2]) == 'UE'):
        Unrealinstall = installation['InstallLocation']

Projpath = str(Path.cwd())
Unrealinstall = str(Path(Unrealinstall) / "Engine" / "Binaries" / "Win64" / "UnrealEditor.exe")
Scriptpath = str(Path(Projpath) / "src" / "Import.py")
Scriptpath = Scriptpath.replace("\\","/")
powershellScript = str(Path(Projpath) / "unrealRun.ps1")

def launchUnreal(unrealProject: str):
    subprocess.run([
        "powershell",
        "-File", powershellScript,
        "-engine", Unrealinstall,
        "-project", unrealProject,
        "-script", Scriptpath
    ], check=True)
