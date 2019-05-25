import shutil
import os
from .solution_base import SolutionBase
from ..helper import misc
from ..errors import *


class SolutionLocal(SolutionBase):
    """Install solution from local folder
    this solution is more for debugging purposes
    """

    def __init__(self, path):
        super().__init__()
        if isinstance(path, list):
            self._path = os.path.join(*path)
        else:
            self._path = path

    @property
    def path(self):
        return os.path.abspath(self._path)

    def local(self):
        return True

    def open(self):
        if not os.path.isdir(self.path):
            raise SolutionUnreachableError("Solution local: no directory error")
        self._tmp = misc.safe_mkdtemp()

    def close(self):
        if self._tmp:
            shutil.rmtree(self._tmp, ignore_errors=True)

    def walk(self):
        for root, dirs, files in os.walk(self.path):
            yield (os.path.relpath(root, self.path), dirs, files)

    def retrieve_file(self, relative_path):
        src = os.path.join(self.path, relative_path)
        if not os.path.isfile(src):
            raise SolutionUnreachableError("File not found on solution: " + relative_path)
        os.makedirs(os.path.join(self._tmp, os.path.dirname(relative_path)),
                    exist_ok=True)
        res = shutil.copy2(src,
                           os.path.join(self._tmp, relative_path))
        return res
