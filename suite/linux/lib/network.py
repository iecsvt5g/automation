#/usr/bin/python3
'''
Created on 2021/12/25

@author: ZL Chen
@title: The network lib.
'''

import configparser
import paramiko
from paramiko import SSHClient

config = configparser.ConfigParser()
config.read(".\..\\ini\\network.ini")

class ssh(object):
	def ssh_connection(self):
		global s
		host = config.get('ssh_setting', 'host')
		name = config.get('ssh_setting', 'name')
		passwd = config.get('ssh_setting', 'passwd')
		port = int(config.get('ssh_setting', 'port'))

		s = paramiko.SSHClient()
		s.load_system_host_keys()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		s.connect(host, port, name, passwd, timeout=8)

	def ssh_command(self, commandline):
		self.ssh_connection()
		global stdin, stdout, stderr
		stdin, stdout, stderr = s.exec_command(commandline)
		print('exec SSH command - ' + '\"' + commandline + '\"')

	def ssh_respone(self, message):
		cmd_result = stdout.read(), stderr.read()
		result = ' '.join(map(str, cmd_result))
		respone_result = result.strip()
		# print(message)
		if message in respone_result:
			# print('found respone message - PASS')
			# print message
			return True, respone_result
		else:
			# raise Exception('not found respone message - FAIL')
			return False, respone_result
		s.close()

# if __name__ == "__main__":
# 	print('The Network.py code.')
	# ssh = ssh()
	# ssh.ssh_command('pwd')
	# ssh.ssh_respone('/home/svt')