import unittest.mock
import os
import quail
from .base_test_case import BaseTestCase


class TestInstaller(BaseTestCase):

    def test_install_uninstall(self):
        testargs = [self.path('emptyfile')]
        with unittest.mock.patch('sys.argv', testargs):
            installer = quail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='emptyfile'
            )
            self.assertFalse(installer._registered())
            installer._register()
            self.assertTrue(installer._registered())
            installer._unregister()
            self.assertFalse(installer._registered())
