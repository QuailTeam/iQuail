import tkinter
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

class ErrorBox(object):

    def __init__(self, ctx, msg):
        tki = tkinter
        self.top = tki.Toplevel(ctx)
        self.top.title("Fatal Error")

        frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        icon = tki.Label(frm, image="::tk::icons::error")
        icon.pack()

        text = ScrolledText(frm)
        text.insert(tki.END, msg)
        text.configure(state="disabled")
        text.pack()

        github_button = tki.Button(frm, text='Submit this bug to Github')
        github_button['command'] = lambda: self._github_report(msg)
        github_button.pack(padx=4, pady=4)

        ok_button = tki.Button(frm, text='OK')
        ok_button['command'] = self.top.destroy
        ok_button.pack(padx=4, pady=4)

    def _github_report(self, msg):
        #TODO implem
        messagebox.showinfo("Success", "A Bug Report has been created on Github, thank you and sorry about that!")

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
