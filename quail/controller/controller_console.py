import sys

from .controller_base import ControllerBase
from ..solution.solution_base import SolutionProgress
from ..helper.traceback_info import ExceptionInfo
from ..errors import SolutionUnreachableError


def _progress_callback(progress: SolutionProgress):
    sys.stdout.write(" %d %% %s ...\r" % (progress.percent, progress.status))
    sys.stdout.flush()


class ControllerConsole(ControllerBase):
    def _excepthook(self, exception_info):
        print("[*] Fatal exception", file=sys.stderr)
        for line in exception_info.traceback:
            print(line, file=sys.stderr, end="")

    def _ask_validate(self, question):
        """Ask to validate question with Y/n input"""
        rep = input("[*] %s (y/n): " % question)
        if rep == 'y' or rep == 'Y':
            return True
        return False

    def start_run_or_update(self):
        if not self.manager.is_new_version_available():
            self.manager.run()
            return
        self.manager.set_solution_progress_hook(_progress_callback)
        print("[*] New version available: %s" % self.manager.get_solution_version())
        try:
            self.manager.update()
            print("[*] Update successful!")
        except SolutionUnreachableError:
            if self._ask_validate("Impossible to update, would you like to run anyway?"):
                self.manager.run()
        else:
            self.manager.run()

    def start_install(self):
        self.manager.set_solution_progress_hook(_progress_callback)
        print("[*] Installing %s" % self.manager.get_name())
        self.manager.install()
        print("[*] Installation successful!")
        self.press_to_exit()

    def start_uninstall(self):
        if self._ask_validate("Would you like to uninstall %s?" % self.manager.get_name()):
            print("[*] Uninstalling %s ..." % self.manager.get_name())
            try:
                self.manager.uninstall()
                print("[*] %s successfully removed!" % self.manager.get_name())
                self.press_to_exit()
            except:
                print("[*] Unknown error while uninstalling %s" % self.manager.get_name())
                self.press_to_exit()

    def press_to_exit(self):
        input("Press enter to exit ...")
