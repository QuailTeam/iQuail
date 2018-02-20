
import os.path
import sys
import winreg
from .AInstaller import AInstaller
from .tools import *

class WindowsInstaller(AInstaller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._uninstallRegKey = os.path.join('SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\', self.get_name())

    def _getPythonPath(self):
        return sys.executable

    def _setRegUninstall(self):
        uninstallPath = get_script() + ' --uninstall'
        if run_from_script():
            uninstallPath = '\"' + self._getPythonPath() + '\" ' +  uninstallPath
        values = [
        ('DisplayName', winreg.REG_SZ, self.get_name()),
        ('InstallLocation', winreg.REG_SZ, self.get_install_path()),
        ('DisplayIcon', winreg.REG_SZ, os.path.join(self.get_install_path(), self.get_icon())),
        ('Publisher', winreg.REG_SZ, 'QuailInc'),
        ('UninstallString', winreg.REG_SZ, uninstallPath),
        ('NoRepair', winreg.REG_DWORD, 1),
        ('NoModify', winreg.REG_DWORD, 1)]
        keyHandler = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self._uninstallRegKey)
        for value in values:
            winreg.SetValueEx(keyHandler, value[0], 0, value[1], value[2])

    def _unsetRegUninstall(self):
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self._uninstallRegKey)

    def install(self):
        super().install()
        self._setRegUninstall()

    def uninstall(self):
        super().uninstall()
        self._unsetRegUninstall()

    def is_installed(self):
        if not super().is_installed():
            return False
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, self._uninstallRegKey)
            return True
        except:
            return False
