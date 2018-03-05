
import configparser
import pathlib
import os.path
import shutil
from .installer_base import InstallerBase
from .constants import Constants
from .helper import Helper

'''
Notes for all user install:

path = os.path.join(os.sep, "usr", "share", "applications",
                            "%s.desktop" % (binary))

Files /opt

'''


class InstallerLinux(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shortcut = self._get_desktop_path(self.name)
        self._shortcut_uninstall = self._get_desktop_path("%s_uninstall" %
                                                          (self.name))

    def _get_desktop_path(self, name):
        return os.path.join(pathlib.Path.home(),
                            ".local", "share", "applications",
                            "%s.desktop" % (name))

    def _write_desktop(self, filename, app_config):
        '''Write desktop entry'''
        config = configparser.ConfigParser()
        config.optionxform = str
        config['Desktop Entry'] = app_config
        with open(filename, "w") as f:
            config.write(f)

    def _register_app(self):
        app_config = {
            'Name': self.name,
            'Path': self.get_install_path(),
            'Exec': self.get_install_path(Helper.get_script_name()),
            'Icon': self.get_install_path(self.icon),
            'Terminal': 'true' if self.console else 'false',
            'Type': 'Application'
        }
        self._write_desktop(self._shortcut, app_config)
        app_config["Exec"] = app_config["Exec"] + \
            " " + Constants.ARGUMENT_UNINSTALL
        app_config["Name"] = "Uninstall " + app_config["Name"]
        self._write_desktop(self._shortcut_uninstall, app_config)

    def install(self):
        super().install()
        self._register_app()

    def uninstall(self):
        super().uninstall()
        os.remove(self._shortcut)
        os.remove(self._shortcut_uninstall)

    def is_installed(self):
        if super().is_installed() and os.path.isfile(self._shortcut):
            return True
        return False
