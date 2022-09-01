#/usr/bin/python3
'''
Created on 2022/09/01

@author: ZL Chen
@title: PHY BLER Parser
'''
import sys
sys.path.insert(0, '../lib')
import subprocess
from influx_db import infulx_db
from time import sleep

class bler_parser(object):
	def parser(self):
		parser_cli_0 = 'grep \"0 (Kbps)\" /home/BaiBBU_XSS/BaiBBU_PXSS/PHY/bin/Phy.log | awk \'END{print $(NF-4)}\' | sed \'s/.$//\''
		parser_cli_1 = 'grep \"1 (Kbps)\" /home/BaiBBU_XSS/BaiBBU_PXSS/PHY/bin/Phy.log | awk \'END{print $(NF-4)}\' | sed \'s/.$//\''
		parser_response_0 = str(subprocess.check_output(parser_cli_0, shell=True)).split('b\'')[1]
		parser_response_1 = str(subprocess.check_output(parser_cli_1, shell=True)).split('b\'')[1]
		parser_response_0 = float(parser_response_0[0:-3])
		parser_response_1 = float(parser_response_1[0:-3])
		return parser_response_0, parser_response_1

if __name__ == '__main__':
	bler = bler_parser()
	while True:
		r_0, r_1 = bler.parser()
		mydb = infulx_db("172.32.3.196", 8086, 'admin', 'admin', 'influx')
		mydb.write(infulx_db.get_phy_bler(r_0, r_1))
		sleep(0.5)