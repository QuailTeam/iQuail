#!/usr/bin/python3

import iquail

if iquail.helper.OS_LINUX:
    iquail.run(
        solution=iquail.SolutionPacked(path='Allum1'),
        installer=iquail.Installer(
            publisher="alies",
            name='Allum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True,
            launch_with_quail=True
        ),
        builder=iquail.builder.Builder(
            iquail.builder.CmdNoconsole()
        ),
        controller=iquail.ControllerTkinter()
    )

if iquail.helper.OS_WINDOWS:
    iquail.run(
        solution=iquail.SolutionPacked(path='OpenHardwareMonitor'),
        installer=iquail.Installer(
            publisher="OHM",
            requires_root=True,
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True,
            launch_with_quail=True
        ),
        builder=iquail.builder.Builder(
            iquail.builder.CmdIcon('icon.ico'),
            iquail.builder.CmdNoconsole()
        ),
        controller=iquail.ControllerTkinter()
    )
