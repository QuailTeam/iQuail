
# from .LinuxInstaller import LinuxInstaller
from .run import run
from .solution_local import SolutionLocal
from .solution_ftp import SolutionFtp
from .solution_zip import SolutionZip
from .helper import Helper
from .builder import Builder
from .build_cmd_zip import BuildCmdZip

if Helper.OS_LINUX:
    from .installer_linux import InstallerLinux
    Installer = InstallerLinux
elif Helper.OS_WINDOWS:
    from .installer_windows import InstallerWindows
    Installer = InstallerWindows
else:
    raise NotImplementedError
