from abc import ABC, abstractmethod
import sys
from ..helper.traceback_info import ExceptionInfo


class ControllerBase(ABC):
    __manager = None

    def setup(self, manager):
        if manager is None:
            raise AssertionError("manager can't be None")
        self.__manager = manager
        sys.excepthook = self.excepthook

    @property
    def manager(self):
        if self.__manager is None:
            raise AssertionError("manager is None, You must call Controller.setup() first")
        return self.__manager

    def excepthook(self, exctype, value, tb):
        self._excepthook(ExceptionInfo(exctype, value, tb))

    @abstractmethod
    def _excepthook(self, exception_info):
        pass

    @abstractmethod
    def start_install(self):
        """ Start install
        """
        pass

    @abstractmethod
    def start_uninstall(self):
        """ Start uninstall
        """
        pass

    @abstractmethod
    def start_update(self):
        """ Start update"""
        pass
