from fnmatch import fnmatch


def accept_path(path, ignore_list):
    """ Check if path should be ignored according to ignore_list
    ignore_list should be a list of ignore
    Example:
    [ "*.py", "!*/test.py"]
    will ignore all path ending with ".py" except
    all files named "test.py"
    """

    def not_pattern(ignore_pattern):
        if ignore_pattern.startswith('!'):
            return ignore_pattern[1:]
        return '!' + ignore_pattern

    accept = True
    for ignore in ignore_list:
        not_ignore = not_pattern(ignore)
        if fnmatch(path, ignore) ^ fnmatch(path, not_ignore):
            accept = fnmatch(path, not_ignore)
    return accept


class FileIgnore:
    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self._ignore_list = f.read().splitlines()
        except FileNotFoundError:
            self._ignore_list = []

    def is_file_ignored(self, path):
        return accept_path(path, self._ignore_list)
