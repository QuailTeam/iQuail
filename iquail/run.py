import sys
import argparse
import shutil
import os
from contextlib import suppress
from .constants import Constants
from . import helper
from .builder import Builder
from .manager import Manager
from .controller import ControllerConsole


def parse_args():
    parser = argparse.ArgumentParser(add_help=helper.running_from_script())
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
                        (this function is used by iquail for windows uninstall)
                        """)
    return parser.parse_known_args()


def run(solution, installer, builder=Builder(), controller=ControllerConsole()):
    """run config"""
    (args, unknown) = parse_args()
    manager = Manager(installer, solution, builder, controller.is_graphical())
    controller.setup(manager)
    if args.quail_rm:
        shutil.rmtree(args.quail_rm)
    elif args.quail_build:
        manager.build()
    elif args.quail_uninstall:
        controller.start_uninstall()
    elif manager.is_installed():
        controller.start_run_or_update()
        # TODO: launch solution first and kill it on update
    else:
        controller.start_install()
