#!/usr/bin/python3

import iquail

if iquail.helper.OS_OSX:
    solution_path = ['MacCalc']
    iquail.run(
        iquail.SolutionLocal(['MacCalc']),
        iquail.Installer(
                name='MacCalc',
                publisher='test',
                icon='icon.icns',
                binary='maccalc',
                console=True,
        ),
        iquail.builder.Builder(iquail.builder.CmdIntegrity(solution_path))
    )
