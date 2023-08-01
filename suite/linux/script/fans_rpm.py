#/usr/bin/python3
'''
Created on 2023/04/13

@author: ZL Chen
@title: BBU FANs rpm
'''

from time import *
from os import popen
from pymysql import connect
from configparser import ConfigParser
from influxdb import InfluxDBClient

config = ConfigParser()
config.read('/etc/inventec_svt_deployment/setting.ini')

class fan(object):
	'''
	Timezone: UTC+8 to UTC
	'''
	def datetime_taiwan_to_utc(self, datetime):
		taiwan_time = mktime(datetime)
		utc_time = taiwan_time - 8 * 60 * 60
		utc_time = localtime(utc_time)
		new_time = strftime('%Y-%m-%d %H:%M:%S', utc_time)
		return new_time
		
	'''
	FANs rpm information
	'''
	def _rpm(self, name):
		fans_name = list()
		fans_rpm = list()
		rpm_data = list()	
		utc_time = self.datetime_taiwan_to_utc(localtime())
		print('utc_time', utc_time)
		ip = self._ip_parser()
		print('ip', ip)
		with open('/etc/hostname', 'r+') as f:
			host_name = f.readlines()[0].strip()
		print('hostname', host_name)
		try:
			if popen(name).read().strip() == 'GIGABYTE':
				print('It\'s GIGABYTE')
				fans_name = popen('ipmitool sdr | grep FAN | awk \'{print $1}\'').readlines()
				fans_rpm = popen('ipmitool sdr | grep FAN | awk \'{print $3}\'').readlines()
				print(fans_name, fans_rpm)
				for i in range(len(fans_name)):
					print(fans_name[i].strip(), fans_rpm[i].strip())
					rpm_data.append(fans_rpm[i].strip())
				print('rpm_data', rpm_data)
				influxdbtime=strptime(utc_time,'%Y-%m-%d %H:%M:%S')
				influxdbtime=int((mktime(influxdbtime)+60*60*8)*1000)
				while len(rpm_data) <= 8 :
					rpm_data.append(None)
				self.insert_database(influxdbtime, ip, host_name, 
                         rpm_data[0],rpm_data[1],rpm_data[2],rpm_data[3],
                         rpm_data[4],rpm_data[5],rpm_data[6],rpm_data[7])
				sleep(60)
			elif popen(name).read().strip() == 'Inventec':
				print('It\'s Inventec')
				fans_name = popen('ipmitool sdr | grep -n \'Fan[[:digit:]]\' | grep \'RPM\' | awk \'{print $1}\'').readlines()
				fans_rpm = popen('ipmitool sdr | grep -n \'Fan[[:digit:]]\' | grep \'RPM\' | awk \'{print $3}\'').readlines()
				print(fans_name, fans_rpm)
				for i in range(len(fans_name)):
					print(fans_name[i].strip(), fans_rpm[i].strip())
					rpm_data.append(fans_rpm[i].strip())
				print('rpm_data', rpm_data)
				influxdbtime=strptime(utc_time,'%Y-%m-%d %H:%M:%S')
				influxdbtime=int((mktime(influxdbtime)+60*60*8)*1000)
				while len(rpm_data) <= 8 :
					rpm_data.append(None)
				self.insert_database(influxdbtime, ip, host_name, 
                         rpm_data[0],rpm_data[1],rpm_data[2],rpm_data[3],
                         rpm_data[4],rpm_data[5],rpm_data[6],rpm_data[7])
			elif popen(name).read().strip() == 'Supermicro':
				print('It\'s Supermicro')
				fans_name = popen('ipmitool sdr | grep FAN | awk \'{print $1}\'').readlines()
				fans_rpm = popen('ipmitool sdr | grep FAN | awk \'{print $3}\'').readlines()
				print(fans_name, fans_rpm)
				for i in range(len(fans_name)):
					if fans_rpm[i].strip() == 'no':
						fans_rpm[i] = None
						print(fans_name[i].strip(), fans_rpm[i])
						rpm_data.append(fans_rpm[i])
					else:
						print(fans_name[i].strip(), fans_rpm[i].strip())
						rpm_data.append(fans_rpm[i].strip())
				print('rpm_data', rpm_data)
				influxdbtime=strptime(utc_time,'%Y-%m-%d %H:%M:%S')
				influxdbtime=int((mktime(influxdbtime)+60*60*8)*1000)
				while len(rpm_data) <= 8 :
					rpm_data.append(None)
				self.insert_database(influxdbtime, ip, host_name, 
                         rpm_data[0],rpm_data[1],rpm_data[2],rpm_data[3],
                         rpm_data[4],rpm_data[5],rpm_data[6],rpm_data[7])
				sleep(60)
			else:
				print('No Fans RPM data')
		except:
			pass
		
	'''
	IP Address Parser
	'''
	def _ip_parser(self):
		try:
			ip_command = config.get('setting', 'bbu_ip')
			return ip_command
		except:
			return 'Not Found IP'

	# '''
	# Insert into date to MySQL (phpmyadmin)
	# '''
	# def insert_database(self, datetime, ip, host_name, fan_len, rpm_data = []):
	# 	try:
	# 		mysql_info = {
	# 			'host': config.get('setting', 'mysql_ip'),
	# 			'port': 3306,
	# 			'user': 'svt',
	# 			'password': '1qaz@WSXiecsvt5g',
	# 			'db': 'svt'
	# 		}
	# 		conn = connect(**mysql_info)
	# 		cur = conn.cursor()
	# 		if fan_len == 4:
	# 			sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, FAN0, FAN1, FAN2, FAN3) \
	# 				VALUES(%s, %s, %s, %s, %s, %s, %s)""".format(table='fan')
	# 			cur.execute(sql, (datetime, ip, host_name, rpm_data[0], rpm_data[1], rpm_data[2], rpm_data[3]))
	# 			# print(sql, (datetime, ip, host_name, rpm_data[0], rpm_data[1], rpm_data[2], rpm_data[3]))
	# 		elif fan_len == 6:
	# 			sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, FAN0, FAN1, FAN2, FAN3, FAN4, FAN5) \
	# 				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table='fan')
	# 			cur.execute(sql, (datetime, ip, host_name, rpm_data[0], rpm_data[1], rpm_data[2], rpm_data[3], rpm_data[4], rpm_data[5]))
	# 			# print(sql, (datetime, ip, host_name, rpm_data[0], rpm_data[1], rpm_data[2], rpm_data[3], rpm_data[4], rpm_data[5]))
	# 		elif fan_len == 8:
	# 			sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, FAN0, FAN1, FAN2, FAN3, FAN4, FAN5, FAN6, FAN7) \
	# 				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table='fan')
	# 			cur.execute(sql, (datetime, ip, host_name, rpm_data[0], rpm_data[1], rpm_data[2], rpm_data[3], rpm_data[4], rpm_data[5], rpm_data[6], rpm_data[7]))
	# 			# print(sql, (datetime, ip, host_name, rpm_data[0], rpm_data[1], rpm_data[2], rpm_data[3], rpm_data[4], rpm_data[5], rpm_data[6], rpm_data[7]))
	# 		else:
	# 			pass
	# 		conn.commit()
	# 		print('The information is commit to database.')
	# 	except Exception as e:
	# 		# raise e
	# 		pass
 
 
	'''
	insert into SMO influxdb
 	'''
	def insert_database(self, TIME, IP, HOST_NAME, FAN0,FAN1,FAN2,FAN3,FAN4,FAN5,FAN6,FAN7) :
		try :
			d= [{
			"measurement": "fan_parser",
			"tags": {
				"ip": IP,
				"hostname":HOST_NAME
			},
			"time": TIME,
			"fields": { 'FAN0':FAN0,'FAN1':FAN1,'FAN2':FAN2,'FAN3':FAN3,
						'FAN4':FAN4,'FAN5':FAN5,'FAN6':FAN6,'FAN7':FAN7
					}
				}]

			client = InfluxDBClient("172.32.3.68",8086,'admin','admin','svt')
			client.write_points(d)
			print('Influxdb Insert Data GOOD')
		except :
			print('Influxdb Insert Data BAD')
	

if __name__ == '__main__':
	func = fan()
	name = 'dmidecode -s baseboard-manufacturer'
	while True:
		func._rpm(name)
		sleep(5)