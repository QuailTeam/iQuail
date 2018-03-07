
from .cmd_base import CmdBase


class CmdIcon(CmdBase):
    def __init__(self, icon):
        self._icon = icon

    def get_build_params(self):
        return ["-i", self._icon]
