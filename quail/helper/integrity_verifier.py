from hashlib import sha256
import os
import pathlib
import json
from contextlib import suppress
from .file_ignore import FileIgnore
from ..constants import Constants


def checksum(file_path, block_size=65536):
    file_path = str(file_path)
    hasher = sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()


class IntegrityVerifier:

    def __init__(self, path):
        self._root = str(path)
        self._checksums_file = os.path.join(self._root,
                                            Constants.CHECKSUMS_FILE)
        integrity_ignore_file = os.path.join(self._root,
                                             Constants.INTEGRITY_IGNORE_FILE)
        self._integrity_ignore = FileIgnore(integrity_ignore_file)

    @classmethod
    def _get_diff(self, base_checksums, new_checksums):
        ''' returns different files
        '''
        def isdict(x): return isinstance(x, dict)
        diff = []

        def get_diff_dir(base_checksums, new_checksums, path='.'):
            for name in base_checksums.keys():
                pathname = os.path.join(path, name)
                if isdict(base_checksums[name]):
                    new = {}
                    if name in new_checksums and isdict(new_checksums[name]):
                        new = new_checksums[name]
                    get_diff_dir(base_checksums[name], new, pathname)
                elif not (name in new_checksums
                          and new_checksums[name] == base_checksums[name]):
                    diff.append(pathname)
        get_diff_dir(base_checksums, new_checksums)
        return diff

    def calc_checksums(self):
        def calc_checksums_dir(path):
            checksums = {}
            for child in path.iterdir():
                basename = os.path.basename(str(child))
                if self._integrity_ignore.accept(str(child)):
                    if child.is_file():
                        checksums.update({basename: checksum(child)})
                    elif child.is_dir():
                        checksums.update({basename: calc_checksums_dir(child)})
            return checksums
        return calc_checksums_dir(pathlib.Path(self._root))

    def dump(self):
        with suppress(FileNotFoundError):
            os.remove(self._checksums_file)
        new_checksums = self.calc_checksums()
        with open(self._checksums_file, 'w') as file:
            json.dump(new_checksums, file)

    def verify(self):
        if not os.path.isfile(self._checksums_file):
            raise FileNotFoundError
        new_checksums = self.calc_checksums()
        with open(self._checksums_file, 'r') as file:
            stored_checksums = json.load(file)
        return self._get_diff(stored_checksums, new_checksums)
