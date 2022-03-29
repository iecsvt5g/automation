import os, sys, time, datetime
try :
    os.system('pip install -r .//wl02281915//svt//linux//ini//requirements.txt')
except :
    print('fail to install packages , whyyyyy?')
sys.path.append('.//wl02281915//svt//linux//lib')
#general setup complete

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#independent setup complete


#script begin
reboot_count={'count':0}
ip_count={'count':0}

try:
    driver_locate=ChromeDriverManager().install()
except:
    print('No internet connect')

for i in range(1,1000+1):
    driver = webdriver.Chrome(driver_locate)
    driver.get('http://192.168.150.1')
    time.sleep(20)
    
    element = driver.find_element_by_class_name('cbi-input-user')
    element.send_keys('admin')
    element = driver.find_element_by_class_name('cbi-input-password')
    element.send_keys('admin')
    button = driver.find_element_by_class_name('cbi-button.cbi-button-apply')
    button.click()

    time.sleep(20)
    ip=driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div/fieldset[4]/fieldset/table/tbody/tr[2]/td[5]').text
    ip_count['count'] = ip_count['count'] + ip.count('10.0.2')
    reboot_count['count'] = reboot_count['count'] + 1
    link=driver.find_element_by_xpath('/html/body/div/div[2]/ul/li[6]/ul/li[10]/a').get_attribute('href')
    driver.get(link)
    time.sleep(20)
    
    link=driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div/p/a').get_attribute('href')
    driver.get(link)
    print('reboot {} times and get ip {} times'.format(reboot_count['count'],ip_count['count']))
    driver.close()
    time.sleep(560)


