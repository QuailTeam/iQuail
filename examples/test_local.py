#!/usr/bin/python3

import os
import os.path
import quail
import platform

configLinux = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'solution': quail.SolutionLocal(['Allum1']),
    'console': True
}

configWindows = {
    'name': 'OpenHardwareMonitor',
    'icon': 'OpenHardwareMonitor.exe',
    'binary': 'OpenHardwareMonitor.exe',
    'solution': quail.SolutionLocal(['OpenHardwareMonitor']),
    'console': True
}

config = configLinux if quail.helper.OS_LINUX else configWindows

quail.run(quail.Installer(**config))
