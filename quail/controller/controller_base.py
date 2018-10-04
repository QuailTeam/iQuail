from abc import ABC, abstractmethod
import sys
from ..helper.traceback_info import ExceptionInfo


class ControllerBase(ABC):
    __manager = None

    def setup(self, manager):
        """Setup controller
        """
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
        """This hook will be called if any unhandled exception happen
        You shouldn't call this function yourself:
        If you want to add callback on this hook, add them on self.excepthook instead
        """
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
    def start_run_or_update(self):
        """ Start update"""
        pass
