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
        self._install_path = self.build_install_path()

    def build_install_path(self):
        '''Build install path
        This function can be overriden to install files to somewhere else
        '''
        return os.path.join(pathlib.Path.home(), '.quail', self.get_name())
    
    def get_install_path(self, *args):
        '''Get file from install path'''
        return os.path.join(self._install_path, *args)
    
    def get_solution_path(self, *args):
        '''Get file from solution
        get_solution_path should be used only before installation
        '''
        if self.is_installed():
            raise AssertionError("Solution installed, use get_install_path instead")
        return os.path.join(self._solution_path, *args)
    
    def get_name(self):
        return self._name

    def get_binary(self):
        return self._binary

    def get_icon(self):
        return self._icon

    def get_console(self):
        return self._console
    
    def install(self):
        if os.path.exists(self.get_install_path()):
            shutil.rmtree(self.get_install_path())
        shutil.copytree(self.get_solution_path(), self.get_install_path())
        shutil.copy2(get_script(), self.get_install_path())
        if run_from_script():
            shutil.copytree(os.path.join(get_script_path(), "quail"),
                            os.path.join(self.get_install_path(), "quail"))

    def uninstall(self):
        shutil.rmtree(self.get_install_path())

    def is_installed(self):
        return os.path.exists(self.get_install_path())

