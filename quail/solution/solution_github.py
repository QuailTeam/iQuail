import json
import re
import os
import shutil
import tempfile
import urllib.request
from pprint import pprint

from .solution_base import SolutionBase
from .solution_zip import SolutionZip


class SolutionGitHub(SolutionBase):
    """ GitHub solution
    Find zip solutions on github
    """

    def __init__(self, zip_name, repo_url):
        super().__init__()
        self._tags = None  # tags json
        self._parsed_github_url = None  # tuple (owner, name)
        self._solution_zip = None
        self._repo_url = repo_url
        self._zip_name = zip_name

    def _parse_github_url(self):
        """Parse github url, returns tuple:
        (repo_owner, repo_name)
        """
        if self._parsed_github_url:
            return self._parsed_github_url
        rep = re.findall(r"github\.com/(.*?)/(.*?)$", self._repo_url)
        if not rep:
            raise AssertionError("Invalid github url")
        self._parsed_github_url = rep[0]
        return self._parsed_github_url

    def _get_tag_url(self):
        return "https://api.github.com/repos/%s/%s/tags" % self._parse_github_url()

    def _get_zip_url(self, tag):
        (owner, name) = self._parse_github_url()
        return "https://github.com/%s/%s/releases/download/%s/%s" % (owner, name, tag, self._zip_name)

    def _get_tags(self):
        if self._tags:
            return self._tags
        response = urllib.request.urlopen(self._get_tag_url())
        data = response.read()
        encoding = response.info().get_content_charset("utf-8")
        tags = json.loads(data.decode(encoding))
        self._tags = tags
        return self._tags

    def _get_last_tag(self):
        if not self._get_tags():
            raise AssertionError("No tags")
        return self._get_tags()[0]

    def local(self):
        return False

    def open(self):
        last_tag_name = self._get_last_tag()["name"]
        zip_url = self._get_zip_url(last_tag_name)
        print(zip_url)

        def hook(count, block_size, total_size):
            self._update_progress(count / (total_size / block_size) * 100)

        (zip_file, headers) = urllib.request.urlretrieve(zip_url,
                                                         reporthook=hook)
        self._solution_zip = SolutionZip(zip_file)
        self._solution_zip.set_hook(self._hook)
        return self._solution_zip.open()

    def close(self):
        self._solution_zip.close()

    def walk(self):
        return self._solution_zip.walk()

    def retrieve_file(self, relative_path):
        return self._solution_zip.retrieve_file(relative_path)
