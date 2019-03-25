import os

class BundleTemplate():

    def __init__(self, CFBundleName):
        self.bundleName = CFBundleName
        #TODO refactor name
        self.baseDir = "/Applications/"
        self.fullPath = self.baseDir + self.bundleName + ".app"
        self.names = [self.fullPath, self.fullPath + "/Contents", self.fullPath + "/Contents/MacOS"]

    def make(self):
        for path in self.names:
            os.mkdir(path)