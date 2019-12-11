from .installer_base import InstallerBase
import os
import stat
import shutil
import pathlib
from ..helper import BundleTemplate, PlistCreator

class InstallerOsx(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bundle_install_path = os.path.join(self._get_application_folder_path(), self.name + '.app')

    """ TODO: Add the icon to the bundle"""
    def _register(self):
        bundle = BundleTemplate(self.name, base_dir=self._get_application_folder_path())
        icon = self.get_install_path(self._icon)
        bundle.make()
        plist = PlistCreator(self.name, self._get_application_folder_path(), {})
        plist.build_tree_and_write_file()
        self._build_launcher()

    def _unregister(self):
        shutil.rmtree(self._bundle_install_path)

    def _registered(self):
        if not os.path.exists(self.build_folder_path(self.binary)):
            return False
        return True

    def __add_to_path(self, binary, name):
        os.symlink(binary, self.build_folder_path(name))

    def _get_application_folder_path(self):
        if self.install_systemwide:
            return os.path.join(os.sep, 'Applications')
        return os.path.join(str(pathlib.Path.home()), 'Applications')

    def build_folder_path(self, name):
        final_folder = os.path.join(self._get_application_folder_path(), self._name + '.app', 'Contents', 'MacOS')
        return os.path.join(final_folder, name)

    def _build_launcher(self):
        with open(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'), 'w') as f:
            shebang = '#!/usr/bin/env bash\n'
            content = '/usr/bin/env python3 ' + self.launcher_binary
            f.write(shebang)
            f.write(content)
        st = os.stat(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'))
        os.chmod(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'), st.st_mode | stat.S_IEXEC)
