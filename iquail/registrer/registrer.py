
from ..helper import *

if OS_LINUX:
    from .registrer_linux import RegistrerLinux
    Installer = RegistrerLinux
elif OS_WINDOWS:
    from .registrer_windows import RegistrerWindows
    Installer = RegistrerWindows
else:
    raise NotImplementedError
