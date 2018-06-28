from abc import ABC, abstractmethod


class ControllerBase(ABC):
    @abstractmethod
    def start_install(self, manager):
        """ Start install
        """
        pass

    @abstractmethod
    def start_uninstall(self, manager):
        """ Start uninstall
        """
        pass

    @abstractmethod
    def start_update(self, manager):
        """ Start update"""
        pass

