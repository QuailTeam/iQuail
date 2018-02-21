
import configparser
import pathlib
import os.path
import shutil
from .AInstaller import AInstaller
from .tools import *
# poc install linux

'''
Notes for all user install:

path = os.path.join(os.sep, "usr", "share", "applications",
                            "%s.desktop" % (binary))

Files /opt

'''

class LinuxInstaller(AInstaller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        apps_path =  os.path.join(pathlib.Path.home(),
                                     ".local", "share", "applications")
        self.desktop = os.path.join(apps_path,
                                    "%s.desktop" % (self.get_name()))
        self.desktop_uninstall = os.path.join(apps_path,
                                              "%s.uninstall.desktop" % (self.get_name()))

    def _write_desktop(self, filename, app_config):
        '''Write desktop entry'''
        config = configparser.ConfigParser()
        config.optionxform=str
        config['Desktop Entry'] = app_config
        with open(filename, "w") as f:
            config.write(f)
        
    def _register_app(self):
        app_config = {
            'Name': self.get_name(),
            'Path': self.get_install_path(),
            'Exec': self.get_install_path(get_script_name()),
            'Icon': self.get_install_path(self.get_icon()),
            'Terminal': 'true' if self.get_console() else 'false',
            'Type': 'Application'
        }
        self._write_desktop(self.desktop, app_config)
        app_config["Exec"] = app_config["Exec"] + " --uninstall"
        app_config["Name"] = "Uninstall " + app_config["Name"]
        self._write_desktop(self.desktop_uninstall, app_config)

    def install(self):
        super().install()
        self._register_app()

    def uninstall(self):
        super().uninstall()
        os.remove(self.desktop)
        os.remove(self.desktop_uninstall)

    def is_installed(self):
        if super().is_installed() and os.path.isfile(self.desktop):
            return True
        return False

