import os.path
import pathlib
import shutil
from .tools import *


class AInstaller:

    def __init__(self, name, solution, binary, icon, publisher='Quail', console=False):
        self._solution = solution
        self._name = name
        self._icon = icon
        self._binary = binary
        self._publisher = publisher
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

    def get_name(self):
        return self._name

    def get_binary(self):
        return self._binary

    def get_publisher(self):
        return self._publisher

    def get_icon(self):
        return self._icon

    def get_console(self):
        return self._console

    def install(self):
        if not self._solution.access():
            raise AssertionError("Can't access solution")
        if os.path.exists(self.get_install_path()):
            shutil.rmtree(self.get_install_path())
        # shutil.copytree(self.get_solution_path(), self.get_install_path())
        makedirs_ignore(self.get_install_path())
        self._solution.open()
        for root, dirs, files in self._solution.walk():
            for sdir in dirs:
                makedirs_ignore(self.get_install_path(root, sdir))
            for sfile in files:
                shutil.copy2(self._solution.get_file(os.path.join(root, sfile)),
                             self.get_install_path(root))
        self._solution.close()
        shutil.copy2(get_script(), self.get_install_path())
        if run_from_script():
            shutil.copytree(get_module_path(),
                            os.path.join(self.get_install_path(), "quail"))

    def uninstall(self):
        shutil.rmtree(self.get_install_path())

    def is_installed(self):
        return os.path.exists(self.get_install_path())
