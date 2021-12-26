'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot for linux by unittest.
'''

import sys
import time
import configparser
sys.path.insert(0, '..\\lib')
from os import system
from time import sleep
from reboot import reboot_machine
from nose.tools import *
from HTMLTestRunner import *

ini = configparser.ConfigParser()
ini.read('.\..\\ini\\reboot_script.ini')

class take_screen_shot():
	def __init__(self, func):
		self.func = func
		# self.name = func.__name__ + ' (__main__.CalTestCase).png'
		self.name = func.__name__ + ' (__main__.reboot).png'
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
		self = self.reboot(1, ini.get('setting', 'ip'), ini.get('setting', 'name'), ini.get('setting', 'interface'))
		if self == False:
			raise(Exception('Error'))

	@take_screen_shot
	def test_case_02_multi_reboot(self):
		self = reboot_machine()
		self = self.reboot(ini.get('setting', 'run_time'), ini.get('setting', 'ip'), ini.get('setting', 'name'), ini.get('setting', 'interface'))
		if self == False:
			raise(Exception('Error'))

if __name__ == '__main__':
	now = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
	report_dir = 'reboot_' + now + '.html'
	re_open = open('.\..\\report\\' + report_dir, 'wb')
	suite = unittest.TestLoader().loadTestsFromTestCase(reboot)
	runner = HTMLTestRunner(
						stream = re_open, \
						title = 'Linux auto reboot by ZL.', \
						description = 'Test Report')
	runner.run(suite)