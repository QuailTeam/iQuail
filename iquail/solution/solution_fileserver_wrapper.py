import pexpect

class QuailFS:
    def __init__(self, client_bin_path, dl_path):
        self.pipe = None
        self.error = ''
        self.client_bin_path = client_bin_path
        self.dl_path = dl_path

    def _send_cmd(self, cmd):
        self.pipe.sendline(cmd)
        self.pipe.expect('> ')
        return list(self.pipe.before.splitlines())[1:]

    def _parse_error(self, lines, start='ERROR:'):
        if len(lines) > 0 and lines[0].startswith(start):
            self.error = lines[0]
            return True
        return False

    def connect(self, ip, port):
        args = ' '.join([self.client_bin_path, ip, port, self.dl_path])
        try:
            self.pipe = pexpect.spawnu(args)
        except pexpect.exceptions.ExceptionPexpect:
            self.error = 'Cannot open pipe'
            return False
        ret = self.pipe.expect(['> ', 'Couldn\'t connect to host', 'Exception:'])
        if ret != 0:
            if ret == 1:
                self.error = 'Cannot connect'
            else:
                self.error = 'Cannot open download directory'
            return False
        return True

    def ls(self, path='.'):
        lines = self._send_cmd('LS ' + path)
        if self._parse_error(lines, 'LS failed'):
            return None
        return lines[1:]

    def get_version(self):
        lines = self._send_cmd('VERSION GET')
        return lines[1]

    def list_versions(self):
        lines = self._send_cmd('VERSION LIST')
        return lines[1:]

    def set_version(self, version):
        lines = self._send_cmd('VERSION SET ' + version)
        if self._parse_error(lines, 'Invalid command'):
            return False
        return True

    def get_file(self, path):
        lines = self._send_cmd('GET_FILE ' + path)
        if self._parse_error(lines, 'File not received'):
            return False
        return True

    def get_error(self):
        return self.error

    def disconnect(self):
        self.pipe.sendline('EXIT')
        self.pipe.expect(pexpect.EOF)
