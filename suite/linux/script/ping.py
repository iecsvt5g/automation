try :
	import os, sys, time, datetime, configparser,pymysql,subprocess
except:
	print('Package error. Please Run Install_Package.py First')

# sys.path.append('../lib')
from line_notify import line_notify



#config setup 
config = configparser.ConfigParser()
config.read('/etc/inventec_svt_deployment/setting.ini')
local_sql_ip = config['ping']['local_sql_ip']
local_sql_port = config['ping']['local_sql_port']
local_sql_user = config['ping']['local_sql_user']
local_sql_password = config['ping']['local_sql_password']
local_sql_database = config['ping']['local_sql_database']
local_sql_table = config['ping']['local_sql_table']
ip_list = config['ping']['host_ip']
ip_list=ip_list.split(',')

dead_time=dict()
for hostname in ip_list:
    dead_time[f'{hostname}']=[]

#ping
while 2 > 1 :
	for hostname in ip_list:
		print(hostname)
		#response = os.popen("ping -c 3 -l 3 " + hostname).read()
		os.popen(f'rm -f {hostname}.txt')
		time.sleep(1)
		subprocess.Popen(f"ping -c 3 -l 3 {hostname} > {hostname}.txt" , shell = True )

	time.sleep(5)

	for hostname in ip_list:	
		try :
			time_record=time.strftime("%Y-%m-%d %H:%M:%S")
			time_counter=time.time()
			response = open(f'{hostname}.txt', 'r').read()
			index_=[pos for pos, char in enumerate(response) if char == '/']
			jitter_=response[index_[-1]+1:index_[-1]+6]
			latency_=response[index_[-3]+1:index_[-2]]
			flag=True
		except :
			print(f'Ping Error {hostname}')
			flag=False
	#sql
		#connect
		if flag :
			try :
				config={'host':f'{local_sql_ip}','port':int(f'{local_sql_port}'),'user':f'{local_sql_user}','password':f'{local_sql_password}','db':f'{local_sql_database}'}
				conn=pymysql.connect(**config)

				cur = conn.cursor()
			except :
				print('sql connect error')
		
			try :
				sql = """CREATE TABLE {table}(
								time  datetime,
								target varchar(255),
								ping  DECIMAL(6,2),
								jitter DECIMAL(6,2))""".format(table=local_sql_table)
				cur.execute(sql)
			except :
				print('Table exist')

			try :
				sql="""INSERT INTO {table}(time,target,ping,jitter)
						VALUES(%s,%s,%s,%s)
						""".format(table=local_sql_table)
				cur.execute(sql,(time_record,hostname.replace('\'',''),latency_,jitter_))

				conn.commit()
			except :
				print()
		else :
			print('nooo')
			if len(dead_time[f'{hostname}']) == 0 :
				dead_time[f'{hostname}']=[time_counter]
				line_notify().send_message(f'\nPing Fail : {hostname} \nTime : {time_record}')
			else :
				if time.time() - dead_time[f'{hostname}'][-1] > 7200 :
					dead_time[f'{hostname}']=[time_counter]
					line_notify().send_message(f'\nPing Fail : {hostname} \nTime : {time_record}')
					print(dead_time)