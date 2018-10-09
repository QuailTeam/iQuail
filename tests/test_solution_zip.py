import os
import iquail
from .base_test_solution import BaseTestSolution


class TestSolutionZip(BaseTestSolution):

    def test_unzip_1(self):
        solution = iquail.SolutionZip(self.path('Allum1.zip'))
        self.assertSolutionFile(solution,
                                'icon.jpeg',
                                '4ab70bcb55ddd942b81485aeb04747531c265778280bf4ca89debbe84209ff41')

    def test_walk_1(self):
        expected = [('.', ['subfolder'], ['allum1', 'icon.jpeg']),
                    ('subfolder', [], ['testfile.txt'])]
        solution = iquail.SolutionZip(self.path('Allum1.zip'))
        self.assertSolutionWalk(solution, expected)
