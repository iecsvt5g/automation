import os, sys, time, datetime
try :
	os.system('pip install -r ..//ini//requirements.txt')
except :
	print('fail to install packages')
sys.path.append('..//lib')
#general setup complete

import configparser
from smb_convert import samba_convert
#independent setup complete

#script begin
config = configparser.ConfigParser()
config.read('.//wl02281915//svt//linux//ini//config.ini')
ip = config['ftp']['ip']
saveplace = config['ftp']['ftp_log']
user=config['ftp']['user']
password=config['ftp']['password']
src_path=config['ftp']['ftp_path']
src_file=config['ftp']['ftp_file']
des_path=config['ftp']['samba_path']
des_file=config['ftp']['samba_file']


while True:
        while True:
            times=time.time()
            os.popen(f'bmon -b -o ascii > {saveplace}//samba.txt')
            time.sleep(10)
            os.system(f'wget -O {des_path}//{des_file}  ftp://{user}:{password}@{ip}//{src_path}//{src_file}')
            time.sleep(10)
            
            sb_t = samba_convert()
            print('Catch the samba.txt...')
            time.sleep(1)
            general_time_string = sb_t.open_file('samba.txt')
            print('\nThe \"samba.txt\" file is converted to \"' + general_time_string + '.log\"')
            os.system(f'rm -rf {saveplace}//*.txt')
            time.sleep(40)
            break