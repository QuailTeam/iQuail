import shutil

from tests.base_test_case import BaseTestCase
from iquail.helper.osx.bundle_template import BundleTemplate
from iquail.helper.osx.plist_creator import PlistCreator


class BaseTestOsxBundle(BaseTestCase):
    # The test folder will always be named test.app
    def setUp(self):
        super(BaseTestOsxBundle, self).setUp()
        self._test_folder_path = self.tmp('test.app')
        self.plistCreator = PlistCreator('test', self._tmpdir)
        self.bt = BundleTemplate('test', self._tmpdir)
        self.bt.make()

    def tearDown(self):
        shutil.rmtree(self.bt.full_path, ignore_errors=True)
