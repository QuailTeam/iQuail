#!/usr/bin/python3

import configparser
import pathlib
import os.path
import shutil
# poc install linux

'''
Notes for all user install:

path = os.path.join(os.sep, "usr", "share", "applications",
                            "%s.desktop" % (binary))

Files /opt

'''

class LinuxInstaller:
    def __init__(self, app_name, solution_path, binary, icon, console=False):
        self.solution_path = solution_path
        self.name = app_name
        self.icon = icon
        self.binary = binary
        self.console = console

    def _copy_files(self):
        dst = os.path.join(pathlib.Path.home(), '.quail', self.name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(self.solution_path, dst)
        return dst

    def _register_app(self, path):
        config = configparser.ConfigParser()
        config.optionxform=str
        config['Desktop Entry'] = {
            'Name': self.name,
            'Path': path,
            'Exec': os.path.join(path, self.binary),
            'Icon': os.path.join(path, self.icon),
            'Terminal': 'true' if self.console else 'false',
            'Type': 'Application'
        }
        path = os.path.join(pathlib.Path.home(),
                        ".local", "share", "applications",
                        "%s.desktop" % (name))

        with open(path, "w") as f:
            config.write(f)

    def user_install(self):
        dst = self._copy_files()
        self._register_app(dst)

if (__name__ == '__main__'):
    solution_path = '/home/mou/perso/quail/test/test_solution/'
    name = 'Lolallum1'
    icon = 'icon.jpeg'
    binary = 'allum1'
    installer = LinuxInstaller(name, solution_path, binary, icon, console=True)
    installer.user_install()
