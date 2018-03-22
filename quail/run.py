
import sys
import argparse
import shutil
from .constants import Constants
from . import helper
from .builder import Builder
from .manager import Manager


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


def run(solution, installer, builder=Builder()):
    '''run config'''
    args = parse_args()
    manager = Manager(installer, solution)
    if args.quail_rm:
        shutil.rmtree(args.quail_rm)
    elif args.quail_build and helper.running_from_script():
        builder.register(solution)
        builder.build()
    elif args.quail_uninstall:
        manager.uninstall()
    else:
        if manager.is_installed():
            manager.run()
        else:
            manager.install()
