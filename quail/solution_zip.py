
import os
import zipfile
import tempfile
import shutil
import sys
from .solution_base import SolutionBase
from . import helper


class SolutionZip(SolutionBase):
    ''' Zip solution
    made to be embeded in the executable (with pyinstaller --add-data)
    limitations:
    max ram size / max tmp size
    '''

    def __init__(self, zip_name):
        if not isinstance(zip_name, str):
            raise AssertionError("Expected string as zip file")
        if helper.running_from_script():
            self._zip_path = os.path.abspath(zip_name)
        else:
            self._zip_path = os.path.join(sys._MEIPASS, zip_name)

    def local(self):
        return True

    def open(self):
        if not os.path.exists(self._zip_path):
            return False
        self._path = tempfile.mkdtemp()
        zip_ref = zipfile.ZipFile(self._zip_path, 'r')
        zip_ref.extractall(self._path)
        zip_ref.close()
        return True

    def close(self):
        shutil.rmtree(self._path)

    def walk(self):
        for root, dirs, files in os.walk(self._path):
            yield (os.path.relpath(root, self._path), dirs, files)

    def get_file(self, relative_path):
        return os.path.join(self._path, relative_path)
