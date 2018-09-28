import quail
import unittest
from .base_test_case import BaseTestCase
from quail.helper import Configuration


class TestConfiguration(BaseTestCase):
    def test_set_get_1(self):
        c = Configuration(self.tmp("test.ini"))
        c.set("test", 1)
        c = Configuration(self.tmp("test.ini"))
        self.assertEqual(c.get("test"), 1)
