
from .helper import *

if OS_LINUX:
    from .installer_linux import InstallerLinux
    Installer = InstallerLinux
elif OS_WINDOWS:
    from .installer_windows import InstallerWindows
    Installer = InstallerWindows
else:
    raise NotImplementedError
