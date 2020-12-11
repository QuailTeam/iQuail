#!/usr/bin/python3

import iquail

if iquail.helper.OS_LINUX:
    raise AssertionError("This test solution is windows only")
if iquail.helper.OS_WINDOWS:
    iquail.run(
        solution=iquail.SolutionGitHub("cmder_mini.zip", "https://github.com/cmderdev/cmder"),
        installer=iquail.Installer(
            publisher='cmderdev',
            name='Cmder',
            icon='Cmder.exe',
            binary='Cmder.exe',
            console=False
        ),
        builder=iquail.builder.Builder(
            iquail.builder.CmdIcon('icon.ico')
        ))
if iquail.helper.OS_OSX:
    iquail.run(
        solution=iquail.SolutionGitHub("Console.app.zip", "https://github.com/macmade/Console"),
        installer=iquail.Installer(
            name='Console',
            publisher='MacMade',
            full_app=True,
            binary='Console.app',
            icon='',
            console=True
        ),
        builder=iquail.builder.Builder()
    )
