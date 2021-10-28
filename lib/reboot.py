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
		try:
			for i in range(int(times)):
				print('Reboot times: ' + str(i+1))
				# sleep(20)
				print('The system is rebooting..')
				# system('echo sudo reboot')
				self.ssh()
			return True
		except:
			return False

	def ssh(self):
		# a = system('ssh -t -l zl 192.168.8.102 ifconfig enp0s3 | grep \"inet \" | awk {\'print $2\'}')
		system('ssh -t -l zl 192.168.8.102 \"sudo reboot\"')

if __name__ == "__main__":
	r = reboot_machine()
	r.reboot(1)