import os
import sys
import shutil
from .solution_base import SolutionBase
from .solution_fileserver_wrapper import QuailFS
from ..builder.cmd_fileserver_client import CmdFileserverClient
from ..errors import SolutionUnreachableError
from ..errors import SolutionFileNotFoundError
from ..errors import SolutionVersionNotFoundError
from ..errors import SolutionDecompressionError
from ..helper import misc

class SolutionFileServer(SolutionBase):
    def __init__(self, host, port, fileserver_path, build_path):
        super().__init__()
        self._binary_name = 'iQuailClient'
        self._host = host
        self._port = port
        self._fileserver_path = fileserver_path
        self._fileserver_path = os.path.abspath(self._fileserver_path)
        self._build_path = build_path
        self._build_path = os.path.abspath(self._build_path)
        if misc.running_from_script():
            self._client_bin_path = os.path.join(self._build_path, self._binary_name)
        else:
            self._client_bin_path = os.path.join(sys._MEIPASS, self._binary_name)
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

    def _decompress(self, sourcename, targetname, diffname):
        def bytes_from_file(filename, chunksize=8192):
            with open(filename, "rb") as f:
                while True:
                    chunk = f.read(chunksize)
                    if chunk:
                        for b in chunk:
                            yield b
                    else:
                        break
        target = open(targetname, 'w+b')
        source = open(sourcename, 'rb')
        buffer = b''
        for byte in bytes_from_file(diffname):
            if byte == ord(b'\n') and len(buffer):
                (header, arg) = buffer.split(b':', maxsplit=1)
                if header == b'INSERT':
                    (off, _, length) = arg.split()
                    source.seek(int(off))
                    target.write(source.read(int(length) + 1))
                elif header == b'COPY' and len(arg) > 1:
                    target.write(bytes([arg[1]]))
                buffer = b''
            else:
                buffer += bytes([byte])
        target.close()
        source.close()

    def _try_decompress(self, relpath):
        source_path = self.retrieve_current_file(relpath)
        print('Retreiving %s' % relpath)
        if source_path == None:
            print('  FAILED')
            return
        print('  SUCCESS')
        diff_path = self._get_tmp_path(relpath)
        target_path = diff_path
        diff_path = diff_path + '_diff'
        os.rename(target_path, diff_path)
        self._decompress(source_path, target_path, diff_path)
        os.remove(diff_path)

    def retrieve_file(self, relpath):
        if not self._serv.get_file(relpath):
            raise SolutionFileNotFoundError('FileServer.get_file() failed')
        try:
            self._try_decompress(relpath)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info() #TODO: rm
            print(e, exc_type, exc_tb.tb_lineno) #TODO: rm
            raise SolutionDecompressionError('Unexcpected error in decompression: ' + str(e))
        self._nbrFilesDownloaded += 1
        self._update_progress(percent=(100*self._nbrFilesDownloaded)/self._nbrFiles, status='downloading', log=relpath+'\n')
        return self._get_tmp_path(relpath)

    def builder_cmds(self):
        cmds = super().builder_cmds() + [CmdFileserverClient(
            self._fileserver_path, self._build_path, self._binary_name)]
        return cmds
