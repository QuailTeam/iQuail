
import stat
import os
import sys

class Manager:
    def __init__(self, installer, solution):
        self._installer = installer
        self._solution = solution
        self._solution.setup(self._installer.get_install_path())

    def install(self):
        with self._solution as solution:
            solution.get_all()
        self._installer.install()

    def uninstall(self):
        self._installer.uninstall()
        # TODO: solution remove

    def is_installed(self):
        # TODO: check solution installed
        return self._installer.is_installed()

    def run(self):
        binary = self._installer.get_install_path(self._installer.binary)
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)
        os.system(binary + " " + " ".join(sys.argv[1:]))
