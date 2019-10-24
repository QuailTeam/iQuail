import shutil
import os
import sys
from ..errors import SolutionNotRemovableError
from ..helper import misc
from ..helper import FileIgnore
from ..constants import Constants


class Solutioner:
    def __init__(self, solution, manager, dest, *, conf_ignore=None):
        if conf_ignore is not None:
            assert isinstance(conf_ignore, list)
        self.conf_ignore = conf_ignore
        self._dest = dest
        self._solution = solution
        solution.setup(self, manager)

    def _remove_solution(self, ignore=None):
        """Remove solution
        If the root solution isn't removable it will be ignored with this function
                def onerror(func, path, exc_info):
            if self.dest() != path:
                raise OSError("Cannot delete " + path)
        shutil.rmtree(self.dest(), onerror=onerror)
        """
        try:
            misc.safe_remove_folder_content(self.dest(), ignore=ignore)
        except Exception as e:
            raise SolutionNotRemovableError(
                "Can't remove %s" % self.dest()) from e

    def dest(self, *args):
        return os.path.realpath(os.path.join(self._dest, *args))

    def _retrieve_file(self, relpath):
        if os.path.exists(self.dest(relpath)):
            print("Ignored file: " + relpath, file=sys.stderr)
            return
        tmpfile = self._solution.retrieve_file(relpath)
        shutil.move(tmpfile, self.dest(os.path.dirname(relpath)))

    def install(self, ignore=None):
        """ Download solution to dest folder
        (open & setup the solution before using download)
        """
        self._solution.open()
        try:
            if os.path.exists(self.dest()):
                self._remove_solution(ignore)
            os.makedirs(self.dest(), 0o777, True)
            for root, dirs, files in self._solution.walk():
                for _dir in dirs:
                    os.makedirs(self.dest(root, _dir),
                                0o777, True)
                for _file in files:
                    self._retrieve_file(os.path.join(root, _file))
        finally:
            self._solution.close()
        if self.conf_ignore:
            with open(self.dest(Constants.CONF_IGNORE), "a") as f:
                # TODO remove conf ignore on uninstall (if its self ignoring)
                f.write("\n")
                f.write("\n".join(self.conf_ignore))

    def get_iquail_update(self):
        path = self.dest(Constants.IQUAIL_TO_UPDATE)
        if os.path.isfile(path):
            return path
        return None

    def installed(self):
        return os.path.exists(self.dest())

    def update(self):
        # TODO: uninstall will be a waste of time on future solution types
        ignore = None
        if self.installed():
            if os.path.isfile(self.dest(Constants.CONF_IGNORE)):
                ignore = FileIgnore(self.dest(Constants.CONF_IGNORE))
            self._remove_solution(ignore=ignore)
        self.install(ignore)

    def uninstall(self):
        if self.installed():
            self._remove_solution()
