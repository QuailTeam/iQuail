#!/usr/bin/python3

import quail

if not quail.helper.OS_WINDOWS:
    raise AssertionError("This test solution is windows only")


class FrameSelectMiniOrFull(quail.controller_tkinter.FrameBaseConfigure):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.version_selected = self.add_combobox("Which version would you like to install?",
                                                  ('Full', 'Mini'))

    def next_pressed(self):
        print(self.version_selected.get())
        self.controller.switch_to_install_frame()


quail.run(
    solution=quail.SolutionGitHub("cmder_mini.zip", "https://github.com/cmderdev/cmder"),
    installer=quail.Installer(
        name='Cmder',
        icon='Cmder.exe',
        binary='Cmder.exe',
        console=False,
        launch_with_quail=True
    ),
    builder=quail.builder.Builder(
        quail.builder.CmdIcon('icon.ico'),
        quail.builder.CmdNoconsole()
    ),
    controller=quail.ControllerTkinter(install_custom_frame=FrameSelectMiniOrFull)
)
