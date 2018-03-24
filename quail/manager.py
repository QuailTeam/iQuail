
from .solution.solutioner import Solutioner
import stat
import os
import sys


class Manager:
    def __init__(self, installer, solution):
        self._installer = installer
        self._solutioner = Solutioner(solution,
                                      self._installer.get_solution_path())

    def install(self):
        self._solutioner.install()
        self._installer.register()

    def uninstall(self):
        self._solutioner.uninstall()
        self._installer.unregister()

    def is_installed(self):
        # TODO: check solution installed
        return self._solutioner.installed() and self._installer.registered()

    def run(self):
        binary = self._installer.get_solution_path(self._installer.binary)
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)
        os.system(binary + " " + " ".join(sys.argv[1:]))
