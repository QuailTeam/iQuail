class SolutionUnreachableError(Exception):
    """Raised if solution is not reachable"""
    pass


class SolutionNotRemovableError(Exception):
    """Raised if solution is not reachable"""
    pass

class SolutionFileNotFoundError(Exception):
    """Raised if solution cannot retreive file"""
    pass

class SolutionVersionNotFoundError(Exception):
    """Raised if distant version cannot be selected"""
    pass
