
import os
import unittest
import tempfile
import shutil

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        # shutil.rmtree(self._tmpdir)
        print(self._tmpdir)

    def tmp(self, *path):
        return os.path.join(self._tmpdir, *path)
