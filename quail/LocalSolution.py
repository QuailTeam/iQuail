
import os
from .ISolutionResolver import ISolutionResolver

class LocalSolution(ISolutionResolver):
    def __init__(self, path):
        self._path = os.path.abspath(path)

    def access(self):
        return os.path.exists(self._path)
    
    def open(self):
        pass

    def close(self):
        pass

    def walk(self):
        for root, dirs, files in os.walk(self._path):
            yield (os.path.relpath(root, self._path), dirs, files)

    def get_file(self, relative_path):
        return os.path.join(self._path, relative_path)
