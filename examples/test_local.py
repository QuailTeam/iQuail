#!/usr/bin/python3

import os
import os.path
import iquail
import platform

if iquail.helper.OS_LINUX:
    solution_path = ['Allum1']
    iquail.run(
        iquail.SolutionLocal(['Allum1']),
        iquail.Installer(
            name='Allum1',
            icon='icon.jpeg',
            binary='allum1',
            console=True,
            linux_exec_flags='%f',
            linux_desktop_conf={
                'MimeTypes': 'text/plain',
                'Comment': 'best game ever'
            }
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIntegrity(solution_path)
        )
    )
if iquail.helper.OS_WINDOWS:
    solution_path = ['OpenHardwareMonitor']
    iquail.run(
        iquail.SolutionLocal(['OpenHardwareMonitor']),
        iquail.Installer(
            name='OpenHardwareMonitor',
            icon='OpenHardwareMonitor.exe',
            binary='OpenHardwareMonitor.exe',
            console=True
        ),
        iquail.builder.Builder(
            iquail.builder.CmdIntegrity(solution_path)
        )
    )
