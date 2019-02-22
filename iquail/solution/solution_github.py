import json
import re
import os
import ssl
import shutil
import tempfile
import urllib.request
from pprint import pprint

from ..errors import *
from ..helper import cache_result
from .solution_base import SolutionBase
from .solution_zip import SolutionZip


#ctx = ssl._create_unverified_context()

ssl._create_default_https_context = ssl._create_unverified_context

"""
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
"""

class SolutionGitHub(SolutionBase):
    """ GitHub solution
    Find zip solutions on github
    """

    def __init__(self, zip_name, repo_url):
        super().__init__()
        self._solution_zip = None
        self._repo_url = repo_url
        self._zip_name = zip_name

    @cache_result
    def _parse_github_url(self):
        """Parse github url, returns tuple:
        (repo_owner, repo_name)
        """
        rep = re.findall(r"github\.com/(.*?)/(.*?)$", self._repo_url)
        if not rep:
            raise ValueError("Invalid github url")
        return rep[0]

    def _get_tag_url(self):
        return "http://api.github.com/repos/%s/%s/tags" % self._parse_github_url()

    def _get_zip_url(self, tag):
        (owner, name) = self._parse_github_url()
        return "http://github.com/%s/%s/releases/download/%s/%s" % (owner, name, tag, self._zip_name)

    @cache_result
    def _get_tags(self):
        response = urllib.request.urlopen(self._get_tag_url())
        data = response.read()
        encoding = response.info().get_content_charset("utf-8")
        tags = json.loads(data.decode(encoding))
        return tags

    def _get_last_tag(self):
        return self._get_tags()[0]

    def get_version_string(self):
        return self._get_last_tag()["name"]

    def local(self):
        return False

    def open(self):
        last_tag_name = self._get_last_tag()["name"]
        zip_url = self._get_zip_url(last_tag_name)

        def hook(count, block_size, total_size):
            self._update_progress(percent=count / (total_size / block_size) * 100,
                                  status="downloading")
        try:
            (zip_file, headers) = urllib.request.urlretrieve(zip_url,
                                                             reporthook=hook
            )
        except Exception as e:
            raise
        self._solution_zip = SolutionZip(zip_file)
        self._solution_zip.set_progress_hook(self._progress_hook)
        return self._solution_zip.open()

    def close(self):
        if self._solution_zip:
            self._solution_zip.close()

    def walk(self):
        return self._solution_zip.walk()

    def retrieve_file(self, relative_path):
        return self._solution_zip.retrieve_file(relative_path)
