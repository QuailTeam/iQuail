
class BuilderAction:
    '''This class is here to be inherited to register build actions by passing
    the instance to builder.register()
    (Ex: solution_pack)
    '''
    def builder_cmds(self):
        '''Additional build commands, which will be passed to builder.Builder
        return a list of builder.CmdBase
        '''
        return []
