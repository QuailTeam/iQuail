import os
import sys

def get_script():
    return os.path.realpath(sys.argv[0])

def get_script_name():
    return os.path.basename(get_script())

def get_script_path():
    return os.path.dirname(get_script())

