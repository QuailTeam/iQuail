import sys

from .controller_base import ControllerBase
try:
    from .controller_tkinter import ControllerTkinter
except ImportError as e:
    print(f"Tkinter not found....", file=sys.stderr)
from .controller_console import ControllerConsole
