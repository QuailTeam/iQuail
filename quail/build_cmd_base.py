
from .helper import Helper


class BuildCmdBase:
    def __init__(self):
        pass

    def get_build_params(self):
        '''Additional build params
        '''
        return []

    def pre_build(self):
        ''' Pre build commands
        '''
        pass

    def post_build(self):
        ''' Post build commands
        '''
        pass
