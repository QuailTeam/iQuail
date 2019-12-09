import shutil
import iquail
import unittest
import sys
import os
import ctypes
from .base_test_case import BaseTestCase
from iquail.helper import misc, Constants
from unittest.mock import MagicMock


class TestMisc(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_dir = self.tmp("Allum1")
        shutil.copytree(self.path("Allum1"), self.test_dir)
        self.verifier = iquail.helper.IntegrityVerifier(self.test_dir)
        self.verifier.dump()

    def test_safe_remove_folder_content(self):
        misc.safe_remove_folder_content(self.test_dir)
        self.assertListEqual(os.listdir(self.test_dir), [])

    def test_safe_remove_folder_content_error(self):
        subfolder = os.path.join(self.test_dir, "subfolder")
        os.chmod(subfolder, 0o555)
        try:
            with open(os.path.join(subfolder, "testfile.txt"), "a") as f:
                self.assertRaises(Exception, misc.safe_remove_folder_content, self.test_dir)
                self.assertListEqual(self.verifier.verify_all(), [])
        finally:
            os.chmod(subfolder, 0o777)


    def test_running_from_installed_binary(self):
        misc.get_script_path = lambda: "/test/test/test/test"
        assert misc.running_from_installed_binary() is False
        misc.get_script_path = lambda: "/test/"
        assert misc.running_from_installed_binary() is False
        misc.get_script_path = lambda: os.path.join("/test/test/", Constants.IQUAIL_ROOT_NAME, "test")
        assert misc.running_from_installed_binary() is True


    def test_rerun_as_admin(self):
        global mock
        if misc.OS_LINUX:
            os.execvp = MagicMock()
            mock = os.execvp
        elif misc.OS_WINDOWS:
            ctypes.windll.shell32.ShellExecuteW = MagicMock()
            mock = ctypes.windll.shell32.ShellExecuteW
            return # TODO test disabled
        sys.argv = ['./test.py']
        misc.rerun_as_admin(False)
        mock.assert_called_with('sudo', ['sudo', './test.py'])
        misc.rerun_as_admin(True, '/dir/', '/bin')
        mock.assert_called_with('pkexec', ['pkexec', '/bin', '--iquail_path', '/dir/'])

