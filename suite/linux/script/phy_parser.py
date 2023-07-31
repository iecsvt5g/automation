#/usr/bin/python3
'''
Created on 2022/09/17

@author: ZL Chen
@title: PHY Parser
'''

from subprocess import check_output
from pymysql import connect
from time import *
from configparser import ConfigParser
from math import log
from influxdb import InfluxDBClient


config = ConfigParser()
config.read('/etc/inventec_svt_deployment/setting.ini')

class phy(object):
	'''
	Timezone: UTC+8 to UTC
	'''
	def datetime_taiwan_to_utc(self, datetime):
		taiwan_time = strptime(datetime, '%Y-%m-%d %H:%M:%S')
		taiwan_time = mktime(taiwan_time)
		utc_time = taiwan_time - 8 * 60 * 60
		utc_time = localtime(utc_time)
		new_time = strftime('%Y-%m-%d %H:%M:%S', utc_time)
		return new_time
		
	'''
	PHY information parser: DateTime, IP, DL, UL, UL BLER, SRS
	'''
	def _phy_parser(self):
		global phy_index
		time_list = list()
		phy_list = list()
		time_parser = 'grep \""SysTimeInfo"\" \
						/home/BaiBBU_XSS/BaiBBU_PXSS/PHY/bin/Phy.log \
						| awk \'END{print $3, $4}\' | sed \'s/*//g\''
		with open('/etc/hostname', 'r+') as f:
			host_name = f.readlines()[0].strip()
		# print('hostname:', host_name)
		try:
			time_parser = check_output(time_parser, shell=True).decode("utf-8").strip()	# parser datetime
			time_parser = time_parser.split(' ')
			date = time_parser[0].replace('SysTimeInfo:', '')	# replace date
			date = date.replace('/', '-')	# for mysql date format
			time = time_parser[1].replace(',runningTime:', '')	# replace time
			datetime = date + ' ' + time
			datetime = self.datetime_taiwan_to_utc(datetime)	# UTC+8 to UTC
			influxdbtime=strptime(datetime,'%Y-%m-%d %H:%M:%S')
			influxdbtime=int((mktime(influxdbtime)+60*60*8)*1000)
			time_list.append(datetime)
			time_list = str(time_list[0])	# date and time
		except:
			pass
		for number in range(10):	# Make sure the Cell number
			phy_parser = 'grep \"' + str(number) + ' (Kbps)\" \
						/home/BaiBBU_XSS/BaiBBU_PXSS/PHY/bin/Phy.log | \
						awk \'END{print $3,$4,$5,$6,$7,$8}\' | sed \'s/\s*$//g\''
			phy_parser = check_output(phy_parser, shell=True).decode("utf-8").strip()
			if len(phy_parser) == 0:
				break
			if '%' in phy_parser:
				phy_parser = phy_parser.replace('%', '')
				pass
			phy_list.append(phy_parser)
		for cell in range(number):	# Deal with data format
			phy_index = cell
			show_phy_str = str(phy_list[phy_index]).split(' ')	# List[Str]
			for index in range(len(show_phy_str)):
				if index == 0:
					if ',' in str(show_phy_str[0]):
						dl_tput = float(show_phy_str[0].replace(',', ''))	# Replace ',' to ''
					else:
						dl_tput = float(show_phy_str[0])
				elif index == 1:
					if ',' in str(show_phy_str[1]):
						ul_tput_1 = float(show_phy_str[1].replace(',', ''))	# Replace ',' to ''
					else:
						ul_tput_1 = float(show_phy_str[1])
				elif index == 2:
					pass
				elif index == 3:
					if ',' in str(show_phy_str[3]):
						ul_tput_2 = float(show_phy_str[3].replace(',', ''))	# Replace ',' to ''
					else:
						ul_tput_2 = float(show_phy_str[3])
				elif index == 4:
					ul_bler = float(show_phy_str[4])
				elif index == 5:
					srs_snr = int(show_phy_str[5])
					if srs_snr > 100:
						srs_snr = int(100 + log(srs_snr-100, 10))
					if srs_snr < -100:
						srs_snr*= -1
						srs_snr = int(100 + log(srs_snr-100, 10))*(-1)
				else:
					pass
			cell = str(cell)
			self.insert_database(influxdbtime, self._ip_parser(), host_name, cell, dl_tput, ul_tput_1, ul_tput_2, ul_bler, srs_snr)

	'''
	IP Address Parser
	'''
	def _ip_parser(self):
		try:
			# ip_command = 'ip addr | grep \'inet 172.32\' | awk \'END{print $2}\''
			# ip_command = check_output(ip_command, shell=True).decode("utf-8").strip()
			# ip_command = ip_command.replace('/24', '')	# replace subnet mask str
			# ip_command = ip_command.replace('/16', '')	# replace subnet mask str
			ip_command = config.get('setting', 'bbu_ip')
			return ip_command
		except:
			return 'Not Found IP'

	'''
	Insert into date to MySQL (phpmyadmin)
	'''
	# def insert_database(self, time_list, ip, host_name, cell, dl_tput, ul_tput_1, ul_tput_2, ul_bler, srs_snr):
	# 	try:
	# 		mysql_info = {
	# 			# 'host': '172.32.3.153',
	# 			'host': config.get('setting', 'mysql_ip'),
	# 			'port': 3306,
	# 			'user': 'svt',
	# 			'password': '1qaz@WSXiecsvt5g',
	# 			'db': 'svt'
	# 		}
	# 		conn = connect(**mysql_info)
	# 		cur = conn.cursor()
	# 		sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, CELL, DL_Tput, UL_Tput_1, UL_Tput_2, UL_BLER, SRS_SNR) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table='phy')
	# 		cur.execute(sql, (time_list, ip, host_name, cell, dl_tput, ul_tput_1, ul_tput_2, ul_bler, srs_snr))
	# 		conn.commit()
	# 		print('The information is commit to database.')
	# 	except Exception as e:
	# 		# raise e
	# 		pass
 
	'''
 	insert into SMO influxdb
  	'''
	def insert_database(self,TIME , IP, HOST_NAME, CELL, DL_Tput, UL_Tput_1, UL_Tput_2, UL_BLER, SRS_SNR) :
		try :
			d= [{
			"measurement": "phy_parser",
			"tags": {
				"ip": IP,
				"hostname":HOST_NAME,
				"cell" : CELL
			},
			"time": TIME,
			"fields": { 'DL_1': DL_Tput, 
						'UL_1': UL_Tput_1,
						'UL_2': UL_Tput_2,
						'BLER': UL_BLER,
						'SRS_SNR': SRS_SNR
					}
				}]

			client = InfluxDBClient("172.32.3.68",8086,'admin','admin','svt')
			client.write_points(d)
			print('Influxdb Insert Data GOOOOOOD')
		except :
			print('Influxdb Insert Data BAAAAAAD')
 
 
if __name__ == '__main__':
	while True:
		func = phy()
		func._phy_parser()
		sleep(5)
