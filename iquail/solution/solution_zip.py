import os
import zipfile
import shutil
import sys
from ..errors import *
from .. import helper
from ..helper import misc
from .solution_base import SolutionBase


class SolutionZip(SolutionBase):
    """ Zip solution
    made to be embeded in the executable (with pyinstaller --add-data)
    limitations:
    max ram size / max tmp size
    """

    def __init__(self, zip_name):
        super().__init__()
        self._tmp = None
        if not isinstance(zip_name, str):
            raise TypeError("Expected string as zip file")
        if helper.running_from_script():
            self._zip_name = os.path.abspath(zip_name)
        else:
            self._zip_name = os.path.join(sys._MEIPASS, zip_name)

    def local(self):
        return True

    def open(self):
        if not os.path.isfile(self._zip_name):
            raise SolutionUnreachableError("File not found %s" % self._zip_name)
        self._tmp = misc.safe_mkdtemp()
        zip_ref = zipfile.ZipFile(self._zip_name, 'r')
        uncompress_size = sum((file.file_size for file in zip_ref.infolist()))
        extracted_size = 0
        for file in zip_ref.infolist():
            extracted_size += file.file_size
            self._update_progress(percent=extracted_size * 100 / uncompress_size,
                                  status="unzipping",
                                  info="extracting: " + file.filename)
            zip_ref.extract(file, self._tmp)
        zip_ref.close()

    def close(self):
        if self._tmp:
            shutil.rmtree(self._tmp)
            self._tmp = None

    def walk(self):
        for root, dirs, files in os.walk(self._tmp):
            yield (os.path.relpath(root, self._tmp), dirs, files)

    def retrieve_file(self, relative_path):
        src = os.path.join(self._tmp, relative_path)
        if not os.path.isfile(src):
            raise SolutionUnreachableError("File not found: " + relative_path)
        return src
