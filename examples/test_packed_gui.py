#!/usr/bin/python3

import os
import os.path
import quail
import platform


def print_progress(percent):
    print("%s%%" % (percent))


if quail.helper.OS_LINUX:
    quail.run(
        quail.SolutionPacked(path='Allum1'),
        quail.Installer(
            name='Allum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True
        ),
        quail.builder.Builder(),
        quail.UITkinter()
    )

if quail.helper.OS_WINDOWS:
    quail.run(
        quail.SolutionPacked(path='OpenHardwareMonitor'),
        quail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True
        ),
        quail.builder.Builder(
            quail.builder.CmdIcon('icon.ico')
        ),
        quail.UITkinter()
    )
