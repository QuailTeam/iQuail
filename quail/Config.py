
class Config:
    '''Class to save solution configuration and default values
    '''

    def __init__(self, name, binary, icon,
                 solution,
                 publisher='Quail',
                 console=False,
                 build_icon='',
                 build_onefile=True):
        self._name = name
        self._binary = binary
        self._icon = icon
        self._solution = solution
        self._publisher = publisher
        self._console = console
        self._build_icon = build_icon
        self._build_onefile = build_onefile

    @property
    def build_onefile(self):
        return self._build_onefile

    @property
    def build_icon(self):
        return self._build_icon

    @property
    def solution(self):
        return self._solution

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def binary(self):
        return self._binary

    @property
    def publisher(self):
        return self._publisher

    @property
    def console(self):
        return self._console
