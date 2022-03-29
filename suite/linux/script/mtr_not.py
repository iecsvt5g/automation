import os, sys, time, datetime
try :
	os.system('pip install -r ..//ini//requirements.txt')
except :
	print('fail to install packages')
sys.path.append('..//lib')
#general setup complete

import configparser
config = configparser.ConfigParser()
ip = config['mtr']['ip']
saveplace = config['mtr']['mtr_log']

while True:

    if datetime.datetime.now().minute % 1 == 0: 
            
        times=time.strftime("%Y-%m-%d-%H-%M", time.localtime())
            
        result=os.popen(f'mtr -n -4 -r -c 30 --csv {ip} > {saveplace}//{times}.csv').read()
    
        time.sleep(40)
