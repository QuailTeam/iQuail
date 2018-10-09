
from .cmd_base import CmdBase


class CmdNoconsole(CmdBase):
    def __init__(self):
        super().__init__()

    def get_build_params(self):
        return ["--noconsole"]
