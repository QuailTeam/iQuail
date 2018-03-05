
# from .LinuxInstaller import LinuxInstaller
from .run import run
from .LocalSolution import LocalSolution
from .FtpSolution import FtpSolution
from .ZipSolution import ZipSolution
from .Helper import Helper
from .Builder import Builder

if Helper.OS_LINUX:
    from .LinuxInstaller import LinuxInstaller
    Installer = LinuxInstaller
elif Helper.OS_WINDOWS:
    from .WindowsInstaller import WindowsInstaller
    Installer = WindowsInstaller
else:
    raise NotImplementedError
