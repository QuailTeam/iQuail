
import unittest.mock
import os
import quail
from .base_test_case import BaseTestCase

class TestInstaller(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.binary = 'nobinary'
        f = open(self.binary, 'w')
        f.close()

    def tearDown(self):
        super().tearDown()
        os.remove(self.binary)

    def test_install_uninstall(self):
        testargs = [self.binary]
        with unittest.mock.patch('sys.argv', testargs):
            installer = quail.Installer(
                name='TestQuail',
                icon='noicon',
                binary='nobinary'
            )
            self.assertTrue(not installer.registered())
            installer.register()
            self.assertTrue(installer.registered())
            installer.unregister()
            self.assertTrue(not installer.registered())
