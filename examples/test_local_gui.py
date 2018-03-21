#!/usr/bin/python3

import os
import os.path
import quail
import platform

if quail.helper.OS_LINUX:
    solution_path = ['Allum1']
    quail.run(
        quail.SolutionLocal(['Allum1']),
        quail.InstallerGui(
            name='LolAllum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIntegrity(solution_path)
        )
    )
if quail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    quail.run(
        quail.SolutionLocal(['OpenHardwareMonitor'])
        quail.InstallerGui(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIntegrity(solution_path)
        )
    )
