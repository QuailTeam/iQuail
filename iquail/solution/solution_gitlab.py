import os
import json
import re
import os
import shutil
import ssl
import tempfile
import urllib.request
from pprint import pprint

from ..errors import *
from ..helper import cache_result
from .solution_base import SolutionBase
from .solution_zip import SolutionZip

ssl._create_default_https_context = ssl._create_unverified_context


class SolutionGitLab(SolutionBase):
    """ Gitlab solution
    Find zip solutions on gitlab
    """

    def __init__(self, zip_name, repo_url, project_id):
        super().__init__()
        self._solution_zip = None
        self._repo_url = repo_url
        self._zip_name = zip_name
        self._project_id = project_id

    @cache_result
    def _parse_gitlab_url(self):
        """Parse gitlab url, returns tuple:
        (repo_owner, repo_name)
        """
        re1 = '.*?'  # Non-greedy match on filler
        re2 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re3 = '.*?'  # Non-greedy match on filler
        re4 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re5 = '.*?'  # Non-greedy match on filler
        re6 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re7 = '.*?'  # Non-greedy match on filler
        re8 = '((?:[a-z][a-z]+))'  # Word 1
        re9 = '.*?'  # Non-greedy match on filler
        re10 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1

        rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8 +
                        re9+re10, re.IGNORECASE | re.DOTALL)
        m = rg.search(self._repo_url)
        owner = m.group(1)
        repo_name = m.group(2)
        return (owner, repo_name)

    def _get_release_url(self):
        return "https://gitlab.com/api/v4/projects/%s/releases" % self._project_id

    def _get_zip_url(self, release):
        re1 = '.*?'  # Non-greedy match on filler
        re2 = '((?:\\/[\\w\\.\\-]+)+)'  # Unix Path 1
        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(release['description'])
        file_path = m.group(1)
        owner, repo_name = self._parse_gitlab_url()
        return "https://gitlab.com/" + owner + '/' + repo_name + '/' + file_path

    @cache_result
    def _get_releases(self):
        try:
            response = urllib.request.urlopen(self._get_release_url())
            data = response.read()
            encoding = response.info().get_content_charset("utf-8")
            releases = json.loads(data.decode(encoding))
        except Exception as e:
            raise SolutionUnreachableError("SolutionGitlab get release") from e
        if not releases:
            raise SolutionUnreachableError("No releases")
        return releases

    def _get_last_release(self):
        return self._get_releases()[0]

    def get_version_string(self):
        return self._get_last_release()["name"]

    def local(self):
        return False

    def open(self):
        last_release_name = self._get_last_release()
        zip_url = self._get_zip_url(last_release_name)
        self._update_progress(percent=0,
                              status="downloading",
                              log="Downloading file:\n" + zip_url + "\n")

        def hook(count, block_size, total_size):
            self._update_progress(percent=count / (total_size / block_size) * 100,
                                  status="downloading")
        try:
            (zip_file, headers) = urllib.request.urlretrieve(zip_url,
                                                             reporthook=hook)
        except Exception as e:
            raise SolutionUnreachableError(
                "Solution gitlab retrieve error") from e
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


p = SolutionGitLab(
    "cmder_mini.zip", "https://gitlab.com/Artous/quail_cmder_test", 14938606)
url = p._get_release_url()
print("release url : " + url)

url = p._get_zip_url(p._get_last_release())
print("zip url : " + url)

