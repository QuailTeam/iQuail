import configparser
import pathlib
import os.path
import shutil
from contextlib import suppress
from ..constants import Constants
from .. import helper
from .installer_base import InstallerBase


class InstallerLinux(InstallerBase):

    def __init__(self, linux_desktop_conf={}, linux_exec_flags='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._desktop_conf = linux_desktop_conf
        self._launch_shortcut = self._desktop(self.name)
        self._uninstall_shortcut = self._desktop("%s_uninstall" % self.name)

        if self._desktop_conf.get('Name') is None:
            self._desktop_conf.update(Name=self.name)
        elif self._desktop_conf.get('Name') != self.name:
            raise RuntimeError('Name field in configuration does not match the one in parameters')
        if self._desktop_conf.get('Icon') is None:
            self._desktop_conf.update(Icon=self.get_solution_icon())
        elif self._desktop_conf.get('Icon') != self._icon:
            raise RuntimeError('Icon field in configuration does not match the one in parameters')
        if self._desktop_conf.get('Terminal') is None:
            self._desktop_conf.update(Terminal='true' if self.console else 'false')
        elif self._desktop_conf.get('Terminal') != self.console:
            raise RuntimeError('Terminal field in configuration does not match the one in parameters')
        if self._desktop_conf.get('Type') is None:
            self._desktop_conf.update(Type='Application')
        if self._desktop_conf.get('Exec') is None:
            self._desktop_conf.update(Exec=self.launch_command + ' ' + linux_exec_flags)

    def _desktop(self, name):
        return os.path.join(str(pathlib.Path.home()),
                            ".local", "share", "applications",
                            "%s.desktop" % name)

    def _write_desktop(self, filename, app_config):
        """Write desktop entry"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        config['Desktop Entry'] = app_config
        with open(filename, "w") as f:
            config.write(f, space_around_delimiters=False)

    def add_shortcut(self, dest, **app_config):
        self._write_desktop(dest, app_config)

    def delete_shortcut(self, dest):
        with suppress(FileNotFoundError):
            os.remove(dest)

    def is_shortcut(self, dest):
        # TODO: abs shortcut path & add desktop var
        return os.path.isfile(dest)

    def _register(self):
        self.add_shortcut(dest=self._launch_shortcut,
                          **self._desktop_conf)
        self.add_shortcut(dest=self._uninstall_shortcut,
                          Type='Application',
                          Name="Uninstall " + self.name,
                          Exec=self.quail_binary + " " + Constants.ARGUMENT_UNINSTALL,
                          Icon=self.get_solution_icon(),
                          Terminal='true' if self.console else 'false')

    def _unregister(self):
        self.delete_shortcut(self._launch_shortcut)
        self.delete_shortcut(self._uninstall_shortcut)

    def _registered(self):
        if not self.is_shortcut(self._launch_shortcut):
            return False
        if not self.is_shortcut(self._uninstall_shortcut):
            return False
        return True
