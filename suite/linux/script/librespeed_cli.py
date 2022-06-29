#/usr/bin/python3
'''
Created on 2022/06/29

@author: ZL Chen
@title: librespeed cli export
'''

from cProfile import label
import csv
from turtle import color
from matplotlib import pyplot as plt

class librespeed(object):

	def csv_strip(self):
		with open('..\\log\\export_csv.csv') as in_file:
			with open('..\\log\\export_csv_output.csv', 'w', newline='') as out_file:
				writer = csv.writer(out_file)
				for row in csv.reader(in_file):
					if any(field.strip() for field in row):
						writer.writerow(row)

	def graph(self):
		self.csv_strip()
		csv_file = open('..\\log\\export_csv_output.csv')  # Open the file
		# print(csv_file)
		csv_reader = csv.reader(csv_file) # Read CSV document
		# print(csv_reader)
		csv_data = list(csv_reader)
		# print(csv_data)
		length_len = len(csv_data) # Get the len
		# print(length_len)
		length_len_number = len(csv_data[0])
		# print(length_len_number)
		date_time = list()
		ping = list()
		jitter = list()
		download = list()
		upload = list()
		for i in range(1, length_len):
			csv_data_date_time = str(csv_data[i][0])[5:10] + '\n' + str(csv_data[i][0])[11:16]
			date_time.append(csv_data_date_time)
			ping.append(int(csv_data[i][3]))
			jitter.append(float(csv_data[i][4]))
			download.append(float(csv_data[i][5]))
			upload.append(float(csv_data[i][6]))
		plt.figure(figsize = (20,10), dpi = 100, linewidth = 2)	
		plt.plot(date_time, ping, 's-', color = 'b', label = 'Librespeed-cli')
		plt.title('Librespeed-CLI', x = 0.5, y = 1.03)
		plt.xlabel('Datetime')
		plt.ylabel('Ping')
		plt.savefig('..\\report\\Ping.png')
		plt.figure(figsize = (20,10), dpi = 100, linewidth = 2)	
		plt.plot(date_time, jitter, 's-', color = 'b', label = 'Librespeed-cli')
		plt.title('Librespeed-CLI', x = 0.5, y = 1.03)
		plt.xlabel('Datetime')
		plt.ylabel('Jitter')
		plt.savefig('..\\report\\Jitter.png')
		plt.figure(figsize = (20,10), dpi = 100, linewidth = 2)	
		plt.plot(date_time, download, 's-', color = 'b', label = 'Librespeed-cli')
		plt.title('Librespeed-CLI', x = 0.5, y = 1.03)
		plt.xlabel('Datetime')
		plt.ylabel('Download')
		plt.savefig('..\\report\\Download.png')
		plt.figure(figsize = (20,10), dpi = 100, linewidth = 2)	
		plt.plot(date_time, upload, 's-', color = 'b', label = 'Librespeed-cli')
		plt.title('Librespeed-CLI', x = 0.5, y = 1.03)
		plt.xlabel('Datetime')
		plt.ylabel('Upload')
		plt.savefig('..\\report\\Upload.png')

if __name__ == '__main__':
	speed = librespeed()
	speed.graph()
