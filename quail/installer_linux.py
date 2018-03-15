
import configparser
import pathlib
import os.path
import shutil
from .installer_base import InstallerBase
from .constants import Constants
from . import helper

class InstallerLinux(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._launch_shortcut = self.name
        self._uninstall_shortcut = "%s_uninstall" % (self.name)

    def _get_desktop_path(self, name):
        return os.path.join(str(pathlib.Path.home()),
                            ".local", "share", "applications",
                            "%s.desktop" % (name))

    def _write_desktop(self, filename, app_config):
        '''Write desktop entry'''
        config = configparser.ConfigParser()
        config.optionxform = str
        config['Desktop Entry'] = app_config
        with open(filename, "w") as f:
            config.write(f)

    def register_app(self, filename, name, binary, icon,
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
        self._write_desktop(self._get_desktop_path(filename), app_config)

    def unregister_app(self, filename):
        os.remove(self._get_desktop_path(filename))

    def registered(self, filename):
        return os.path.isfile(self._get_desktop_path(self._launch_shortcut))

    def install(self):
        super().install()
        binary = self.get_install_path(helper.get_script_name())
        self.register_app(filename=self._launch_shortcut,
                          name=self.name,
                          workpath=self.get_install_path(),
                          binary=binary,
                          icon=self.get_install_path(self.icon),
                          console=self.console
                          )
        self.register_app(filename=self._uninstall_shortcut,
                          name="Uninstall " + self.name,
                          workpath=self.get_install_path(),
                          binary=binary + " " + Constants.ARGUMENT_UNINSTALL,
                          icon=self.get_install_path(self.icon),
                          console=self.console
                          )

    def uninstall(self):
        super().uninstall()
        self.unregister_app(self._launch_shortcut)
        self.unregister_app(self._uninstall_shortcut)

    def is_installed(self):
        if super().is_installed() and self.registered(self._launch_shortcut):
            return True
        return False
