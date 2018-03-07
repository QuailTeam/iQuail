
from .cmd_base import CmdBase


class CmdNoconsole(CmdBase):
    def __init__(self):
        pass

    def get_build_params(self):
        return ["--noconsole"]
