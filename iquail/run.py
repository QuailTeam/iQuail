import argparse
import argparse
import shutil
from abc import ABC, abstractmethod

from . import helper
from .builder import Builder
from .constants import Constants
from .controller import ControllerConsole
from .manager import Manager


class Setup(ABC):
    @abstractmethod
    def get_installer(self):
        pass

    @abstractmethod
    def get_solution(self):
        pass

    @abstractmethod
    def get_builder(self):
        pass


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


def build(builder):
    if helper.running_from_script():
        builder.build()
    else:
        raise AssertionError("Can't build from an executable")


def run(solution, installer, builder=None, controller=None):
    """run config"""
    (args, unknown) = parse_args()
    if not builder:
        builder = Builder()
    if not controller:
        controller = ControllerConsole()
    manager = Manager(installer, solution, builder)
    controller.setup(manager)
    if args.quail_rm:
        shutil.rmtree(args.quail_rm)
    elif args.quail_build:
        build(builder)
    elif args.quail_uninstall:
        controller.start_uninstall()
    else:
        if manager.is_installed():
            controller.start_run_or_update()
            # TODO: launch solution first and kill it on update
        else:
            controller.start_install()
