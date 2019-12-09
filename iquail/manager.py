import os
import stat
import sys
import logging

from . import helper
from .helper import misc
from .constants import Constants
from .solution.solutioner import Solutioner
from .validate import Validate


logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, installer, solution, builder, graphical, *, conf_ignore=None):
        self._graphical = graphical
        self._installer = installer
        self._solution = solution
        self._builder = builder
        self._solutioner = Solutioner(self._solution,
                                      self,
                                      self._installer.get_solution_path(),
                                      conf_ignore=conf_ignore)
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
        version = self._solution.get_version_string()
        logger.info("Manager got solution version: " + str(version))
        return version

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
        # permission checked here because tkinter calls this method directly instead of install()
        self.apply_conf()  # because conf have been just selected
        self._solutioner.install()
        self._set_solution_installed_version()

    def install_part_register(self):
        """this part of the installation will register the solution
        """
        self._installer.register()
        self._chmod_binary()
        self.config.save()
        logger.info("Saved config")

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
        logger.info("Updating...")
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

    def validate_solution(self, path):
        v = Validate(os.path.realpath(
            path), self._installer, self._builder)
        return v.run()

    def restart_quail(self):
        os.chdir(self._installer.get_solution_path())
        binary = self._installer.launcher_binary
        binary_args = [binary] + misc.filter_iquail_args(sys.argv[1:])
        logger.info("Restarting quail: %s with args: %s" %
                    (binary, str(binary_args)))
        os.execl(binary, *binary_args)

    def run(self):
        """Run solution"""
        # TODO: self.config.save() config could be used for "don't ask me again to update" feature
        binary = self._installer.binary
        if self.solutioner.get_iquail_update() is not None:
            # TODO: verify binary (run validations)
            misc.exit_and_replace(
                misc.get_script(), self.solutioner.get_iquail_update(), run=True)
        self._chmod_binary()
        args = misc.filter_iquail_args(sys.argv[1:])
        binary_args = [os.path.basename(binary)] + args
        os.chdir(self._installer.get_solution_path())
        logger.info("Running: %s with args: %s" % (binary, str(binary_args)))
        os.execl(binary, *binary_args)

    def check_permissions(self, uid):
        if self._installer.install_systemwide and os.geteuid() != 0:
            # TODO fix os.geteuid doesn't exist on windows
            if self._graphical is False:
                logger.error(
                    'Root access is required for further action, relaunching as root')
            logger.info("Re-running as admin with UID %s" % str(uid))
            misc.rerun_as_admin(self._graphical, uid)
