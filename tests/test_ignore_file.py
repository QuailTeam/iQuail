import os
from .base_test_case import BaseTestCase
from quail.constants import Constants
import quail
from quail.solution.solutioner import Solutioner


class TestUpdateFileIgnore(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.solutioner = Solutioner(None, os.path.curdir)
