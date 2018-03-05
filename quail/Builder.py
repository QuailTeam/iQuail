
from .Helper import Helper
from .Config import Config

class Builder:
    def __init__(self, config):
        if not isinstance(config, Config):
            raise AssertionError("Expecting quail.Config()")
        self._config = config

    @property
    def config(self):
        return self._config

    def get_build_params(self):
        params = [Helper.get_script(),
                  "--exclude-module", "PyInstaller"]
        if self.config.build_icon:
            params += ["-i", self.config.build_icon]
        if self.config.build_onefile:
            params += ["--onefile"]
        if not self.config.console:
            params += ["--noconsole"]
        return params

    def build(self):
        import PyInstaller.__main__ as PyInstallerMain
        # PyInstaller will not exist in bundle, importing only when needed
        PyInstallerMain.run(self.get_build_params())
