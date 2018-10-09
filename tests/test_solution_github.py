import unittest

from iquail import SolutionGitHub
from .base_test_solution import BaseTestSolution


class TestSolutionGithub(BaseTestSolution):
    """ See https://github.com/QuailTeam/TestProject/releases
    """

    def __init__(self, *args, **kwargs):
        super(TestSolutionGithub, self).__init__(*args, **kwargs)

    def test_file_1(self):
        solution = SolutionGitHub("TestProject.zip", "https://github.com/QuailTeam/TestProject")
        self.assertSolutionFile(solution,
                                'subfolder/test.txt',
                                '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')

    def test_walk_1(self):
        expected = [('.', ['subfolder'], ['README.md']),
                    ('subfolder', [], ['test.txt'])]
        solution = SolutionGitHub("TestProject.zip", "https://github.com/QuailTeam/TestProject")
        self.assertSolutionWalk(solution, expected)
