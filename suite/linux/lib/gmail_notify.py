#/usr/bin/python3
'''
Created on 2021/10/02
Modified on 2022/02/05

@author: ZL Chen
@title: Sent the email notify.
'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class gmail_notify(object):	
	def gmail(self, sent_email, receive_email, content):  
		self.content = MIMEMultipart()  # Created on MIMEMultipart OO
		self.content['subject'] = 'Warning!'  # Mail title
		self.content['from'] = sent_email  # Sender
		self.content['to'] = receive_email # Receiver
		self.content.attach(MIMEText(content))  # Mail content
		self.smtplib_smtp()

	def smtplib_smtp(self):
		with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:  # Set the SMTP Server
			try:
				smtp.ehlo()  # Verify the SMTP Server
				smtp.starttls()  # Build the SSL
				smtp.login(self.content['from'], 'pcsctakjcqgrcmgr')  # Login the sender mail
				smtp.send_message(self.content)  # Send the mail
				print('Complete!')
			except Exception as e:
				print('Error message: ', e)
	
# if __name__ == "__main__":
# 	g_n = gmail_notify()
# 	g_n.gmail('iecsvt5g.family@gmail.com', 'Chen.ZL@inventec.com, iec100535@gmail.com, iecsvt5g@gmail.com, iecsvt5g.family@gmail.com',
# 				'\n\nDear SVT members,\n\n\tWarning! \
# 				\n\tWe are under a attack! \
# 				\n\t"The SVT NOTIFY is notify by ZL demo.\"\n\nZL.')