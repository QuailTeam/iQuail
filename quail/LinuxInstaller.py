
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
        self.install_path = os.path.join(pathlib.Path.home(), '.quail', self.get_name())

    def _copy_files(self):
        if os.path.exists(self.install_path):
            shutil.rmtree(self.install_path)
        shutil.copytree(self.get_solution_path(), self.install_path)
        shutil.copy2(get_script(), self.install_path)
        if (get_script().endswith(".py")):
            # copy quail if its not run in standalone
            shutil.copytree(os.path.join(get_script_path(), "quail"),
                            os.path.join(self.install_path, "quail"))

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
            'Path': self.install_path,
            'Exec': self.get_file(get_script_name()),
            'Icon': self.get_file(self.get_icon()),
            'Terminal': 'true' if self.get_console() else 'false',
            'Type': 'Application'
        }
        self._write_desktop(self.desktop, app_config)
        app_config["Exec"] = app_config["Exec"] + " --uninstall"
        app_config["Name"] = "Uninstall " + app_config["Name"]
        self._write_desktop(self.desktop_uninstall, app_config)

    def get_file(self, *args):
        if not os.path.exists(self.install_path):
            raise AssertionError("Not installed")
        return os.path.join(self.install_path, *args)

    def install(self):
        self._copy_files()
        self._register_app()

    def uninstall(self):
        shutil.rmtree(self.install_path)
        os.remove(self.desktop)
        os.remove(self.desktop_uninstall)

    def is_installed(self):
        if os.path.exists(self.install_path) and os.path.isfile(self.desktop):
            return True
        return False

