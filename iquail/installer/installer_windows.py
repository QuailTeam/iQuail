import os
import sys
import winreg
import shutil
from win32com.shell import shell, shellcon
from win32com.client import Dispatch
from contextlib import suppress
from ..constants import Constants
from .. import helper
from .installer_base import InstallerBase


def on_rmtree_error(function, path, excinfo):
    """function to ignore if windows can't remove iquail binary
    On windows we can't remove binaries being run
    iquail binary will be removed at exit with _delete_itself when uninstalling
    """
    if not (path == helper.get_script() or
            (function == os.rmdir and path == helper.get_script_path())):
        raise OSError("Cannot delete " + path)


class InstallerWindows(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._uninstall_reg_key = os.path.join(
            'SOFTWARE', 'Microsoft', 'Windows', 'CurrentVersion', 'Uninstall',
            self.uid)
        # use this instead?
        # https://msdn.microsoft.com/fr-fr/library/0ea7b5xe(v=vs.84).aspx
        shortcut_name = self.uid + '.lnk'
        self._desktop_shortcut = os.path.join(
            shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0),
            shortcut_name)
        self._start_menu_path = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu', 'Programs',
            self.uid)
        self._start_menu_shortcut = os.path.join(
            self._start_menu_path,
            shortcut_name)

    def _set_reg_uninstall(self):
        uninstall_path = "%s %s" % (
            self.iquail_binary,
            Constants.ARGUMENT_UNINSTALL)
        if helper.running_from_script():
            uninstall_path = sys.executable + ' ' + uninstall_path
        values = [
            ('DisplayName', winreg.REG_SZ, self.name),
            ('InstallLocation', winreg.REG_SZ, self.get_install_path()),
            ('DisplayIcon', winreg.REG_SZ, self.get_solution_icon()),
            ('Publisher', winreg.REG_SZ, self.publisher),
            ('UninstallString', winreg.REG_SZ, uninstall_path),
            ('NoRepair', winreg.REG_DWORD, 1),
            ('NoModify', winreg.REG_DWORD, 1)]
        key_handler = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, self._uninstall_reg_key)
        for reg_name, reg_type, reg_value in values:
            winreg.SetValueEx(key_handler, reg_name, 0, reg_type, reg_value)

    def _unset_reg_uninstall(self):
        with suppress(FileNotFoundError):
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self._uninstall_reg_key)

    def add_shortcut(self, dest, binary, icon, workpath=None):
        if not workpath:
            workpath = os.path.dirname(binary)
        shell_script = Dispatch('WScript.Shell')
        shortcut = shell_script.CreateShortCut(dest)
        shortcut.Targetpath = binary
        shortcut.WorkingDirectory = workpath
        shortcut.IconLocation = icon
        shortcut.save()

    def delete_shortcut(self, dest):
        with suppress(FileNotFoundError):
            os.remove(dest)

    def _register(self):
        self._set_reg_uninstall()
        shortcut_config = {
            "binary": self.launcher_binary,
            "icon": self.get_solution_icon(),
            "workpath": self.get_solution_path()
        }
        self.add_shortcut(self._desktop_shortcut, **shortcut_config)
        os.makedirs(self._start_menu_path, 0o777, True)
        self.add_shortcut(self._start_menu_shortcut, **shortcut_config)

    def _unregister(self):
        self.delete_shortcut(self._desktop_shortcut)
        with suppress(FileNotFoundError):
            shutil.rmtree(self._start_menu_path)
        self._unset_reg_uninstall()

    def _registered(self):
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, self._uninstall_reg_key)
            return True
        except:
            return False
