"""
Module used to verify the integrity of a repository.

- use IntegrityVerifier.dump() to generate the integrity file.
- use IntegrityVerifier.verify() to check it again.
"""

import hashlib
import json
import os
import pathlib


class IntegrityVerifier:
    """Verify integrity of a given path."""

    def __init__(self, path):
        """
        Initialize the integrity verifier.

        path: The path of the checked folder.
        Only use the object to verify this folder.
        """
        self.path = pathlib.Path(path)

    def __iterate(self, path=None):
        path = path or self.path
        hashs = {os.path.basename(str(elem)): self.__consume(elem)
                 for elem in path.iterdir()
                 if not str(os.path.basename(str(elem))).startswith(".")}
        return hashs

    def __consume(self, path):
        if path.is_dir():
            return self.__iterate(path=path)
        elif path.is_file():
            return hashlib.sha256(path.read_bytes()).hexdigest()
        raise AssertionError("Type of file '{0}' unhandled".format(str(path)))

    def __generate(self):
        self.hashs = self.__iterate()

    def __compare_hashs(self, d1, d2, path=[]):
        for k in d1:
            if k not in d2:
                self.missing.append(path + [k])
            else:
                if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                    self.__compare_hashs(d1[k], d2[k], path + [k])
                elif d1[k] != d2[k]:
                    self.diffs.append(path + [k])
        return len(self.missing) + len(self.diffs) == 0

    def dump(self, path=None):
        """
        Dump the hashs of a folder.

        Iterate over every file in the linked folder, generating the hashs.
        Then dump them in a file called '.integrity.json' or at the path
        if specified.
        """
        self.__generate()
        with open(os.path.join(str(self.path), path or ".integrity.json"),
                  mode='w+') as file:
            json.dump(self.hashs, file)

    def verify(self, path=None):
        """
        Verify the hashs of a folder.

        Iterate over every file in the linked folder, generating the hashs.
        Then compare them with the content of the '.integrity.json' file
        or the file situated on the given path.
        Return True if no errors were found.
        In case of errors being encoutered, the paths are saved in self.missing
        and self.diffs as lists.
        """
        self.__generate()
        with open(os.path.join(str(self.path), path or ".integrity.json"),
                  mode='r') as file:
            hashs = json.load(file)
        self.missing = []
        self.diffs = []
        return self.__compare_hashs(hashs, self.hashs)
