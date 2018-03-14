
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

    def __enter__(self):
        if not self.open():
            raise AssertionError("Can't access solution")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def local(self):
        '''returns True if solution is stored locally,
        and if there is any corruption, it will not try again
        '''
        raise NotImplementedError

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

    def get_file(self, relpath):
        '''Load file if needed, from solution relative path
        returns file real path'''
        raise NotImplementedError
