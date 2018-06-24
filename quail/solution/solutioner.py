import shutil
import os


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

    def update(self):
        # TODO: uninstall will be a waste of time on future solution types
        self.uninstall()
        self.install()

    def uninstall(self):
        if self.installed():
            shutil.rmtree(self.dest())
