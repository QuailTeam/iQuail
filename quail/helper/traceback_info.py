import traceback


class ExceptionInfo:
    """This class is just an helper to get information about an exception
    """
    def __init__(self, exctype, value, tb):
        self.exception = value
        self.traceback_list = traceback.format_exception(exctype, value, tb)
        self.traceback_str = ''.join(self.traceback_list)
