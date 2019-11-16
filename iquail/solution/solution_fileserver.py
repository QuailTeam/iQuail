import os
import shutil
from .solution_base import SolutionBase
from .solution_fileserver_wrapper import QuailFS
from ..errors import SolutionUnreachableError
from ..errors import SolutionFileNotFoundError
from ..errors import SolutionVersionNotFoundError
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
        self._nbrFiles = 1
        self._nbrFilesDownloaded = 0
        self._update = False

    def local(self):
        return False

    def get_version_string(self):
        if self._serv == None:
            self._init_server()
            version = self._serv.get_version()
            self._fini_server()
            return version
        return self._serv.get_version()

    def _get_patch_version_name(self, curr, last):
        return curr + '_TO_' + last

    def _init_server(self):
        self._tmpdir = misc.safe_mkdtemp()
        self._serv = QuailFS(self._client_bin_path, self._tmpdir)
        if not self._serv.connect(self._host, self._port):
            raise SolutionUnreachableError("FileServer.connect() failed: %s" %
                                           self._serv.get_error())

    def _fini_server(self):
        self._serv.disconnect()
        shutil.rmtree(self._tmpdir)
        self._serv = None

    def open(self):
        self._init_server()
        currentVersion = self.get_installed_version()
        lastVersion = self.get_version_string()
        if currentVersion != None and currentVersion != lastVersion:
            self._update = True
            patchName = self._get_patch_version_name(currentVersion, lastVersion)
            if not self._serv.set_version(patchName):
                raise SolutionVersionNotFoundError("FileServer.set_version() failed: %s" %
                                                   self._serv.get_error())
        self._nbrFiles = self._serv.get_nbr_files()
        self._nbrFilesDownloaded = 0

    def close(self):
        self._fini_server()
        self._update = False

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
        # if patch: uncompress
        self._nbrFilesDownloaded += 1
        self._update_progress(percent=(100*self._nbrFilesDownloaded)/self._nbrFiles, status='downloading', log=relpath+'\n')
        return self._get_tmp_path(relpath)
