#!/usr/bin/python3

import os
import os.path
import quail
import platform

if quail.Helper.OS_LINUX:
    solution_path = ['Allum1']
    config = {
        'name': 'LolAllum1',
        'icon': 'icon.jpeg',
        'binary': 'allum1',
        'solution': quail.SolutionZip('solution.zip'),
        'console': True
    }
elif quail.Helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    config = {
        'name': 'OpenHardwareMonitor',
        'icon': 'OpenHardwareMonitor.exe',
        'binary': 'OpenHardwareMonitor.exe',
        'solution': quail.SolutionZip('solution.zip'),
        'console': True
    }

quail.run(quail.Installer(**config),
          quail.Builder(
          quail.BuildCmdZip(solution_path, 'solution.zip'))
          )
