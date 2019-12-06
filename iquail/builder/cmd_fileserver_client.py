import os
import logging
from .. import helper
from .cmd_base import CmdBase
from ..errors import BuilderError

logger = logging.getLogger(__name__)


class CmdFileserverClient(CmdBase):
    """ Compile a Fileserver Client and add it to the executable
    """

    def __init__(self, fileserver_path, build_path, binary_name):
        super().__init__()
        self._binary_name = binary_name
        self._fileserver_path = fileserver_path
        self._fileserver_path = os.path.abspath(self._fileserver_path)
        self._build_path = build_path
        self._build_path = os.path.abspath(self._build_path)
        self._client_path = os.path.join(self._build_path, self._binary_name)

    def _run_cmake(self):
        cmd = 'cmake -B' + self._build_path
        cmd += ' -S' + self._fileserver_path
        status = os.system(cmd)
        if status != 0:
            raise BuilderError('CmdFileserverClient: CMake failed')

    def _run_make(self):
        cmd = 'make -j' + str(os.cpu_count())
        cmd += ' -C ' + self._build_path
        cmd += ' ' + self._binary_name
        status = os.system(cmd)
        if status != 0:
            raise BuilderError('CmdFileserverClient: Make failed')

    def pre_build(self):
        logger.info("Calling CMake:")
        self._run_cmake()
        logger.info("Calling Make:")
        self._run_make()

    def get_build_params(self):
        params = []
        params += ['--add-data', self._client_path + os.path.pathsep + '.']
        return params
