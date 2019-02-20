#!/usr/bin/python3

import iquail

if not iquail.helper.OS_LINUX:
    raise AssertionError("This test solution is linux only")

iquail.run(
    solution=iquail.SolutionGitHub("indie.zip", "https://github.com/QuailTeam/cpp_indie_studio"),
    installer=iquail.Installer(
        publisher='tek',
        name='Indie',
        icon='icon.png',
        binary='indie_studio',
        console=False,
        launch_with_quail=True
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.ico'),
        iquail.builder.CmdNoconsole()
    ),
    controller=iquail.ControllerTkinter()
)
