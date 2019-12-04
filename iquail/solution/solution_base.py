import os
import shutil
import typing
from abc import ABC, abstractmethod
from .. import builder


class SolutionProgress:
    """Class returned in callback to notify progress
    (see SolutionBase._update_progress
    """

    def __init__(self, percent, status, log):
        self.percent = percent
        self.status = status
        self.log = log


class SolutionBase(ABC, builder.BuilderAction):
    """ The goal of this interface is to be able to resolve solution files
    coming from anywhere.
    current goals are:
    - from builtin data (added with pyinstaller)
    - from local directory
    - over network
    """

    def __init__(self):
        self._progress_hook = None
        self.__solutioner = None
        self.__manager = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def set_progress_hook(self, hook):
        """set progression hook"""
        self._progress_hook = hook

    def _update_progress(self, percent, status="loading", log=""):
        """ This function will be called to update solution progression
        while downloading.
        It will call
        """
        if self._progress_hook:
            self._progress_hook(SolutionProgress(percent, status, log))

    """Setup manager and installer
    """

    def setup(self, solutioner, manager):
        self.__solutioner = solutioner
        self.__manager = manager

    """Get installed version of the solution, if there is one"""

    def get_installed_version(self):
        return self.__manager.get_installed_version()

    """Get current installed file with relative path
    If the file exists then return the absolute path
    else return None
    """

    def retrieve_current_file(self, *relpath):
        res = self.__solutioner.backup_dest(*relpath)
        if os.path.isfile(res):
            return res
        # TODO copy res in tmp before returning
        return None

    def get_version_string(self):
        """ return version string of a solution
        This function is meant to be overridden
        by default returns None
        """
        return None

    @abstractmethod
    def local(self):
        """returns True if solution is stored locally,
        and if there is any corruption, it will not try again
        """
        pass

    @abstractmethod
    def open(self):
        """Open solution
        """
        pass

    @abstractmethod
    def close(self):
        """Close solution"""
        pass

    @abstractmethod
    def walk(self):
        """Iter files
        returns iterator,
        iter file solution relative path
        same output as os.walk
        """
        pass

    @abstractmethod
    def retrieve_file(self, relative_path):
        """ Retrieve file from solution and returns file path"""
        pass
