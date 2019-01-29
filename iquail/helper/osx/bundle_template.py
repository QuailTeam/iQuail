import os

"""

iquail.app/
    Contents/
        Info.plist
        MacOS/
            iquail
        Resources/
            iquail.icns

"""

class BundleTemplate():

    def __init__(self, CFBundleName):
        self.bundleName = CFBundleName
        self.baseDir = "/Applications/"
        self.fullPath = self.baseDir + self.bundleName + ".app"
        self.names = [self.fullPath, self.fullPath + "/Contents", self.fullPath + "/Contents/MacOS"]

    def make(self):
        for path in self.names:
            print("Creating folder: " + path)
            os.mkdir(path)
        # mkdir /Applications/Bundle.app
        # mkdir /Applications/Bundle.app/Contents
        # mkdir /Applications/Bundle.app/Contents/MacOS
        # mkdir /Applications/Bundle.app/Contents/Resources
        
        # touch mkdir /Applications/Bundle.app/Contents/Info.plist
        # OR MV # touch mkdir /Applications/Bundle.app/Resources/XXX.icns
        # OR MV # touch mkdir /Applications/Bundle.app/MacOS/XXX -> BINARY
