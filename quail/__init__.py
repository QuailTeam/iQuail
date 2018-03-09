
# from .LinuxInstaller import LinuxInstaller
from .run import run
from .solution_local import SolutionLocal
from .solution_ftp import SolutionFtp
from .solution_zip import SolutionZip
from . import helper
from . import builder


if helper.OS_LINUX:
    from .installer_linux import InstallerLinux
    Installer = InstallerLinux
elif helper.OS_WINDOWS:
    from .installer_windows import InstallerWindows
    Installer = InstallerWindows
else:
    raise NotImplementedError
