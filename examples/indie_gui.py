#!/usr/bin/python3

import iquail
import os

if not iquail.helper.OS_LINUX:
    raise AssertionError("This test solution is linux only")


class MyInstaller(iquail.Installer):
    def register(self):
        super().register()
        for file in os.listdir(self.get_solution_path()):
            if ".so." in file:
                os.chmod(self.get_solution_path(file), 0o777)


iquail.run(
    solution=iquail.SolutionGitHub("indie.zip", "https://github.com/QuailTeam/cpp_indie_studio"),
    installer=MyInstaller(
        publisher='tek',
        name='Indie',
        icon='icon.png',
        binary='indie_studio',
        console=False,
        launch_with_quail=True
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.png'),
        iquail.builder.CmdNoconsole()
    ),
    controller=iquail.ControllerTkinter()
)
