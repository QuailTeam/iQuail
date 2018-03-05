
import stat
import sys
import os
import argparse
from .Constants import Constants
from .Helper import Helper
from .Config import Config
from .Builder import Builder

if Helper.OS_LINUX:
    from .LinuxInstaller import LinuxInstaller
    Installer = LinuxInstaller
elif Helper.OS_WINDOWS:
    from .WindowsInstaller import WindowsInstaller
    Installer = WindowsInstaller
else:
    raise NotImplementedError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(Constants.ARGUMENT_UNINSTALL,
                        help="uninstall program",
                        action="store_true")
    parser.add_argument(Constants.ARGUMENT_BUILD,
                        help="build executable",
                        action="store_true")
    return parser.parse_args()


def run(config_dict):
    '''run config'''
    args = parse_args()
    config = Config(**config_dict)
    if (args.quail_build):
        builder = Builder(config)
        builder.build()
        sys.exit(0)
    installer = Installer(config)
    if args.quail_uninstall:
        installer.uninstall()
        sys.exit(0)
    if installer.is_installed():
        binary = installer.get_install_path(installer.config.binary)
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)
        os.system(binary + " " + " ".join(sys.argv))
    else:
        installer.install()
