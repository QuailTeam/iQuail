#!/usr/bin/python3

import os
import os.path
import iquail
import platform


if iquail.helper.OS_LINUX:
    solution_path = ['Allum1']
    iquail.run(
        iquail.SolutionFtp('10.19.253.230',
                           ['pub', 'Allum1']),
        iquail.Installer(
            name='Allum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True
        )
    )

if iquail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    iquail.run(
        iquail.SolutionFtp('10.19.253.230',
                           ['pub', 'OpenHardwareMonitor']),
        iquail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True
        )
    )
