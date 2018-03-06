import os
import zipfile
from .helper import Helper
from .builder_base import BuilderBase


class BuilderZip(BuilderBase):
    def __init__(self, path, zip_name, zip_clean=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(path, list):
            raise AssertionError("Expected list as path")
        self._zip_clean = zip_clean
        self._path = os.path.abspath(os.path.join(*path))
        self._zip = zip_name

    def pre_build(self):
        super().pre_build()
        zipf = zipfile.ZipFile(self._zip, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(self._path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path,
                           arcname=os.path.relpath(file_path, self._path))
                print(os.path.relpath(file_path, self._path))
        zipf.close()

    def post_build(self):
        super().post_build()
        if self._zip_clean:
            os.remove(self._zip)

    def get_build_params(self):
        params = super().get_build_params()
        params += ['--add-data', self._zip + os.path.pathsep + '.']
        return params
