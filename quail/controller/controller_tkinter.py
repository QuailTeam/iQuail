import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading
from .controller_base import ControllerBase


class FrameInstalling(tk.Frame):
    def __init__(self, parent, controller, manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        manager.set_solution_hook(self.progress_callback)

        label = tk.Label(self, text="Installing...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self,
                                             orient=tk.HORIZONTAL,
                                             length=100,
                                             mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack()
        self._thread = threading.Thread(target=manager.install)
        self._thread.start()

    def progress_callback(self, float_progress):
        progress = int(float_progress)
        if 0 <= progress <= 100:
            self.progress_var.set(progress)


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
        button.pack()

    def _run_install(self):
        self.controller.switch_frame(FrameInstalling)


class ControllerTkinter(ControllerBase):
    def __init__(self):
        self._tk = None
        self._base_frame = None
        self._frame = None
        self._manager = None
        self.title_font = None
        # self.window = tk.Tk()

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
        self._tk = tk.Tk()
        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self._base_frame = tk.Frame()
        self._base_frame.pack(side="top", fill="both", expand=True)
        self._base_frame.grid_rowconfigure(0, weight=1)
        self._base_frame.grid_columnconfigure(0, weight=1)

        self.switch_frame(FrameInstall)
        self._tk.mainloop()

    def start_uninstall(self, manager):
        manager.uninstall()
