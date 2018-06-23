#!/usr/bin/python3

import os
import os.path
import quail
import platform


def print_progress(percent):
    print("%s%%" % percent)


if quail.helper.OS_LINUX:
    quail.run(
        solution=quail.SolutionPacked(path='Allum1'),
        installer=quail.Installer(
            name='Allum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True,
            launch_with_quail=False
        ),
        builder=quail.builder.Builder(),
        controller=quail.ControllerTkinter()
    )

if quail.helper.OS_WINDOWS:
    quail.run(
        solution=quail.SolutionPacked(path='OpenHardwareMonitor'),
        installer=quail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True,
            launch_with_quail=False
        ),
        builder=quail.builder.Builder(
            quail.builder.CmdIcon('icon.ico')
        ),
        controller=quail.ControllerTkinter()
    )
