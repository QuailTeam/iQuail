import tkinter as tk
import sys
from abc import ABC, abstractmethod
from tkinter.font import Font
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askretrycancel
import threading


class FrameBase(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.manager = controller.manager

    def hook_exceptions(self, func, exception_handler=None):
        """Decorator: Hook exceptions from a function
        If the function raises something, it will call exception_handler
        in the main tk thread with the exception as parameter
        By default the exception_handler will call self.controller.exception_hook
        """
        assert callable(func)

        if exception_handler is None:
            exception_handler = self.controller.excepthook

        def wrapper():
            try:
                return func()
            except Exception as e:
                exctype, value, tb = sys.exc_info()
                self.controller.tk.after(0, exception_handler, exctype, value, tb)

        return wrapper

    def tk_thread(self, func, exception_handler=None):
        """Same as threading.Thread()
        but decorate func with self.hook_exceptions
        (Otherwise the exceptions which happen within a thread would be ignored)
        """
        target = self.hook_exceptions(func, exception_handler)
        thread = threading.Thread(target=target)
        thread.daemon = True
        return thread


class FrameValidate(FrameBase):
    """Frame to ask user to validate an action"""

    def __init__(self, parent, controller, question, hook, positive_str="yes"):
        """
        :param parent: tkinter parent
        :param controller: self explanatory
        :param question: question string for the user
        :param hook: this hook will be called if user accept
        :param positive_str: positive answer string
        """
        super().__init__(parent, controller)
        label = tk.Label(self,
                         text=question,
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        button = tk.Button(self,
                           text=positive_str,
                           command=hook)
        button.pack(side="bottom", padx=20, pady=20)


class FrameInProgress(FrameBase):
    def __init__(self, parent, controller, label_str):
        super().__init__(parent, controller)
        self._label = tk.Label(self, text=label_str, font=controller.title_font)
        self._label.pack(side="top", fill="x", pady=10)
        self.progress_var = tk.IntVar()
        self._progress_bar = ttk.Progressbar(self,
                                             orient=tk.HORIZONTAL,
                                             length=100,
                                             mode='determinate',
                                             variable=self.progress_var)
        self._progress_bar.pack(side="bottom", fill="x", padx=20, pady=20)

    def update_label(self, text):
        self._label.configure(text=text)
        self._label.update()

    def update_progress(self, percent):
        if percent < 0:
            percent = 0
        if percent > 100:
            percent = 100
        self.progress_var.set(percent)


class FrameConfigure(FrameBase):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = tk.Label(self,
                         text="Install configuration",
                         font=controller.title_font)
        label.pack(side="top", fill="x", padx=10, pady=10)
        # self.var = self.add_combobox("Select cmder version:", ('Full', 'Mini'))
        button = tk.Button(self,
                           text="next",
                           command=self.next_pressed)
        button.pack(side="bottom", padx=20, pady=5, anchor=tk.CENTER)

    def add_combobox(self, hint, choices):
        """Add combox box (drop list choices)
        :param hint: Hint for the user
        :param choices: tuple of choices in the combo box (strings)
        :return: StringVar to get the result of the choice
        """
        choice_frame = tk.Frame(self)
        choice_frame.pack(side=tk.TOP, fill=tk.X)
        label = tk.Label(choice_frame,
                         text=hint,
                         font=self.controller.medium_font)
        label.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=10)
        choice_var = tk.StringVar()
        choice_var.set(choices[0])
        option_menu = ttk.Combobox(choice_frame,
                                   textvariable=choice_var,
                                   values=choices,
                                   state="readonly")
        option_menu.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES, padx=10)
        option_menu.set(choices[0])
        return choice_var

    @abstractmethod
    def next_pressed(self):
        # self.controller.switch_frame(FrameInstalling)
        pass
