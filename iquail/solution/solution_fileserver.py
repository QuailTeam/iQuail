import os
import shutil
from .solution_base import SolutionBase
from .solution_fileserver_wrapper import QuailFS
from ..errors import SolutionUnreachableError
from ..errors import SolutionFileNotFoundError
from ..helper import misc

class SolutionFileServer(SolutionBase):
    def __init__(self, host, port, client_bin_path):
        super().__init__()
        self._host = host
        self._port = port
        self._client_bin_path = client_bin_path
        self._tmpdir = None
        self._serv = None
        self._files = None

    def local(self):
        return False

    def get_version_string(self):
        if self._serv == None:
            return None
        return self._serv.get_version()

    def open(self):
        self._tmpdir = misc.safe_mkdtemp()
        self._serv = QuailFS(self._client_bin_path, self._tmpdir)
        if not self._serv.connect(self._host, self._port):
            raise SolutionUnreachableError("FileServer.connect() failed: %s" %
                                           self._serv.get_error())

    def close(self):
        self._serv.disconnect()
        shutil.rmtree(self._tmpdir)
        self._serv = None

    def _parse_ls(self, lines):
        dirs, files = [], []
        for line in lines:
            ftype, fsize, fname = line.split()
            if ftype == 'd':
                dirs.append(fname)
            else:
                files.append(fname)
        return (dirs, files)

    def _walk_rec(self, root):
        lines = self._serv.ls(root)
        dirs, files = self._parse_ls(lines)
        yield (root, dirs, files)
        for d in dirs:
            yield from self._walk_rec(os.path.join(root, d))

    def walk(self):
        return self._walk_rec('.')

    def _get_tmp_path(self, relpath):
        return os.path.join(self._tmpdir, relpath)

    def retrieve_file(self, relpath):
        if not self._serv.get_file(relpath):
            raise SolutionFileNotFoundError('FileServer.get_file() failed')
        return self._get_tmp_path(relpath)
