

class CmdBase:
    def __init__(self):
        pass

    def get_build_params(self):
        '''Additional build params for pyinstaller
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
