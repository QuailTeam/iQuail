
import os
import quail
import quail.helper.integrity_verifier
from .base_test_case import BaseTestCase


class TestSolutionZip(BaseTestCase):

    def test_unzip_one(self):
        solution = quail.SolutionZip(self.testdata('Allum1.zip'))
        solution.open()
        try:
            f = solution.retrieve_file('icon.jpeg')
            checksum = quail.helper.integrity_verifier.checksum_file(f)
            self.assertEqual(checksum,
                             '4ab70bcb55ddd942b81485aeb04747531c265778280bf4ca89debbe84209ff41')
        finally:
            solution.close()
        self.assertFalse(os.path.isfile(f))

    def test_walk_one(self):
        expected = [('.', ['subfolder'], ['allum1', 'icon.jpeg']),
                    ('subfolder', [], ['testfile.txt'])]
        solution = quail.SolutionZip(self.testdata('Allum1.zip'))
        solution.open()
        try:
            res = []
            for x in solution.walk():
                res.append(x)
            self.assertListEqual(res, expected)
        finally:
            solution.close()
