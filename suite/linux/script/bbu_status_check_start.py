#/usr/bin/python3
'''
Created on 2022/08/25

@author: ZL Chen
@title: BBU status check.
'''

import sys, subprocess
sys.path.insert(0, '/root/automation/suite/linux/lib')
# from gmail_notify import gmail_notify
from line_notify import line_notify
from datetime import datetime

class bbu_check(object):
	def log(self):
		print("BBU is started.")
		self.notify()	

	def notify(self):
		# g_n = gmail_notify()
		l_n = line_notify()
		result = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
		_ip = subprocess.check_output('ip address show enp0s20f0u1 | grep \"inet \" | awk {\'print $2\'}', shell=True)
		ip = str(_ip[0:-4]).split('b')[1]
		print('ip = ' + ip)
		message = 'BBU is started.\n' + 'ip = ' + str(ip) + '\n' + result
		# g_n.gmail('iecsvt5g@gmail.com', 'Chen.ZL@inventec.com, iec100535@gmail.com', message)
		l_n.send_message(message)

if __name__ == '__main__':
	bbu_status_check = bbu_check()
	bbu_status_check.log()
