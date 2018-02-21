import os
import sys


def get_script():
    return os.path.realpath(sys.argv[0])


def get_script_name():
    return os.path.basename(get_script())


def get_script_path():
    return os.path.dirname(get_script())


def run_from_script():
    '''check if being run from script and not builded in standalone binary'''
    return get_script().endswith(".py")
