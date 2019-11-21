import os
import logging
from ..constants import Constants
from .. import helper

logger = logging.getLogger(__name__)


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


class Builder:
    """Build executable using PyInstaller
    Takes BuildCmd as argument
    """

    def __init__(self, *build_cmds, side_img_override=None):
        self._side_img = helper.get_side_img_path()
        if side_img_override is not None:
            assert os.path.basename(
                side_img_override) == Constants.SIDE_IMG_NAME
            self._side_img = side_img_override
            _validate_side_img(side_img_override)
        self._build_cmds = list(build_cmds)

    def register(self, builder_action):
        """see builder_action for more information"""
        self._build_cmds.extend(builder_action.builder_cmds())

    def default_build_params(self):
        params = [helper.get_script(),
                  "--onefile",
                  '--add-data', self._side_img + os.path.pathsep + "iquail",
                  "--exclude-module", "PyInstaller",
                  "--exclude-module", "PIL"]
        if helper.OS_WINDOWS:
            # upx slows down the launch time
            params.append("--noupx")
        return params

    def get_build_params(self):
        params = self.default_build_params()
        for build_cmd in self._build_cmds:
            params += build_cmd.get_build_params()
        return params

    def pre_build(self):
        for build_cmd in self._build_cmds:
            build_cmd.pre_build()

    def post_build(self):
        for build_cmd in self._build_cmds:
            build_cmd.post_build()

    def build(self):
        import PyInstaller.__main__ as PyInstallerMain
        # PyInstaller will not exist in bundle, importing only when needed
        self.pre_build()
        PyInstallerMain.run(self.get_build_params())
        self.post_build()
