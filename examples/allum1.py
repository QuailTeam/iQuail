#!/usr/bin/python3

import iquail

iquail.run(
    solution=iquail.SolutionPacked(path='Allum1'),
    installer=iquail.Installer(
        publisher="alies",
        name='Allum1',
        icon='icon.jpeg',
        binary='allum1',
        console=True,
        launch_with_quail=True
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdNoconsole()
    ),
    controller=iquail.ControllerTkinter()
)
