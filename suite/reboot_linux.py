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

class take_screen_shot():
	def __init__(self, func):
		self.func = func
		# self.name = func.__name__ + ' (__main__.CalTestCase).png'
		self.name = func.__name__ + ' (__main__.reboot_linux).png'
	def __call__(self, *args):
		try:
			self.func(self, *args)
		finally:
			# driver.get_screenshot_as_file(self.name)
			pass

class reboot(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print('Start:\tReboot for linux by unittest.')

	@classmethod
	def tearDownClass(self):
		print('End:\tReboot for linux by unittest.')

	@take_screen_shot
	def test_case_01_reboot(self):
		self = reboot_machine()
		self = self.reboot(1, '172.20.10.5')
		if self == False:
			raise(Exception('Error'))

	@take_screen_shot
	def test_case_02_multi_reboot(self):
		self = reboot_machine()
		self = self.reboot(1000, '172.20.10.5')
		# self = self.reboot(1000, '172.20.10.5')
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