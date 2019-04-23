#!/usr/bin/python3

import os
import os.path
import iquail
import platform
from iquail.controller import ControllerTkinter

if iquail.helper.OS_LINUX:
    solution_path = ['examples/Allum1']
    iquail.run(
        iquail.SolutionLocal(solution_path),
        iquail.Installer(
            name='Allum1',
            publisher='alies',
            icon='icon.jpeg',
            binary='allum1',
            console=True,
            install_systemwide=True,
            linux_exec_flags='%f',
            linux_desktop_conf={
                'MimeTypes': 'text/plain',
                'Comment': 'best game ever'
            }
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIntegrity(solution_path)
        ),
        controller=ControllerTkinter(eula='FRANCIS')
    )
if iquail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    iquail.run(
        iquail.SolutionLocal(['OpenHardwareMonitor']),
        iquail.Installer(
            publisher='OHM',
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIntegrity(solution_path)
        )
    )
