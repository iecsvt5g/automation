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
bbu_ip = config['ping']['target_ip']
bbu_user = config['ping']['target_user']
bbu_password = config['ping']['target_password']
csv_place = config['bler']['csv_place']
sql_ip = config['bler']['az_sql_ip']
sql_port = config['bler']['az_sql_port']
sql_user = config['bler']['az_sql_user']
sql_password = config['bler']['az_sql_password']
sql_database = config['bler']['az_sql_database']
sql_table = config['bler']['az_sql_table']
#config setup complete


import csv, pymysql

time_alarm = time.time()

while True:
        try :
                time_=time.strftime("%Y-%m-%d-%H-%M-%S")
                os.popen(f"sshpass -p {bbu_password} ssh {bbu_user}@{bbu_ip} 'bash -s' < ..//subroutine//create_data.sh")
                time.sleep(5)
                os.popen(f"sshpass -p {bbu_password} ssh {bbu_user}@{bbu_ip}:/root/bler_test.txt bler_test.txt")
                time.sleep(5)
                txt_=open('bler_test.txt', 'r').read()
                if 'BLER' in txt_ :
                        list_=list(txt_[txt_.find('%')-6:txt_.find('%')].replace(' ','0'))
                        value_=int(list_[0])*100+int(list_[1])*10+int(list_[2])*1+int(list_[4])*0.1+int(list_[5])*0.01
                        with open(f'{csv_place}//{time.strftime("%Y-%m-%d")}.csv', 'at', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([time_,value_])
                                csvfile.close
                        print('success and do not close it')
                else :
                        print('BBU fail')
                        value_=None
                os.remove('bler_test.txt')
        except :
                print('error and do not close it')
                value_=None

        if value_ % 1 != 0 :
                print('BBU error')
                sleep(8)
        if value_ == 100:
                #gmail_notify().gmail('iecsvt5g@gmail.com', 'iecsvt5g@gmail.com', 'BBU is dead!!!!!')
                ms = 'BBU is dead!!!!!\n\n The UL BLER is ' + str(value_)
                line_notify().send_message(ms)
                print(time.strftime("%Y-%m-%d-%H-%M-%S"))
        if value_ < 85:
                print('The UL BLER is ' + str(value_))
                pass
        if value_ >= 85 and value_ < 100:
                alarm_['count'] = alarm_['count'] + 1
        if alarm_['count'] == 10 and (time.time()-time_alarm) > 300  :
                time_alarm = time.time()
                #gmail_notify().gmail('iecsvt5g@gmail.com', 'iecsvt5g@gmail.com', 'BBU is dying(5 times BLER > 85%)')
                line_notify().send_message('BBU is dying(10 times BLER > 85%) \
                                                                \n\nThe BBU UL BLER is ' + str(value_))
                alarm_={'count':0}
                

#sql
        try :
                config={'host':f'{sql_ip}','port':f'{sql_port}','user':f'{sql_user}','password':f'{sql_password}','db':f'{sql_database}'}
                conn=pymysql.connect(**config)

                cur = conn.cursor()
        except :
                print('sql connect error')
        try :
                sql = """CREATE TABLE {table}(
                         time  datetime,
                         value  DECIMAL(6,2))""".format(table=sql_table)
                cur.execute(sql)
        except :
                print('Table exist')

        try :
                sql="""INSERT INTO {table}(time,value)
                 VALUES(%s,%s)
                 """.format(table=sql_table)
                cur.execute(sql,(time_,value_))

                conn.commit()
        except :
                print()

