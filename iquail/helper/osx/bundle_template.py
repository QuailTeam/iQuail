import os
import shutil


class BundleTemplate:
    def __init__(self, bundle_name: str, base_dir='/Applications'):
        self.full_path = os.path.join(base_dir, bundle_name + ".app")
        self.names = [
                    self.full_path,
                    os.path.join(self.full_path, 'Contents'),
                    os.path.join(self.full_path, 'Contents/MacOS'),
                    os.path.join(self.full_path, 'Contents/Resources')
        ]
    def installIcon(self, icon_file_name, icon_quail_path):
        dest_path = os.path.join(self.full_path, 'Contents/Resources', icon_file_name)
        try:
            shutil.copy(icon_quail_path, dest_path)
        except FileNotFoundError as e:
            print("Error icon file {} was not found when installing".format(icon_quail_path))


    def make(self):
        for path in self.names:
            os.mkdir(path)
