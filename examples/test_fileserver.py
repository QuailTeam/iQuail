#!/usr/bin/python3

import iquail

if not iquail.helper.OS_LINUX:
    raise AssertionError("This test solution is linux only")

iquail.run(
    solution=iquail.SolutionFileServer('localhost', '4242',
                                       './build_fs', '../iQuailFileServer'),
    #solution=iquail.SolutionFileServer('localhost', '4242', '../iQuailFileServer/build'),
    installer=iquail.Installer(
        name='Allum1',
        publisher='alies',
        icon='icon.jpg',
        binary='allum1',
        console=True,
        launch_with_quail=True
    ),
    builder=iquail.builder.Builder(),
    controller=iquail.ControllerTkinter()
)
