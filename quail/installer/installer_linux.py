
import configparser
import pathlib
import os.path
import shutil
from contextlib import suppress
from ..constants import Constants
from .. import helper
from .installer_base import InstallerBase


class InstallerLinux(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._launch_shortcut = self._desktop(self.name)
        self._uninstall_shortcut = self._desktop("%s_uninstall" % (self.name))

    def _desktop(self, name):
        return os.path.join(str(pathlib.Path.home()),
                            ".local", "share", "applications",
                            "%s.desktop" % (name))

    def _write_desktop(self, filename, app_config):
        '''Write desktop entry'''
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        config = configparser.ConfigParser()
        config.optionxform = str
        config['Desktop Entry'] = app_config
        with open(filename, "w") as f:
            config.write(f)

    def add_shortcut(self, dest, name, binary, icon,
                     workpath=None, console=None):
        if not workpath:
            workpath = os.path.dirname(binary)
        app_config = {
            'Name': name,
            'Path': workpath,
            'Exec': binary,
            'Icon': icon,
            'Terminal': 'true' if console else 'false',
            'Type': 'Application'
        }
        self._write_desktop(dest, app_config)

    def delete_shortcut(self, dest):
        with suppress(FileNotFoundError):
            os.remove(dest)

    def is_shortcut(self, dest):
        # TODO: abs shortcut path & add desktop var
        return os.path.isfile(dest)

    def register(self):
        super().register()
        binary = self._get_install_launcher()
        self.add_shortcut(dest=self._launch_shortcut,
                          name=self.name,
                          workpath=self.get_solution_path(),
                          binary=binary,
                          icon=self._get_solution_icon(),
                          console=self.console
                          )
        self.add_shortcut(dest=self._uninstall_shortcut,
                          name="Uninstall " + self.name,
                          workpath=self.get_solution_path(),
                          binary=binary + " " + Constants.ARGUMENT_UNINSTALL,
                          icon=self._get_solution_icon(),
                          console=self.console
                          )

    def unregister(self):
        super().unregister()
        self.delete_shortcut(self._launch_shortcut)
        self.delete_shortcut(self._uninstall_shortcut)

    def registered(self):
        if not super().registered():
            return False
        if not self.is_shortcut(self._launch_shortcut):
            return False
        if not self.is_shortcut(self._uninstall_shortcut):
            return False
        return True
