import configparser
import os.path
import pathlib
from contextlib import suppress

from .installer_base import InstallerBase
from ..constants import Constants


class InstallerLinux(InstallerBase):

    def __init__(self, linux_desktop_conf={}, linux_exec_flags='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        if any(c in linux_desktop_conf for c in ['Name', 'Icon', 'Terminal']):
            raise RuntimeError('\'Name\', \'Icon\' and \'Terminal\' fields should be defined in parameters')

        self._desktop_conf = {'Name': self.name,
                              'Icon': self.get_solution_icon(),
                              'Terminal': 'true' if self.console else 'false',
                              'Type': 'Application',
                              'Exec': self.launch_command + ' ' + linux_exec_flags}
        self._desktop_conf.update(linux_desktop_conf)
        self._launch_shortcut = self._desktop(self.uid)
        self._uninstall_shortcut = self._desktop("%s_uninstall" % self.uid)

    def _desktop(self, name):
        return os.path.join(os.path.join(str(pathlib.Path.root), "/usr") if self._install_systemwide
                            else os.path.join(str(pathlib.Path.home()), ".local"),
                            "share", "applications", "%s.desktop" % name)

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

    def build_install_path(self):
        return '/opt/' + os.path.join(Constants.IQUAIL_ROOT_NAME, self.name) if self._install_systemwide else \
            os.path.join(str(pathlib.Path.home()), Constants.IQUAIL_ROOT_NAME, self.name)

    def _register(self):
        self.add_shortcut(dest=self._launch_shortcut,
                          **self._desktop_conf)
        self.add_shortcut(dest=self._uninstall_shortcut,
                          Type='Application',
                          Name="Uninstall " + self.name,
                          Exec=self.iquail_binary + " " + Constants.ARGUMENT_UNINSTALL,
                          Icon=self.get_solution_icon(),
                          Terminal='true' if self.console else 'false')
        self.add_to_path(self.binary, self._binary_name)

    def _unregister(self):
        self.delete_shortcut(self._launch_shortcut)
        self.delete_shortcut(self._uninstall_shortcut)
        self.remove_from_path(self.binary)

    def _registered(self):
        if not self.is_shortcut(self._launch_shortcut):
            return False
        if not self.is_shortcut(self._uninstall_shortcut):
            return False
        return True

    def add_to_path(self, binary, name):
        os.symlink(binary, self.build_symlink_path(name))

    def remove_from_path(self, name):
        os.remove(self.build_symlink_path(name))

    def build_symlink_path(self, name):
        return os.path.join("/usr/bin" if self._install_systemwide
                            else os.path.join(str(pathlib.Path.home()), '.local/bin'), name)

