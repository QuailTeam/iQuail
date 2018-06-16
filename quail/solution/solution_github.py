import json
import re
import shutil
import tempfile
import urllib.request
from pprint import pprint

from .solution_base import SolutionBase


class SolutionGitHub(SolutionBase):
    """ GitHub solution
    Find zip solutions on github
    """

    def __init__(self, zip_name, repo_url):
        super().__init__()
        self._path = None  # tmpdir
        self._parsed_github_url = None  # tuple (owner, name)
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
        # https://api.github.com/repos/rails/rails/tags
        return "https://api.github.com/repos/%s/%s/tags" % self._parse_github_url()

    def _get_zip_url(self):
        # https://github.com/cmderdev/cmder/releases/download/v1.3.6/cmder.zip
        pass #WIP

    def _get_tags(self):
        response = urllib.request.urlopen(self._get_tag_url())
        data = response.read()
        encoding = response.info().get_content_charset("utf-8")
        tags = json.loads(data.decode(encoding))
        pprint(tags)

    def local(self):
        return False

    def open(self):
        self._path = tempfile.mkdtemp()

        return True

    def close(self):
        shutil.rmtree(self._path)

    def walk(self):
        pass

    def retrieve_file(self, relpath):
        pass
