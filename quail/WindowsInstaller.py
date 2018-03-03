
import os
import sys
import winreg
import shutil
from win32com.shell import shell, shellcon
from win32com.client import Dispatch
from .AInstaller import AInstaller
from .Constants import Constants
from contextlib import suppress
from .Helper import *


class WindowsInstaller(AInstaller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._uninstallRegKey = os.path.join(
            'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\', self.get_name())
        shortcutName = self.get_name() + '.lnk'
        self._desktopShortcut = os.path.join(shell.SHGetFolderPath(
            0, shellcon.CSIDL_DESKTOP, 0, 0), shortcutName)
        self._startupBarShortcutPath = os.path.join(os.getenv(
            'APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs', self.get_name())
        self._startupBarShortcut = os.path.join(
            self._startupBarShortcutPath, shortcutName)

    def _get_python_path(self):
        return sys.executable

    def _set_reg_uninstall(self):
        uninstallPath = Helper.get_script() + ' ' + Constants.ARGUMENT_UNINSTALL
        if Helper.running_from_script():
            uninstallPath = '\"' + self._get_python_path() + '\" ' + uninstallPath
        values = [
            ('DisplayName', winreg.REG_SZ, self.get_name()),
            ('InstallLocation', winreg.REG_SZ, self.get_install_path()),
            ('DisplayIcon', winreg.REG_SZ, self.get_install_path(self.get_icon())),
            ('Publisher', winreg.REG_SZ, self.get_publisher()),
            ('UninstallString', winreg.REG_SZ, uninstallPath),
            ('NoRepair', winreg.REG_DWORD, 1),
            ('NoModify', winreg.REG_DWORD, 1)]
        keyHandler = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, self._uninstallRegKey)
        for RegName, RegType, RegValue in values:
            winreg.SetValueEx(keyHandler, RegName, 0, RegType, RegValue)

    def _unset_reg_uninstall(self):
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self._uninstallRegKey)

    def _create_shortcut(self, destPath):
        shellScript = Dispatch('WScript.Shell')
        shortcut = shellScript.CreateShortCut(destPath)
        shortcut.Targetpath = self.get_install_path(self.get_binary())
        shortcut.WorkingDirectory = self.get_install_path()
        shortcut.IconLocation = self.get_install_path(self.get_icon())
        shortcut.save()

    def _create_shortcuts(self):
        self._create_shortcut(self._desktopShortcut)
        os.makedirs(self._startupBarShortcutPath, 0o777, True)
        self._create_shortcut(self._startupBarShortcut)

    def _delete_shortcuts(self):
        with suppress(FileNotFoundError):
            os.remove(self._desktopShortcut)
        with suppress(FileNotFoundError):
            shutil.rmtree(self._startupBarShortcutPath)

    def install(self):
        super().install()
        self._set_reg_uninstall()
        self._create_shortcuts()

    def uninstall(self):
        super().uninstall()
        self._unset_reg_uninstall()
        self._delete_shortcuts()

    def is_installed(self):
        if not super().is_installed():
            return False
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, self._uninstallRegKey)
            return True
        except:
            return False
