from abc import ABC, abstractmethod


class UiBase(ABC):
    @abstractmethod
    def start_install(self):
        """ Start ui
        """
        pass

    @abstractmethod
    def progress_callback(self, progress):
        """This method will be set in solutioner
        Ui must show the update the progress when this method is called
        """
        pass
