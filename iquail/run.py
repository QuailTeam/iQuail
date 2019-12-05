import sys
import argparse
import shutil
import os
import logging

from contextlib import suppress
from .constants import Constants
from . import helper
from .builder import Builder
from .manager import Manager
from .controller import ControllerConsole
from .helper import misc

logger = logging.getLogger(__name__)


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
    parser.add_argument(Constants.ARGUMENT_REPLACE,
                        type=str,
                        help="""replace file:
                            dest:src
                            this function is used by iquail for windows self update
                            """)
    parser.add_argument(Constants.ARGUMENT_RUN,
                        help="Before exiting the solution will be run",
                        action="store_true")
    parser.add_argument(Constants.ARGUMENT_INSTALL_POLKIT,
                        action="store_true",
                        help="Tells iQuail to install a polkit authorization file in /usr/bin/polkit-1/actions and "
                             "then rerun itself with pkexec (Linux only)")
    parser.add_argument(Constants.ARGUMENT_VALIDATE,
                        type=str,
                        help="Validate a solution")

    return parser.parse_known_args()


def run(solution, installer, builder=None, controller=None, conf_ignore=None):
    """run config"""
    (args, unknown) = parse_args()

    # chdir to the directory where the executable is at
    # os.chdir(os.path.dirname(sys.argv[0]))

    if not builder:
        builder = Builder()
    if not controller:
        controller = ControllerConsole()
    manager = Manager(installer, solution, builder, controller.is_graphical(),
                      conf_ignore=conf_ignore)
    if args.iquail_validate:
        success, _ = manager.validate_solution(args.iquail_validate)
        if not success:
            print("VALIDATION FAILED", file=sys.stderr)
            exit(1)
        print("VALIDATION PASSED", file=sys.stderr)
        exit(0)
    controller.setup(manager)
    if args.iquail_rm:
        shutil.rmtree(args.iquail_rm)
    elif args.iquail_replace:
        dest, src = args.iquail_replace.split(Constants.PATH_SEP)
        os.replace(src, dest)
    elif args.iquail_build:
        manager.build()
    elif args.iquail_uninstall:
        controller.start_uninstall()
    else:
        if misc.running_from_installed_binary():
            controller.start_run_or_update()
        else:
            if manager.is_installed():
                logger.info(misc.get_script_path())
                # program is installed but we are not launched from the installed folder
                # TODO: ask repair/uninstall
                controller.start_uninstall()
            else:
                controller.start_install()
    if args.iquail_run:
        controller.start_run_or_update()
