
import unittest.mock
import os
import quail
from .base_test_case import BaseTestCase

class TestInstaller(BaseTestCase):

    def test_install_uninstall(self):
        testargs = [self.testdata('emptyfile')]
        with unittest.mock.patch('sys.argv', testargs):
            installer = quail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='emptyfile'
            )
            self.assertFalse(installer.registered())
            installer.register()
            self.assertTrue(installer.registered())
            installer.unregister()
            self.assertFalse(installer.registered())
