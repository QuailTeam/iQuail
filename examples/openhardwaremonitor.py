#!/usr/bin/python3

import iquail

iquail.run(
    solution=iquail.SolutionPacked(path='OpenHardwareMonitor'),
    installer=iquail.Installer(
        publisher="Michael Moller",
        name='OpenHardwareMonitor',
        icon='OpenHardwareMonitor.exe',
        binary='OpenHardwareMonitor.exe',
        console=True,
        launch_with_quail=False
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.ico'),
        iquail.builder.CmdNoconsole(),
        side_img_override="side_img.gif",
    ),
    controller=iquail.ControllerTkinter()
)
