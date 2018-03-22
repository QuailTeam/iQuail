

import os
from ..builder.cmd_zip import CmdZip
from .. import helper
from .solution_zip import SolutionZip

class SolutionPacked(SolutionZip):
    def __init__(self, path, *args, **kwargs):
        if isinstance(path, list):
            self._path = os.path.join(*path)
        else:
            self._path = path
        self._path = os.path.abspath(self._path)
        self._zip_name = 'solution.zip'
        super().__init__(zip_name=self._zip_name, *args, **kwargs)


    def builder_cmds(self):
        cmds = super().builder_cmds() + [CmdZip(self._path, self._zip_name)]
        return cmds
