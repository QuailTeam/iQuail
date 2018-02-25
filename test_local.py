#!/usr/bin/python3

import os
import os.path
import quail
import platform

configLinux = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'publisher': 'A Nice Publisher',
    'solution': quail.LocalSolution(['test_local', 'Allum1']),
    'console': True
}

configWindows = {
    'name': 'OpenHardwareMonitor',
    'icon': 'OpenHardwareMonitor.exe',
    'binary': 'OpenHardwareMonitor.exe',
    'publisher': 'A Nice Publisher',
    'solution': quail.LocalSolution(['test_local', 'OpenHardwareMonitor']),
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
