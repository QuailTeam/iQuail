import configparser
from pathlib import Path


class Configuration:
    """This is an helper to save and load configuration"""
    def __init__(self, filename):
        self._filename = filename
        self._parser = configparser.ConfigParser()
        self._default_scope = "DEFAULT"
        self._config = {}

    def read(self):
        Path(self._filename).touch()
        self._parser.read(self._filename)
        if self._default_scope not in self._parser:
            self._parser[self._default_scope] = {}
        self._config = self._parser[self._default_scope]

    def save(self):
        self._parser[self._default_scope] = self._config
        with open(self._filename, "w") as f:
            self._parser.write(f)

    def set(self, name, value):
        assert value is not None
        self._config[name] = value

    def get(self, name, default=None):
        value = self._config.get(name, None)
        if value is not None:
            return value
        return default

