import atexit
import os
import shutil
import sys
import copy
import ctypes
import platform
import tempfile

from ..constants import Constants

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


def running_from_installed_binary():
    # TODO: unittest
    split_script_path = os.path.normpath(get_script_path()).split(os.path.sep)
    # split script path should look like [..,".iquail", "project_name"]
    if len(split_script_path) < 2:
        return False
    return split_script_path[-2] == Constants.IQUAIL_ROOT_NAME


def running_from_script():
    """check if being run from script
    and not builded in standalone binary"""
    if getattr(sys, 'frozen', False):
        return False
    return True


def _delete_atexit(path_to_delete):
    """On windows we can't remove binaries being run.
    This function will remove a file or folder at exit
    to be able to delete itself
    """
    assert os.path.isdir(path_to_delete)

    def _delete_from_tmp():
        tmpdir = tempfile.mkdtemp()
        newscript = shutil.copy2(get_script(), tmpdir)
        args = (newscript, Constants.ARGUMENT_RM, path_to_delete)
        if running_from_script():
            os.execl(sys.executable, sys.executable, *args)
        else:
            os.execl(newscript, *args)

    atexit.register(_delete_from_tmp)


def self_remove_directory(directory):
    """Remove directory but if we are running from a compiled binary
    it will remove the directory only when exiting.
    This function was made for windows, because we can't remove ourself on windows
    """
    if running_from_script():
        shutil.rmtree(directory)
    else:
        _delete_atexit(directory)


def rerun_as_admin(graphical):
    if OS_LINUX:
        cmd = None
        if graphical is False:
            cmd = ['sudo', '-A']
        elif shutil.which('gksudo'):
            cmd = ['gksudo', '--']
        elif shutil.which('kdesudo'):
            cmd = ['kdesudo']
        sys.exit(os.execvp(cmd[0], cmd + sys.argv))
    elif OS_WINDOWS:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None,
                                                'runas',
                                                sys.executable,
                                                ' '.join(sys.argv),
                                                None, 1)
    exit(0)


def move_folder_content(src, dest, ignore_errors=False):
    """Move folder content to another folder"""
    for f in os.listdir(src):
        # print("moved %s >> %s" % (os.path.join(src, f), dest))
        try:
            shutil.move(os.path.join(src, f), dest)
        except:
            if not ignore_errors:
                raise


def safe_remove_folder_content(src):
    """Remove folder content
    If an error happens while removing
    the content will be untouched
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        move_folder_content(src, tmp_dir)
    except Exception:
        # rollback move on exception
        move_folder_content(tmp_dir, src, ignore_errors=True)
        raise
    finally:
        # TODO chmod -R +w ?
        shutil.rmtree(tmp_dir)


def safe_mkdtemp(debug=False):
    """Same as mkdtemp but removes the directory when quail exit
    """
    tmp_dir = tempfile.mkdtemp()
    if debug:
        print("Created: " + tmp_dir, file=sys.stderr)

    def delete_tmp_dir():
        if not os.path.isdir(tmp_dir):
            return
        try:
            shutil.rmtree(tmp_dir)
            if debug:
                print("Removed: " + tmp_dir, file=sys.stderr)
        except Exception as e:
            print("Can't remove: " + tmp_dir + " : " + str(e), file=sys.stderr)

    atexit.register(delete_tmp_dir)
    return tmp_dir
