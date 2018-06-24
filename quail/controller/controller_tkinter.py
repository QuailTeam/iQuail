import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading
from .controller_base import ControllerBase


class FrameInstallFinished(tk.Frame):
    def __init__(self, parent, controller, manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         text="%s successfully installed!" % manager.get_name(),
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)

        button = tk.Button(self,
                           text="exit",
                           command=self._exit)
        button.pack(side="bottom", padx=20, pady=20)

    def _exit(self):
        self.controller.tk.quit()


class FrameUpdating(tk.Frame):
    def __init__(self, parent, controller, manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.manager = manager
        manager.set_solution_progress_hook(self.progress_callback)
        manager.set_install_part_solution_hook(self.solution_finished_callback)

        label = tk.Label(self, text="Updating...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self,
                                             orient=tk.HORIZONTAL,
                                             length=100,
                                             mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack(side="bottom", fill="x", padx=20, pady=20)
        self._thread = threading.Thread(target=manager.update)
        self._thread.start()

    def progress_callback(self, float_progress):
        progress = int(float_progress)
        if 0 <= progress <= 100:
            self.progress_var.set(progress)

    def solution_finished_callback(self):
        self.controller.tk.quit()


class FrameInstalling(tk.Frame):
    def __init__(self, parent, controller, manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.manager = manager
        manager.set_solution_progress_hook(self.progress_callback)
        manager.set_install_part_register_hook(self.install_finished_callback)
        manager.set_install_part_solution_hook(self.solution_finished_callback)

        label = tk.Label(self, text="Installing...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self,
                                             orient=tk.HORIZONTAL,
                                             length=100,
                                             mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack(side="bottom", fill="x", padx=20, pady=20)
        self._thread = threading.Thread(target=manager.install_part_solution)
        self._thread.start()

    def progress_callback(self, float_progress):
        progress = int(float_progress)
        if 0 <= progress <= 100:
            self.progress_var.set(progress)

    def solution_finished_callback(self):
        self.controller.tk.after(0, self.manager.install_part_register)

    def install_finished_callback(self):
        self.controller.switch_frame(FrameInstallFinished)


class FrameInstall(tk.Frame):
    def __init__(self, parent, controller, manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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


class ControllerTkinter(ControllerBase):

    def __init__(self):
        self.tk = None
        self._base_frame = None
        self._frame = None
        self._manager = None
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

    def switch_frame(self, frame_class, **kwargs):
        assert self._manager is not None
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame_class(parent=self._base_frame,
                                  controller=self,
                                  manager=self._manager,
                                  **kwargs)
        self._frame.grid(row=0, column=0, sticky="nsew")
        self._frame.tkraise()

    def start_install(self, manager):
        self._manager = manager
        self._init_tkinter()
        self.tk.title("%s installer" % self._manager.get_name())
        self.switch_frame(FrameInstall)
        self.tk.mainloop()

    def start_uninstall(self, manager):
        manager.uninstall()

    def start_update(self, manager):
        self._manager = manager
        self._init_tkinter()
        self.tk.title("%s update" % self._manager.get_name())
        self.switch_frame(FrameUpdating)
        self.tk.mainloop()