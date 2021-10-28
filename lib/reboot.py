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
				for wait_time in range(times):
					print('Waitting....' + str(wait_time + 1))
				print('The system is rebooting..')
				self.ssh(ip)
			return True
		except:
			return False

	def ssh(self, ip):
		# system('ssh -t -l zl 192.168.8.102 ifconfig enp0s3 | grep \"inet \" | awk {\'print $2\'}')
		system('ssh -t -l zl ' + ip + ' \"sudo reboot\"')

if __name__ == "__main__":
	r = reboot_machine()
	r.reboot(1, '172.20.10.5')