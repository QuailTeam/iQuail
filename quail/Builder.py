
from .Helper import Helper


class Builder:
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

    def build(self):
        import PyInstaller.__main__ as PyInstallerMain
        # PyInstaller will not exist in bundle, importing only when needed
        PyInstallerMain.run(self.get_build_params())
