#/usr/bin/python3
'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot for linux by unittest.
'''

from os import system
import sys
from time import sleep
sys.path.insert(0, '..\\lib')
from reboot import reboot_machine
from nose.tools import *
from HTMLTestRunner import *
from configparser import ConfigParser

ini = ConfigParser()
reboot_linux_ini = ini.read('.\..\\ini\\reboot_linux.ini')

class reboot(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print('Start:\tReboot for linux by unittest.')

	@classmethod
	def tearDownClass(self):
		print('End:\tReboot for linux by unittest.')

	def test_case_01_reboot(self):
		self = reboot_machine()
		self = self.reboot(30, '172.20.10.13')
		if self == False:
			raise(Exception('Error'))

	def test_case_02_multi_reboot(self):
		self = reboot_machine()
		self = self.reboot(30, '172.20.10.13')
		if self == False:
			raise(Exception('Error'))

if __name__ == '__main__':
	system('del reboot.html')
	sleep(1)
	report_dir = 'reboot.html'
	re_open = open(report_dir, 'wb')
	suite = unittest.TestLoader().loadTestsFromTestCase(reboot)
	runner = HTMLTestRunner(
						stream = re_open, \
						title = 'Linux auto reboot by ZL.', \
						description = 'Test Report')
	runner.run(suite)