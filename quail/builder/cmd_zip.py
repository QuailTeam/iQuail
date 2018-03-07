import os
import zipfile
from ..helper import Helper
from .cmd_base import CmdBase


class CmdZip(CmdBase):
    ''' Zip a folder and add it to the executable
    '''
    def __init__(self, path, zip_name, zip_clean=True):
        if not isinstance(path, list):
            raise AssertionError("Expected list as path")
        self._zip_clean = zip_clean
        self._path = os.path.abspath(os.path.join(*path))
        self._zip = zip_name

    def pre_build(self):
        zipf = zipfile.ZipFile(self._zip, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(self._path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path,
                           arcname=os.path.relpath(file_path, self._path))
                print(os.path.relpath(file_path, self._path))
        zipf.close()

    def post_build(self):
        if self._zip_clean:
            os.remove(self._zip)

    def get_build_params(self):
        params = []
        params += ['--add-data', self._zip + os.path.pathsep + '.']
        return params
