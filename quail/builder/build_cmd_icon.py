
from .build_cmd_base import BuildCmdBase


class BuildCmdIcon(BuildCmdBase):
    def __init__(self, icon):
        self._icon = icon

    def get_build_params(self):
        return ["-i", self._icon]
