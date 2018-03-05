
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._uninstall_reg_key = os.path.join(
            'SOFTWARE', 'Microsoft', 'Windows', 'CurrentVersion', 'Uninstall',
            self.name)
        shortcut_name = self.name + '.lnk'
        self._desktop_shortcut = os.path.join(
            shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0),
            shortcut_name)
        self._start_menu_path = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu', 'Programs',
            self.name)
        self._start_menu_shortcut = os.path.join(
            self._start_menu_path,
            shortcut_name)

    def _get_python_path(self):
        return sys.executable

    def _set_reg_uninstall(self):
        uninstall_path = "%s %s" % (self.get_install_path(Helper.get_script_name()),
                                    Constants.ARGUMENT_UNINSTALL)
        if Helper.running_from_script():
            uninstall_path = self._get_python_path() + ' ' + uninstall_path
        values = [
            ('DisplayName', winreg.REG_SZ, self.name),
            ('InstallLocation', winreg.REG_SZ, self.get_install_path()),
            ('DisplayIcon', winreg.REG_SZ, self.get_install_path(self.icon)),
            ('Publisher', winreg.REG_SZ, self.publisher),
            ('UninstallString', winreg.REG_SZ, uninstall_path),
            ('NoRepair', winreg.REG_DWORD, 1),
            ('NoModify', winreg.REG_DWORD, 1)]
        key_handler = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, self._uninstall_reg_key)
        for reg_name, reg_type, reg_value in values:
            winreg.SetValueEx(key_handler, reg_name, 0, reg_type, reg_value)

    def _unset_reg_uninstall(self):
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self._uninstall_reg_key)

    def _create_shortcut(self, dest):
        shell_script = Dispatch('WScript.Shell')
        shortcut = shell_script.CreateShortCut(dest)
        shortcut.Targetpath = self.get_install_path(Helper.get_script_name())
        shortcut.WorkingDirectory = self.get_install_path()
        shortcut.IconLocation = self.get_install_path(self.icon)
        shortcut.save()

    def _create_shortcuts(self):
        self._create_shortcut(self._desktop_shortcut)
        os.makedirs(self._start_menu_path, 0o777, True)
        self._create_shortcut(self._start_menu_shortcut)

    def _delete_shortcuts(self):
        with suppress(FileNotFoundError):
            os.remove(self._desktop_shortcut)
        with suppress(FileNotFoundError):
            shutil.rmtree(self._start_menu_path)

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
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, self._uninstall_reg_key)
            return True
        except:
            return False
