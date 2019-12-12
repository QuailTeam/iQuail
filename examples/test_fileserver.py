#!/usr/bin/python3

import iquail

if iquail.helper.OS_LINUX:
	iquail.run(
		solution=iquail.SolutionFileServer('localhost', '4242',
                                       './build_fs', '../iQuailFileServer'),
		#solution=iquail.SolutionFileServer('localhost', '4242', '../iQuailFileServer/build'),
		installer=iquail.Installer(
			name='Allum1',
			publisher='alies',
			icon='icon.jpg',
			binary='allum1',
			console=True,
			launch_with_quail=True
		),
		builder=iquail.builder.Builder(),
		controller=iquail.ControllerTkinter()
	)
else:
	iquail.run(
		solution=iquail.SolutionFileServer('192.168.0.13', '4242', '../iQuailFileServer/build'),
		installer=iquail.Installer(
			publisher="Michael Moller",
			name='OpenHardwareMonitor',
			icon='OpenHardwareMonitor.exe',
			binary='OpenHardwareMonitor.exe',
			console=True,
			launch_with_quail=True,
			requires_root=True
		),
		builder=iquail.builder.Builder(
			iquail.builder.CmdIcon('icon.ico'),
			iquail.builder.CmdNoconsole(),
			side_img_override="side_img.gif",
		),
		controller=iquail.ControllerTkinter()
	)

