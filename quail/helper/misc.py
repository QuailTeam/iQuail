import os
import sys
import copy
import ctypes
import platform

OS_LINUX = platform.system() == 'Linux'
OS_WINDOWS = platform.system() == 'Windows'


def cache_result(func):
    """ Decorator to save the return value of a function
    Function will be only run once.
    WARNING:
    - The cached return value will be copied with copy.copy
    - Only shallow copy, not deep copy
    - Use this if you know what you are doing!
    """
    cache_attr = "___cache_result"

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})
        cache = getattr(self, cache_attr)
        if func.__name__ not in cache:
            cache[func.__name__] = func(self, *args, **kwargs)
        return copy.copy(cache[func.__name__])

    return wrapper


def get_module_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_script():
    return os.path.realpath(sys.argv[0])


def get_script_name():
    return os.path.basename(get_script())


def get_script_path():
    return os.path.dirname(get_script())


def running_from_script():
    """check if being run from script
    and not builded in standalone binary"""
    if getattr(sys, 'frozen', False):
        return False
    return True


def rerun_as_admin():
    if OS_LINUX:
        # os.system('pkexec %s %s' % (get_script_path(),
        # ' '.join(sys.argv[1:])))
        raise NotImplementedError
    elif OS_WINDOWS:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None,
                                                'runas',
                                                sys.executable,
                                                ' '.join(sys.argv),
                                                None, 1)
    exit(0)
