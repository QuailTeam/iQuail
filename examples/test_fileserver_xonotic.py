#!/usr/bin/python3

import iquail

if not iquail.helper.OS_LINUX:
    raise AssertionError("This test solution is linux only")

iquail.run(
    solution=iquail.SolutionFileServer('localhost', '4242',
                                       '../iQuailFileServer', './build_fs'),
    installer=iquail.Installer(
        name='Xonotic',
        publisher='OHM',
        icon='misc/logos/icons_png/xonotic_512.png',
        binary='xonotic-linux64-sdl',
        console=True,
        launch_with_quail=True
    ),
    builder=iquail.builder.Builder(side_img_override='side_img.gif'),
    controller=iquail.ControllerTkinter()
)
