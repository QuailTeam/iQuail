import logging
import configparser
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfVar:
    def __init__(self, key, cast=str, default_value=None):
        """ Configuration variable
        It will be replaced by its configuration value when Configuration.apply is called
        :param key: key which will be found in the configuration
        :param cast: cast function (by default all configuration variables are strings)
        """
        self.key = key
        self.default_value = default_value
        self.cast = cast


class Configuration:
    """This is an helper to save and load configuration"""

    def __init__(self, filename):
        self._filename = filename
        self._parser = configparser.ConfigParser()
        self._default_scope = "DEFAULT"
        self._config = {}

    def read(self):
        self._parser.read(self._filename)
        if self._default_scope not in self._parser:
            self._parser[self._default_scope] = {}
        self._config = self._parser[self._default_scope]

    def save(self):
        self._parser[self._default_scope] = self._config
        with open(self._filename, "w") as f:
            self._parser.write(f)

    def set(self, key, value):
        assert value is not None
        self._config[key] = value

    def get(self, key, default=None):
        value = self._config.get(key, None)
        if value is not None:
            return value
        return default

    def apply(self, *instances):
        """Apply config variables on a list of instances
        All ConfVars within instances will be replaced by their value from the configuration
        See example in unittests tests.test_configuration
        """
        for instance in instances:
            instance_vars = instance.__dict__
            for var_name, var_value in instance_vars.items():
                if isinstance(var_value, ConfVar):
                    value = var_value.cast(self.get(var_value.key,
                                                    default=var_value.default_value))
                    if value is not None:
                        logger.info("Applying conf var: %s = %s" %
                                    (var_name, str(value)))
                        setattr(instance, var_name, value)
