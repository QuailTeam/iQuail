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

    """ 
        This function makes sure that all the files defined in the file with path=Constants.UPDATE_IGNORE_FILE 
        are not deleted when the software is updating
        
        First parameter is the root path for the solution. We could have used self.dest() but is not
        an acceptable solution for tests.
        TODO: Make sure that we set up the solution properly during the test, this problem should'nt happen
    """
    def _clear_non_ignored_files(self, path):
        fi = FileIgnore(os.path.join(path, Constants.UPDATE_IGNORE_FILE))
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]
        files_to_remove = [item for item in result if fi.accept(item) and not item.endswith(Constants.UPDATE_IGNORE_FILE)]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

    def __update_solution_files(self):
        self._solution.open()
        try:
            if not os.path.exists(self.dest()):
                os.makedirs(self.dest(), 0o777, True)
            for root, dirs, files in self._solution.walk():
                for dir in dirs:
                    if not os.path.exists(dir):
                        os.makedirs(self.dest(root, dir), 0o777, True)
                for file in files:
                    self._retrieve_file(os.path.join(root, file))
        finally:
            self._solution.close()

    def update(self):
        self._clear_non_ignored_files(self.dest())
        self.__update_solution_files()

    def uninstall(self):
        if self.installed():
            shutil.rmtree(self.dest())
