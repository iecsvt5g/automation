#/usr/bin/python3
'''
Created on 2022/02/05

@author: ZL Chen
@title: RU Temperture.
'''

import configparser, sys, time, datetime
sys.path.insert(0, './../lib')
from gmail_notify import gmail_notify
from line_notify import line_notify
from network import ssh
from csv import writer

config = configparser.ConfigParser()
config.read('./../ini/acc_card_temperature_parser.ini')

class acc_parser(object):
	def parser(self, cmd, res):
		count = 0
		content = list()
		while True:
			today_date = str(datetime.date.today()) + '.csv'
			today_now = str(datetime.datetime.now())
			ssh().ssh_command(cmd)
			result, respone_result = ssh().ssh_respone(res)
			respone_result = respone_result.split('b\'')[1].strip()
			respone_result = float(respone_result[:-3])
			with open('../log/' + today_date, 'a+', newline='') as csvfile:
				_writer = writer(csvfile)
				_writer.writerow([today_now, respone_result])
			if respone_result > float(res):
				count += 1
				content.append(respone_result)
				print('Warning, RU Temperture > ' + res + ':', count)
			if count == 5:
				# self.notify(res, content)
				print('RU Temperture list:', content)
				self.notify(res, content)
				break
			time.sleep(int(config.get('setting', 'wait_time')))

	def notify(self, res, content):
		g_n = gmail_notify()
		l_n = line_notify()
		message = '\n\nDear SVT members,\n\nWarning! \
				\nRU Temperture > ' + res \
				+ '\nTemperture list: \n' + str(content) + '\n\nNotification by SVT alert.'
		l_n.send_message(message)
 
if __name__ == '__main__':
	acc_parser = acc_parser()
	while True:
		command = 'ru_cmd gettemp | sed \'s/[a-z]*//g\' | tr -d \':\''
		acc_parser.parser(command, config.get('setting', 'limit_acc'))
		print('Done')
		time.sleep(10)
