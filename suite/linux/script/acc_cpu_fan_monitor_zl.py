#/usr/bin/python3
'''
Created on 2022/02/05
Modified on 2023/04/04

@author: ZL Chen
@title: ACC & RU temperature monitor
'''

import os, time, configparser, paramiko
# from network_ssh_no_close import ssh

config = configparser.ConfigParser()
config.read('setting.ini')
tempmax = float(config.get('fan', 'tempmax'))
tempmin = float(config.get('fan', 'tempmin'))
monitortime = int(config.get('fan', 'monitortime'))
ssh_result = False

class ssh(object):
	def ssh_connection(self):
		global s
		host = config.get('fan', 'host')
		name = config.get('fan', 'name')
		passwd = config.get('fan', 'passwd')
		port = int(config.get('fan', 'port'))
		s = paramiko.SSHClient()
		s.load_system_host_keys()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		s.connect(host, port, name, passwd, timeout=8)

	def ssh_command(self, commandline):
		global stdin, stdout, stderr
		stdin, stdout, stderr = s.exec_command(commandline)

	def ssh_respone(self):
		cmd_result = stdout.read(), stderr.read()
		result = ' '.join(map(str, cmd_result))
		respone_result = result.strip()
		return respone_result

	def ssh_close(self):
		s.close()

class fan(object):
	# def ipmicmd(self, cmdIn):
	# 	return os.popen('ipmitool ' + cmdIn)

	# def getcputemp(self):
	# 	cmd = self.ipmicmd('sdr | grep \"TEMP\"')
	# 	cputemperatures = []
	# 	cputemplist = cmd.readlines()
	# 	for cputemp in cputemplist:
	# 		print(cputemp)
	# 		degree = float(cputemp[cputemp.find('degrees')-4 : cputemp.find('degrees')].strip())
	# 		print(degree, 'degree')
	# 		cputemperatures.append(int(degree))
	# 		print(cputemperatures, 'cputemperatures')
	# 	print('ZL')
	# 	time.sleep(11111)
	# 	cputemp_sum = float(0)
	# 	for cputemp_n in cputemperatures:
	# 		cputemp_sum += cputemp_n
	# 	cputemp_avg = cputemp_sum / len(cputemperatures)
	# 	return cputemp_avg

	def getacctemp(self):
		command = 'ru_cmd gettemp | sed \'s/[a-z]*//g\' | tr -d \':\''
		try:
			_s.ssh_connection()
			_s.ssh_command(command)
			respone = _s.ssh_respone()
			respone = respone.split('b\'')[1].strip()
			respone = int(respone[:-3])
			# print(respone_temp)
			return respone
		except:
			pass
		finally:
			_s.ssh_close()

	# def monitor(self, acctemp, cputemp, nowfan):
	# 	if acctemp > tempmax:
	# 		print('acctemp > tempmax')
	# 		nowfan += int(config.get('fan', 'fanup'))
	# 		nowfan = min(nowfan, int(config.get('fan', 'fanmax')))
	# 		ipmitemp = 'ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x02 0x48 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}'.format(fan=nowfan)
	# 		os.popen('ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x00 0x01')
	# 		os.popen(ipmitemp)
	# 	if acctemp < tempmin:
	# 		print('acctemp < tempmin')
	# 		nowfan -= int(config.get('fan', 'fandown'))
	# 		nowfan = max(nowfan, int(config.get('fan', 'fanmin')))
	# 		ipmitemp = 'ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x02 0x48 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}'.format(fan=nowfan)
	# 		os.popen('ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x00 0x01')
	# 		os.popen(ipmitemp)
	# 	return nowfan

	def monitor(self, acctemp):
		if acctemp > tempmax:
			print('acctemp > tempmax')
			# nowfan += int(config.get('fan', 'fanup'))
			# nowfan = min(nowfan, int(config.get('fan', 'fanmax')))
			ipmitemp = 'ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x02 0x48 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}'\
							.format(fan=int(config.get('fan', 'fanmax')))
			print(ipmitemp)
			os.popen('ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x00 0x01')
			os.popen(ipmitemp)
			print('ACC > MAX')
		if acctemp < tempmin:
			print('acctemp < tempmin')
			# nowfan -= int(config.get('fan', 'fandown'))
			# nowfan = max(nowfan, int(config.get('fan', 'fanmin')))
			ipmitemp = 'ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x02 0x48 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}'\
							.format(fan=int(config.get('fan', 'fanmin')))
			print(ipmitemp)
			os.popen('ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x00 0x01')
			os.popen(ipmitemp)
			print('ACC < MIN')
		# return nowfan

	def main(self):
		# nowfan = int(config.get('fan', 'fanstart'))
		# ipmitemp = 'ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x02 0x48 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}'.format(fan=nowfan)
		# os.popen('ipmitool raw 0x2e 0x31 0xa9 0x19 0x00 0x00 0x01')
		# os.popen(ipmitemp)
		print('Fan started')
		# _s.ssh_connection()
		while True:
			acctemp = int(self.getacctemp())
			# cputemp = self.getcputemp()
			# nowfan = self.monitor(acctemp, cputemp, nowfan)
			self.monitor(acctemp)
			time.sleep(monitortime)

if __name__ == '__main__':
	_s = ssh()
	f = fan()
	f.main()