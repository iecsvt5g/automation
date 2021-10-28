#/usr/bin/python3
'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot for linux by unittest.
'''

import sys
sys.path.insert(0, '..\\lib')
from reboot import reboot_machine
from nose.tools import *
from HTMLTestRunner import *

class reboot(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print('Start:\tReboot for linux by unittest.')

	@classmethod
	def tearDownClass(self):
		print('End:\tReboot for linux by unittest.')

	def test_case_01_reboot(self):
		self = reboot_machine()
		print(self.reboot(1))
		if self.reboot(1) == False:
			raise(Exception('Error'))

	def test_case_02_multi_reboot(self):
		self = reboot_machine()
		print(self.reboot(5))
		if self.reboot(5) == False:
			raise(Exception('Error'))

if __name__ == '__main__':
	report_dir=r'reboot.html'
	re_open = open(report_dir, 'wb')
	suite = unittest.TestLoader().loadTestsFromTestCase(reboot)
	runner = HTMLTestRunner(
						stream=re_open, \
						title=u'Linux auto reboot by ZL.', \
						description=u'Test Report')
	runner.run(suite)