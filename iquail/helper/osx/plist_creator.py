import os
import xml.etree.ElementTree as ET


class PlistCreator:
    def __init__(self, bundle_name: str, application_path: str, plist_dict=None):
        # The argument plist_dict can't be mutable
        if not plist_dict:
            plist_dict = {}
        self.__filename = os.path.join(application_path, bundle_name + ".app/Contents/Info.plist")
        self.__data = ""
        self.__plist_dict = {
            "CFBundleGetInfoString": bundle_name,
            "CFBundleExecutable": 'launcher',
            "CFBundleIdentifier": bundle_name,
            "CFBundleName": bundle_name
        }
        self.__plist_header = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        """
        self.__plist_dict.update(plist_dict)

    @property
    def plist_dict(self):
        return self.__plist_dict

    def __make_key_with_text(self, key: str, value: str):
        item = ET.Element(key)
        item.text = value
        return item

    def __indent_tree(self, elem, level=0):
            i = "\n" + level * "  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    self.__indent_tree(elem, level + 1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

    def __add_icon(self, root: ET.Element, icon_name: str):
        root.append(self.__make_key_with_text('key', 'CFBundleIconFile'))
        root.append(self.__make_key_with_text('string', icon_name))

    def __create_header(self):
        self.__data += self.__plist_header

    def __create_tree(self) -> ET.Element:
        root = ET.Element('plist', {'version':'1.0'})
        return root

    def write_file(self):
        self.__create_header()
        tree = self.__create_tree()
        self.__write_dict_to_file(tree)
        self.__indent_tree(tree)
        tree_data = ET.tostring(tree, encoding='unicode')
        with open(self.__filename, 'w+') as f:
            total_data = self.__data + tree_data
            f.write(total_data)

    def __write_dict_to_file(self, root: ET.Element):
        for key, value in self.plist_dict.items():
            root.append(self.__make_key_with_text('key', key))
            root.append(self.__make_key_with_text('string', value))




