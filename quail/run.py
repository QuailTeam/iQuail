import argparse
import platform
from .LinuxInstaller import LinuxInstaller


def get_installer(config):
    # move this later
    if (platform.system() == 'Linux'):
        return LinuxInstaller(**config)
    raise NotImplementedError

def run(config):
    parser = argparse.ArgumentParser()
    parser.add_argument("--uninstall", help="Uninstall program", action="store_true")
    args = parser.parse_args()
    installer = get_installer(config)
    if args.uninstall:
        installer.uninstall()
    else:
        installer.install()
