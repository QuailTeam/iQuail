
import os
from .solution_base import SolutionBase
from . import helper


class SolutionLocal(SolutionBase):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(path, list):
            self._path = os.path.join(*path)
        else:
            self._path = path
        self._path = os.path.abspath(self._path)

    def local(self):
        return True

    def open(self):
        return os.path.exists(self._path)

    def close(self):
        pass

    def walk(self):
        for root, dirs, files in os.walk(self._path):
            yield (os.path.relpath(root, self._path), dirs, files)

    def get_file(self, relative_path):
        return os.path.join(self._path, relative_path)
