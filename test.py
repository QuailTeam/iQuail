#!/usr/bin/python3


import os
import os.path
import quail
import platform

solution_path = os.path.join(os.getcwd(), 'test_solution')

config = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'solution_path': solution_path,
    'console': True
}

configWindows = {
    'name': 'OpenHardwareMonitor',
    'icon': 'OpenHardwareMonitor.exe',
    'binary': 'OpenHardwareMonitor.exe',
    'solution_path': os.path.join(os.getcwd(), 'OpenHardwareMonitor'),
    'console': True
}

if (platform.system() == 'Linux'):
    quail.run(config)
else:
    quail.run(configWindows)
