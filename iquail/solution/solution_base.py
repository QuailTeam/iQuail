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
