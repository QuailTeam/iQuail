import os

class BundleTemplate():

    def __init__(self, CFBundleName):
        self.bundle_name = CFBundleName
        #TODO refactor name
        self.base_dir = "/Applications/"
        self.full_path = self.base_dir + self.bundle_name + ".app"
        self.names = [self.full_path, self.full_path + "/Contents", self.full_path + "/Contents/MacOS"]

    def make(self):
        for path in self.names:
            os.mkdir(path)