import os, sys, time, datetime
try :
	os.system('pip install -r ..//ini//requirements.txt')
except :
	print('fail to install packages')
sys.path.append('..//lib')
#general setup complete

import configparser
config = configparser.ConfigParser()
config.read('..//ini//config.ini')
az_sql_ip = config['ping']['az_sql_ip']
az_sql_port = config['ping']['az_sql_port']
az_sql_user = config['ping']['az_sql_user']
az_sql_password = config['ping']['az_sql_password']
az_sql_database = config['ping']['az_sql_database']
az_sql_table = config['ping']['az_sql_table']
local_sql_ip = config['ping']['local_sql_ip']
local_sql_port = config['ping']['local_sql_port']
local_sql_user = config['ping']['local_sql_user']
local_sql_password = config['ping']['local_sql_password']
local_sql_database = config['ping']['local_sql_database']
local_sql_table = config['ping']['local_sql_table']
#hostname = config['ping']['host_ip']
#config setup complete


hostname = "google.com" #example

import pymysql
while True :
	try :
		response = os.popen("ping -c 3 " + hostname).read()
		time_=time.strftime("%Y-%m-%d-%H-%M-%S")
		index_=[pos for pos, char in enumerate(response) if char == '/']
		jitter_=response[index_[-1]+1:index_[-1]+6]
		latency_=response[index_[-3]+1:index_[-2]]
	except :
		print('Ping error')

#sql
	try :
		config={'host':f'{az_sql_ip}','port':int(f'{az_sql_port}'),'user':f'{az_sql_user}','password':f'{az_sql_password}','db':f'{az_sql_database}'}
		conn=pymysql.connect(**config)

		cur = conn.cursor()
	except :
		print('sql connect error')
	try :
		sql = """CREATE TABLE {table}(
                         time  datetime,
                         value  DECIMAL(6,2))""".format(table=az_sql_table)
		cur.execute(sql)
	except :
		print('Table exist')

	try :
		sql="""INSERT INTO {table}(time,value)
                 VALUES(%s,%s)
                 """.format(table=az_sql_table)
		cur.execute(sql,(time_,latency_))

		conn.commit()
	except :
		print()


#sql
	try :
		config={'host':f'{local_sql_ip}','port':int(f'{local_sql_port}'),'user':f'{local_sql_user}','password':f'{local_sql_password}','db':f'{local_sql_database}'}
		conn=pymysql.connect(**config)

		cur = conn.cursor()
	except :
		print('sql connect error')
	try :
		sql = """CREATE TABLE {table}(
                         time  datetime,
                         value  DECIMAL(6,2))""".format(table=local_sql_table)
		cur.execute(sql)
	except :
		print('Table exist')

	try :
		sql="""INSERT INTO {table}(time,value)
                 VALUES(%s,%s)
                 """.format(table=local_sql_table)
		cur.execute(sql,(time_,latency_))

		conn.commit()
	except :
		print()

