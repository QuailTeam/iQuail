
import sys
import argparse
import shutil
import os
from contextlib import suppress
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
                        help="""remove file or folder:
                        if file is passed as argument and the file's directory
                        is empty, the directory will be removed
                        (this function is used by quail for windows uninstall)
                        """)
    return parser.parse_args()


def run(solution, installer, builder=None, ui=None):
    """run config"""
    args = parse_args()
    manager = Manager(installer, solution, builder, ui)
    if args.quail_rm:
        try:
            shutil.rmtree(args.quail_rm)
        except NotADirectoryError:
            os.remove(args.quail_rm)
            with suppress(OSError):
                os.rmdir(os.path.dirname(args.quail_rm))
    elif args.quail_build:
        if not builder:
            builder = Builder()
        manager.build()
    elif args.quail_uninstall:
        manager.uninstall()
    else:
        if manager.is_installed():
            manager.run()
        else:
            manager.install()
