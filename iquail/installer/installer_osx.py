from .installer_base import InstallerBase
import os
import stat
import shutil
import pathlib
from ..helper import BundleTemplate, PlistCreator

class InstallerOsx(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bundle_install_path = os.path.join(os.sep, 'Applications', self.name + '.app')

    """ We need to put a syslink into /usr/local/bin or into a local folder inside the user's home directory"""
    """ TODO: Add the icon to the bundle"""
    def _register(self):
        bundle = BundleTemplate(self.name)
        bundle.make()
        plist = PlistCreator(self.name, '/Applications', {})
        plist.build_tree_and_write_file()
        self._build_launcher()
        #self.add_to_path(self.binary, self._binary_name)

    def _unregister(self):
        self.__remove_from_path(self.binary)

    def _registered(self):
        if not os.path.exists(self.build_symlink_path(self.binary)):
            return False
        return True

    def __add_to_path(self, binary, name):
        os.symlink(binary, self.build_symlink_path(name))

    def __remove_from_path(self, name):
        shutil.rmtree(self._bundle_install_path)

    def build_symlink_path(self, name):
        if self.install_systemwide:
            #TODO setup local installation
            #final_folder = '/Applications'
            final_folder = os.path.join(str(pathlib.Path.home()), 'Applications', self._name + '.app', 'Contents', 'MacOS')
        else:
            final_folder = os.path.join(str(pathlib.Path.home()), 'Applications', self._name + '.app', 'Contents', 'MacOS')
        return os.path.join(final_folder, name)

    def _build_launcher(self):
        with open(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'), 'w') as f:
            content = '/usr/local/bin/python3 ~/.iquail/' + self.uid + '/iquail_launcher.py'
            shebang = '#!/bin/bash\n'
            f.write(shebang)
            f.write(content)
        st = os.stat(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'))
        os.chmod(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'), st.st_mode | stat.S_IEXEC)
