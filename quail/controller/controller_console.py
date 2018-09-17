import sys

from .controller_base import ControllerBase
from ..solution.solution_base import SolutionProgress
from ..helper.traceback_info import ExceptionInfo


def _progress_callback(progress: SolutionProgress):
    sys.stdout.write(" %d %% %s ...\r" % (progress.percent, progress.status))
    sys.stdout.flush()


class ControllerConsole(ControllerBase):
    def exception_hook(self, exception):
        print("[*] Fatal exception", file=sys.stderr)
        for line in ExceptionInfo(exception).traceback:
            print(line, file=sys.stderr, end="")

    def _start_update(self):
        self.manager.set_solution_progress_hook(_progress_callback)
        print("[*] New version available: %s" % self.manager.get_solution_version())
        self.manager.update()
        print("[*] Update successful!")

    def _start_install(self):
        self.manager.set_solution_progress_hook(_progress_callback)
        print("[*] Installing %s" % self.manager.get_name())
        self.manager.install()
        print("[*] Installation successful!")
        self.press_to_exit()

    def _start_uninstall(self):
        rep = input("[*] Would you like to uninstall %s? (y/n): " % self.manager.get_name())
        if rep == 'y' or rep == 'Y':
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
