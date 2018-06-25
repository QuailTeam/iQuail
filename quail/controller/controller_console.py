import sys

from quail.solution.solution_base import SolutionProgress
from .controller_base import ControllerBase


def _progress_callback(progress: SolutionProgress):
    sys.stdout.write(" %d %% %s ...\r" % (progress.percent, progress.status))
    sys.stdout.flush()


class ControllerConsole(ControllerBase):
    def start_update(self, manager):
        manager.set_solution_progress_hook(_progress_callback)
        print("[*] New version available: %s" % manager.get_solution_version())
        manager.update()
        print("[*] Update successful!")

    def start_install(self, manager):
        manager.set_solution_progress_hook(_progress_callback)
        print("[*] Installing %s" % manager.get_name())
        manager.install()
        print("[*] Installation successful!")
        self.press_to_exit()

    def start_uninstall(self, manager):
        rep = input("[*] Would you like to uninstall %s? (y/n): " % manager.get_name())
        if rep == 'y' or rep == 'Y':
            print("[*] Uninstalling %s ..." % manager.get_name())
            try:
                manager.uninstall()
                print("[*] %s successfully removed!" % manager.get_name())
                self.press_to_exit()
            except:
                print("[*] Unknown error while uninstalling %s" % manager.get_name())
                self.press_to_exit()

    def press_to_exit(self):
        input("Press enter to exit ...")
