#!/usr/bin/python3
import os
import iquail
import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(os.path.dirname(__file__), '..', 'iquail.log'),
)

if not iquail.helper.OS_OSX:
    raise AssertionError("This test solution is macOs only")


class FrameSelectMiniOrFull(iquail.controller_tkinter.FrameBaseConfigure):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.version_selected = self.add_combobox("Which version would you like to install?",
                                                  ('2.2.6', '2.2.6'))

    def next_pressed(self):
        print(self.version_selected.get())
        version = self.version_selected.get().lower()
        zip = "cmder_mini.zip" if version == "mini" else "cmder.zip"
        self.manager.config.set("zip_url", zip)
        self.controller.switch_to_install_frame()

iquail.run(
    solution=iquail.SolutionLocal(['Vagrant']),
    installer=iquail.Installer(
        publisher='HashiCorp',
        name='vagrant',
        icon='vagrant.pkg',
        binary='vagrant.pkg',
        console=False,
        launch_with_quail=True,
    ),
    builder=iquail.builder.Builder(
        iquail.builder.CmdIcon('icon.ico'),
        iquail.builder.CmdNoconsole()
    ),
    controller=iquail.ControllerTkinter(
        install_custom_frame=FrameSelectMiniOrFull),
    conf_ignore=["config/*"]
)
