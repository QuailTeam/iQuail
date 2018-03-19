
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

    def __init__(self, zip_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(zip_name, str):
            raise AssertionError("Expected string as zip file")
        if helper.running_from_script():
            self._zip_name = os.path.abspath(zip_name)
        else:
            self._zip_name = os.path.join(sys._MEIPASS, zip_name)

    def local(self):
        return True

    def open(self):
        if not os.path.exists(self._zip_name):
            return False
        self._path = tempfile.mkdtemp()
        zip_ref = zipfile.ZipFile(self._zip_name, 'r')
        uncompress_size = sum((file.file_size for file in zip_ref.infolist()))
        extracted_size = 0
        for file in zip_ref.infolist():
            extracted_size += file.file_size
            self.update_progress(extracted_size * 100 / uncompress_size)
            zip_ref.extract(file, self._path)
        zip_ref.close()
        return True

    def close(self):
        shutil.rmtree(self._path)

    def walk(self):
        for root, dirs, files in os.walk(self._path):
            yield (os.path.relpath(root, self._path), dirs, files)

    def get_file(self, relative_path):
        return os.path.join(self._path, relative_path)
