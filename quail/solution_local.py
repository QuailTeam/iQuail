import shutil
import os
from .solution_base import SolutionBase
from . import helper


class SolutionLocal(SolutionBase):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(path, list):
            self._src = os.path.join(*path)
        else:
            self._src = path
        self._src = os.path.abspath(self._src)

    def local(self):
        return True

    def open(self):
        return os.path.exists(self._src)

    def close(self):
        pass

    def walk(self):
        for root, dirs, files in os.walk(self._src):
            yield (os.path.relpath(root, self._src), dirs, files)

    def get_file(self, relpath):
        return shutil.copy2(os.path.join(self._src, relpath),
                            os.path.join(self._dest, relpath))
