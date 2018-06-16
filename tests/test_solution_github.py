import unittest

from quail import SolutionGitHub
from .base_test_solution import BaseTestSolution


class TestSolutionGithub(BaseTestSolution):
    def __init__(self, *args, **kwargs):
        super(TestSolutionGithub, self).__init__(*args, **kwargs)

    def xtest_open_gitHub(self):
        f = SolutionGitHub("cmder.zip", "https://github.com/cmderdev/cmder")
        f.open()


if __name__ == '__main__':
    print("Test Solution zip")
    unittest.main()
