import winreg
import pathlib
import os.path
import shutil
import sys

PYTHON_PATH = 'C:\\Program Files\\Python36\\python.exe'

class WindowsInstaller:
    def __init__(self, name, solution_path, binary, icon, console=False):
        self.solution_path = solution_path
        self.name = name
        self.icon = icon
        self.binary = binary
        self.console = console
        self.uninstallRegKey = os.path.join('SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\', self.name)
        self.finalSolutionPath = os.path.join(pathlib.Path.home(), '.quail', self.name)

    def _delete_files(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def _copy_files(self, path):
        self._delete_files(path)
        shutil.copytree(self.solution_path, path)

    def _setRegUninstall(self, path):
        quailScriptName = sys.argv[0]
        quailScriptName = quailScriptName.split('\\')[-1]
        values = [
        ('DisplayName', winreg.REG_SZ, self.name),
        ('InstallLocation', winreg.REG_SZ, path),
        ('DisplayIcon', winreg.REG_SZ, os.path.join(path, self.icon)),
        ('Publisher', winreg.REG_SZ, 'QuailInc'),
        ('UninstallString', winreg.REG_SZ, '\"' + PYTHON_PATH + '\" ' + os.path.join(os.getcwd(), quailScriptName) + ' uninstall'),
        ('NoRepair', winreg.REG_DWORD, 1),
        ('NoModify', winreg.REG_DWORD, 1)]
        keyHandler = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.uninstallRegKey)
        for value in values:
            winreg.SetValueEx(keyHandler, value[0], 0, value[1], value[2])

    def _unsetRegUninstall(self):
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.uninstallRegKey)

    def _register_app(self, path):
        self._setRegUninstall(path)

    def install(self):
        if self.is_installed():
            print("Solution already installed")
            return
        dst = self._copy_files(self.finalSolutionPath)
        self._register_app(self.finalSolutionPath)

    def uninstall(self):
        if not self.is_installed():
            print("Solution already uninstalled")
            return
        self._delete_files(self.finalSolutionPath)
        self._unsetRegUninstall()

    def is_installed(self):
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.uninstallRegKey)
            return True
        except:
            return False


print("Launching Quail:")
installer = WindowsInstaller("LeBonTest", os.path.join(os.getcwd(), 'OpenHardwareMonitor'), 'OpenHardwareMonitor.exe', 'OpenHardwareMonitor.exe')
if len(sys.argv) == 1:
    installer.install()
    print("Solution Installed")
else:
    installer.uninstall()
    print("Solution Uninstalled")

# other register HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\xxx
