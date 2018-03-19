#!/usr/bin/python3

import os
import os.path
import quail
import platform

def print_progress(percent):
    print("%s%%" % (percent))

if quail.helper.OS_LINUX:
    quail.run(
        quail.Installer(
            name='LolAllum1',
            icon='icon.jpeg',
            binary='allum1',
            solution=quail.SolutionPacked(path='Allum1', hook=print_progress),
            console=True
        ),
        quail.builder.Builder()
    )

if quail.helper.OS_WINDOWS:
    quail.run(
        quail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            solution=quail.SolutionPacked(path='OpenHardwareMonitor', hook=print_progress),
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIcon('icon.ico')
        )
    )
