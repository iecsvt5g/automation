#/usr/bin/python3
'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot script under the linux environment.
'''

from time import sleep, time
from os import system
import sys

class reboot_machine(object):
	def reboot(self, times, ip):
		try:
			for i in range(int(times)):
				print('Reboot times: ' + str(i+1))
				print('The system is rebooting..')
				self.ssh(ip)
				if i >= 0:
					for wait_time in range(30):
						print('Waitting....' + str(wait_time + 1))
						sleep(1)
					self.ssh_ip(ip)
			return True
		except:
			return False

	def ssh(self, ip):
		system('ssh -t -l zl ' + ip + ' \"sudo reboot\"')

	def ssh_ip(self, ip):
		system('ssh -t -l zl ' + ip + ' \"ifconfig enp0s3 | grep "inet " | awk {\'print $2\'}\"')

if __name__ == "__main__":
	r = reboot_machine()
	r.reboot(2, '172.20.10.5')