import os
import pathlib
import shutil
from . import helper
from .constants import Constants

class InstallerBase:
    '''Register application for the OS'''
    def __init__(self,
                 name,
                 binary,
                 icon,
                 publisher='Quail',
                 console=False):
        self._name = name
        self._binary = binary
        self._icon = icon
        self._publisher = publisher
        self._console = console
        self._install_path = self.build_install_path()

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
        os.makedirs(self.get_install_path(), 0o777, True)
        # install script and module:
        shutil.copy2(helper.get_script(), self.get_install_path())
        if helper.running_from_script():
            shutil.copytree(helper.get_module_path(),
                            os.path.join(self.get_install_path(), "quail"))

    def uninstall(self, on_error=None):
        # TODO: remove only binary and lib
        shutil.rmtree(self.get_install_path(), False, on_error)

    def is_installed(self):
        return os.path.isfile(self.get_install_path(helper.get_script()))
