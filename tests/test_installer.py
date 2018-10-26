import unittest.mock
import os
import iquail
import tempfile
from .base_test_case import BaseTestCase


class TestInstaller(BaseTestCase):

    def test_install_uninstall(self):
        testargs = [self.path('emptyfile')]
        with unittest.mock.patch('sys.argv', testargs):
            installer = iquail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='emptyfile'
            )
            self.assertFalse(installer._registered())
            installer._register()
            self.assertTrue(installer._registered())
            installer._unregister()
            self.assertFalse(installer._registered())

    def test_installer_shortcut(self):

        testargs = [self.path('emptyfile')]
        with unittest.mock.patch('sys.argv', testargs):
            installer = iquail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='emptyfile'
            )
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.close()
            tmp_name = tmp_file.name
            self.assertFalse(os.path.isfile(tmp_name))
            installer.add_shortcut(
                tmp_name,
                os.path.basename(tmp_name),
                installer.binary,
                installer.get_solution_icon()
            )
            self.assertTrue(os.path.isfile(tmp_name))
            installer.delete_shortcut(tmp_name)
            self.assertFalse(os.path.isfile(tmp_name))
            installer.delete_shortcut(tmp_name)
