#/usr/bin/python3
'''
Created on 2021/10/27
Modified on 2022/01/03

@author: ZL Chen
@title: Reboot script under the linux environment.
'''

from time import sleep
from sys import path
path.insert(0, '.\..\\lib')
from network import ssh
import configparser

config = configparser.ConfigParser()
config.read(".\..\\ini\\reboot_script.ini")

class reboot_machine():
	def reboot(self, passwd, times, waittime, interface):
		try:
			for i in range(int(times)):
				print('Reboot times: ' + str(i+1))
				print('The system is rebooting..')
				sh = ssh()
				sh.ssh_command('echo \'' + passwd + '\' | sudo -S reboot')
				sh.ssh_respone('')
				if i >= 0:
					for wait_time in range(waittime):
						print('Waitting....' + str(wait_time + 1))
						sleep(1)
					sh.ssh_command('ip address show dev ' + interface + ' | grep \"inet \" | awk {\'print $2\'}')
					sh.ssh_respone(config.get('setting', 'response_ip'))
			return True
		except:
			return False

if __name__ == '__main__':
	r = reboot_machine()
	r.reboot(config.get('setting', 'passwd'), config.get('setting', 'times'), config.get('setting', 'waittime'), config.get('setting', 'interface'))