import os
import unittest
import tempfile
import shutil


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self._testdata = os.path.join(os.path.dirname(__file__), 'testdata')
        self._tmpdir = tempfile.mkdtemp()

    def path(self, *args):
        return os.path.join(self._testdata, *args)

    def tearDown(self):
        shutil.rmtree(self._tmpdir)

    def tmp(self, *path):
        return os.path.join(self._tmpdir, *path)
