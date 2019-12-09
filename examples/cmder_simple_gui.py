#!/usr/bin/python3

import iquail

iquail.run(
    solution=iquail.SolutionGitHub("cmder_mini.zip", "https://github.com/cmderdev/cmder"),
    installer=iquail.Installer(
        publisher='cmderdev',
        name='Cmder',
        icon='Cmder.exe',
        binary='Cmder.exe',
        console=False,
        launch_with_quail=True,
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.ico'),
        iquail.builder.CmdNoconsole()
    ),
    controller=iquail.ControllerTkinter()
)
