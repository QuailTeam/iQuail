#!/usr/bin/python3

import iquail

if not iquail.helper.OS_WINDOWS:
    raise AssertionError("This test solution is windows only")

iquail.run(
    solution=iquail.SolutionBitBucket(
        "cmder_mini.zip", "https://bitbucket.org/artous/cmder/downloads/"),
    installer=iquail.Installer(
        publisher='cmderdev',
        name='Cmder',
        icon='Cmder.exe',
        binary='Cmder.exe',
        console=False,
        launch_with_quail=True
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.ico'),
        iquail.builder.CmdNoconsole()
    ),
    controller=iquail.ControllerTkinter(eula="This is a test")
)
