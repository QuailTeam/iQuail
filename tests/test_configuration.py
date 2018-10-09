import iquail
import unittest
from .base_test_case import BaseTestCase
from iquail.helper import Configuration, ConfVar


class TestConfiguration(BaseTestCase):
    def test_set_get_1(self):
        c = Configuration(self.tmp("test.ini"))
        c.set("test", "test_value")
        c.save()
        c = Configuration(self.tmp("test.ini"))
        c.read()
        self.assertEqual(c.get("test"), "test_value")

        # Test apply:
        class Test:
            def __init__(self):
                self.conf_var = ConfVar("test")

        t = Test()
        c.apply(t)
        self.assertEqual(t.conf_var, "test_value")

    def test_no_value(self):
        c = Configuration(self.tmp("test.ini"))
        c.read()
        self.assertEqual(c.get("test", default=1), 1)
