#/usr/bin/python3
'''
Created on 2022/02/05

@author: ZL Chen
@title: RU Temperture.
'''

import configparser, sys, time, datetime, os, string, pymysql
sys.path.insert(0, '/root/automation/suite/linux/lib')
from network_ssh_no_close import ssh

config = configparser.ConfigParser()
config.read('/root/automation/suite/linux/ini/acc_cpu_fan.ini')
##SQL
az_sql_ip = config.get('setting','az_sql_ip')
az_sql_port = config.get('setting','az_sql_port')
az_sql_user = config.get('setting','az_sql_user')
az_sql_password = config.get('setting','az_sql_password')
az_sql_database = config.get('setting','az_sql_database')
az_sql_table = config.get('setting','az_sql_table_cpu_acc_fan')
recordtime = int(config.get('setting', 'recordtime'))
ip = config.get('setting','local_ip')
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

	return cputemperatures

def getfanrpm():
	cmd = ipmicmd('sdr | grep "Fan "')
	fanrpms = []
	fanlist = cmd.readlines()
	for fan in fanlist:
		if fan.startswith("F"):
			fanrpm = fan[fan.find('RPM')-6 : fan.find('RPM')].strip()
		fanrpms.append(int(fanrpm))

	return fanrpms

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

def insertValue(time, cputemp, acctemp, fanrpm):
	cputemp_avg = float(0)
	cputemp_sum = float(0)
	fanrpm_avg = float(0)
	fanrpm_sum = float(0)
	
	for cputemp_n in cputemp:
		cputemp_sum += cputemp_n
	cputemp_avg = cputemp_sum / len(cputemp)
	
	for fanrpm_n in fanrpm:
		fanrpm_sum += fanrpm_n
	fanrpm_avg = fanrpm_sum / len(fanrpm)
	
	try :
		sql_config = {'host':f'{az_sql_ip}','port':int(f'{az_sql_port}'),'user':f'{az_sql_user}','password':f'{az_sql_password}','db':f'{az_sql_database}'}
		conn = pymysql.connect(**sql_config)
		cur = conn.cursor()
		
	except :
		print('sql connect error')

	try :		
		sql="""INSERT INTO {table}(time, ip, cputemp_1, cputemp_2, cputemp_avg, acctemp, fanrpm_1, fanrpm_2, fanrpm_3, fanrpm_4, fanrpm_5, fanrpm_6, fanrpm_avg)
				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				""".format(table=az_sql_table)
		cur.execute(sql, (time, ip, cputemp[0], cputemp[1], cputemp_avg, acctemp, fanrpm[0], fanrpm[1], fanrpm[2], fanrpm[3], fanrpm[4], fanrpm[5], fanrpm_avg))

		conn.commit()

	except Exception as e:
			print(e)	

def main():
	ssh().ssh_connection()

	while True:
		acctemp = getacctemp()
		cputemp = getcputemp()
		fanrpm = getfanrpm()
		insertValue(time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()), cputemp, acctemp, fanrpm)
		time.sleep(recordtime)

if __name__ == '__main__':
	main()
