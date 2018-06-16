import sys
from .ui_base import UiBase


class UiConsole(UiBase):
    def exit_install(self):
        input("[*] Installation successful!\nPress enter to quit...")

    def progress_callback(self, progress):
        sys.stdout.write(" %d %% installing ...\r" % progress)
        sys.stdout.flush()

    def start_install(self):
        sys.stdout.write("[*] Installation started\n")
