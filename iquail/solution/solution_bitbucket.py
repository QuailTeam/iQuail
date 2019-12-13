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


class SolutionBitBucket(SolutionBase):
    """ BitBucket solution
    Find zip solutions on bitbucket
    """

    def __init__(self, zip_name, repo_url):
        super().__init__()
        self._solution_zip = None
        self._repo_url = repo_url.strip('/')
        self._zip_name = zip_name

    @cache_result
    def _parse_bitbucket_url(self):
        """Parse bitbucket url, returns tuple:
        (repo_owner, repo_name)
        """
        [(owner, repo_name)] = re.findall(r"bitbucket\.org/(.*?)/(.*?)$", self._repo_url)
        return owner, repo_name

    def _get_zip_url(self):
        return "%s/downloads/%s" % (self._repo_url, self._zip_name)

    def get_version_string(self):
        owner, repo_name = self._parse_bitbucket_url()
        try:
            response = urllib.request.urlopen("https://api.bitbucket.org/2.0/repositories/%s/%s/downloads/" % (owner, repo_name))
            data = response.read()
            encoding = response.info().get_content_charset("utf-8")
            downloads = json.loads(data.decode(encoding))
        except Exception as e:
            raise SolutionUnreachableError("SolutionBitBucket get release") from e
        if not downloads:
            raise SolutionUnreachableError("No releases")
        for download in downloads['values']:
            if download['name'] is self._zip_name:
                return download['created_on']
        raise SolutionUnreachableError("Can not find release file on remote source")

    def local(self):
        return False

    def open(self):
        zip_url = self._get_zip_url()
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
                "Solution bitbucket retrieve error") from e
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
