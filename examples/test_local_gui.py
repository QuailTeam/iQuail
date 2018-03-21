#!/usr/bin/python3

import os
import os.path
import quail
import platform

if quail.helper.OS_LINUX:
    solution_path = ['Allum1']
    quail.run(
        quail.InstallGui(
            name='LolAllum1',
            icon='icon.jpeg',
            binary='allum1',
            solution=quail.SolutionLocal(['Allum1']),
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIntegrity(solution_path)
        )
    )
if quail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    quail.run(
        quail.InstallGui(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            solution=quail.SolutionLocal(['OpenHardwareMonitor']),
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIntegrity(solution_path)
        )
    )
