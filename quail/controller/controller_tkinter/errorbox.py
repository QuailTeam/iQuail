import tkinter
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import webbrowser
from urllib.parse import quote

class ErrorBox(object):

    def __init__(self, ctx, msg):
        tki = tkinter
        self.top = tki.Toplevel(ctx)
        self.top.title("Fatal Error")

        frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        icon = tki.Label(frm, image="::tk::icons::error")
        icon.pack()

        scrolledtext_exception = ScrolledText(frm)
        scrolledtext_exception.insert(tki.END, msg)
        scrolledtext_exception.configure(state="disabled")
        scrolledtext_exception.pack()

        github_button = tki.Button(frm, text='Submit this bug to Github')
        github_button['command'] = lambda: self._github_report(msg)
        github_button.pack(padx=4, pady=4)

        ok_button = tki.Button(frm, text='OK')
        ok_button['command'] = self.top.destroy
        ok_button.pack(padx=4, pady=4)

    def _github_report(self, exception):
        repo_owner = 'QuailTeam'
        repo_name = 'TestProject'
        base_url = 'https://github.com/' + repo_owner + '/' + repo_name + '/issues/new'

        report_title = 'Automatic Exception Report'

        url = base_url + '?title=' + quote(report_title) + '&body=' + quote(exception)

        try:
            webbrowser.open_new_tab(url)
        except webbrowser.Error:
            messagebox.showerror('Bug Report Failed', 'Reason: Browser control error occured')

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
