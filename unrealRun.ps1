#Setup variables
$engine = "D:\Unreal\UE_5.4\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$project = "D:\UnrealProjects\ImporterProject\ImporterProject.uproject"
$script = "C:\Users\ht-23\Documents\PythonProjects\USDMayaAnimImporter\src\Import.py"

#Start headless editor with specified script. Backtick ` used to preserve quotes in argument list.
Start-Process $engine -ArgumentList "`"$project`" -run=pythonscript -script=`"$script`""