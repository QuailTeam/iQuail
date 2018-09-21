import tkinter as tk
import sys
from tkinter.font import Font
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askretrycancel
import threading

from ...solution.solution_base import SolutionProgress
from ..controller_base import ControllerBase
from .frames import FrameInProgress, FrameAccept, FrameBase


class FrameAcceptInstall(FrameAccept):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="%s installer\nWould you like to install this program?" %
                                  controller.manager.get_name(),
                         positive_str="Install!")

    def accept(self):
        self.controller.switch_frame(FrameInstalling)


class FrameInstalling(FrameInProgress):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Installing...")
        self.manager.set_solution_progress_hook(self.progress_callback)
        self.manager.set_install_finished_hook(self.install_finished_callback)
        self.manager.set_install_part_solution_hook(self.solution_finished_callback)
        thread = self.tk_thread(self.manager.install_part_solution)
        thread.start()

    def progress_callback(self, progress: SolutionProgress):
        self.update_label(progress.status.capitalize() + " ...")
        self.update_progress(progress.percent)

    def solution_finished_callback(self):
        self.controller.tk.after(0, self.manager.install_part_register)

    def install_finished_callback(self):
        self.controller.switch_frame(FrameInstallFinished)


class FrameInstallFinished(FrameAccept):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="%s successfully installed!" %
                                  controller.manager.get_name(),
                         positive_str="exit")

    def accept(self):
        self.controller.tk.quit()


class FrameAcceptUninstall(FrameAccept):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         question="%s installer\nWould you like to uninstall this program?" %
                                  controller.manager.get_name(),
                         positive_str="Uninstall!")

    def accept(self):
        self.manager.uninstall()
        self.controller.tk.quit()


class FrameUpdating(FrameInProgress):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Updating...")
        self.manager.set_solution_progress_hook(self.progress_callback)
        self.manager.set_install_part_solution_hook(self.solution_finished_callback)
        thread = self.tk_thread(self.manager.update)
        thread.start()

    def progress_callback(self, progress: SolutionProgress):
        self.update_label(progress.status.capitalize() + " ...")
        self.update_progress(progress.percent)

    def solution_finished_callback(self):
        self.controller.tk.quit()


class ControllerTkinter(ControllerBase):
    def __init__(self):
        self.tk = None
        self._base_frame = None
        self._frame = None
        self.title_font = None
        # self.window = tk.Tk()

    def _init_tkinter(self):
        tk.Tk.report_callback_exception = self.excepthook
        self.tk = tk.Tk()
        self.tk.minsize(width=500, height=200)
        self.tk.maxsize(width=500, height=200)
        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.medium_font = Font(family='Helvetica', size=12, weight="bold")
        self._base_frame = tk.Frame()
        self._base_frame.pack(side="top", fill="both", expand=True)
        self._base_frame.grid_rowconfigure(0, weight=1)
        self._base_frame.grid_columnconfigure(0, weight=1)

    def _start_tk(self, frame, title):
        self._init_tkinter()
        self.tk.title(title)
        self.switch_frame(frame)
        self.tk.mainloop()

    def switch_frame(self, frame_class, **kwargs):
        assert self.manager is not None
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame_class(parent=self._base_frame,
                                  controller=self,
                                  **kwargs)
        self._frame.grid(row=0, column=0, sticky="nsew")
        self._frame.tkraise()

    def _excepthook(self, exception_info):
        showerror("Fatal exception", exception_info.traceback_str)
        self.tk.quit()

    def start_install(self):
        self._start_tk(FrameAcceptInstall,
                       "%s installer" % self.manager.get_name())

    def start_uninstall(self):
        self._start_tk(FrameAcceptUninstall,
                       "%s uninstall" % self.manager.get_name())

    def start_update(self):
        self._start_tk(FrameUpdating,
                       "%s update" % self.manager.get_name())
