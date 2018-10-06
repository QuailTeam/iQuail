from abc import ABC, abstractmethod
import sys
from ..errors import SolutionUnreachableError
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
    def callback_update_solution_unreachable(self, exception):
        """This handler will be called when start_run_or_update raises SolutionUnreachableError"""
        pass

    @abstractmethod
    def _start_run_or_update(self):
        """ Start update"""
        pass

    def start_run_or_update(self):
        try:
            self._start_run_or_update()
        except SolutionUnreachableError as e:
            self.callback_update_solution_unreachable(e)
