import shutil
import os
import glob
from quail.helper.file_ignore import FileIgnore
from quail.constants import Constants


class Solutioner:
    def __init__(self, solution, dest):
        self._dest = dest
        self._solution = solution

    def dest(self, *args):
        return os.path.join(self._dest, *args)

    def _retrieve_file(self, relpath):
        tmpfile = self._solution.retrieve_file(relpath)
        shutil.move(tmpfile, self.dest(os.path.dirname(relpath)))

    def install(self):
        """ Download solution to dest folder
        (open & setup the solution before using download)
        """
        self._solution.open()
        try:
            if os.path.exists(self.dest()):
                shutil.rmtree(self.dest())
            os.makedirs(self.dest(), 0o777, True)
            for root, dirs, files in self._solution.walk():
                for _dir in dirs:
                    os.makedirs(self.dest(root, _dir),
                                0o777, True)
                for _file in files:
                    self._retrieve_file(os.path.join(root, _file))
        finally:
            self._solution.close()

    def installed(self):
        return os.path.exists(self.dest())

    def __update_solution_files(self):
        self._solution.open()
        fi = FileIgnore(os.path.join(self.dest(), Constants.UPDATE_IGNORE_FILE))
        try:
            if not os.path.exists(self.dest()):
                os.makedirs(self.dest(), 0o777, True)
            for root, dirs, files in self._solution.walk():
                for d in dirs:
                    if not os.path.exists(d):
                        os.makedirs(self.dest(root, d), 0o777, True)
                for file in files:
                    if not fi.is_file_ignored(file):
                        self._retrieve_file(os.path.join(root, file))
        finally:
            self._solution.close()

    def update(self):
        self.__update_solution_files()

    def uninstall(self):
        if self.installed():
            shutil.rmtree(self.dest())
