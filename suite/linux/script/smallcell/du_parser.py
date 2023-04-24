#/usr/bin/python3
'''
Created on 2022/10/04

@author: ZL Chen
@title: DU Parser
'''

from subprocess import check_output
from pymysql import connect
from time import *
from line_notify import line_notify
import re
from configparser import ConfigParser

config = ConfigParser()
config.read('/etc/inventec_svt_deployment_smallcell/setting.ini')

class du(object):
	'''
	Timezone: UTC+8 to UTC
	'''
	def datetime_taiwan_to_utc(self, datetime):
		taiwan_time = strptime(datetime, "%a %b %d %H:%M:%S %Y")
		taiwan_time = mktime(taiwan_time)
		utc_time = taiwan_time - 8 * 60 * 60
		utc_time = localtime(utc_time)
		new_time = strftime('%Y-%m-%d %H:%M:%S', utc_time)
		return new_time
		
	'''
	DU information parser
	'''
	def _du_parser(self):
		with open('/etc/hostname', 'r+') as f:
			host_name = f.readlines()[0].strip()
		# print('hostname:', host_name)
		status_check = 0
		while True:
			status_check += 1
			# print('status_check', status_check)
			if status_check > 999 and int(status_check % 1000) == 0:
				_ip = self._ip_parser()
				line_notify().send_message('\n(Notification)\nIP = ' + _ip + \
					'\nDU parser is NOT found element > ' + str(status_check) + ' times')
				sleep(1)
			cell_tail= 'grep \'cell_idx\' /userdata/DU/bin/' + config.get('du', 'filename') + '| awk \'END{print $(NF)}\''
			# cell_tail = 'grep \'cell_idx\' logs_gNB_DU_155 | awk \'END{print $(NF)}\''
			# cell_tail = 'grep \'cell_idx\' logs_gNB_DU_199 | awk \'END{print $(NF)}\''
			du_tail = 'tail -n 500 /userdata/DU/bin/' + config.get('du', 'filename')
			# du_tail = 'tail -n 500 logs_gNB_DU_155'
			# du_tail = 'tail -n 500 logs_gNB_DU_199'
			try:
				cell_tail = check_output(cell_tail, shell=True).decode('utf-8').strip()
				cell_tail = cell_tail.split('[')[1].split(']')[0]
				cell_tail = int(cell_tail) + 1
				print('Cell number:', cell_tail)
				re_du = check_output(du_tail, shell=True).decode('utf-8').strip()
				# print(re_du, 're_du')

				# contentRex
				find_du_str = ''
				find_du_str = r'Timer:(\D+\d+\D+\d+\D+\d+\D+\d+\D+\d+)\D+RLC  '\
					r'UL traffic :ingress\D{1}(\d+\D+\d+)\D{1} pkt\D{1}(\d+)\D{1} '\
						r'::egress\D{1}(\d+\D+\d+)\D{1} pkt\D{1}(\d+)\D{1} \D+\d+\D+\d+\D+'\
						r'RLC  DL traffic :ingress\D{1}(\d+\D+\d+)\D{1} pkt\D{1}(\d+)\D{1} '\
							r'::egress\D{1}(\d+\D+\d+)\D{1} pkt\D{1}(\d+)\D{1} \D+\d+\D+\d+\D+RLCL  '\
							r'DL traffic um throughput\D{1}(\d+\D+\d+)\D{1} um sche cnt\D+\d+\D+am throughput\D{1}(\d+\D+\d+)\D{1} am sche cnt\D{1}\d+\D{1}\D{1}'
				contentRex = ''
				contentRex = re.findall(find_du_str, re_du)
				print(contentRex, 'find_du_str findall')
				if len(contentRex) == 0:
					print('len(contentRex) == 0')
					break
				for cell_number in range(int(cell_tail)):
					find_du_cell_str = ''
					## 'BBU'
					# find_du_cell_str = r'5GNR SYSTEM OVERVIEW AT\D+\d+\D+\d+\D+\d+\D+' + str(cell_number) + '\D.*\D+.*\D+.*\D+.*'\
					# 		r'CRC_GOOD \D{1}(\d+)\D{1}\D+.*CRC_BAD\D{1}(\d+)\D{1}\D+.*UL_MCS_AVG\D{1}(\d+)\D{1}'\
					# 		r'\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*PUSCH MAX DMRS PWR RBIDX\D+\d+ (\d+)\D+\d+_\d+ (\d+)\D+\d+_\d+ (\d+)\D+\d+_\d+ (\d+)\D+\d+_\d+ (\d+)\D+\d+_\d+ (\d+)\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*'\
					# 			r'ACK\D+(\d+)\D+\D+(\d+)\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*'\
					# 			r'UL: rank1\D{1}(\d+)\D+rank2\D{1}(\d+)\D{1} schedduled layer1\D{1}(\d+)\D{1} layer2\D{1}(\d+)\D{1}'\
					# 				r'\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+macActiveUe\D{1}(\d+)\D{1}\D+.*\D+.*avgPrbAsgnRateDl\D+(\d+)%\D+.*\D+.*avgPrbAsgnRateUl\D+(\d+)%\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+'\
					# 				r'.*\D+.*\D+'\
					# 					r'MAC DL traffic :ingress\D{1}(\d+\D+\d+)\D{1}\D+.*cell_index\D{1}(\d+)\D{1}'
					
					## 'SmallCell'
					find_du_cell_str = r'5GNR SYSTEM OVERVIEW AT\D+\d+\D+\d+\D+\d+\D+' + str(cell_number) + '\D.*\D+.*\D+.*\D+.*'\
										r'\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*\D+.*macActiveUe\D{1}(\d+)\D{1}\D+.*\D+.*\D+.*\D+.*\D+.*'\
										r'CRCGood\D{1}(\d+)\D{1} CRCBad\D{1}(\d+)\D{1}\D+.*NACK\D{1}(\d+)\D{1}\D+.*\D+.*\D+.*'\
											r'MAC DL traffic :ingress\D{1}(\d+\D+\d+)\D{1}\D+.*cell_index\D{1}(\d+)\D{1}'
					# print(find_du_cell_str)
					contentRex_cell = ''
					contentRex_cell = re.findall(find_du_cell_str, re_du)
					print(contentRex_cell)
					if len(contentRex_cell) == 0:
						print('len(contentRex_cell) == 0')
						break
					else:
						# contentRex
						contentRex = contentRex[:]
						print(contentRex, 'contentRex')
						len_contentRex = len(contentRex)-1
						print(len_contentRex, 'len')
						re_contentRex = contentRex[len_contentRex]
						print(re_contentRex, 're_contentRex')

						timerRex = re_contentRex[0]
						print(timerRex, 'timeRex')
						utc_time = self.datetime_taiwan_to_utc(timerRex)
						print(utc_time)
						ip = self._ip_parser()
						print(ip)
						
						# contentRex cell
						new_contentRex_cell = contentRex_cell[:]
						print(new_contentRex_cell, 'contentRex_cell')
						len_contentRex = len(new_contentRex_cell)-1
						print(len_contentRex, 'len')
						re_contentRex_cell = new_contentRex_cell[len_contentRex]
						print(re_contentRex_cell, 're_contentRex_cell')

						# for i in range(1, 11):
						# 	print('contentRex', re_contentRex[i])
						# print('UL traffic ingress', re_contentRex[1])
						# print('UL traffic ingress pkt', re_contentRex[2])
						# print('UL traffic egress', re_contentRex[3])
						# print('UL traffic egress pkt', re_contentRex[4])
						# print('DL traffic ingress', re_contentRex[5])
						# print('DL traffic ingress pkt', re_contentRex[6])
						# print('DL traffic egress', re_contentRex[7])
						# print('DL traffic egress pkt', re_contentRex[8])
						# print('RLCL DL traffic um throughput', re_contentRex[9])
						# print('RLCL DL traffic am throughput', re_contentRex[10])

						# for j in range(6):
						# 	print('re_contentRex_cell', re_contentRex_cell[j])					
						# print('Cell', re_contentRex_cell[5])
						# print('macActiveUe', re_contentRex_cell[0])
						# print('CRC GOOD', re_contentRex_cell[1])
						# print('CRC BAD', re_contentRex_cell[2])
						# print('NACK', re_contentRex_cell[3])
						# print('MAC DL traffic ingress', re_contentRex_cell[4])
						
						self.insert_database(utc_time, ip, host_name, re_contentRex[1], re_contentRex[2], re_contentRex[3], re_contentRex[4], \
							re_contentRex[5], re_contentRex[6], re_contentRex[7], re_contentRex[8], re_contentRex[9], re_contentRex[10], \
							re_contentRex_cell[5], re_contentRex_cell[1], re_contentRex_cell[2], None, None, \
							None, None, None, None, None, \
							None, re_contentRex_cell[3], None, None, None, \
							None, re_contentRex_cell[0], None, None, re_contentRex_cell[4])
		
						# print(utc_time, ip, host_name, re_contentRex[1], re_contentRex[2], re_contentRex[3], re_contentRex[4], \
						# 	re_contentRex[5], re_contentRex[6], re_contentRex[7], re_contentRex[8], re_contentRex[9], re_contentRex[10], \
						# 	re_contentRex_cell[5], re_contentRex_cell[1], re_contentRex_cell[2], None, None, \
						# 	None, None, None, None, None, \
						# 	None, re_contentRex_cell[3], None, None, None, \
						# 	None, re_contentRex_cell[0], None, None, re_contentRex_cell[4])
						print('Insert database is done.')
				break
			except:
				sleep(1)
				# pass
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
	def insert_database(self, datetime, ip, host_name, UL_Ingress, UL_Ingress_PKT, UL_Egress, UL_Egress_PKT, \
			DL_Ingress, DL_Ingress_PKT, DL_Egress, DL_Egress_PKT, RLCL_DL_UM_Throughput, RLCL_DL_AM_Throughput, \
			Cell_number, CRC_GOOD, CRC_BAD, UL_MCS_AVG, PUSCH_PWR_0_45, PUSCH_PWR_45_90, PUSCH_PWR_90_135, \
			PUSCH_PWR_135_180, PUSCH_PWR_180_225, PUSCH_PWR_225_273, ACK, NACK, UL_RANK_1, UL_RANK_2, \
			UL_Scheduled_Layer_1, UL_Scheduled_Layer_2, macActiveUe, avgPrbAsgnRateDl, avgPrbAsgnRateUl, MAC_DL_traffic_ingress):
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
			sql = """INSERT INTO {table}(DateTime , IP, HOST_NAME, UL_Ingress, UL_Ingress_PKT, UL_Egress, UL_Egress_PKT, \
				DL_Ingress, DL_Ingress_PKT, DL_Egress, DL_Egress_PKT, RLCL_DL_UM_Throughput, RLCL_DL_AM_Throughput, \
				Cell_number, CRC_GOOD, CRC_BAD, UL_MCS_AVG, PUSCH_PWR_0_45, PUSCH_PWR_45_90, PUSCH_PWR_90_135, \
				PUSCH_PWR_135_180, PUSCH_PWR_180_225, PUSCH_PWR_225_273, ACK, NACK, UL_RANK_1, UL_RANK_2, \
				UL_Scheduled_Layer_1, UL_Scheduled_Layer_2, macActiveUe, avgPrbAsgnRateDl, avgPrbAsgnRateUl, MAC_DL_traffic_ingress) \
			VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table='du')
			# print(sql)
			print('SQL print done.')
			cur.execute(sql, (datetime, ip, host_name, UL_Ingress, UL_Ingress_PKT, UL_Egress, UL_Egress_PKT, \
				DL_Ingress, DL_Ingress_PKT, DL_Egress, DL_Egress_PKT, RLCL_DL_UM_Throughput, RLCL_DL_AM_Throughput, \
				Cell_number, CRC_GOOD, CRC_BAD, UL_MCS_AVG, PUSCH_PWR_0_45, PUSCH_PWR_45_90, PUSCH_PWR_90_135, \
				PUSCH_PWR_135_180, PUSCH_PWR_180_225, PUSCH_PWR_225_273, ACK, NACK, UL_RANK_1, UL_RANK_2, \
				UL_Scheduled_Layer_1, UL_Scheduled_Layer_2, macActiveUe, avgPrbAsgnRateDl, avgPrbAsgnRateUl, MAC_DL_traffic_ingress))
			print('SQL execute done.')
			conn.commit()
			print('The information is commit to database.')
		except Exception as e:
			# raise e
			pass
		finally:
			print('Connection is closed.')
			conn.close()

if __name__ == '__main__':
	while True:
		func = du()
		func._du_parser()
		sleep(6)