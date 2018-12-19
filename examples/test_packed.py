#!/usr/bin/python3

import os
import os.path
import iquail
import platform


def print_progress(percent):
    print("%s%%" % percent)


if iquail.helper.OS_LINUX:
    iquail.run(
        iquail.SolutionPacked(path='Allum1'),
        iquail.Installer(
            name='Allum1',
            icon='icon.jpeg',
            publisher='alies',
            binary='allum1',
            console=True,
            launch_with_quail=False
        ),
        iquail.builder.Builder()
    )

if iquail.helper.OS_WINDOWS:
    iquail.run(
        iquail.SolutionPacked(path='OpenHardwareMonitor'),
        iquail.Installer(
            publisher='OHM',
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True,
            launch_with_quail=False
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIcon('icon.ico')
        )
    )
