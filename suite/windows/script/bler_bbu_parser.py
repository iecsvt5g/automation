'''
Created on 2021/12/25

@author: ZL Chen
@title: BLER BBU parser.
'''

import configparser, sys, time
sys.path.insert(0, '.\..\\lib')
from gmail_notify import gmail_notify
from line_notify import line_notify
from network import ssh

config = configparser.ConfigParser()
config.read('.\..\\ini\\bler_bbu_parser.ini')

class bler_parser(object):
	def parser(self, cmd, res):
		count = 0
		content = list()
		while True:
			ssh().ssh_command(cmd)
			result, respone_result = ssh().ssh_respone(res)
			respone_result = respone_result.split('b\'')[1].strip()
			respone_result = float(respone_result[:-3])
			if respone_result > int(res):
				count += 1
				content.append(respone_result)
				print('Warning, NL BLER > ' + res + ':', count)
				time.sleep(int(config.get('setting', 'wait_time')))
			if count == 5:
				self.notify()
				print('UL BLER list:', content)
				break

	def notify(self):
		g_n = gmail_notify()
		l_n = line_notify()
		message = '\n\nDear SVT members,\n\n\tWarning! \
				\n\tWe are under a attack! \
				\n\t"The SVT NOTIFY is notify by ZL demo.\"\n\nZL.'
		l_n.send_message(message)

if __name__ == '__main__':
	bler_parser = bler_parser()
	while True:
		command = 'cat /home/zl/bler.log | awk \'END{print $(NF-4)}\' | sed \'s/.$//\''
		bler_parser.parser(command, config.get('setting', 'limit_bler'))
		print('Done')
