import os

from iquail.helper.osx.plist_creator import PlistCreator
from tests.base_test_osx_bundle import BaseTestOsxBundle


class TestOsxBundle(BaseTestOsxBundle):
    """
        In this test we make sure that the proper folder has the right name and that all the subfolders are created correctly
    """
    def test_default_bundle_setup(self):
        # Bundle template create a folder appended with .app
        assert os.path.exists(self._test_folder_path)
        assert os.path.exists(os.path.join(self._test_folder_path, 'Contents'))

    def test_plist_creation(self):
        plist_creator = PlistCreator('test', self._tmpdir)
        plist_creator.write_file()
        assert os.path.exists(os.path.join(self._test_folder_path, 'Contents', 'info.plist'))
