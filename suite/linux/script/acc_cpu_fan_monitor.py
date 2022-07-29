#/usr/bin/python3
'''
Created on 2022/02/05

@author: ZL Chen
@title: RU Temperture.
'''

import configparser, sys, time, datetime, os
sys.path.insert(0, '/root/automation/suite/linux/lib')
from network_ssh_no_close import ssh

config = configparser.ConfigParser()
config.read('/root/automation/suite/linux/ini/acc_cpu_fan.ini')
tempmax = float(config.get('setting', 'tempmax'))
tempmin = float(config.get('setting', 'tempmin'))
monitortime = int(config.get('setting', 'monitortime'))
ssh_result = False

def ipmicmd(cmdIn):
	return os.popen("ipmitool " + cmdIn)

def getcputemp():
	cmd = ipmicmd('sdr | grep "TEMP"')
	cputemperatures = []
	cputemplist = cmd.readlines()
	for cputemp in cputemplist:
		degree = float(cputemp[cputemp.find('degrees')-4 : cputemp.find('degrees')].strip())
		cputemperatures.append(int(degree))

	cputemp_sum = float(0)
	for cputemp_n in cputemperatures:
		cputemp_sum += cputemp_n
	cputemp_avg = cputemp_sum / len(cputemperatures)

	return cputemp_avg

def getacctemp():
	command = 'ru_cmd gettemp | sed \'s/[a-z]*//g\' | tr -d \':\''
	try:
		ssh().ssh_command(command)
		respone_temp = ssh().ssh_respone()
		respone_temp = respone_temp.split('b\'')[1].strip()
		respone_temp = float(respone_temp[:-3])
		return respone_temp
	except:
		ssh().close
		ssh().ssh_connection()

def monitor(acctemp, cputemp, nowfan):
	if acctemp > tempmax:
		print("acctemp > tempmax")
		nowfan += int(config.get('setting', 'fanup'))
		nowfan = min(nowfan, int(config.get('setting', 'fanmax')))
		ipmitemp = "ipmitool raw 0x30 0xCA 0x0 0x2 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}".format(fan=nowfan)
		os.popen("ipmitool raw 0x30 0xCA 0x0 0x0 0x1")
		os.popen(ipmitemp)
	
	if acctemp < tempmin:
		print("acctemp < tempmin")
		nowfan -= int(config.get('setting', 'fandown'))
		nowfan = max(nowfan, int(config.get('setting', 'fanmin')))
		ipmitemp = "ipmitool raw 0x30 0xCA 0x0 0x2 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}".format(fan=nowfan)
		os.popen("ipmitool raw 0x30 0xCA 0x0 0x0 0x1")
		os.popen(ipmitemp)
	#print(str(nowfan) + " " + str(nowfan/64*100) + "%")
	return nowfan

def main():
	nowfan = int(config.get('setting', 'fanstart'))
	ipmitemp = "ipmitool raw 0x30 0xCA 0x0 0x2 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan} 0x{fan}".format(fan=nowfan)
	os.popen("ipmitool raw 0x30 0xCA 0x0 0x0 0x1")
	os.popen(ipmitemp)
	print('Fan started')
	ssh().ssh_connection()

	while True:
		acctemp = getacctemp()
		cputemp = getcputemp()
		nowfan = monitor(acctemp, cputemp, nowfan)
		time.sleep(monitortime)

if __name__ == '__main__':
	main()		

#if __name__ == '__main__':
#	acc_parser = acc_parser()
#	while True:
#		command = 'ru_cmd gettemp | sed \'s/[a-z]*//g\' | tr -d \':\''
#		acc_parser.parser(command, config.get('setting', 'limit_acc'))
#		print('Done')
#		time.sleep(10)
