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
ip = config['samba']['ip']
saveplace = config['samba']['samba_log']
user=config['samba']['user']
password=config['samba']['password']
src_path=config['samba']['src_path']
src_file=config['samba']['src_file']
des_path=config['samba']['des_path']
des_file=config['samba']['des_file']

while True:
    while True:
        times=time.time()
        os.popen(f'bmon -b -o ascii > {des_path}//samba.txt')
        time.sleep(5)
        os.system(f'smbget -r -b 90000000 -U {user}%{password} smb://{ip}//{src_path}//{src_file} -o {des_path}//{des_file}')
        time.sleep(5)
        sb_t = samba_convert()
        print('Catch the samba.txt...')
        time.sleep(1)
        general_time_string = sb_t.open_file('{des_path}//samba.txt')
        print('\nThe \"samba.txt\" file is converted to \"' + general_time_string + '.log\"')
        os.system(f'rm -rf {des_path}//*.txt')
        time.sleep(40)
        os.system(f'rm -rf {des_path}//*.iso')
        break