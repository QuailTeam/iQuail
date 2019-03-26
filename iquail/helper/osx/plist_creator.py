import xml.etree.ElementTree as ET

class PlistCreator:
    def __init__(self, bundle_name: str, plistDict: dict):
        self.__file = open("/applications/" + bundle_name + ".app/contents/info.plist", "a+")
        self.__
        self.__plist_dict = {
            "CFBundleGetInfoString": bundle_name,
            "CFBundleExecutable": 'launcher',
            "CFBundleIdentifier": bundle_name,
            "CFBundleName": bundle_name
        }
        self.__plist_header = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        """
        self.__plist_dict.update(plistDict)

    def __del__(self):
        self.__file.close()

    @property
    def plist_dict(self):
        return self.__plist_dict

    def write_file(self):
        self.__create_header()

    def __create_header(self):
        self.__file.write(self.__plist_header)


