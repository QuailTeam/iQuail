#!/usr/bin/python3
 
import iquail
 
if iquail.helper.OS_LINUX:
    binary = "xonotic-linux64-sdl"
    icon = "misc/logos/icons_png/xonotic_512.png"
 
if iquail.helper.OS_WINDOWS:
    binary = "xonotic-x86.exe"
    icon = "xonotic-x86.exe"
 
iquail.run(
    solution=iquail.SolutionPacked(path='Xonotic'),
    installer=iquail.Installer(
        publisher="OHM",
        name='Xonotic',
        icon=icon,
        binary=binary,
        console=False,
        launch_with_quail=False,
        is_large_solution=True,
    ),
 
    # iquail.builder.CmdIcon('icon.ico'),
    builder=iquail.builder.Builder(
        iquail.builder.CmdNoconsole(),
        side_img_override='side_img.gif',
    ),
    controller=iquail.ControllerTkinter()
)
