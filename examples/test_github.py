#!/usr/bin/python3

import iquail

if not iquail.helper.OS_WINDOWS:
    raise AssertionError("This test solution is windows only")

iquail.run(
    solution=iquail.SolutionGitHub("cmder_mini.zip", "https://github.com/cmderdev/cmder"),
    installer=iquail.Installer(
        publisher='OHM',
        name='Cmder',
        icon='Cmder.exe',
        binary='Cmder.exe',
        console=False
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.ico')
    )
)
