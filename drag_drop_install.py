from pathlib import Path
import maya.cmds as cmds
import sys
import os 
import shutil



def install():
    """
    Installs the plugin by copying source files to Maya's plug-ins directory and updating sys.path.
    """
    shelves_dir = cmds.internalVar(userShelfDir=True)
    base_dir = Path(shelves_dir).parents[1]
    plugins_dir = base_dir / 'plug-ins'
    Path(plugins_dir).mkdir(parents=True, exist_ok=True)

    print(f"PLugins directory {plugins_dir}")

    install_dir = os.path.dirname(__file__)
    print(install_dir)
    source = os.path.join(install_dir,'src')
    
    destination = plugins_dir / 'src'

    print(f"Source directory is {source}")
    
    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(source,destination)

    dest_str = str(destination)
    if dest_str not in sys.path:
        sys.path.append(fr"{destination}")
        print(f"added {dest_str} to sys.path")

def add_shelf_button():
    """
    Adds a shelf button in Maya to run the plugin script.
    """

    shelf_name = "UsdPlugin"

    shelves_dir = cmds.internalVar(userShelfDir=True)
    base_dir = Path(shelves_dir).parents[1]

    plugin_script_path = Path(base_dir) / 'plug-ins' / 'src' / 'main.py'

    if not plugin_script_path.exists():
        print("main.py not found, can't create shelf button.")
        return
    
    with open(plugin_script_path, 'r') as f:
        command = f.read()

    shelves_dir = cmds.internalVar(userShelfDir=True)

    shelf_file = Path(shelves_dir) / f"shelf_{shelf_name}.mel"

    if not cmds.shelfLayout(shelf_name, exists=True):
        cmds.setParent("ShelfLayout")
        cmds.shelfLayout(shelf_name)

    if not cmds.shelfButton("MyPluginButton", exists=True):
        cmds.setParent(shelf_name)
        cmds.shelfButton(
            command=command,
            annotation="Run My Plugin",
            image="commandButton.png",  # Or another Maya icon name
            label="MyPlugin",
            sourceType="python",
            style="iconAndTextVertical",
            width=37,
            height=37
        )
        print("Shelf button added.")
    else:
        print("Shelf button already exists.")



def onMayaDroppedPythonFile(*args):
    """
    Entry point when the file is drag-and-dropped into Maya. Installs the plugin and adds the shelf button.
    """
    
    install()
    print("Plugin Installed")
    add_shelf_button()
    print("Added Shelf Button")
