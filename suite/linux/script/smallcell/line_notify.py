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
			'Authorization': 'Bearer ' + 'qJQeg65a8eQBfnXwZbZUb6539PN1c3cXrFvfgxxkXz7', # SVT Group Notification
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		params = {'message': message}
		requests.post('https://notify-api.line.me/api/notify', headers=headers, params=params, verify=False)