#/usr/bin/python3
'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot script under the linux environment.
'''

from time import sleep
from os import system
import sys

class reboot_machine(object):
	def reboot(self, times):
		for i in range(int(times)):
			print('Reboot times: ' + str(i+1))
			# sleep(1)
			print('The system is rebooting..')
			# system('echo sudo reboot')ss


if __name__ == "__main__":
	rb = reboot_machine()
	rb.reboot(sys.argv[1])