#/usr/bin/python3
'''
Created on 2022/08/31

@author: ZL Chen
@title: Influx Database
'''

from os import stat
import sys
sys.path.insert(0, '/root/automation/suite/linux/lib')
from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep
import random

class infulx_db(object):
	def __init__(self, ip='localhost', port=8086, user="admin", password="admin", db="influx"):
		self.client=InfluxDBClient(ip, port, user, password, db)
		self.client.switch_database(db)

	def write(self,json_payload):
		self.client.write_points(json_payload)

	def gen_data():
		json_payload=[]
		for i in range(5):
			for j in ['gnbs','pdu_sessions','throuphput','critcal_alert','major_alert','minor_alert','reg_devices']:
				d= {
					"measurement": "core_alert",
					"tags": {
						"core_ip": "172.32.3.203",
						"vendor":"metaswitch",
						'info': j
					},
					"time": datetime.now(),
					"fields": { 'value': random.randint(1,10)  }
				}
				sleep(0.1)
				json_payload.append(d)
				print(d)
		return json_payload

	def gen_data2():
		json_payload=[]
		for i in range(10):
			d= {
				"measurement": "core_alert",
				"tags": {
					"core_ip": "172.32.3.203",
					"vendor":"metaswitch",
				},
	#           "time": datetime.now(),
				"fields": {
					'gnbs': random.randint(1,10),
					'pdu_sessions': random.randint(1,10),
					'throuphput': random.randint(1,100),
					'reg_devices': random.randint(1,10),
					'critcal_alert': random.randint(1,10),
					'major_alert': random.randint(1,10),
					'minor_alert': random.randint(1,10),
				}
			}
			sleep(0.2)
			json_payload.append(d)
			print(d)
		return json_payload
		#client.write_points(gen_data2())
		#client.write_points(gen_data())

	def get_bbu_status(bbu_status):
		json_payload = list()
		for i in range(1):
			status = {
				"measurement": "bbu_alert",
				"tags": {
					"bbu_ip": "172.32.3.155",
					"vendor":"BaiCells",
				},
			#   "time": datetime.now(),
				"fields": {
					# 'gnbs': random.randint(1,10),
					# 'pdu_sessions': random.randint(1,10),
					# 'throuphput': random.randint(1,100),
					# 'reg_devices': random.randint(1,10),
					# 'critcal_alert': random.randint(1,10),
					# 'major_alert': random.randint(1,10),
					# 'minor_alert': random.randint(1,10),
					# 'bbu_status': random.randint(0, 1)
					'bbu_status': bbu_status
				}
			}
			sleep(0.2)
			json_payload.append(status)
			print(status)
		return json_payload

if __name__ == '__main__':
	mydb = infulx_db("172.32.3.196", 8086, 'admin', 'admin', 'influx')
	mydb.write(infulx_db.get_bbu_status(0))