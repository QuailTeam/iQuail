from abc import ABC, abstractmethod
import sys
from ..errors import SolutionUnreachableError, SolutionNotRemovableError
from ..helper.traceback_info import ExceptionInfo


class ControllerBase(ABC):
    __manager = None

    def __init__(self, eula=None):
        self._eula = eula

    @property
    def eula(self):
        return self._eula

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
            raise AssertionError(
                "manager is None, You must call Controller.setup() first")
        return self.__manager

    def excepthook(self, exctype, value, tb):
        exc_info = ExceptionInfo(exctype, value, tb)
        if isinstance(value, SolutionNotRemovableError):
            self.callback_solution_not_removable_error(exc_info)
        elif isinstance(value, SolutionUnreachableError):
            self.callback_solution_unreachable_error(exc_info)
        elif isinstance(value, KeyboardInterrupt):
            sys.__excepthook__(exctype, value, tb)
        else:
            self._excepthook(exc_info)

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
    def callback_solution_unreachable_error(self, exception_info):
        """This handler will be called when start_run_or_update
        raises SolutionUnreachableError"""
        pass

    @abstractmethod
    def callback_solution_not_removable_error(self, exception_info):
        """This handler will be called when SolutionNotRemovable
        is raised"""
        pass

    @abstractmethod
    def start_run_or_update(self):
        """ Start update"""
        pass

    @abstractmethod
    def is_graphical(self):
        """Tells if controller is graphical or terminal
        :return: Boolean
        """
        pass
