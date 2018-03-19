

import os
from .solution_zip import SolutionZip
from .builder.cmd_zip import CmdZip
from . import helper

class SolutionPacked(SolutionZip):
    def __init__(self, path, *args, **kwargs):
        if isinstance(path, list):
            self._path = os.path.join(*path)
        else:
            self._path = path
        self._path = os.path.abspath(self._path)
        self._zip_name = 'solution.zip'
        super().__init__(zip_name=self._zip_name, *args, **kwargs)


    def additional_build_cmds(self):
        return [CmdZip(self._path, self._zip_name)]
