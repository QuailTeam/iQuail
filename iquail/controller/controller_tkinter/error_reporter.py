import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import webbrowser
from urllib.parse import quote


def _github_report(repo_owner, repo_name, title, body):
    # TODO unittest?
    base_url = 'https://github.com/' + repo_owner + '/' + repo_name + '/issues/new'
    url = base_url + '?title=' + quote(title) + '&body=' + quote(body)
    try:
        webbrowser.open_new_tab(url)
    except webbrowser.Error:
        messagebox.showerror('Bug Report Failed', 'Reason: Browser control error occured')


class ErrorReporter(tk.Toplevel):
    def __init__(self, title, body):
        super().__init__()
        self._error_title = title
        self._error_body = body
        self.title("Fatal Error")

        frame = tk.Frame(self, borderwidth=4, relief='ridge')
        frame.pack(fill='both', expand=True)

        icon = tk.Label(frame, image="::tk::icons::error")
        icon.pack()

        exception_scrolled_text = ScrolledText(frame)
        exception_scrolled_text.insert(tk.END, self._error_body)
        exception_scrolled_text.configure(state="disabled")
        exception_scrolled_text.pack()

        submit_button = tk.Button(frame,
                                  text='Submit this bug on Github',
                                  command=self._submit)
        submit_button.pack(padx=4, pady=4)

        exit_button = tk.Button(frame,
                                text='Exit',
                                command=self.destroy)
        exit_button.pack(padx=4, pady=4)

    def _submit(self):
        _github_report('QuailTeam',
                       'TestProject',
                       self._error_title,
                       self._error_body)

    def show(self):
        """Display the error report"""
        self.grab_set()
        self.wait_window()
