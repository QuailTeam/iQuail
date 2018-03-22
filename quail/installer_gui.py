#!/usr/bin/python3

import sys
from threading import Thread
from tkinter import Button, Label, Tk, messagebox
from .installer import Installer


class InstallerGui(Installer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tk = Tk()
        self._thread = None

    def _init_gui(self):
        self.button_install = Button(self.tk,
                                     text="Install",
                                     command=self._run_install)
        self.button_install.pack(side="left", padx=2, pady=2)

    def register(self):
        self._init_gui()
        self.tk.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.tk.mainloop()

    def _on_closing(self):
        if self._thread is not None and self._thread.is_alive():
            if not messagebox.askokcancel("Quit", "Do you want to quit?"):
                return
        if self._thread is not None:
            self._thread.join()
        self.tk.destroy()

    def _run_install(self):
        if self._thread is not None:
            return
        self._thread = Thread(target=super().register)
        self._thread.start()
