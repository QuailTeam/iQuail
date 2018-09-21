import tkinter
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import json
import requests

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

        frm_login = tki.Frame(frm)
        frm_login.pack()

        label_username = tki.Label(frm_login, text="Username")
        label_password = tki.Label(frm_login, text="Password")


        self.entry_username = tki.Entry(frm_login)
        self.entry_password = tki.Entry(frm_login, show="*")

        label_username.grid(row=0, sticky=tki.E)
        label_password.grid(row=1, sticky=tki.E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.github_button = tki.Button(frm_login, text='Submit this bug to Github')
        self.github_button['command'] = lambda: self._github_report(msg)
        self.github_button.grid(columnspan=2)

        ok_button = tki.Button(frm, text='OK')
        ok_button['command'] = self.top.destroy
        ok_button.pack(padx=4, pady=4)

    def _post_github_issue(self, auth, content):
        repo_owner = 'QuailTeam'
        repo_name = 'TestProject'
        url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo_name)
        session = requests.Session()
        session.auth = auth
        issue = {'title': 'Automatic Exception Report',
                 'body': content,
                 'labels': ['bug']}
        r = session.post(url, json.dumps(issue))
        if r.status_code == 201:
            return None
        response_dict = json.loads(r.content)
        return response_dict['message']

    def _github_report(self, exception):
        username = self.entry_username.get()
        password = self.entry_password.get()
        response = 'Missing Credential'
        if username and password:
            response = self._post_github_issue((username, password), exception)
        if response == None:
            messagebox.showinfo('Bug Report Succeed', 'A Bug Report has been created on Github, thank you and sorry about that!')
            self.github_button.config(state='disabled')
        else:
            messagebox.showerror('Bug Report Failed', 'Reason: ' + response)

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
