import os

class PlistTemplate():
    def __init__(self, CFBundleName, plistDict):
        print("init template")
        self.file = open("/Applications/" + CFBundleName + ".app/Contents/Info.plist", "a+")
        self.plistDict = dict(
            CFBundleGetInfoString=CFBundleName,
            CFBundleExecutable=CFBundleName,
            CFBundleIdentifier=CFBundleName,
            CFBundleName=CFBundleName
        )
        self.plistDict.update(plistDict)

    def make(self):
        self._createHeader()
        for key, value in self.plistDict.items():
            self._writeProperty(key, value, "string")
        self._createFooter()

    def getInfoPlist(self):
        return self.plistDict

    def _createHeader(self):
        self.plistHeader = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
        """
        self.file.write(self.plistHeader)

    def _createFooter(self):
        self.plistFooter = """
            </dict>
            </plist>
        """
        self.file.write(self.plistFooter)

    def _writeProperty(self, key, value, typeValue):
        self.file.write("  <key>" + key + "</key>\n")
        self.file.write("  <" + typeValue + ">" + value + "</" + typeValue + ">\n")