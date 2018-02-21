#!/usr/bin/python3

import os
import os.path
import quail
import platform

solution_path = os.path.join(os.getcwd(), 'test_solution')

configLinux = {
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

def install(installer):
    print("example custom install")
    installer.install()

def uninstall(installer):
    print("uninstall")
    installer.uninstall()

config = configLinux if platform.system() == 'Linux' else configWindows

quail.run(config,
          install=install,
          uninstall=uninstall
)
