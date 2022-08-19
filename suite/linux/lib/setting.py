#/usr/bin/python3
'''
Created on 2022/08/18

@author: ZL Chen
@title: The configparser lib.
'''

#acc_card_temperature_parser.ini
limit_acc = '40.0'
wait_time = '5'

#acc_cpu_fan.ini
fanmax = '64'
fanmin = '32'
fanstart = '64'
fanup = '2'
fandown = '1'
monitortime = '10'
recordtime = '60'
tempmax = '46'
tempmin = '44'
local_ip = '172.32.3.164'
az_sql_ip = '20.212.112.202'
az_sql_port = '3306'
az_sql_user = 'TAO'
az_sql_password = 'admin'
az_sql_database = 'test'
az_sql_table_cpu_acc_fan = 'acc_cpu_fan'

#bler_bbu_parser.ini
limit_bler = '50'
wait_time = '5'

#network.ini
host = '172.20.10.3'
name = 'zl'
passwd = 'zl'
port = '22'

#reboot_script.ini
passwd = 'zl'
times = '5'
waittime = '120'
interface = 'enp0s3'
response_ip = '172.20.10.3/28'