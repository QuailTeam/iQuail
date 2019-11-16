
import os
from abc import ABC, abstractmethod
import logging
from ..constants import Constants

logger = logging.getLogger(__name__)


class Validate:
    def __init__(self, path, installer):
        assert os.path.exists(path)
        self._path = path
        self._installer = installer

    def path(self, *args):
        return os.path.join(self._path, *args)

    def isfile(self, *args):
        return os.path.isfile(self.path(*args))

    def run(self):
        assert self.isfile(self._installer.binary_name)
        print("Binary OK")
        if self.isfile(Constants.IQUAIL_TO_UPDATE):
            print("Found " + Constants.IQUAIL_TO_UPDATE)
        else:
            print("Not found " + Constants.IQUAIL_TO_UPDATE)
