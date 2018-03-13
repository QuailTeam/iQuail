
import os
import shutil

class SolutionBase:
    ''' The goal of this interface is to be able to resolve solution files
    comming from anywhere.
    current goals are:
    - from builtin data (added with pyinstaller)
    - from local directory
    - over network
    '''

    def download(self, dest):
        ''' Download solution to dest folder
        (open the solution before using download)
        '''
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.makedirs(dest, 0o777, True)
        for root, dirs, files in self.walk():
            for sdir in dirs:
                os.makedirs(os.path.join(dest, root, sdir), 0o777, True)
            for sfile in files:
                shutil.copy2(self.get_file(os.path.join(root, sfile)),
                             os.path.join(dest, root))

    def open(self):
        '''Open solution if needed
        (planned for unzipping, connecting to network, etc)
        return False if failed to open
        '''
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def walk(self):
        '''Iter files
        returns iterator,
        iter file solution relative path
        same output as os.walk
        '''
        raise NotImplementedError

    def get_file(self, relative_path):
        '''Load file if needed, from solution relative path
        returns file real path'''
        raise NotImplementedError
