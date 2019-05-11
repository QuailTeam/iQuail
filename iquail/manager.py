import os
import stat
import sys
from .helper import misc

from . import helper
from .constants import Constants
from .solution.solutioner import Solutioner

class Manager:
    def __init__(self, installer, solution, builder, graphical):
        self._exec_dir = os.getcwd()
        self._exec_bin = os.path.basename(sys.argv[0])
        self._graphical = graphical
        self._installer = installer
        self._solution = solution
        self._builder = builder
        self._solutioner = Solutioner(self._solution,
                                      self._installer.get_solution_path())
        self._config = helper.Configuration(
            self._installer.get_install_path(Constants.CONFIG_FILE)
        )
        if self.is_installed():
            # If iquail is not installed the conf doesn't exist yet
            self.config.read()
            self.apply_conf()

    @property
    def uid(self):
        return self._installer.uid

    def apply_conf(self):
        """Apply configuration on Manager's arguments
        (replace ConfVars with their actual values"""
        self.config.apply(self._solution, self._installer)

    def _get_version_file_path(self):
        return self._installer.get_install_path(Constants.VERSION_FILE)

    def _chmod_binary(self):
        binary = self._installer.binary
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)

    def _set_solution_installed_version(self):
        version = self.get_solution_version()
        if version is None:
            return
        with open(self._get_version_file_path(), "w") as f:
            f.write(version)

    # Hooks
    def set_solution_progress_hook(self, hook):
        """Set solution update progress hook
        """
        self._solution.set_progress_hook(hook)

    def get_name(self):
        """Get solution name"""
        return self._installer.name

    @property
    def config(self):
        return self._config

    @property
    def solutioner(self):
        return self._solutioner

    def build(self):
        """Build binary"""
        if helper.running_from_script():
            self._builder.register(self._solution)
            self._builder.build()
        else:
            raise AssertionError("Can't build from an executable")

    def get_solution_version(self):
        """Get version from solution"""
        return self._solution.get_version_string()

    def get_installed_version(self):
        """Get installed version"""
        if not os.path.isfile(self._get_version_file_path()):
            return None
        with open(self._get_version_file_path(), "r") as f:
            return f.readline()

    def is_new_version_available(self):
        """Check if new version is available
        """
        return self.get_installed_version() != self.get_solution_version()

    def install_part_solution(self):
        """part 1 of the installation will install the solution
        """
        #permission checked here because tkinter calls this method directly instead of install()
        self.apply_conf()  # because conf have been just selected
        self._solutioner.install()
        self._set_solution_installed_version()

    def install_part_register(self):
        """this part of the installation will register the solution
        """
        self._installer.register()
        self._chmod_binary()
        self.config.save()

    def install(self):
        """Installation process was split in multiple parts
        to allow controller to choose if the installation part must be
        run in a thread or not.
        This is due to windows not allowing registering shortcuts in a thread
        easily.
        """
        self.install_part_solution()
        self.install_part_register()

    def update(self):
        """Update process"""
        # TODO: kill solution here
        self._solutioner.update()
        self._set_solution_installed_version()

    def uninstall(self):
        """ Uninstall process
        """
        self._installer.unregister()
        self._solutioner.uninstall()

    def is_installed(self):
        """Check if solution is installed"""
        return self._solutioner.installed()  # and self._installer.registered()

    def run(self):
        """Run solution"""
        # self.config.save() config could be used for "don't ask me again to update" feature
        binary = self._installer.binary
        self._chmod_binary()
        args = list(filter(lambda x: "--iquail" not in x, sys.argv[1:]))
        binary_args = [os.path.basename(binary)] + args
        os.chdir(self._installer.get_solution_path())
        os.execl(binary, *binary_args)

    def check_permissions(self):
        return not (self._installer.install_systemwide and os.geteuid() != 0)

