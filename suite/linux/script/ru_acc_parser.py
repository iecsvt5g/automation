#/usr/bin/python3
'''
Created on 2023/03/16

@author: ZL Chen
@title: RU & rHub & AccCard Temperature
'''

from pymysql import connect
from time import *
import paramiko, os, configparser

config = configparser.ConfigParser()
config.read('/etc/inventec_svt_deployment/setting.ini')

class ru_acc(object):
	'''
	Timezone: UTC+8 to UTC
	'''
	def datetime_taiwan_to_utc(self, datetime):
		# taiwan_time = strptime(datetime, '%Y-%m-%d %H:%M:%S')
		taiwan_time = mktime(datetime)
		# print(taiwan_time)
		utc_time = taiwan_time - 8 * 60 * 60
		utc_time = localtime(utc_time)
		new_time = strftime('%Y-%m-%d %H:%M:%S', utc_time)
		return new_time
		
	'''
	RU & rHub & AccCard information parser
	'''
	def _ru_acc_parser(self):
		time_list = self.datetime_taiwan_to_utc(localtime())
		print(time_list)
		with open('/etc/hostname', 'r+') as f:
			host_name = f.readlines()[0].strip()
		print('hostname:', host_name)
		ip_list = list()
		ip_address_list  = os.popen('arp | grep xeth | awk {\'print $1\'}')
		ip_address_list = ip_address_list.readlines()
		for loop in range(len(ip_address_list)):
			ip_address_append = ip_address_list[loop].strip()
			ip_list.append(ip_address_append)
		print(ip_list)	# arp | grep xeth
		ru_acc_user = config.get('ru_acc', 'user')
		ru_acc_passwd = config.get('ru_acc', 'passwd')
		for i in range(len(ip_list)):
			print(ip_list[i])
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(hostname=ip_list[i], port=22, username=ru_acc_user, password=ru_acc_passwd)
				# ssh.connect(hostname=ip_list[i], port=22, username='root', password='root123')
				stdin, stdout, stdrr = ssh.exec_command('cat /etc/banner')
				result = stdout.read().decode().strip()
				# print(result)
				if 'AccCard' in result:
					print('Find the AccCard')
					try:
						stdin, stdout, stdrr = ssh.exec_command('ru_cmd gettemp')
						temperature = stdout.read().decode().strip()
						temperature = int(temperature.split(':')[-1])
						print('Celsius is', temperature, 'degree')
						acccard = list()
						acccard.append(temperature)
						self.insert_database(time_list, self._ip_parser(), host_name, ip_list[i], 'acc', acccard)
					except:
						pass
					ssh.close()
				elif 'BaiRRU_pRU' in result:
					print('Find the BaiRRU')
					try:
						stdin, stdout, stdrr = ssh.exec_command('ru_cmd p radio')
						temperature = stdout.read().decode().strip()
						temperature = temperature.split('\n')
						bairru_pru = list()
						for show in range(3, 7):
							bairru_pru.append(temperature[show].strip().split(' ')[-4])
						self.insert_database(time_list, self._ip_parser(), host_name, ip_list[i], 'ru', bairru_pru)
					except:
						pass
					ssh.close()
				elif '_pRU' in result:
					print('Find the pRU')
					try:
						stdin, stdout, stdrr = ssh.exec_command('ru_cmd radio antni')
						temperature = stdout.read().decode().strip()
						temperature = temperature.split('|')
						print('RF CH:', temperature[-9-8*3].strip(), ',Temperature:', temperature[-3-8*3].strip())
						print('RF CH:', temperature[-9-8*2].strip(), ',Temperature:', temperature[-3-8*2].strip())
						print('RF CH:', temperature[-9-8*1].strip(), ',Temperature:', temperature[-3-8*1].strip())
						print('RF CH:', temperature[-9].strip(), ',Temperature:', temperature[-3-8*0].strip())
						pru = list()
						pru.append(temperature[-3-8*3].strip())
						pru.append(temperature[-3-8*2].strip())
						pru.append(temperature[-3-8*1].strip())
						pru.append(temperature[-3-8*0].strip())
						self.insert_database(time_list, self._ip_parser(), host_name, ip_list[i], 'ru', pru)
					except:
						pass
					ssh.close()
				else:
					pass
			except:
				print('It\'s NOT the AccCard & BaiRRU.')
				pass
			finally:
				print('SSH is closed.')
				ssh.close()
			# sleep(1)
			try:
				ssh.connect(hostname=ip_list[i], port=22, username='root', password='Baicells@123')
				stdin, stdout, stdrr = ssh.exec_command('cat /etc/release')
				rhub_result = stdout.read().decode().strip()
				print(rhub_result)
				if 'BaiHub' in rhub_result:
					print('Find the BaiHub')
				else:
					pass
			except:
				print('It\'s NOT the rHub.')
				pass
			finally:
				print('SSH is closed.')
				ssh.close()
			# sleep(1)
		sleep(1)

	'''
	IP Address Parser
	'''
	def _ip_parser(self):
		try:
			ip_command = config.get('setting', 'bbu_ip')
			return ip_command
		except:
			return 'Not Found IP'

	'''
	Insert into date to MySQL (phpmyadmin)
	'''
	def insert_database(self, time_list, ip, host_name, acc_ru_ip, name, temperature = []):
		# if name == 'acc':
		# 	print(temperature[:])
		# if name == 'ru':
		# 	print(temperature[0])
		# 	print(temperature[1])
		# 	print(temperature[2])
		# 	print(temperature[3])
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
			if name == 'acc':
				sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, ACC_IP, ACC) VALUES(%s, %s, %s, %s, %s)""".format(table='acc')
				# print(sql, (time_list, ip, host_name, acc_ru_ip, temperature[:]))
				cur.execute(sql, (time_list, ip, host_name, acc_ru_ip, temperature[:]))
			elif name == 'ru':
				sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, RU_IP, RU_0, RU_1, RU_2, RU_3) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""".format(table='ru')
				# print(sql, (time_list, ip, host_name, acc_ru_ip, temperature[0], temperature[1], temperature[2], temperature[3]))
				cur.execute(sql, (time_list, ip, host_name, acc_ru_ip, temperature[0], temperature[1], temperature[2], temperature[3]))
			else:
				pass
			conn.commit()
			print('The information is commit to database.')
		except Exception as e:
			# raise e
			pass

if __name__ == '__main__':
	while True:
		func = ru_acc()
		func._ru_acc_parser()
		sleep(60)