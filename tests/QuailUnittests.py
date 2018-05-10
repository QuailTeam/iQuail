import unittest
import os
import quail
from test_helper_integrity import TestHelperIntegrity

def load_tests(loader, test_cases):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
	

if __name__ == '__main__':
	tests = [TestHelperIntegrity]
	runner = unittest.TextTestRunner()
	runner.run(load_tests(unittest.defaultTestLoader, tests))
