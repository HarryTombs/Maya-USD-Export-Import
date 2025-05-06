
# Project Ideas

## Unreal animation pipeline

A "send this to unreal" button

What i need to do next!!

write Mesh, Camera, Light and Animation Data (bones?) to the .USDA

send it to unreal and make sure unreal knows that happens, then deal with unreal usd importing

``` mermaid
flowchart TD

in1[/Animation in Maya/]--> Do1
in2[/Unreal Project Directory/] --> Do1[FBX export from Maya] --> Do2[Place in unreal project animation folder] --> Do3[Unreal detects update] --> check1{Is it an fbx??}
check1-- Yes ---Do4a[Assign Animation to right bit] --> End[End]
check1-- No ---Do4b[Ignore] --> End[End]


```


https://nccastaff.bournemouth.ac.uk/jmacey/MastersProject/MSc24/07/masters_thesis_final.pdf

https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/?application_version=4.27

https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python

https://dev.epicgames.com/community/learning/tutorials/LnE7/unreal-engine-asset-import-export-using-unreal-python-api

https://www.youtube.com/watch?v=Ue5SyNc1nKg

https://www.youtube.com/watch?v=72n-UmfmepQ

https://www.youtube.com/watch?v=noNjWvMdOZY

https://www.artstation.com/blogs/deonwilson/bl7N/using-python-in-unreal-to-import-static-meshes

https://github.com/20tab/UnrealEnginePython/blob/master/tutorials/YourFirstAutomatedPipeline.md

https://developer.nvidia.com/usd/apinotes

https://openusd.org/docs/api/index.html

https://openusd.org/dev/api/index.html

https://www.youtube.com/watch?v=rA7LPiDkdJI

https://www.youtube.com/watch?v=S6NBc3oUlFk

https://forums.developer.nvidia.com/t/resources-from-the-learn-with-me-streaming-series/304680

https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=__CommandsPython_index_html

https://github.com/PixarAnimationStudios/OpenUSD?tab=readme-ov-file

https://www.sidefx.com/docs/houdini/solaris/usd.html#:~:text=In%20USD%2C%20geometry%20settings%2C%20such,in%20an%20array%20of%20coordinates.

https://docs.omniverse.nvidia.com/kit/docs/pxr-usd-api/105.0.2/pxr/UsdGeom.html

https://docs.omniverse.nvidia.com/usd/latest/technical_reference/usd-types.html

https://docs.omniverse.nvidia.com/kit/docs/usdrt/latest/_apidocs/classusdrt_1_1UsdSkelSkeleton.html#classusdrt_1_1usdskelskeleton_1a1f5ca4a07b3ae24048bf68c9059a1ff9



https://openusd.org/dev/tut_xforms.html#id2

https://dev.epicgames.com/documentation/en-us/unreal-engine/universal-scene-description-in-unreal-engine

https://animationmethods.com/rigs.html

https://animationmethods.com/rigs.html

https://openusd.org/dev/api/_usd_skel__schema_overview.html

https://openusd.org/dev/api/class_gf_matrix4d.html

https://openusd.org/dev/api/_usd_skel__best_practices.html

https://openusd.org/release/index.html

https://openusd.org/release/tut_end_to_end.html#end-to-end-example

https://help.autodesk.com/view/MAYAUL/2025/ENU/?guid=GUID-36808BCC-ACF9-4A9E-B0D8-B8F509FEC0D5








[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Tn7g_Mhz)
