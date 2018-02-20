
import os
import sys
import winreg
import pythoncom
import shutil
from win32com.shell import shell, shellcon
from .AInstaller import AInstaller
from .tools import *

class WindowsInstaller(AInstaller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._uninstallRegKey = os.path.join('SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\', self.get_name())
        shortcutName = self.get_name() + '.lnk'
        self._desktopShortcut = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0), shortcutName)
        self._startupBarShortcutPath = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs', self.get_name())
        self._startupBarShortcut =  os.path.join(self._startupBarShortcutPath, shortcutName)

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

    def _createShortCut(self, destPath):
        shortcut = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        shortcut.SetPath(os.path.join(self.get_install_path(), self.get_binary()))
        shortcut.SetDescription (self.get_name() + " shortcut")
        shortcut.SetIconLocation(os.path.join(self.get_install_path(), self.get_icon()), 0)
        persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
        persist_file.Save(destPath, 0)

    def _createShortcuts(self):
        self._createShortCut(self._desktopShortcut)
        os.makedirs(self._startupBarShortcutPath, 0o777, True)
        self._createShortCut(self._startupBarShortcut)

    def _deleteShortcuts(self):
        os.remove(self._desktopShortcut)
        shutil.rmtree(self._startupBarShortcutPath)

    def install(self):
        super().install()
        self._setRegUninstall()
        self._createShortcuts()

    def uninstall(self):
        super().uninstall()
        self._unsetRegUninstall()
        self._deleteShortcuts()

    def is_installed(self):
        if not super().is_installed():
            return False
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, self._uninstallRegKey)
            return True
        except:
            return False
