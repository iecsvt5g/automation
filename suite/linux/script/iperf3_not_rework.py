import os, sys, time, datetime
try :
    os.system('pip install -r .//wl02281915//svt//linux//ini//requirements.txt')
except :
    print('fail to install packages , whyyyyy?')
sys.path.append('.//wl02281915//svt//linux//lib')
#general setup complete

import configparser
#independent setup complete

#script begin
config = configparser.ConfigParser()
config.read('.//wl02281915//svt//linux//ini//config.ini')
IP = config['server']['ip']
SavePlace = config['client']['iperf3_log']

while True:
        if datetime.datetime.now().minute % 1 == 0: 
            
            times = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
            
            result = os.popen(f'iperf3 -c {ip} -u -b 500m -R -J').read()
            
            if 'error' in result :
                with open("{saveplace_}//{time_}".format(time_ = times,saveplace_=saveplace), "w") as f:
                    f.write(result)
                    f.close()
            else:
                with open("{saveplace_}//{time_}.json".format(time_= times,saveplace_=saveplace), "w") as f:
                    f.write(result)
                    f.close()
         
        time.sleep(40)