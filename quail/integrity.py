"""
Module used to verify the integrity of a repository.

- use IntegrityVerifier.dump() to generate the integrity file.
- use IntegrityVerifier.verify() to check it again.
"""

import hashlib
import json
import os
import pathlib
import re


class IntegrityVerifier:
    """Verify integrity of a given path."""

    def __init__(self, path, dump_ignore=None, verify_ignore=None):
        """
        Initialize the integrity verifier.

        path: The path of the checked folder.
        Only use the object to verify this folder.
        """
        self._path = pathlib.Path(path)
        self._dump_ignore = dump_ignore or [r"^\."]
        self._verify_ignore = verify_ignore or [r"^\."]

    def _iterate(self, path=None):
        path = path or self._path
        hashs = {os.path.basename(str(elem)): self._consume(elem)
                 for elem in path.iterdir()
                 if self._accept(str(os.path.basename(str(elem))))}
        return hashs

    def _accept(self, filename):
        if filename == ".integrity.json":
            return False
        for rule in self._ignore:
            if re.search(rule, filename):
                return False
        return True

    def _consume(self, path):
        if path.is_dir():
            return self._iterate(path=path)
        elif path.is_file():
            return hashlib.sha256(path.read_bytes()).hexdigest()
        raise AssertionError("Type of file '{0}' unhandled".format(str(path)))

    def _generate(self):
        self._hashs = self._iterate()

    def _compare_hashs(self, file_hashs, new_hashs, path=[]):
        for filename in file_hashs:
            if filename not in new_hashs:
                self.missing.append(path + [filename])
            else:
                if isinstance(file_hashs[filename], dict) \
                        and isinstance(new_hashs[filename], dict):
                    self._compare_hashs(file_hashs[filename],
                                        new_hashs[filename],
                                        path + [filename])
                elif file_hashs[filename] != new_hashs[filename]:
                    self.changed.append(path + [filename])
        return len(self.missing) + len(self.changed) == 0

    def dump(self, path=None):
        """
        Dump the hashs of a folder.

        Iterate over every file in the linked folder, generating the hashs.
        Then dump them in a file called '.integrity.json' or at the path
        if specified.
        """
        self._ignore = self._dump_ignore
        self._generate()
        filename = os.path.join(str(self._path), path or ".integrity.json")
        with open(filename, mode='w+') as file:
            json.dump(self._hashs, file)

    def verify(self, path=None):
        """
        Verify the hashs of a folder.

        Iterate over every file in the linked folder, generating the hashs.
        Then compare them with the content of the '.integrity.json' file
        or the file situated on the given path.
        Return True if no errors were found.
        In case of errors being encoutered, the paths are saved in self.missing
        and self.changed as lists.
        """
        self._ignore = self._verify_ignore
        self._generate()
        filename = os.path.join(str(self._path), path or ".integrity.json")
        with open(filename, mode='r') as file:
            hashs = json.load(file)
        self.missing = []
        self.changed = []
        return self._compare_hashs(hashs, self._hashs)
