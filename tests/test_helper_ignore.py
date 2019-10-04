import os
import iquail
from .base_test_case import BaseTestCase


class TestHelperIgnore(BaseTestCase):
    def test_basic(self):
        ignore = iquail.helper.FileIgnore(self.path("Ignore", "ignore_basic"))
        self.assertTrue(ignore.accept("randomfile"))
        self.assertTrue(ignore.accept("not_conf.conf"))
        self.assertFalse(ignore.accept("file.conf"))
        self.assertFalse(ignore.accept("conf_file"))

    def test_path(self):
        ignore = iquail.helper.FileIgnore(self.path("Ignore", "ignore_path"))
        self.assertTrue(ignore.accept("test.txt"))
        self.assertTrue(ignore.accept("./conf/not_conf"))
        self.assertTrue(ignore.accept("folder/test.txt"))

        self.assertFalse(ignore.accept("./conf/test.txt"))

    def test_copy_ignored(self):
        ignore = iquail.helper.FileIgnore(self.path("Allum1", ".conf_ignore"))
        ignore.copy_ignored(self.path("Allum1"), self.tmp())
        self.assertFalse(os.path.exists(self.tmp("subfolder")))
        self.assertFalse(os.path.exists(self.tmp("allum1")))
        self.assertTrue(os.path.exists(self.tmp("test.conf")))
        self.assertTrue(os.path.exists(self.tmp("conf", "test.txt")))
