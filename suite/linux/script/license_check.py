#/usr/bin/python3
'''
Created on 2022/05/04

@author: ZL Chen
@title: BaiCell license check.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from sys import path
path.insert(0, '.\..\\lib')
from line_notify import line_notify

class bbu_license_check(object):
	def setup(self):
		self.driver = webdriver.Chrome('chromedriver')
		self.line_notify = line_notify()

	def remain_time_parser(self):
		url = 'http://172.32.3.155/'
		self.driver.get(url)
		self.driver.maximize_window()
		self.driver.refresh()
		print('Open the Baicells website.')
		try:
			username = self.element_get(By.ID, 'username')
			username.send_keys('admin')
			password = self.element_get(By.ID, 'password')
			password.send_keys('admin')
			self.element_get(By.CSS_SELECTOR, 
				'#loginVue > div:nth-child(2) > form > div > div.el-card__body > div:nth-child(4) > div > button').click()
			self.driver.implicitly_wait(10)
			self.element_get(By.CSS_SELECTOR, '#myMenu > ul > li:nth-child(4) > div > span').click()
			sleep(2)
			self.element_get(By.CSS_SELECTOR, '#license').click()
			sleep(2)
			license_generatedate_name = self.element_get(By.XPATH, '//*[@id="licenseVue"]/form/div[1]/section/div[2]/div[4]/label').text
			license_generatedate = self.element_get(By.XPATH, '//*[@id="licenseVue"]/form/div[1]/section/div[2]/div[4]/div/span').text
			remain_time_name = self.element_get(By.XPATH, '//*[@id="firstContent"]/div[2]/div/div[2]/div[2]/table/thead/tr/th[4]/div').text
			remain_time = self.element_get(By.XPATH, '//*[@id="firstContent"]/div[2]/div/div[2]/div[3]/table/tbody/tr/td[4]/div').text
			self.line_notify.send_message('\nAttention, please.\nBaiCells\'s BBU information: \n'
											+ license_generatedate_name + ': ' + license_generatedate + '\n'
											+ remain_time_name + ': ' + remain_time)
			print(license_generatedate_name + ': ' + license_generatedate)
			print(remain_time_name + ': ' + remain_time)
			sleep(2)
		except:
			raise
		finally:
			self.driver.quit()

	def element_get(self, name, element):
		return WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((name, element))
			)

if __name__ == '__main__':
	l = bbu_license_check()
	l.setup()
	l.remain_time_parser()