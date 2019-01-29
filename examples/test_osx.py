#!/usr/bin/python3

import os
import os.path
import iquail
import platform

if iquail.helper.OS_OSX:
    solution_path = ['MacCalc']
    iquail.run(
        iquail.SolutionLocal(['MacCalc']),
        iquail.Installer(
                name='MacCalc',
                publisher='test',
                icon='icon.jpeg',
                binary='maccalc',
                console=True,
        ),
        iquail.builder.Builder(iquail.builder.CmdIntegrity(solution_path))
    )
