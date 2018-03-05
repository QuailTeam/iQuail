import os
import sys
import ctypes
import platform


class Helper:
    OS_LINUX = platform.system() == 'Linux'
    OS_WINDOWS = platform.system() == 'Windows'

    @staticmethod
    def makedirs_ignore(*args, **kwargs):
        try:
            os.makedirs(*args, **kwargs)
        except FileExistsError:
            pass

    @staticmethod
    def get_module_path():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def get_script():
        return os.path.realpath(sys.argv[0])

    @staticmethod
    def get_script_name():
        return os.path.basename(Helper.get_script())

    @staticmethod
    def get_script_path():
        return os.path.dirname(Helper.get_script())

    @staticmethod
    def running_from_script():
        '''check if being run from script and not builded in standalone binary'''
        if getattr(sys, 'frozen', False):
            return False
        return True

    @staticmethod
    def rerun_as_admin():
        if Helper.OS_LINUX:
            # os.system('pkexec %s %s' % (Helper.get_script_path(), ' '.join(sys.argv[1:])))
            raise NotImplementedError
        elif Helper.OS_WINDOWS:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None,
                                                    'runas',
                                                    sys.executable,
                                                    ' '.join(sys.argv),
                                                    None, 1)
        exit(0)
