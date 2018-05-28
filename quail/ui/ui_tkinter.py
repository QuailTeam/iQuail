import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading
from .ui_base import UiBase


class FrameInstall(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Run the installation by clicking the Button", font=controller._title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Install",
                           command=self._run_install)
        button.pack()

    def _run_install(self):
        self.controller._show_frame("FrameInstalling")
        self.controller._event_run_install.set()


class FrameInstalling(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Installing...", font=controller._title_font)
        label.pack(side="top", fill="x", pady=10)

        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack()


class UiTkinter(UiBase, threading.Thread):
    def __init__(self):
        self._tk = None
        self._event_run_install = threading.Event()
        self._frames = {}
        self._title_font = None
        UiBase.__init__(self)
        threading.Thread.__init__(self)

    def run(self):
        self._tk = tk.Tk()
        self._title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (FrameInstall, FrameInstalling):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self._frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self._show_frame("FrameInstall")

        self._tk.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._tk.mainloop()
        self._tk.quit()

    def start_install(self):
        UiBase.start_install(self)
        threading.Thread.start(self)
        self._event_run_install.wait()

    def progress_callback(self, float_progress):
        progress = int(float_progress)
        if 0 <= progress <= 100:
            self._frames["FrameInstalling"].progress_var.set(int(progress))

    def _show_frame(self, page_name):
        frame = self._frames[page_name]
        frame.tkraise()

    def _on_closing(self):
        self._tk.destroy()
