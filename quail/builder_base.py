
from .helper import Helper


class BuilderBase:
    def __init__(self,
                 console=True,
                 icon='',
                 onefile=True):
        self._icon = icon
        self._onefile = onefile
        self._console = console

    @property
    def onefile(self):
        return self._onefile

    @property
    def icon(self):
        return self._icon

    @property
    def console(self):
        return self._console

    def get_build_params(self):
        params = [Helper.get_script(),
                  "--exclude-module", "PyInstaller"]
        if self.icon:
            params += ["-i", self.icon]
        if self.onefile:
            params += ["--onefile"]
        if not self.console:
            params += ["--noconsole"]
        return params

    def pre_build(self):
        ''' Pre build commands
        (Don't call this function yourself)
        '''
        pass

    def post_build(self):
        ''' Post build commands
        (Don't call this function yourself)
        '''
        pass

    def build(self):
        self.pre_build()
        import PyInstaller.__main__ as PyInstallerMain
        # PyInstaller will not exist in bundle, importing only when needed
        PyInstallerMain.run(self.get_build_params())
        self.post_build()
