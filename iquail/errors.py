class SolutionUnreachableError(Exception):
    """Raised if solution is not reachable"""
    pass


class SolutionNotRemovableError(Exception):
    """Raised if solution is not reachable"""
    pass

class SolutionFileNotFoundError(SolutionUnreachableError):
    """Raised if solution cannot retreive file"""
    pass

class SolutionVersionNotFoundError(SolutionUnreachableError):
    """Raised if distant version cannot be selected"""
    pass

class SolutionDecompressionError(SolutionUnreachableError):
    """Raised if distant version cannot be selected"""
    pass
