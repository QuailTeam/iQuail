#!/usr/bin/python3

import os
import os.path
import quail
import platform

configLinux = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'solution': quail.LocalSolution(['Allum1']),
    'console': True
}

configWindows = {
    'name': 'OpenHardwareMonitor',
    'icon': 'OpenHardwareMonitor.exe',
    'binary': 'OpenHardwareMonitor.exe',
    'solution': quail.LocalSolution(['OpenHardwareMonitor']),
    'console': True
}

config = configLinux if quail.Helper.OS_LINUX else configWindows

quail.run(config)
