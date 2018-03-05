
import os
from .solution_base import SolutionBase
from .helper import Helper


class SolutionLocal(SolutionBase):
    def __init__(self, path):
        if not isinstance(path, list):
            raise AssertionError("Expected list as solution path")
        self._path = os.path.abspath(os.path.join(*path))

    def open(self):
        return os.path.exists(self._path)

    def close(self):
        pass

    def walk(self):
        for root, dirs, files in os.walk(self._path):
            yield (os.path.relpath(root, self._path), dirs, files)

    def get_file(self, relative_path):
        return os.path.join(self._path, relative_path)
