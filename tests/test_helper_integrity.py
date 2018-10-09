import os
import iquail
from .base_test_case import BaseTestCase


class TestHelperIntegrity(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.verifier = iquail.helper.IntegrityVerifier(self.tmp())

    def test_verify_basic(self):
        os.mkdir(self.tmp("test"))
        with open(self.tmp("test", "1.txt"), "w") as f:
            f.write("test data")
        with open(self.tmp("2.txt"), "w") as f:
            f.write("test data")
        self.verifier.dump()
        self.assertTrue(len(self.verifier.verify_all()) == 0)

    def test_verify_basic_corrupt(self):
        os.mkdir(self.tmp("test"))
        with open(self.tmp("test", "1.txt"), "w") as f:
            f.write("test data")
        with open(self.tmp("2.txt"), "w") as f:
            f.write("test data")
        self.verifier.dump()
        with open(self.tmp("2.txt"), "w") as f:
            f.write("test dataa")
        self.assertTrue(len(self.verifier.verify_all()) > 0)
