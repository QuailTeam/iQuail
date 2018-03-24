
import os
import shutil
from abc import ABC, abstractmethod
from .. import builder


class SolutionBase(ABC, builder.BuilderAction):
    ''' The goal of this interface is to be able to resolve solution files
    comming from anywhere.
    current goals are:
    - from builtin data (added with pyinstaller)
    - from local directory
    - over network
    '''

    def setup(self, dest, hook=None):
        '''hook(integer) will be called to update progression status
        '''
        self.__dest = dest
        self.__hook = hook

    def _dest(self, *args):
        '''Get destination path'''
        return os.path.join(self.__dest, *args)

    def _update_progress(self, percent):
        ''' This function will be called to update solution progression
        while downloading.
        It will call
        '''
        if self.__hook:
            self.__hook(percent)

    def __enter__(self):
        if not self.open():
            raise AssertionError("Can't access solution")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    @abstractmethod
    def local(self):
        '''returns True if solution is stored locally,
        and if there is any corruption, it will not try again
        '''
        pass

    @abstractmethod
    def open(self):
        '''Open solution if needed
        (planned for unzipping, connecting to network, etc)
        return False if failed to open
        '''
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def walk(self):
        '''Iter files
        returns iterator,
        iter file solution relative path
        same output as os.walk
        '''
        pass

    @abstractmethod
    def get_file(self, relpath):
        ''' Download file to dest folder
        (open & setup the solution before using download)'''
        pass


    def get_all(self):
        ''' Download solution to dest folder
        (open & setup the solution before using download)
        '''
        if os.path.exists(self._dest()):
            shutil.rmtree(self._dest())
        os.makedirs(self._dest(), 0o777, True)
        for root, dirs, files in self.walk():
            for sdir in dirs:
                os.makedirs(self._dest(root, sdir),
                            0o777, True)
            for sfile in files:
                self.get_file(os.path.join(root, sfile))
