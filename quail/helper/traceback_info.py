import traceback


class ExceptionInfo:
    """This class is just an helper to get information about an exception
    """
    def __init__(self, exception):
        self.exception = exception
        self.traceback = traceback.format_tb(self.exception.__traceback__)
        assert isinstance(self.traceback, list)
        self.traceback_str = "".join(self.traceback)
