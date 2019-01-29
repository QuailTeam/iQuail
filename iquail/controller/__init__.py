from .controller_base import ControllerBase
try:
    from .controller_tkinter import ControllerTkinter
except:
    print("No display found or tkinter missing, console mode enabled !")
from .controller_console import ControllerConsole
