
class ISolutionResolver:
    ''' The goal of this interface is to be able to resolve solution files
    comming from anywhere.
    current goals are:
    - from builtin data (added with pyinstaller)
    - from local directory
    - over network
    '''

    def access(self):
        '''Check if solution can be accessed
        returns boolean
        '''
        raise NotImplementedError
    
    def open(self):
        '''Open solution if needed
        (planned for unzipping, connecting to network, etc)
        '''
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def walk(self):
        '''Iter files
        returns iterator,
        iter file solution relative path
        same output as os.walk
        '''
        raise NotImplementedError
    
    def get_file(self, relative_path):
        '''Load file if needed, from solution relative path
        returns file real path'''
        raise NotImplementedError
