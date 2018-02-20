import os.path
import pathlib
import shutil
from .tools import *


class AInstaller:
    def __init__(self, name, solution_path, binary, icon, console=False):
        self._solution_path = solution_path
        self._name = name
        self._icon = icon
        self._binary = binary
        self._console = console
        self._install_path = self.get_install_path()

    def get_install_path(self):
        return os.path.join(pathlib.Path.home(), '.quail', self.get_name())
    
    def get_file(self, *args):
        '''Get installed path'''
        if not os.path.exists(self._install_path):
            raise AssertionError("Not installed")
        return os.path.join(self._install_path, *args)

    def get_name(self):
        return self._name

    def get_solution_path(self):
        return self._solution_path

    def get_binary(self):
        return self._binary

    def get_icon(self):
        return self._icon

    def get_console(self):
        return self._console
    
    def install(self):
        if os.path.exists(self._install_path):
            shutil.rmtree(self._install_path)
        shutil.copytree(self.get_solution_path(), self._install_path)
        shutil.copy2(get_script(), self._install_path)
        if (get_script().endswith(".py")):
            shutil.copytree(os.path.join(get_script_path(), "quail"),
                            os.path.join(self._install_path, "quail"))

    def uninstall(self):
        shutil.rmtree(self._install_path)

    def is_installed(self):
        return os.path.exists(self._install_path)

