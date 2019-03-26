import os

#TODO : add full PATH to spotlight env to access python3
class PlistTemplate():
    def __init__(self, CFBundleName, plistDict):
        self.file = open("/Applications/" + CFBundleName + ".app/Contents/Info.plist", "a+")
        self.plist_dict = dict(
            CFBundleGetInfoString=CFBundleName,
            CFBundleExecutable='launcher',
            CFBundleIdentifier=CFBundleName,
            CFBundleName=CFBundleName
        )
        self.plist_dict.update(plistDict)

    def make(self):
        self._createHeader()
        for key, value in self.plist_dict.items():
            self._writeProperty(key, value, "string")
        self._createFooter()

    def getInfoPlist(self):
        return self.plist_dict

    def _createHeader(self):
        self.plist_header = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
        """
        self.file.write(self.plist_header)

    def _createFooter(self):
        self.plist_footer = """
            </dict>
            </plist>
        """
        self.file.write(self.plist_footer)

    def _writeProperty(self, key, value, typeValue):
        self.file.write("  <key>" + key + "</key>\n")
        self.file.write("  <" + typeValue + ">" + value + "</" + typeValue + ">\n")