from .solution.solutioner import Solutioner
from . import helper
import stat
import os
import sys


class Manager:
    def __init__(self, installer, solution, builder):
        self._installer = installer
        self._solution = solution
        self._builder = builder
        self.__solutioner = None

    @property
    def _solutioner(self):
        if self.__solutioner is None:
            self.__solutioner = Solutioner(self._solution,
                                           self._installer.get_solution_path())
        return self.__solutioner

    def build(self):
        if helper.running_from_script():
            self._builder.register(self._solution)
            self._builder.build()
        else:
            raise AssertionError("Can't build from an executable")

    def install(self):
        self._solutioner.install()
        self._installer.register()

    def uninstall(self):
        self._solutioner.uninstall()
        self._installer.unregister()

    def is_installed(self):
        # TODO: optimisation
        return self._solutioner.installed() and self._installer.registered()

    def run(self):
        binary = self._installer.get_solution_path(self._installer.binary)
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)
        os.system(binary + " " + " ".join(sys.argv[1:]))
