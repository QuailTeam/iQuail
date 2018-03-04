
class Config:
    '''Class to save solution configuration and default values
    '''
    def __init__(self, name, solution, binary, icon, publisher='Quail', console=False):
        self._solution = solution
        self._name = name
        self._icon = icon
        self._binary = binary
        self._publisher = publisher
        self._console = console

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
