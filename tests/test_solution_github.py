import unittest

from quail import SolutionGitHub


class TestSolutionGithub(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSolutionGithub, self).__init__(*args, **kwargs)

    def test_openGitHub(self):
        f = SolutionGitHub("cmder.zip", "https://github.com/cmderdev/cmder")
        f.open()


if __name__ == '__main__':
    print("Test Solution zip")
    unittest.main()
