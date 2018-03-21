#!/usr/bin/python3

import os
import os.path
import quail
import platform

def print_progress(percent):
    print("%s%%" % (percent))

if quail.helper.OS_LINUX:
    quail.run(
        quail.Install(
            name='LolAllum1',
            icon='icon.jpeg',
            binary='allum1',
            solution=quail.SolutionPacked(path='Allum1'),
            console=True
        ),
        quail.builder.Builder()
    )

if quail.helper.OS_WINDOWS:
    quail.run(
        quail.Install(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            solution=quail.SolutionPacked(path='OpenHardwareMonitor'),
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIcon('icon.ico')
        )
    )
