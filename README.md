# Unreal animation Exporter

This is a tool for extracting data from maya scenes using USD and injecting it directly to a specified Unreal project file, in the hypothetical scenario where they remove the "Export" button. Intended for use with maya 2024+ and Unreal Engine 5.4+ on Windows.

![Image](https://github.com/user-attachments/assets/cd00fa90-0502-4c5a-a65c-73c952b4f5be)

It detects and extracts keyframe information transfering them into USD, as well as other information like position data, start and end frames and camera focal length, being converted to fit the scale and limits of an unreal project. The goal is to have objects feel the same scale between programs as seamlessly as possible.

It was originally planned to include rigged and animated characters but due to my lack of knowledge and experience in that area it became more of a holdup to finishing the pipeline as a whole, therefore was dropped.

## How to install

At a minimum you'll require the entire "/src" folder and the "drag_drop_install.py" file to install.

Ensure you have the mayaUSDPlugin in Maya enabled.

![Image](https://github.com/user-attachments/assets/eb37d216-2665-489d-a258-fa0d72cf980d)

As well as the USD Importer, Pyhton Editor Script and Sequencer Scripting plugins in Unreal enabled.

![Image](https://github.com/user-attachments/assets/3792e064-bce0-4274-951c-3365e17d7985)
![Image](https://github.com/user-attachments/assets/b29b8b8d-bd85-4d99-92b7-86464522baea)
![Image](https://github.com/user-attachments/assets/ed28b433-4f72-4813-b6c5-a0d3d4ee8994)

In a saved Maya Scene, drag and drop the "drag_drop_install.py" file anywhere on mayas interface.


A shelf called USD importer should appear with a single button with prompts to export from there.

![image](https://github.com/user-attachments/assets/2cce6104-921e-45bc-9748-6eb669b75661)


## Sources

ChatGPT (2025). Used Throughout for debugging, document explaination and small tasks (type hints, formating, etc) [online]. Available at: https://chatgpt.com/.

20tab (2016). UnrealEnginePython/tutorials/YourFirstAutomatedPipeline.md at master · 20tab/UnrealEnginePython. [online] GitHub. Available at: https://github.com/20tab/UnrealEnginePython/blob/master/tutorials/YourFirstAutomatedPipeline.md [Accessed 21 May 2025].

Autodesk (2025). Python Commands. [online] Autodesk.com. Available at: https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=__CommandsPython_index_html [Accessed 21 May 2025].

Cheller, L. (2023). Xforms - Usd Survival Guide. [online] Github.io. Available at: https://lucascheller.github.io/VFX-UsdSurvivalGuide/pages/production/caches/xform.html [Accessed 21 May 2025].

Decogged (2020). Create Maya UIs in under 20mins (Part 1) - Let’s Payathon #14. [online] YouTube. Available at: https://www.youtube.com/watch?v=UEf-d4CVv5c [Accessed 21 May 2025].

Epic Games (2025a). Scripting the Unreal Editor Using Python | Unreal Engine 5.5 Documentation | Epic Developer Community. [online] Epic Games Developer. Available at: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python#thecommandline [Accessed 21 May 2025].

Epic Games (2025b). Universal Scene Description in Unreal Engine | Unreal Engine 5.5 Documentation | Epic Developer Community. [online] Epic Games Developer. Available at: https://dev.epicgames.com/documentation/en-us/unreal-engine/universal-scene-description-in-unreal-engine.

Epic Games (2025c). Unreal Python API Documentation — Unreal Python 5.5 (Experimental) documentation. [online] Epicgames.com. Available at: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/ [Accessed 21 May 2025].

Nvidia (2025a). USD Python API Notes. [online] NVIDIA Developer. Available at: https://developer.nvidia.com/usd/apinotes [Accessed 21 May 2025].

Nvidia (2025b). UsdGeom module — pxr-usd-api 105.0.2 documentation. [online] Nvidia.com. Available at: https://docs.omniverse.nvidia.com/kit/docs/pxr-usd-api/105.0.2/pxr/UsdGeom.html [Accessed 21 May 2025].

Nvidia (2025c). usdview Quickstart — Omniverse USD. [online] Nvidia.com. Available at: https://docs.omniverse.nvidia.com/usd/latest/usdview/quickstart.html [Accessed 21 May 2025].

OpenUsd (2021). End to End Example — Universal Scene Description 25.05 documentation. [online] Openusd.org. Available at: https://openusd.org/release/tut_end_to_end.html#end-to-end-example [Accessed 21 May 2025].

OpenUsd (2025). Universal Scene Description: Universal Scene Description (USD). [online] Openusd.org. Available at: https://openusd.org/dev/api/index.html [Accessed 21 May 2025].

Phillips, S. (2025). [online] Epicgames.com. Available at: https://dev.epicgames.com/community/snippets/J5R1/unreal-engine-run-headless-unreal-editor-with-python-script [Accessed 21 May 2025].

Purkiss, J. (2024). Unreal Engine USD Attribute Toolset.

Wilson, D. (2022). Using Python in Unreal to import static meshes. [online] Artstation.com. Available at: https://www.artstation.com/blogs/deonwilson/bl7N/using-python-in-unreal-to-import-static-meshes [Accessed 21 May 2025].








[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Tn7g_Mhz)
