
import os
import tempfile
import shutil
import urllib.request
import sys
import json
from .solution_zip import SolutionZip
from . import helper


class SolutionGitHub(SolutionZip):
    ''' GitHub solution
    made to be embeded in the executable (with pyinstaller --add-data)
    limitations:
    max ram size / max tmp size
    '''

    def __init__(self, name, glink, process = None):
        self._glink = glink
        self._name = name
        
    def local(self):
        return True

    def open(self):
        self._path = tempfile.mkdtemp()
        jstr = urllib.request.urlopen(self._glink).read()
        lol = json.loads(jstr)
        lol = lol[0]
        print (json.dumps(lol, indent=2, sort_keys=True))
        #~ lol = lol[0]
        #~ print (lol['zipball_url'])
        return True

    def close(self):
        shutil.rmtree(self._path)

    def walk(self):
        pass

    def get_file(self, relative_path):
        return os.path.join(self._path, relative_path)

if __name__ == '__main__':
	print("Test Solution zip")
	unittest.main()
