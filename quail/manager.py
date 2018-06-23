import os
import stat
import sys

from . import helper
from .solution.solutioner import Solutioner


class Manager:
    def __init__(self, installer, solution, builder):
        self._installer = installer
        self._solution = solution
        self._builder = builder
        self._install_finished_hook = None
        self._install_part_1_hook = None
        self._solutioner = Solutioner(self._solution,
                                      self._installer.get_solution_path())

    def set_solution_hook(self, hook):
        """Set solution update progress hook
        """
        self._solution.set_hook(hook)

    def set_install_part_1_hook(self, hook):
        """Set install part 1 finished hook
        this hook will be called when install_part_1 have been completed
        """
        self._install_part_1_hook = hook

    def set_install_finished_hook(self, hook):
        """Set install finished hook
        this hook will be called when the installation process is done
        """
        self._install_finished_hook = hook

    def get_name(self):
        return self._installer.name

    @property
    def solutioner(self):
        return self._solutioner

    def _chmod_binary(self):
        binary = self._installer.binary
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)

    def build(self):
        if helper.running_from_script():
            self._builder.register(self._solution)
            self._builder.build()
        else:
            raise AssertionError("Can't build from an executable")

    def install_part_1(self):
        self._solutioner.install()
        if self._install_part_1_hook:
            self._install_part_1_hook()

    def install_part_2(self):
        self._installer.register()
        self._chmod_binary()
        if self._install_finished_hook:
            self._install_finished_hook()

    def install(self):
        """Installation process was split in multiple parts
        to allow controller to choose if the installation part must be
        run in a thread or not.
        This is due to windows not allowing registering shortcuts in a thread
        easily.
        """
        self.install_part_1()
        self.install_part_2()

    def uninstall(self):
        self._solutioner.uninstall()
        self._installer.unregister()

    def is_installed(self):
        # TODO: optimisation
        return self._solutioner.installed()  # and self._installer.registered()

    def run(self):
        binary = self._installer.binary
        self._chmod_binary()
        os.system(binary + " " + " ".join(sys.argv[1:]))
