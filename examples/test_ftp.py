#!/usr/bin/python3

import os
import os.path
import quail
import platform


if quail.helper.OS_LINUX:
    solution_path = ['Allum1']
    quail.run(
        quail.Installer(
            name='LolAllum1',
            icon='icon.jpeg',
            binary='allum1',
            solution=quail.SolutionFtp('10.19.253.230',
                                       ['pub', 'Allum1']),
            console=True
        )
    )

if quail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    quail.run(
        quail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            solution=quail.SolutionFtp('10.19.253.230',
                                       ['pub', 'OpenHardwareMonitor']),
            console=True
        )
    )
