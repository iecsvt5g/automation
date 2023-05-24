#/usr/bin/python3
'''
Created on 2021/12/25
Modified on 2022/02/05

@author: ZL Chen
@title: The network lib.
'''

import configparser
import paramiko
from paramiko import SSHClient

config = configparser.ConfigParser()
config.read('/root/automation/suite/linux/ini/network.ini')

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
		global stdin, stdout, stderr
		stdin, stdout, stderr = s.exec_command(commandline)
		#print('exec SSH command - ' + '\"' + commandline + '\"')

	def ssh_respone(self):
		cmd_result = stdout.read(), stderr.read()
		result = ' '.join(map(str, cmd_result))
		respone_result = result.strip()
		return respone_result

	def ssh_close(self):
		s.close()
