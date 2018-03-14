
import os
import shutil
from . import helper


class SolutionDownloader:

    def __init__(self, solution, dest):
        self._dest = dest
        self._solution = solution
        self._verifier = helper.IntegrityVerifier(dest)

    def _download_file(self, relpath):
        tmpfile = self._solution.get_file(relpath)
        shutil.copy2(tmpfile, os.path.join(self._dest,
                                           os.path.dirname(relpath)))

    def _download_file_verify(self, relpath):
        self._download_file(relpath)
        corrupt = not self._verifier.verify_file(relpath)
        if corrupt:
            # TODO: check if self._solution.local()
            raise AssertionError("Corrupt file: " + relpath)

    def download_all(self):
        ''' Download solution to dest folder
        (open the solution before using download)
        '''
        with self._solution as solution:
            if os.path.exists(self._dest):
                shutil.rmtree(self._dest)
            os.makedirs(self._dest, 0o777, True)
            for root, dirs, files in solution.walk():
                for sdir in dirs:
                    os.makedirs(os.path.join(self._dest, root, sdir),
                                0o777, True)
                for sfile in files:
                    self._download_file(os.path.join(root, sfile))
