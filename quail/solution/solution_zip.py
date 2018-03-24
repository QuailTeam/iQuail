
import os
import zipfile
import tempfile
import shutil
import sys
from .. import helper
from .solution_base import SolutionBase

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
            raise FileNotFoundError
        self._src = tempfile.mkdtemp()
        zip_ref = zipfile.ZipFile(self._zip_name, 'r')
        uncompress_size = sum((file.file_size for file in zip_ref.infolist()))
        extracted_size = 0
        for file in zip_ref.infolist():
            extracted_size += file.file_size
            self._update_progress(extracted_size * 100 / uncompress_size)
            zip_ref.extract(file, self._src)
        zip_ref.close()

    def close(self):
        shutil.rmtree(self._src)

    def walk(self):
        for root, dirs, files in os.walk(self._src):
            yield (os.path.relpath(root, self._src), dirs, files)

    def get_file(self, relpath):
        return os.path.join(self._src, relpath)
