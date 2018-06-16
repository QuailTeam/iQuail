import shutil
import os
import tempfile
from .solution_base import SolutionBase
from .. import helper


class SolutionLocal(SolutionBase):
    """Install solution from local folder
    this solution is more for debugging purposes
    """

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
        self._tmp = tempfile.mkdtemp()

    def close(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def walk(self):
        for root, dirs, files in os.walk(self._path):
            yield (os.path.relpath(root, self._path), dirs, files)

    def retrieve_file(self, relpath):
        os.makedirs(os.path.join(self._tmp, os.path.dirname(relpath)),
                    exist_ok=True)
        res = shutil.copy2(os.path.join(self._path, relpath),
                           os.path.join(self._tmp, relpath))
        return res
