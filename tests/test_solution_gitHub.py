
import unittest
import os
import quail
from base_test_case import BaseTestCase
from quail import SolutionGitHub


class SolutionGitHub(unittest.TestCase):
	
    def __init__(self, *args, **kwargs):
        super(SolutionGitHub, self).__init__(*args, **kwargs)
	
    @classmethod
    def setUpClass(cls):
        pass
    
    #~ def test_wrong_link(self):
        #~ try :
            #~ quail.SolutionGitHub("test", "https://api.github.com/res/cmderdev/cmder/tags", print)
        #~ finally :
            #~ return True
        #~ return False
    
    def test_openGitHub(slef):
        verifier = quail.SolutionGitHub("test", "https://api.github.com/repos/cmderdev/cmder/releases", print)
        #~ verifier = quail.SolutionGitHub("test", "https://api.github.com/repos/cmderdev/cmder", print)
        #~ verifier = quail.SolutionGitHub("test", "https://api.github.com/repos/Microsoft/ChakraCore/releases", print)
        verifier.open() 

if __name__ == '__main__':
    print("Test Solution zip")
    unittest.main()
