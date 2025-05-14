import subprocess
import json
import os 

unrealProject = r"D:\UnrealProjects\ImporterProject\ImporterProject.uproject"  ### THIS WILL BE INPUTED BY USER

with open("C:\\ProgramData\\Epic\\UnrealEngineLauncher\\LauncherInstalled.dat","r") as f:
    data = json.load(f)

for installation in data["InstallationList"]:
    if((installation['AppName'][:2]) == 'UE'):
        Unrealinstall = installation['InstallLocation']

path = os.path.abspath(os.getcwd())        

Unrealinstall += r"\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"

Scriptpath = fr"{path}\src\Import.py"

powershellScript = fr"{path}\unrealRun.ps1"

subprocess.run([
    "powershell",
    "-File", powershellScript,
    "-engine", Unrealinstall,
    "-project", unrealProject,
    "-script", Scriptpath
], check=True)