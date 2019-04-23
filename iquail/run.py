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
from .helper import misc


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
    parser.add_argument(Constants.ARGUMENT_INSTALL_POLKIT,
                        action="store_true",
                        help="Tells iQuail to install a polkit authorization file in /usr/bin/polkit-1/actions and "
                             "then rerun itself with pkexec (Linux only)")
    return parser.parse_known_args()


def run(solution, installer, builder=None, controller=None):
    """run config"""
    (args, unknown) = parse_args()

    # chdir to the directory where the executable is at
    os.chdir(os.path.dirname(os.path.sys.argv[0]))

    if not builder:
        builder = Builder()
    if not controller:
        controller = ControllerConsole()
    manager = Manager(installer, solution, builder, controller.is_graphical())
    controller.setup(manager)

    if args.iquail_build:
        manager.build()
    elif misc.running_from_installed_binary():
        controller.start_run_or_update()
    else:
        manager.check_permissions(manager.uid)
        if args.iquail_install_polkit:
            helper.polkit_install(helper.get_script(), manager.uid)
            helper.rerun_as_admin(controller.is_graphical(), manager.uid)
        elif args.iquail_uninstall:
            controller.start_uninstall()
        elif args.iquail_rm:
            shutil.rmtree(args.iquail_rm)
        else:
            if manager.is_installed():
                print(misc.get_script_path())
                # program is installed but we are not launched from the installed folder
                # TODO: ask repair/uninstall
                controller.start_uninstall()
            else:
                controller.start_install()
