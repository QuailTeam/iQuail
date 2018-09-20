import tkinter
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

        okButton = tki.Button(frm, text='OK')
        okButton['command'] = self.top.destroy
        okButton.pack(padx=4, pady=4)

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
