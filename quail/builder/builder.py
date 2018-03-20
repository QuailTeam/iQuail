
from .. import helper


class Builder:
    '''Build executable using PyInstaller
    Takes BuildCmd as argument
    '''

    def __init__(self, *build_cmds):
        self._build_cmds = list(build_cmds)

    def register(self, builder_action):
        '''see builder_action for more information'''
        self._build_cmds.extend(builder_action.builder_cmds())

    def default_build_params(self):
        params = [helper.get_script(),
                  "--onefile",
                  "--exclude-module", "PyInstaller"]
        return params

    def get_build_params(self):
        params = self.default_build_params()
        for build_cmd in self._build_cmds:
            params += build_cmd.get_build_params()
        return params

    def pre_build(self):
        for build_cmd in self._build_cmds:
            build_cmd.pre_build()

    def post_build(self):
        for build_cmd in self._build_cmds:
            build_cmd.post_build()

    def build(self):
        import PyInstaller.__main__ as PyInstallerMain
        # PyInstaller will not exist in bundle, importing only when needed
        self.pre_build()
        PyInstallerMain.run(self.get_build_params())
        self.post_build()
