import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import threading

from quail.solution.solution_base import SolutionProgress
from .controller_base import ControllerBase
from ..helper.traceback_info import ExceptionInfo


class TkFrameBase(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        assert isinstance(controller, ControllerTkinter)
        self.controller = controller
        self.manager = controller.manager

    def callback_on_exception(self, func, exception_handler=None):
        def display_unhandled_error(exception):
            self.controller.exception_callback(ExceptionInfo(exception))

        if exception_handler is None:
            exception_handler = display_unhandled_error

        def target_wrapper():
            try:
                return func()
            except Exception as e:
                self.controller.tk.after(0, exception_handler, e)

        return target_wrapper

    def start_thread(self, func, exception_handler=None):
        """Same as threading.Thread().start()
        but if an error happen while the thread is running
        the error will be sent to the exception_handler
        """
        target = self.callback_on_exception(func, exception_handler)
        thread = threading.Thread(target=target)
        thread.start()


class FrameInstallFinished(TkFrameBase):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = tk.Label(self,
                         text="%s successfully installed!" % self.manager.get_name(),
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)

        button = tk.Button(self,
                           text="exit",
                           command=self._exit)
        button.pack(side="bottom", padx=20, pady=20)

    def _exit(self):
        self.controller.tk.quit()


class FrameUpdating(TkFrameBase):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        manager = self.manager
        manager.set_solution_progress_hook(self.progress_callback)
        manager.set_install_part_solution_hook(self.solution_finished_callback)

        self._label = tk.Label(self, text="Updating...", font=controller.title_font)
        self._label.pack(side="top", fill="x", pady=10)

        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self,
                                             orient=tk.HORIZONTAL,
                                             length=100,
                                             mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack(side="bottom", fill="x", padx=20, pady=20)
        self.start_thread(manager.update)

    def progress_callback(self, progress: SolutionProgress):
        self._label.configure(text=progress.status.capitalize() + " ...")
        self._label.update()
        progress = int(progress.percent)
        if 0 <= progress <= 100:
            self.progress_var.set(progress)

    def solution_finished_callback(self):
        self.controller.tk.quit()


class FrameInstalling(TkFrameBase):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        manager = self.manager
        manager.set_solution_progress_hook(self.progress_callback)
        manager.set_install_finished_hook(self.install_finished_callback)
        manager.set_install_part_solution_hook(self.solution_finished_callback)

        self._label = tk.Label(self, text="Installing...", font=controller.title_font)
        self._label.pack(side="top", fill="x", pady=10)

        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self,
                                             orient=tk.HORIZONTAL,
                                             length=100,
                                             mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack(side="bottom", fill="x", padx=20, pady=20)
        self.start_thread(manager.install_part_solution)

    def progress_callback(self, progress: SolutionProgress):
        self._label.configure(text=progress.status.capitalize() + " ...")
        self._label.update()
        progress = int(progress.percent)
        if 0 <= progress <= 100:
            self.progress_var.set(progress)

    def solution_finished_callback(self):
        self.controller.tk.after(0, self.manager.install_part_register)

    def install_finished_callback(self):
        self.controller.switch_frame(FrameInstallFinished)


class FrameAskInstall(TkFrameBase):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        manager = self.manager

        label = tk.Label(self,
                         text="%s installer\nWould you like to install this program?" % manager.get_name(),
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)

        button = tk.Button(self,
                           text="Install!",
                           command=self._run_install)
        button.pack(side="bottom", padx=20, pady=20)

    def _run_install(self):
        self.controller.switch_frame(FrameInstalling)


class FrameAskUninstall(TkFrameBase):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        manager = self.manager

        label = tk.Label(self,
                         text="%s installer\nWould you like to uninstall this program?" % manager.get_name(),
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)

        button = tk.Button(self,
                           text="Uninstall!",
                           command=self._run_uninstall)
        button.pack(side="bottom", padx=20, pady=20)

    def _run_uninstall(self):
        self.manager.uninstall()
        self.controller.tk.quit()


class ControllerTkinter(ControllerBase):
    def __init__(self):
        self.tk = None
        self._base_frame = None
        self._frame = None
        self.title_font = None
        # self.window = tk.Tk()

    def _init_tkinter(self):
        self.tk = tk.Tk()
        self.tk.minsize(width=500, height=200)
        self.tk.maxsize(width=500, height=200)
        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
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

    def exception_callback(self, traceback_info):
        showerror("Fatal exception", traceback_info.traceback_str)

    def _start_install(self):
        self._start_tk(FrameAskInstall,
                       "%s installer" % self.manager.get_name())

    def _start_uninstall(self):
        self._start_tk(FrameAskUninstall,
                       "%s uninstall" % self.manager.get_name())

    def _start_update(self):
        self._start_tk(FrameUpdating,
                       "%s update" % self.manager.get_name())
