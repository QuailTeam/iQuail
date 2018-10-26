import os
import quail
from .base_test_case import BaseTestCase
from quail.constants import Constants
from quail.solution.solutioner import Solutioner


class TestUpdateFileIgnore(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.solutioner = Solutioner(None, os.path.curdir)

    def test_basic_ignore(self):
        os.mkdir(self.tmp("test"))
        with open(self.tmp("test", "1.txt"), "a+"):
            pass
        with open(self.tmp("test", "2.txt"), "a+"):
            pass
        with open(self.tmp("test", Constants.UPDATE_IGNORE_FILE), "a+") as f:
            f.write("*1.txt")
        self.solutioner._clear_non_ignored_files(self.tmp("test"))

        assert os.path.exists(self.tmp("test", Constants.UPDATE_IGNORE_FILE))
        assert not os.path.exists(self.tmp("test", "2.txt"))


#TODO:  Add multiple test with edge case
