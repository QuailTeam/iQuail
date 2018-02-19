

class AInstaller:
    def __init__(self, name, solution_path, binary, icon, console=False):
        self._solution_path = solution_path
        self._name = name
        self._icon = icon
        self._binary = binary
        self._console = console
    
    def get_name(self):
        return self._name

    def get_solution_path(self):
        return self._solution_path

    def get_binary(self):
        return self._binary

    def get_icon(self):
        return self._icon

    def get_console(self):
        return self._console
    
    def install(self):
        raise NotImplementedError

    def uninstall(self):
        raise NotImplementedError

    def is_installed(self):
        raise NotImplementedError

    def get_file(self, *args):
        raise NotImplementedError

