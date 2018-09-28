import configparser
import pickle
from pathlib import Path


class Configuration:
    """This is an helper to save and load configuration"""
    def __init__(self, filename):
        Path(filename).touch()
        self._filename = filename
        self._parser = configparser.ConfigParser()
        self._parser.read(filename)
        default_scope = "DEFAULT"
        if default_scope not in self._parser:
            self._parser[default_scope] = {}
        self._config = self._parser[default_scope]

    def _save(self):
        with open(self._filename, "w") as f:
            self._parser.write(f)

    def set(self, name, value):
        assert value is not None
        self._config[name] = pickle.dumps(value)
        self._save()

    def get(self, name, default=None):
        value = self._config.get(name, None)
        if value is not None:
            return pickle.loads(value)
        return default

