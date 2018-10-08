import shutil
import quail
import unittest
import os
from .base_test_case import BaseTestCase
from quail.helper import misc


class TestCacheResult(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_dir = self.tmp("Allum1")
        shutil.copytree(self.path("Allum1"), self.test_dir)

    def test_safe_remove_folder_content(self):
        misc.safe_remove_folder_content(self.test_dir)
        self.assertListEqual(os.listdir(self.test_dir), [])
