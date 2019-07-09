import shutil
import os
from ..errors import SolutionNotRemovableError
from ..helper import misc
from ..constants import Constants


class Solutioner:
    def __init__(self, solution, dest):
        self._dest = dest
        self._solution = solution

    def _remove_solution(self):
        """Remove solution
        If the root solution isn't removable it will be ignored with this function
                def onerror(func, path, exc_info):
            if self.dest() != path:
                raise OSError("Cannot delete " + path)
        shutil.rmtree(self.dest(), onerror=onerror)
        """
        try:
            misc.safe_remove_folder_content(self.dest())
        except Exception as e:
            raise SolutionNotRemovableError("Can't remove %s" % self.dest()) from e

    def dest(self, *args):
        return os.path.realpath(os.path.join(self._dest, *args))

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
                self._remove_solution()
            os.makedirs(self.dest(), 0o777, True)
            for root, dirs, files in self._solution.walk():
                for _dir in dirs:
                    os.makedirs(self.dest(root, _dir),
                                0o777, True)
                for _file in files:
                    self._retrieve_file(os.path.join(root, _file))
        finally:
            self._solution.close()

    def get_iquail_update(self):
        path = self.dest(Constants.IQUAIL_TO_UPDATE)
        if os.path.isfile(path):
            return path
        return None

    def installed(self):
        return os.path.exists(self.dest())

    def update(self):
        # TODO: uninstall will be a waste of time on future solution types
        self.uninstall()
        self.install()

    def uninstall(self):
        if self.installed():
            self._remove_solution()
