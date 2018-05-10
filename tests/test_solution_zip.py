
import unittest
import os
import quail
from base_test_case import BaseTestCase
from quail import SolutionZip


class TestSolutionZip(unittest.TestCase):
	
	def __init__(self, *args, **kwargs):
		super(TestSolutionZip, self).__init__(*args, **kwargs)
		self.verifier = quail.SolutionZip("res/lol.zip", print)
	
	@classmethod
	def setUpClass(cls):
		pass
		
	def test_openZip(self):
		pass
		
	def test_local(self):
		self.assertTrue(self.verifier.local(), True)

	
	def test_openZip(self):
		self.assertTrue(self.verifier.open(), True)
		self.verifier.close()

if __name__ == '__main__':
	print("Test Solution zip")
	unittest.main()
