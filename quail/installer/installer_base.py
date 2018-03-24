import os
import pathlib
import shutil
import atexit
import tempfile
import sys
from contextlib import suppress
from abc import ABC, abstractmethod
from .. import helper
from ..constants import Constants

def delete_atexit(to_delete):
    '''On windows we can't remove binaries being run.
    This function will remove a file or folder at exit
    to be able to delete itself
    '''
    def _delete_from_tmp():
        if not (os.path.exists(to_delete) or os.path.isfile(to_delete)):
            return
        tmpdir = tempfile.mkdtemp()
        newscript = shutil.copy2(helper.get_script(), tmpdir)
        args = (newscript, "--quail_rm", to_delete)
        if helper.running_from_script():
            os.execl(sys.executable, sys.executable, *args)
        else:
            os.execl(newscript, *args)
    atexit.register(_delete_from_tmp)

class InstallerBase(ABC):
    '''Register application on the OS'''

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
        self._solution_path = os.path.join(self._install_path, 'solution')

    def _get_install_launcher(self):
        '''Get quail executable install path'''
        return self._get_install_path(helper.get_script_name())

    def _get_solution_icon(self):
        '''Get solution's icon'''
        return self.get_solution_path(self._icon)

    def _get_install_path(self, *args):
        '''Get install path'''
        return os.path.join(self._install_path, *args)

    @property
    def name(self):
        return self._name

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

    def get_solution_path(self, *args):
        '''Get solution path'''
        return os.path.join(self._solution_path, *args)

    @abstractmethod
    def register(self):
        os.makedirs(self._get_install_path(), exist_ok=True)
        # install script and module:
        shutil.copy2(helper.get_script(), self._get_install_launcher())
        if helper.running_from_script():
            shutil.copytree(helper.get_module_path(),
                            self._get_install_path("quail"))

    @abstractmethod
    def unregister(self):
        if helper.running_from_script():
            shutil.rmtree(self._get_install_path("quail"), ignore_errors=True)
            with suppress(FileNotFoundError):
                os.remove(self._get_install_launcher())
            with suppress(OSError):
                os.rmdir(self._get_install_path())
        else:
            # Assuming we can't remove our own binary
            delete_atexit(self._get_install_launcher())

    @abstractmethod
    def registered(self):
        return os.path.isfile(self._get_install_launcher())
