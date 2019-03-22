import tkinter as tk
from tkinter import messagebox
from tkinter import Text
from tkinter import END
import sys
from tkinter.font import Font
from tkinter import ttk
import threading

from ...solution.solution_base import SolutionProgress
from ..controller_base import ControllerBase
from .frames import FrameBaseInProgress, FrameBaseAccept, FrameBase, FrameBaseTwoChoice
from .error_reporter import ErrorReporter


class FrameAcceptEULA(FrameBaseTwoChoice):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Do you accept the End-User "
                                             "License agreement",
                         "I accept", "I refuse")
        la = Text(self, height=30, width=30)
        la.pack()
        la.insert(END, self.controller.eula)

    def choice1_selected(self):
        if self.controller.install_custom_frame is not None:
            self.controller.switch_frame(self.controller.install_custom_frame)
        else:
            self.controller.switch_frame(FrameInstalling)

    def choice2_selected(self):
        self.quit()


class FrameAcceptInstall(FrameBaseAccept):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="%s installer\nWould you like to install "
                                  "this program?" %
                                  controller.manager.get_name(),
                         positive_str="Install!")

    def accept(self):
        if self.controller.eula_file is not None:
            self.controller.switch_frame(FrameAcceptEULA)
        elif self.controller.install_custom_frame is not None:
            self.controller.switch_frame(self.controller.install_custom_frame)
        else:
            self.controller.switch_frame(FrameInstalling)


class FrameInstalling(FrameBaseInProgress):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Installing...")
        self.manager.set_solution_progress_hook(self.progress_callback)
        thread = self.tk_thread(self.manager.install_part_solution,
                                complete_hook=self.solution_finish_callback)
        thread.start()

    def progress_callback(self, progress: SolutionProgress):
        self.update_label(progress.status.capitalize() + " ...")
        self.update_progress(progress.percent)

    def solution_finish_callback(self):
        self.manager.install_part_register()
        self.controller.switch_frame(FrameInstallFinished)


class FrameInstallFinished(FrameBaseAccept):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="%s successfully installed!" %
                                  controller.manager.get_name(),
                         positive_str="exit")

    def accept(self):
        self.controller.quit_tk()


class FrameAcceptUninstall(FrameBaseAccept):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="%s installer\nWould you like to uninstall this program?" %
                                  controller.manager.get_name(),
                         positive_str="Uninstall!")

    def accept(self):
        self.manager.uninstall()
        self.controller.quit_tk()


class FrameUpdating(FrameBaseInProgress):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Updating...")
        self.manager.set_solution_progress_hook(self.progress_callback)
        thread = self.tk_thread(self.manager.update,
                                complete_hook=self.solution_finish_callback)
        thread.start()

    def progress_callback(self, progress: SolutionProgress):
        self.update_label(progress.status.capitalize() + " ...")
        self.update_progress(progress.percent)

    def solution_finish_callback(self):
        self.controller.quit_tk()
        self.manager.run()


class FrameAskToUpdate(FrameBaseTwoChoice):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="New version is available!\nWould you like to update?",
                         choice1=" update! ",
                         choice2="   run!   ")

    def choice1_selected(self):
        self.controller.switch_frame(FrameUpdating)

    def choice2_selected(self):
        self.manager.run()


class ControllerTkinter(ControllerBase):

    def __init__(self,
                 install_custom_frame=None,
                 ask_for_update=False,
                 *args,
                 **kwargs):
        """ Controller tkinter
        :param install_custom_frame: An instance of FrameBase, this frame will be called during installation
        """
        super().__init__(*args, **kwargs)
        self.tk = None
        self._base_frame = None
        self._frame = None
        self.title_font = None
        self._ask_for_update = ask_for_update
        tk.Tk.report_callback_exception = self.excepthook
        assert install_custom_frame is None or issubclass(install_custom_frame, FrameBase)
        self.install_custom_frame = install_custom_frame

    def quit_tk(self):
        if self.tk is not None:
            self.tk.quit()

    def _start_tk(self, frame, title):
        assert self.tk is None
        # Setup Tk window
        self.tk = tk.Tk()
        self.tk.minsize(width=500, height=200)
        self.tk.maxsize(width=500, height=200)
        self.tk.title(title)
        # Setup base frame
        self.root_frame = tk.Frame()
        self.root_frame.pack(side="top", fill="both", expand=True)
        self.root_frame.grid_rowconfigure(0, weight=1)
        self.root_frame.grid_columnconfigure(0, weight=1)
        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.medium_font = Font(family='Helvetica', size=12)
        # Select frame
        self.switch_frame(frame)
        # Start mainloop
        self.tk.mainloop()

    def switch_to_install_frame(self):
        """Switch to install frame (begin installation)"""
        self.switch_frame(FrameInstalling)

    def switch_frame(self, frame_class, **kwargs):
        assert self.manager is not None
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame_class(parent=self.root_frame,
                                  controller=self,
                                  **kwargs)
        self._frame.grid(row=0, column=0, sticky="nsew")
        self._frame.tkraise()

    def _excepthook(self, exception_info):
        reporter = ErrorReporter("Automatic bug report", exception_info.traceback_str)
        reporter.show()
        self.quit_tk()

    def start_install(self):
        self._start_tk(FrameAcceptInstall,
                       "%s installer" % self.manager.get_name())

    def start_uninstall(self):
        self._start_tk(FrameAcceptUninstall,
                       "%s uninstall" % self.manager.get_name())

    def callback_solution_unreachable_error(self, exception_info):
        name = self.manager.get_name()
        self.quit_tk()
        if self.manager.is_installed():
            rep = messagebox.askyesno("[%s] Impossible to check update" % name,
                                      "Impossible to check update.\n" +
                                      "Check your internet connection!\n" +
                                      "Would you like to run %s anyway?" % name)

            if rep:
                self.manager.run()
        else:
            messagebox.showerror("[%s] solution not reachable!" % name,
                                 "Impossible to install %s\n" % name +
                                 "Check your internet connection, and try again")

    def callback_solution_not_removable_error(self, exception_info):
        messagebox.showerror("Impossible to remove / update application",
                             "Please close application first!")
        self.quit_tk()

    def start_run_or_update(self):
        # TODO: add "checking for update frame"
        if not self.manager.is_new_version_available():
            self.manager.run()
            return
        if self._ask_for_update:
            start_frame = FrameAskToUpdate
        else:
            start_frame = FrameUpdating
        self._start_tk(start_frame,
                       "%s update" % self.manager.get_name())

    def is_graphical(self):
        return True