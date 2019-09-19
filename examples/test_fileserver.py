#!/usr/bin/python3

import iquail

if not iquail.helper.OS_LINUX:
    raise AssertionError("This test solution is windows only")

iquail.run(
    solution=iquail.SolutionFileServer('localhost', '4242', '/home/tetra/rendu/Quail/iQuailFileServer/build/iQuailClient'),
    installer=iquail.Installer(
        name='Allum1',
        publisher='alies',
        icon='icon.jpeg',
        binary='allum1',
        console=True,
        launch_with_quail=False
    ),
    builder=iquail.builder.Builder(),
    controller=iquail.ControllerTkinter()
)
