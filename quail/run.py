import os
import argparse
import platform
if (platform.system() == 'Linux'):
    from .LinuxInstaller import LinuxInstaller
    Installer = LinuxInstaller
elif (platform.system() == 'Windows'):
    from .WindowsInstaller import WindowsInstaller
    Installer =	Installer
else:
    raise NotImplementedError

def run(config):
    parser = argparse.ArgumentParser()
    parser.add_argument("--uninstall", help="uninstall program", action="store_true")
    args = parser.parse_args()
    installer = Installer(**config)
    if args.uninstall:
        installer.uninstall()
    else:
        if installer.is_installed():
            os.system(installer.get_install_path(installer.get_binary()))
        else:
            installer.install()
