
from .helper import *

if OS_LINUX:
    from .install_linux import InstallLinux
    Install = InstallLinux
elif OS_WINDOWS:
    from .install_windows import InstallWindows
    Install = InstallWindows
else:
    raise NotImplementedError
