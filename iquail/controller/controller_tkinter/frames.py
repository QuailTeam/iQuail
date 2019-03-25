import tkinter as tk
import sys
from abc import ABC, abstractmethod
from tkinter.font import Font
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo, showerror, askretrycancel
import threading
import os
from ... import helper


class FrameBase(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.manager = controller.manager

        self._img = tk.PhotoImage(file=helper.get_side_img_path())
        self._label = tk.Label(self, image=self._img)
        self._label.pack(side="left")

    def tk_thread(self, target, exception_hook=None, complete_hook=None):
        """Same as threading.Thread() BUT:
        - If the function raises something, it will call exception_handler
            in the main tk thread with the exception as parameter
            By default the exception_handler will call self.controller.exception_hook
            (Otherwise the exceptions which happen within a thread would be ignored)
        - When the thread is completed, it will call complete_handler in the main tk thread
        """
        assert callable(target)

        if exception_hook is None:
            exception_hook = self.controller.excepthook

        def wrapper():
            try:
                ret = target()
                if complete_hook is not None:
                    self.controller.tk.after(0, complete_hook)
                return ret
            except Exception as e:
                exctype, value, tb = sys.exc_info()
                self.controller.tk.after(0, exception_hook, exctype, value, tb)

        thread = threading.Thread(target=wrapper)
        thread.daemon = True
        return thread


class FrameBaseAccept(FrameBase):
    """Frame to ask user to validate an action"""

    def __init__(self, parent, controller, question, positive_str="yes"):
        """
        :param parent: tkinter parent
        :param controller: self explanatory
        :param question: question string for the user
        :param positive_str: positive answer string
        """
        super().__init__(parent, controller)
        label = tk.Label(self,
                         text=question,
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        button = tk.Button(self,
                           text=positive_str,
                           command=self.accept)
        button.pack(side="bottom", padx=20, pady=20)

    @abstractmethod
    def accept(self):
        """This method will be called when user accept/validate"""
        pass


class FrameBaseTwoChoice(FrameBase):
    """Frame to ask user to validate an action"""

    def __init__(self, parent, controller, question, choice1, choice2):
        """
        :param parent: tkinter parent
        :param controller: self explanatory
        :param question: question string for the user
        :param choice1: choice 1 answer string
        :param choice1: choice 2 answer string
        """
        super().__init__(parent, controller)
        label = tk.Label(self,
                         text=question,
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10, padx=10)
        button1 = tk.Button(self,
                            text=choice1,
                            command=self.choice1_selected)
        button2 = tk.Button(self,
                            text=choice2,
                            command=self.choice2_selected)

        button1.pack(side="left", expand=True, padx=20, pady=20)
        button2.pack(side="right", expand=True, padx=20, pady=20)

    @abstractmethod
    def choice1_selected(self):
        """This method will be called when choice 1 have been selected"""
        pass

    @abstractmethod
    def choice2_selected(self):
        """This method will be called when choice 1 have been selected"""
        pass


class FrameBaseInProgress(FrameBase):
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
        self._progress_bar.pack(fill="x", padx=10, pady=10)

        self._info_log = ScrolledText(self)
        self._info_log.pack(fill="x", side="bottom")

    def update_label(self, text):
        self._label.configure(text=text)
        self._label.update()

    def update_log(self, info_text):
        if info_text:
            self._info_log.insert(tk.END, info_text)
            self._info_log.see(tk.END)
            self._info_log.update()

    def set_indeterminate(self):
        self._progress_bar.configure(mode='indeterminate')
        self._progress_bar.start()

    def update_progress(self, percent):
        if percent < 0:
            percent = 0
        if percent > 100:
            percent = 100
        self.progress_var.set(percent)


class FrameBaseConfigure(FrameBase):
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
