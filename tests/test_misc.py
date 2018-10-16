import shutil
import iquail
import unittest
import os
from .base_test_case import BaseTestCase
from iquail.helper import misc


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

