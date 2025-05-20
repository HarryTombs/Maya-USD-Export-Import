import maya.cmds as cmds
import sys
from pathlib import Path

path = str(Path.cwd())
sys.path.append(fr"{path}\src")

import Export
import LaunchUnreal

def start_export(UsdFilename: str, UnrealPath: str, UserSelected: bool) -> None:
    startFrame = cmds.playbackOptions(q=True, min=True)
    endFrame = cmds.playbackOptions(q=True, max=True)
    frameTimeCode = 24.0   

    Export.execute_export(UsdFilename,UnrealPath,UserSelected,startFrame,endFrame,frameTimeCode)
    LaunchUnreal.launchUnreal(UnrealPath)

class MyWindow:
    def __init__(self) -> None:
        self.window: str = "MyWin"
        self.unreal_text: str = ""
        self.name_text: str = ""
        self.select_bool: bool | None = None

    def create(self) -> None:
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)
        self.window = cmds.window(self.window, title = "Export USD")

        cmds.columnLayout(adjustableColumn=True,rowSpacing = 2)
        cmds.rowLayout(adjustableColumn=2, numberOfColumns = 2)
        cmds.text( label='Export Name' )
        self.name_text = cmds.textField()
        cmds.setParent('..')
        cmds.textField(self.name_text, edit = True)
        self.unreal_text = cmds.textFieldButtonGrp(columnAlign3 = ["left","center","right"], cat = [1,"left",2] ,adjustableColumn = 2,label='Unreal Project', buttonLabel='Browse', bc = self.locate_ureal_file, editable = True)
        self.select_bool = cmds.radioButtonGrp(select=1,columnAlign3 = ["left","center","center"],label = "Export Selection:", label1 = "Selected", label2 = "All", enable2 = True, numberOfRadioButtons=2, enable1 = True)
        cmds.rowLayout(adjustableColumn=1,numberOfColumns = 2)
        cmds.button(label = "Export", c = self.export_pressed)
        cmds.button(label = "Cancel", width = 100, c = self.close)
        cmds.setParent('..')

        cmds.showWindow(self.window)
    
    def print_value(self, *args) -> None:
        self.unreal_text = cmds.textFieldButtonGrp(self.unreal_text, query = True, text= True)
        self.name_text = cmds.textField(self.name_text,query = True, text = True)
        if (cmds.radioButtonGrp(self.select_bool,query =True, select = True) == 1):
            self.select_bool = True
        else:
            self.select_bool = False

    def export_pressed(self, *args) -> None:
        self.unreal_text = cmds.textFieldButtonGrp(self.unreal_text, query = True, text= True)
        self.name_text = cmds.textField(self.name_text,query = True, text = True)
        if (cmds.radioButtonGrp(self.select_bool,query =True, select = True) == 1):
            self.select_bool = True
        else:
            self.select_bool = False
        try:
            start_export(self.name_text,self.unreal_text,self.select_bool)
        except Exception as e:
            print(f"Export Failed {e}")
        self.close()
    
    def locate_ureal_file(self) -> str:
        basicFilter = "*.uproject"
        unrealProj = cmds.fileDialog(m=0,dm=basicFilter)
        cmds.textFieldButtonGrp(self.unreal_text, edit = True, text = unrealProj)
    def close(self, *args) -> None:
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)
    

win = MyWindow()
win.create()

