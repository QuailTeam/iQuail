import os
import pathlib
import shutil
from . import helper
from .constants import Constants
from .solution_downloader import SolutionDownloader

class InstallerBase:

    def __init__(self,
                 name,
                 binary,
                 icon,
                 solution,
                 publisher='Quail',
                 console=False,
                 integrity=False):
        self._name = name
        self._binary = binary
        self._icon = icon
        self._solution = solution
        self._publisher = publisher
        self._console = console
        self._install_path = self.build_install_path()
        self._integrity = integrity

    @property
    def solution(self):
        return self._solution

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def binary(self):
        return self._binary

    @property
    def publisher(self):
        return self._publisher

    @property
    def console(self):
        return self._console

    def build_install_path(self):
        '''Build install path
        This function can be overriden to install files to somewhere else
        '''
        return os.path.join(str(pathlib.Path.home()), '.quail', self.name)

    def get_install_path(self, *args):
        '''Get file from install path'''
        return os.path.join(self._install_path, *args)

    def install(self):
        downloader = SolutionDownloader(self.solution, self.get_install_path())
        downloader.download_all()
        # install script and module:
        shutil.copy2(helper.get_script(), self.get_install_path())
        if helper.running_from_script():
            shutil.copytree(helper.get_module_path(),
                            os.path.join(self.get_install_path(), "quail"))

    def uninstall(self):
        shutil.rmtree(self.get_install_path())

    def is_installed(self):
        return os.path.exists(self.get_install_path())
