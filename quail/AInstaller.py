import os
import pathlib
import shutil
from .Helper import Helper
from .Config import Config


class AInstaller:

    def __init__(self, config):
        if not isinstance(config, Config):
            raise AssertionError("Expecting quail.Config()")
        self._config = config
        self._install_path = self.build_install_path()

    @property
    def config(self):
        return self._config

    def build_install_path(self):
        '''Build install path
        This function can be overriden to install files to somewhere else
        '''
        return os.path.join(pathlib.Path.home(), '.quail', self.config.name)

    def get_install_path(self, *args):
        '''Get file from install path'''
        return os.path.join(self._install_path, *args)

    def install(self):
        solution = self.config.solution
        if not solution.open():
            raise AssertionError("Can't access solution")
        if os.path.exists(self.get_install_path()):
            shutil.rmtree(self.get_install_path())
        # shutil.copytree(self.get_solution_path(), self.get_install_path())
        os.makedirs(self.get_install_path(), 0o777, True)
        for root, dirs, files in solution.walk():
            for sdir in dirs:
                os.makedirs(self.get_install_path(root, sdir), 0o777, True)
            for sfile in files:
                shutil.copy2(solution.get_file(os.path.join(root, sfile)),
                             self.get_install_path(root))
        solution.close()
        shutil.copy2(Helper.get_script(), self.get_install_path())
        if Helper.running_from_script():
            shutil.copytree(Helper.get_module_path(),
                            os.path.join(self.get_install_path(), "quail"))

    def uninstall(self):
        shutil.rmtree(self.get_install_path())

    def is_installed(self):
        return os.path.exists(self.get_install_path())
