
import stat
import sys
import os
import argparse
import shutil
from .constants import Constants
from . import helper
from .builder import Builder


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(Constants.ARGUMENT_UNINSTALL,
                        help="uninstall program",
                        action="store_true")
    parser.add_argument(Constants.ARGUMENT_BUILD,
                        help="build executable",
                        action="store_true")
    parser.add_argument(Constants.ARGUMENT_RM,
                        type=str,
                        help="remove folder")
    return parser.parse_args()


def run(installer, builder=Builder()):
    '''run config'''
    args = parse_args()

    if args.quail_rm:
        shutil.rmtree(args.quail_rm)
    elif args.quail_build and helper.running_from_script():
        builder.build()
    elif args.quail_uninstall:
        installer.uninstall()
    else:
        if installer.is_installed():
            binary = installer.get_install_path(installer.binary)
            if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
                os.chmod(binary, 0o755)
            os.system(binary + " " + " ".join(sys.argv[1:]))
        else:
            installer.install()
