#/usr/bin/python3
'''
Created on 2021/10/02

@author: ZL Chen
@title: Sent the line notify.
'''

import requests

class line_notify(object):
		
	def send_message(self, message):
		headers = {
			'Authorization': 'Bearer ' + 'F3gpivGNwmcRvILJCslMdEVlUHdfFvPKBtib03kJKnT', # SVT
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		params = {'message': message}
		requests.post('https://notify-api.line.me/api/notify', headers=headers, params=params)
		# r = requests.post('https://notify-api.line.me/api/notify', headers=headers, params=params)
		# print('Send Line Message ', r.status_code)  #200
		
if __name__ == '__main__':
	l_n = line_notify()
	message = '\n\nDear SVT members,\n\n\tWarning! \
			\n\tWe are under a attack! \
			\n\t"The SVT NOTIFY is notify by ZL demo.\"\n\nZL.'
	l_n.send_message(message)