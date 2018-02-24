#!/usr/bin/python3

import os
import os.path
import quail
import platform

config = {
    'name': 'OpenHardwareMonitor',
    'icon': 'OpenHardwareMonitor.exe',
    'binary': 'OpenHardwareMonitor.exe',
    'solution': quail.FtpSolution('mafreebox.freebox.fr', 21, 'Disque dur','autres', 'OpenHardwareMonitor'),
    'console': True
}

quail.run(config)
