#/usr/bin/python3
'''
Created on 2023/03/16

@author: ZL Chen
@title: RU & rHub & AccCard Temperature
'''

from pymysql import connect
from time import *
from line_notify import line_notify
import paramiko, os, configparser

config = configparser.ConfigParser()
config.read('/etc/inventec_svt_deployment/setting.ini')
line = line_notify()

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
	def _ru_acc_parser(self, acc_n, acc_warn_n, acc_critical_n, \
				pru_n_0, pru_warn_n_0, pru_critical_n_0, \
				pru_n_1, pru_warn_n_1, pru_critical_n_1, \
				pru_n_2, pru_warn_n_2, pru_critical_n_2, \
				pru_n_3, pru_warn_n_3, pru_critical_n_3, \
				bairru_n_0, bairru_warn_n_0, bairru_critical_n_0, \
				bairru_n_1, bairru_warn_n_1, bairru_critical_n_1, \
				bairru_n_2, bairru_warn_n_2, bairru_critical_n_2, \
				bairru_n_3, bairru_warn_n_3, bairru_critical_n_3):
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
						if acc_n > 0 and int(temperature) <= int(config.get('ru_acc', 'temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nAccCard Temperature: ' + str(temperature))
							acc_n = 0
						if int(temperature) > int(config.get('ru_acc', 'temperature_warning')) and int(temperature) <= int(config.get('ru_acc', 'temperature_critical')):
							acc_critical_n = 0
							if acc_n != acc_warn_n:
								acc_n = 0
								acc_warn_n = 0
							if acc_warn_n == 0 or (acc_warn_n + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nAccCard Temperature: ' + str(temperature) + ' > ' + config.get('ru_acc', 'temperature_warning'))
							acc_n += 1
							acc_warn_n = acc_n
						elif int(temperature) > int(config.get('ru_acc', 'temperature_critical')):
							acc_warn_n = 0
							if acc_n != acc_critical_n:
								acc_n = 0
								acc_critical_n = 0
							if (acc_critical_n + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nAccCard Temperature: ' + str(temperature) + ' > ' + config.get('ru_acc', 'temperature_critical'))
							else:
								pass
							acc_n += 1
							acc_critical_n = acc_n
						else:
							pass
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
						# RU0
						if bairru_n_0 > 0 and int(bairru_pru[0]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU0 Temperature: ' + str(bairru_pru[0]))
							bairru_n_0 = 0
						if int(bairru_pru[0]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(bairru_pru[0]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_critical_n_0 = 0
							if bairru_n_0 != bairru_warn_n_0:
								bairru_n_0 = 0
								bairru_warn_n_0 = 0
							if bairru_warn_n_0 == 0 or (bairru_warn_n_0 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU0 Temperature: ' + str(bairru_pru[0]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							bairru_n_0 += 1
							bairru_warn_n_0 = bairru_n_0
						elif int(bairru_pru[0]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_warn_n_0 = 0
							if bairru_n_0 != bairru_critical_n_0:
								bairru_n_0 = 0
								bairru_critical_n_0 = 0
							if (bairru_critical_n_0 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU0 Temperature: ' + str(bairru_pru[0]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							bairru_n_0 += 1
							bairru_critical_n_0 = bairru_n_0
						else:
							pass
						# RU1
						if bairru_n_1 > 0 and int(bairru_pru[1]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU1 Temperature: ' + str(bairru_pru[1]))
							bairru_n_1 = 0
						if int(bairru_pru[1]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(bairru_pru[1]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_critical_n_1 = 0
							if bairru_n_1 != bairru_warn_n_1:
								bairru_n_1 = 0
								bairru_warn_n_1 = 0
							if bairru_warn_n_1 == 0 or (bairru_warn_n_1 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU1 Temperature: ' + str(bairru_pru[1]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							bairru_n_1 += 1
							bairru_warn_n_1 = bairru_n_1
						elif int(bairru_pru[1]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_warn_n_1 = 0
							if bairru_n_1 != bairru_critical_n_1:
								bairru_n_1 = 0
								bairru_critical_n_1 = 0
							if (bairru_critical_n_1 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU1 Temperature: ' + str(bairru_pru[1]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							bairru_n_1 += 1
							bairru_critical_n_1 = bairru_n_1
						else:
							pass
						# RU2
						if bairru_n_2 > 0 and int(bairru_pru[2]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU2 Temperature: ' + str(bairru_pru[2]))
							bairru_n_2 = 0
						if int(bairru_pru[2]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(bairru_pru[2]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_critical_n_2 = 0
							if bairru_n_2 != bairru_warn_n_2:
								bairru_n_2 = 0
								bairru_warn_n_2 = 0
							if bairru_warn_n_2 == 0 or (bairru_warn_n_2 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU2 Temperature: ' + str(bairru_pru[2]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							bairru_n_2 += 1
							bairru_warn_n_2 = bairru_n_2
						elif int(bairru_pru[2]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_warn_n_2 = 0
							if bairru_n_2 != bairru_critical_n_2:
								bairru_n_2 = 0
								bairru_critical_n_2 = 0
							if (bairru_critical_n_2 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU2 Temperature: ' + str(bairru_pru[2]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							bairru_n_2 += 1
							bairru_critical_n_2 = bairru_n_2
						else:
							pass
						# RU3
						if bairru_n_3 > 0 and int(bairru_pru[3]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU3 Temperature: ' + str(bairru_pru[3]))
							bairru_n_3 = 0
						if int(bairru_pru[3]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(bairru_pru[3]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_critical_n_3 = 0
							if bairru_n_3 != bairru_warn_n_3:
								bairru_n_3 = 0
								bairru_warn_n_3 = 0
							if bairru_warn_n_3 == 0 or (bairru_warn_n_3 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU3 Temperature: ' + str(bairru_pru[3]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							bairru_n_3 += 1
							bairru_warn_n_3 = bairru_n_3
						elif int(bairru_pru[3]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							bairru_warn_n_3 = 0
							if bairru_n_3 != bairru_critical_n_3:
								bairru_n_3 = 0
								bairru_critical_n_3 = 0
							if (bairru_critical_n_3 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU3 Temperature: ' + str(bairru_pru[3]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							bairru_n_3 += 1
							bairru_critical_n_3 = bairru_n_3
						else:
							pass
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
						print(pru[0], pru[1], pru[2], pru[3])
						# RU0
						if pru_n_0 > 0 and int(pru[0]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU0 Temperature: ' + str(pru[0]))
							pru_n_0 = 0
						if int(pru[0]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(pru[0]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_critical_n_0 = 0
							if pru_n_0 != pru_warn_n_0:
								pru_n_0 = 0
								pru_warn_n_0 = 0
							if pru_warn_n_0 == 0 or (pru_warn_n_0 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU0 Temperature: ' + str(pru[0]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							pru_n_0 += 1
							pru_warn_n_0 = pru_n_0
						elif int(pru[0]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_warn_n_0 = 0
							if pru_n_0 != pru_critical_n_0:
								pru_n_0 = 0
								pru_critical_n_0 = 0
							if (pru_critical_n_0 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU0 Temperature: ' + str(pru[0]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							pru_n_0 += 1
							pru_critical_n_0 = pru_n_0
						else:
							pass
						# RU1
						if pru_n_1 > 0 and int(pru[1]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU1 Temperature: ' + str(pru[1]))
							pru_n_1 = 0
						if int(pru[1]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(pru[1]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_critical_n_1 = 0
							if pru_n_1 != pru_warn_n_1:
								pru_n_1 = 0
								pru_warn_n_1 = 0
							if pru_warn_n_1 == 0 or (pru_warn_n_1 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU1 Temperature: ' + str(pru[1]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							pru_n_1 += 1
							pru_warn_n_1 = pru_n_1
						elif int(pru[1]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_warn_n_1 = 0
							if pru_n_1 != pru_critical_n_1:
								pru_n_1 = 0
								pru_critical_n_1 = 0
							if (pru_critical_n_1 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU1 Temperature: ' + str(pru[1]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							pru_n_1 += 1
							pru_critical_n_1 = pru_n_1
						else:
							pass
						# RU2
						if pru_n_2 > 0 and int(pru[2]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU2 Temperature: ' + str(pru[2]))
							pru_n_2 = 0
						if int(pru[2]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(pru[2]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_critical_n_2 = 0
							if pru_n_2 != pru_warn_n_2:
								pru_n_2 = 0
								pru_warn_n_2 = 0
							if pru_warn_n_2 == 0 or (pru_warn_n_2 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU2 Temperature: ' + str(pru[2]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							pru_n_2 += 1
							pru_warn_n_2 = pru_n_2
						elif int(pru[2]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_warn_n_2 = 0
							if pru_n_2 != pru_critical_n_2:
								pru_n_2 = 0
								pru_critical_n_2 = 0
							if (pru_critical_n_2 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU2 Temperature: ' + str(pru[2]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							pru_n_2 += 1
							pru_critical_n_2 = pru_n_2
						else:
							pass
						# RU3
						if pru_n_3 > 0 and int(pru[3]) <= int(config.get('ru_acc', 'pru_temperature_warning')):
							line.send_message('\nInfo.\nIP: ' + host_name + '\nRU3 Temperature: ' + str(pru[3]))
							pru_n_3 = 0
						if int(pru[3]) > int(config.get('ru_acc', 'pru_temperature_warning')) and int(pru[3]) <= int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_critical_n_3 = 0
							if pru_n_3 != pru_warn_n_3:
								pru_n_3 = 0
								pru_warn_n_3 = 0
							if pru_warn_n_3 == 0 or (pru_warn_n_3 + 1) % 30 == 0:
								line.send_message('\nWarning.\nIP: ' + host_name + '\nRU3 Temperature: ' + str(pru[3]) + ' > ' + config.get('ru_acc', 'pru_temperature_warning'))
							pru_n_3 += 1
							pru_warn_n_3 = pru_n_3
						elif int(pru[3]) > int(config.get('ru_acc', 'pru_temperature_critical')):
							pru_warn_n_3 = 0
							if pru_n_3 != pru_critical_n_3:
								pru_n_3 = 0
								pru_critical_n_3 = 0
							if (pru_critical_n_3 + 1) > 0:
								line.send_message('\nCritical.\nIP: ' + host_name + '\nRU3 Temperature: ' + str(pru[3]) + ' > ' + config.get('ru_acc', 'pru_temperature_critical'))
							else:
								pass
							pru_n_3 += 1
							pru_critical_n_3 = pru_n_3
						else:
							pass

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
				rhub_user = config.get('ru_acc', 'user')
				rhub_passwd = config.get('ru_acc', 'passwd')
				ssh.connect(hostname=ip_list[i], port=22, username=rhub_user, password=rhub_passwd)
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
		return  acc_n, acc_warn_n, acc_critical_n, \
				pru_n_0, pru_warn_n_0, pru_critical_n_0, pru_n_1, pru_warn_n_1, pru_critical_n_1, \
				pru_n_2, pru_warn_n_2, pru_critical_n_2, pru_n_3, pru_warn_n_3, pru_critical_n_3, \
				bairru_n_0, bairru_warn_n_0, bairru_critical_n_0, bairru_n_1, bairru_warn_n_1, bairru_critical_n_1, \
				bairru_n_2, bairru_warn_n_2, bairru_critical_n_2, bairru_n_3, bairru_warn_n_3, bairru_critical_n_3

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
	acc_n = 0
	acc_warn_n = 0
	acc_critical_n = 0
	pru_n_0 = 0
	pru_warn_n_0 = 0
	pru_critical_n_0 = 0
	pru_n_1 = 0
	pru_warn_n_1 = 0
	pru_critical_n_1 = 0
	pru_n_2 = 0
	pru_warn_n_2 = 0
	pru_critical_n_2 = 0
	pru_n_3 = 0
	pru_warn_n_3 = 0
	pru_critical_n_3 = 0
	bairru_n_0 = 0
	bairru_warn_n_0 = 0
	bairru_critical_n_0 = 0
	bairru_n_1 = 0
	bairru_warn_n_1 = 0
	bairru_critical_n_1 = 0
	bairru_n_2 = 0
	bairru_warn_n_2 = 0
	bairru_critical_n_2 = 0
	bairru_n_3 = 0
	bairru_warn_n_3 = 0
	bairru_critical_n_3 = 0
	while True:
		# input_number0 = input()
		# input_number1 = input()
		# input_number2 = input()
		# input_number3 = input()
		# input_number = []
		# input_number.append(input_number0)
		# input_number.append(input_number1)
		# input_number.append(input_number2)
		# input_number.append(input_number3)
		func = ru_acc()
		acc_n, acc_warn_n, acc_critical_n, \
		pru_n_0, pru_warn_n_0, pru_critical_n_0, \
		pru_n_1, pru_warn_n_1, pru_critical_n_1, \
		pru_n_2, pru_warn_n_2, pru_critical_n_2, \
		pru_n_3, pru_warn_n_3, pru_critical_n_3, \
		bairru_n_0, bairru_warn_n_0, bairru_critical_n_0, \
		bairru_n_1, bairru_warn_n_1, bairru_critical_n_1, \
		bairru_n_2, bairru_warn_n_2, bairru_critical_n_2, \
		bairru_n_3, bairru_warn_n_3, bairru_critical_n_3 \
			= func._ru_acc_parser(acc_n, acc_warn_n, acc_critical_n, \
				pru_n_0, pru_warn_n_0, pru_critical_n_0, \
				pru_n_1, pru_warn_n_1, pru_critical_n_1, \
				pru_n_2, pru_warn_n_2, pru_critical_n_2, \
				pru_n_3, pru_warn_n_3, pru_critical_n_3, \
				bairru_n_0, bairru_warn_n_0, bairru_critical_n_0, \
				bairru_n_1, bairru_warn_n_1, bairru_critical_n_1, \
				bairru_n_2, bairru_warn_n_2, bairru_critical_n_2, \
				bairru_n_3, bairru_warn_n_3, bairru_critical_n_3)
		# print(acc_n, acc_warn_n, acc_critical_n, \
		# 		pru_n_0, pru_warn_n_0, pru_critical_n_0, \
		# 		pru_n_1, pru_warn_n_1, pru_critical_n_1, \
		# 		pru_n_2, pru_warn_n_2, pru_critical_n_2, \
		# 		pru_n_3, pru_warn_n_3, pru_critical_n_3, \
		# 		bairru_n_0, bairru_warn_n_0, bairru_critical_n_0, \
		# 		bairru_n_1, bairru_warn_n_1, bairru_critical_n_1, \
		# 		bairru_n_2, bairru_warn_n_2, bairru_critical_n_2, \
		# 		bairru_n_3, bairru_warn_n_3, bairru_critical_n_3)
		sleep(60)