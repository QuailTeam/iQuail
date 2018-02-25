#!/usr/bin/python3

import os
import os.path
import quail
import platform

configLinux = {
    'name': 'LolAllum1',
    'icon': 'icon.jpeg',
    'binary': 'allum1',
    'solution': quail.FtpSolution('mafreebox.freebox.fr',
                                  ['Disque dur','autres', 'test_solution']),
    'console': True
}

configWindows = {
    'name': 'OpenHardwareMonitor',
    'icon': 'OpenHardwareMonitor.exe',
    'binary': 'OpenHardwareMonitor.exe',
    'solution': quail.FtpSolution('mafreebox.freebox.fr',
                                  ['Disque dur','autres', 'OpenHardwareMonitor']),
    'console': True
}

config = configLinux if platform.system() == 'Linux' else configWindows

quail.run(config)
