
import configparser
import pathlib
import os.path
import shutil
from contextlib import suppress
from ..constants import Constants
from .. import helper
from .installer_base import InstallerBase


class InstallerLinux(InstallerBase):

    def __init__(self, binary, exec_flags='', *args, **kwargs):
        super().__init__(binary, *args, **kwargs)
        self._exec_flags = exec_flags
        self._launch_shortcut = self._desktop(self.name)
        self._uninstall_shortcut = self._desktop("%s_uninstall" % self.name)
        self._kwargs = kwargs

    def _desktop(self, name):
        return os.path.join(str(pathlib.Path.home()),
                            ".local", "share", "applications",
                            "%s.desktop" % (name))

    def _write_desktop(self, filename, app_config):
        """Write desktop entry"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        config['Desktop Entry'] = app_config
        with open(filename, "w") as f:
            config.write(f, space_around_delimiters=False)

    def add_shortcut(self, dest, **kwargs):

        if kwargs.get('Path', None) is None:
            kwargs.update(Path=os.path.dirname(self.launcher_binary))
        if kwargs.get('Exec', None) is None:
            kwargs.update(Exec=self.launcher_binary + ' ' + self.binary_options + ' ' + self._exec_flags)
        if kwargs.get('Type', None) is None:
            kwargs.update(Type='Application')

        app_config = kwargs
        self._write_desktop(dest, app_config)

    def delete_shortcut(self, dest):
        with suppress(FileNotFoundError):
            os.remove(dest)

    def is_shortcut(self, dest):
        # TODO: abs shortcut path & add desktop var
        return os.path.isfile(dest)

    def _register(self):
        self.add_shortcut(dest=self._launch_shortcut,
                          **self._kwargs)
        self.add_shortcut(dest=self._uninstall_shortcut,
                          name="Uninstall " + self.name,
                          workpath=self.get_solution_path(),
                          binary=self.quail_binary + " " + Constants.ARGUMENT_UNINSTALL,
                          icon=self.get_solution_icon(),
                          console=self.terminal
                          )

    def _unregister(self):
        self.delete_shortcut(self._launch_shortcut)
        self.delete_shortcut(self._uninstall_shortcut)

    def _registered(self):
        if not self.is_shortcut(self._launch_shortcut):
            return False
        if not self.is_shortcut(self._uninstall_shortcut):
            return False
        return True
