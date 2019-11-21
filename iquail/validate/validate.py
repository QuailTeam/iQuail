
import os
from abc import ABC, abstractmethod
import logging
from ..constants import Constants
from ..helper.traceback_info import ExceptionInfo

logger = logging.getLogger(__name__)

TEST_PREFIX = "test_"


def _validate_side_img(path):
    try:
        from PIL import Image
        with Image.open(path) as img:
            width, height = img.size
            if height != 250:
                logger.warn("Side image is not valid: height should be 250px")
            else:
                logger.info("Side image is valid")
    except ImportError:
        logger.warn("Cannot check side image: please install Pillow module")


class TestResult:
    def __init__(self, name, success, is_critical, exception_info=None):
        assert isinstance(name, str)
        assert isinstance(success, bool)
        assert isinstance(is_critical, bool)
        if exception_info is not None:
            assert isinstance(exception_info, ExceptionInfo)
        # TODO add help string as param
        self.name = name
        self.success = success
        self.is_critical = is_critical
        self.exception_info = exception_info

    def log(self):
        success_str = "SUCCESS" if self.success else "FAIL"
        res = "test result: %s: %s" % (self.name, success_str)
        # TODO log traceback
        if self.success:
            logger.info(res)
        else:
            if self.is_critical:
                logger.error(res)
            else:
                logger.warn(res)

    def get_dict(self):
        return {
            "name": self.name,
            "success": self.success,
            "is_critical": self.is_critical,
            "exception_info": self.exception_info
        }


class Validate:
    def __init__(self, path, installer):
        assert os.path.exists(path)
        self._path = path
        self._installer = installer

    def path(self, *args):
        return os.path.join(self._path, *args)

    def isfile(self, *args):
        return os.path.isfile(self.path(*args))

    def test_binary(self):
        success = self.isfile(self._installer.binary_name)
        return TestResult("binary", success, is_critical=True)

    def test_icon(self):
        success = self.isfile(self._installer.icon)
        return TestResult("icon", success, is_critical=True)

    def test_iquail_update(self):
        success = self.isfile(Constants.IQUAIL_TO_UPDATE)
        return TestResult("iquail_update", success, is_critical=False)

    def test_conf_ignore(self):
        success = self.isfile(Constants.CONF_IGNORE)
        # TODO add tests
        return TestResult("conf_ignore", success, is_critical=False)

    def run(self):
        success = True
        res = []
        tests = list(filter(lambda x: x.startswith(TEST_PREFIX), dir(self)))
        logger.info("Running tests...")
        for test in tests:
            name = test[len(TEST_PREFIX):]
            f = getattr(self, test)
            test_result = f()
            test_result.log()
            if not test_result.success and test_result.is_critical:
                success = False
            res.append(test_result.get_dict())
        return success, res
