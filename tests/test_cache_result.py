import quail
import unittest
from .base_test_case import BaseTestCase
from quail.helper import cache_result


class TestCacheResult(BaseTestCase):
    def test_cache_result(self):
        class TestClass:
            def __init__(self):
                self.x = 0

            @cache_result
            def cached(self):
                self.x += 42
                return self.x

            def not_cached(self):
                self.x += 42
                return self.x

        f = TestClass()
        self.assertEqual(f.cached(), 42)
        self.assertEqual(f.cached(), 42)
        self.assertEqual(f.cached(), 42)
        f = TestClass()
        self.assertEqual(f.not_cached(), 42)
        self.assertEqual(f.not_cached(), 84)

    def test_cache_property(self):
        class TestClass:
            def __init__(self):
                self.x = 0

            @property
            @cache_result
            def cached(self):
                self.x += 42
                return self.x

        f = TestClass()
        self.assertEqual(f.cached, 42)
        self.assertEqual(f.cached, 42)
        self.assertEqual(f.cached, 42)

    def test_cache_shallow(self):
        class TestClass:
            def __init__(self):
                self.x = [1, 2, 3]

            @cache_result
            def cached(self):
                return self.x

            def not_cached(self):
                return self.x

        f = TestClass()
        x = f.cached()
        x.append(4)
        self.assertNotEqual(x, f.cached())

        f = TestClass()
        x = f.not_cached()
        x.append(4)
        self.assertListEqual(x, f.not_cached())
