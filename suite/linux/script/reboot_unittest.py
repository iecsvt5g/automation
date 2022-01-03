#/usr/bin/python3
'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot for linux by unittest.
'''

from time import strftime
from reboot import reboot_machine
from nose.tools import *
from HTMLTestRunner import *
from configparser import ConfigParser

config = ConfigParser()
config.read(".\..\\ini\\reboot_script.ini")

class take_screen_shot():
	def __init__(self, func):
		self.func = func
		self.name = func.__name__ + ' (__main__.reboot).png'
	def __call__(self, *args):
		try:
			self.func(self, *args)
		finally:
			pass

class reboot_unittest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print('Start:\tReboot for linux by unittest.')

	@classmethod
	def tearDownClass(self):
		print('End:\tReboot for linux by unittest.')

	@take_screen_shot
	def test_case_01_reboot(self):
		self = reboot_machine()
		self = self.reboot(config.get('setting', 'passwd'), '1', config.get('setting', 'waittime'), config.get('setting', 'interface'))
		if self == False:
			raise(Exception('Error'))

	@take_screen_shot
	def test_case_02_multi_reboot(self):
		self = reboot_machine()
		self = self.reboot(config.get('setting', 'passwd'), config.get('setting', 'times'), config.get('setting', 'waittime'), config.get('setting', 'interface'))
		if self == False:
			raise(Exception('Error'))

if __name__ == '__main__':
	now = strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
	report_dir = 'reboot_' + now + '.html'
	re_open = open('.\..\\report\\' + report_dir, 'wb')
	suite = unittest.TestLoader().loadTestsFromTestCase(reboot_unittest)
	runner = HTMLTestRunner(
						stream = re_open, \
						title = 'Linux auto test by ZL.', \
						description = 'Test Report')
	runner.run(suite)