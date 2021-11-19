#/usr/bin/python3
'''
Created on 2021/10/27

@author: ZL Chen
@title: Reboot script under the linux environment.
'''

from time import sleep, time
from os import name, system
import sys

class reboot_machine(object):
	def reboot(self, times, ip, name, interface):
		try:
			for i in range(int(times)):
				print('Reboot times: ' + str(i+1))
				print('The system is rebooting..')
				self.ssh(ip, name)
				if i >= 0:
					for wait_time in range(60):
						print('Waitting....' + str(wait_time + 1))
						sleep(1)
					self.ssh_ip(ip, name, interface)
			return True
		except:
			return False

	def ssh(self, ip, name):
		system('ssh -t -l ' + name + ' ' + ip + ' \"echo ' + name + ' | sudo -S reboot\"')

	def ssh_ip(self, ip, name, interface):
		system('ssh -t -l ' + name + ' ' + ip + ' \"ifconfig ' + interface + ' | grep "inet " | awk {\'print $2\'}\"')

# if __name__ == '__main__':
# 	r = reboot_machine()
	# r.reboot(2, '172.20.10.13', 'zl', 'wlp2s0')