
import os
import quail
import quail.helper.integrity_verifier
from .base_test_case import BaseTestCase


class BaseTestSolution(BaseTestCase):
    def assertSolutionFile(self, solution, relpath, checksum):
        '''Download file and verify checksum'''
        solution.open()
        try:
            path = solution.retrieve_file(relpath)
            new_checksum = quail.helper.integrity_verifier.checksum_file(path)
            self.assertEqual(checksum,
                             new_checksum)
        finally:
            solution.close()
        self.assertFalse(os.path.isfile(path))

    def assertSolutionWalk(self, solution, expected):
        solution.open()
        try:
            res = []
            for (root, dirs, files) in solution.walk():
                dirs = sorted(dirs)
                files = sorted(files)
                res.append((root, dirs, files))
            self.assertListEqual(sorted(res), expected)
        finally:
            solution.close()
