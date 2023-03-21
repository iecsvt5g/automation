#/usr/bin/python3
'''
Created on 2022/09/27

@author: ZL Chen
@title: PHY Status Parser
'''

from subprocess import check_output
from pymysql import connect
from time import *
import re
from configparser import ConfigParser

config = ConfigParser()
config.read('/etc/inventec_svt_deployment/setting.ini')

class phy(object):
	'''
	Timezone: UTC+8 to UTC
	'''
	def datetime_taiwan_to_utc(self, datetime):
		taiwan_time = strptime(datetime, "%Y-%m-%d %H:%M:%S")
		taiwan_time = mktime(taiwan_time)
		utc_time = taiwan_time - 8 * 60 * 60
		utc_time = localtime(utc_time)
		new_time = strftime('%Y-%m-%d %H:%M:%S', utc_time)
		return new_time
		
	'''
	PHY information parser: PHY status parser
	'''
	def _phy_parser(self):
		with open('/etc/hostname', 'r+') as f:
			host_name = f.readlines()[0].strip()
		# print('hostname:', host_name)
		while True:
			die_status = bool()
			# gnb_io_fpga_thread_stop parser
			gnb_stop = 'grep \"gnb_io_fpga_thread_stop\" /home/BaiBBU_XSS/BaiBBU_PXSS/PHY/bin/Phy.log \
							| awk \'END{print $1}\' | sed \'s/*//g\''
			# gnb_stop = 'grep \"gnb_io_fpga_thread_stop\" Phy.log | awk \'END{print $1}\' | sed \'s/*//g\''
			phy_gnb_stop = check_output(gnb_stop, shell=True).decode('utf-8').strip()
			if len(phy_gnb_stop) == 0:
				print('no value')
				break
			else:
				print('value', phy_gnb_stop)
			
			ip = self._ip_parser()
			print(ip)
			# locat time parser
			local_time = 'grep \"local time:  \" /home/BaiBBU_XSS/BaiBBU_PXSS/PHY/bin/Phy.log \
							| awk \'END{print $(NF-1), $(NF)}\' | sed \'s/*//g\''
			# local_time = 'grep \"local time:  \" Phy.log | awk \'END{print $(NF-1), $(NF)}\' | sed \'s/*//g\''
			phy_local_time = check_output(local_time, shell=True).decode('utf-8').strip()
			# print(phy_local_time)

			# PHY status check
			if phy_local_time:
				print('value')
				utc_time = self.datetime_taiwan_to_utc(phy_local_time)
				die_status = True
				self.insert_database(utc_time, ip, host_name, die_status)
				break
			else:
				print('no value', phy_local_time)
				break

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
	def insert_database(self, datetime, ip, host_name, die_status):
		try:
			mysql_info = {
				# 'host': '172.32.3.153',
				'host': config.get('setting', 'mysql_ip'),
				'port': 3306,
				'user': 'svt',
				'password': '1qaz@WSXiecsvt5g',
				'db': 'svt'
			}
			conn = connect(**mysql_info)
			cur = conn.cursor()
			sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, PHY_PARSER_STATUS) \
				VALUES(%s, %s, %s)""".format(table='phy_parser_status')
			# print(sql)
			cur.execute(sql, (datetime, ip, host_name, die_status))
			conn.commit()
			print('The information is commit to database.')
		except Exception as e:
			# raise e
			pass

if __name__ == '__main__':
	while True:
		func = phy()
		func._phy_parser()
		sleep(3)