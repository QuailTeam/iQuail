import os

class BundleTemplate():

    def __init__(self, bundle_name: str, base_dir='/Application'):
        self.full_path = os.path.join(base_dir, bundle_name + ".app")
        self.names = [
                    self.full_path,
                    os.path.join(self.full_path, 'Contents'),
                    os.path.join(self.full_path, 'Contents/MacOS'),
                    os.path.join(self.full_path, 'Contents/Resources')
        ]

    def make(self):
        for path in self.names:
            os.mkdir(path)
