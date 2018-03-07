#!/usr/bin/python3

import os
import os.path
import quail
import platform

if quail.Helper.OS_LINUX:
    solution_path = ['Allum1']
    quail.run(
        quail.Installer(
            name='LolAllum1',
            icon='icon.jpeg',
            binary='allum1',
            solution=quail.SolutionZip('solution.zip'),
            console=True
        ),
        quail.Builder(
            quail.BuildCmdIcon('icon.png'),
            quail.BuildCmdZip(solution_path, 'solution.zip'))
    )
if quail.Helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    quail.run(
        quail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            solution=quail.SolutionZip('solution.zip'),
            console=True
        ),
        quail.Builder(
            quail.BuildCmdIcon('icon.ico'),
            quail.BuildCmdZip(solution_path, 'solution.zip'))
    )
