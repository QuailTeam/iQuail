
import os
from abc import ABC, abstractmethod
import logging
from ..constants import Constants

logger = logging.getLogger(__name__)

TEST_PREFIX = "test_"


class Validate:
    def __init__(self, path, installer):
        assert os.path.exists(path)
        self._path = path
        self._installer = installer

    def path(self, *args):
        return os.path.join(self._path, *args)

    def isfile(self, *args):
        return os.path.isfile(self.path(*args))

    def test_binary(self):
        return self.isfile(self._installer.binary_name)

    def test_icon(self):
        return self.isfile(self._installer.icon)

    def _notify_file_exists(self, f):
        if self.isfile(f):
            print("Found " + f)
        else:
            print("Not found " + f)

    def run(self):
        attrs = dir(self)
        tests = list(filter(lambda x: x.startswith(TEST_PREFIX), attrs))

        print("Running tests...")
        for test in tests:
            name = test[len(TEST_PREFIX):]
            f = getattr(self, test)
            assert f(), test + " FAILED"
            print(test + " OK")
        print("Running notifications...")
        self._notify_file_exists(Constants.IQUAIL_TO_UPDATE)
        self._notify_file_exists(Constants.CONF_IGNORE)
        return 0
