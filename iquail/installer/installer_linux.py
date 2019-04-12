import configparser
import os.path
import pathlib
from contextlib import suppress

from .installer_base import InstallerBase
from ..constants import Constants
from ..helper import misc


class InstallerLinux(InstallerBase):

    def __init__(self, linux_desktop_conf=None, linux_exec_flags='',
                 add_to_path=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._desktop_conf = {'Name': self.name,
                              'Icon': self.get_solution_icon(),
                              'Terminal': 'true' if self.console else 'false',
                              'Type': 'Application',
                              'Exec': self.launch_command + ' ' +
                                      linux_exec_flags}
        if linux_desktop_conf:
            if any(c in linux_desktop_conf for c in
                   ['Name', 'Icon', 'Terminal']):
                raise RuntimeError('\'Name\', \'Icon\' and \'Terminal\' fields'
                                   ' should be defined in parameters of the '
                                   'installer')
            self._desktop_conf.update(linux_desktop_conf)
        self._launch_shortcut = self._desktop(self.name)
        self._uninstall_shortcut = self._desktop("%s_uninstall" % self.name)
        self._add_to_path = add_to_path

    def _desktop(self, name):
        if self._install_systemwide:
            basepath = os.path.join("/", "usr")
        else:
            basepath = os.path.join(str(pathlib.Path.home()), ".local")
        return os.path.join(basepath, "share", "applications",
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

    def build_root_path(self):
        if self._install_systemwide:
            return "/opt/.iquail/"
        else:
            return super().build_root_path()

    def _register(self):
        self.add_shortcut(dest=self._launch_shortcut,
                          **self._desktop_conf)
        self.add_shortcut(dest=self._uninstall_shortcut,
                          Type='Application',
                          Name="Uninstall " + self.name,
                          Exec=self.iquail_binary + " " +
                               Constants.ARGUMENT_UNINSTALL,
                          Icon=self.get_solution_icon(),
                          Terminal='true' if self.console else 'false')
        if self._add_to_path:
            self.add_to_path(self.launcher_binary, self._binary_name)

    def _unregister(self):
        self.delete_shortcut(self._launch_shortcut)
        self.delete_shortcut(self._uninstall_shortcut)
        self.remove_from_path(self._binary_name)

    def _registered(self):
        if not self.is_shortcut(self._launch_shortcut):
            return False
        if not self.is_shortcut(self._uninstall_shortcut):
            return False
        return True

    def add_to_path(self, binary, name):
        os.symlink(binary, self.build_symlink_path(name))

    def remove_from_path(self, name):
        os.unlink(self.build_symlink_path(name))

    @misc.cache_result
    def build_symlink_path(self, name):
        name = os.path.basename(name)
        if self._install_systemwide:
            path = "/usr/bin"
        else:
            path = os.path.join(str(pathlib.Path.home()), '.local', 'bin')
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, name)
