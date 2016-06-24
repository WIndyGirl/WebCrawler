#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + "/../")

import urllib2
import xlwt
import xlrd
from xlutils.copy import copy
from bs4 import BeautifulSoup
import datetime
import re
import json

import db.mysql.HistoryStatisticsDataHandler as HistoryStatisticsDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class LianjiaHisStatisticsData:
	def __init__(self):
		self.logger = Logger(logname='/var/log/houseData.log', loglevel=1, logger="houseDataLogger").getLogger()

	def get_response(self, url):
		# add header to avoid get 403 fobbiden message
		i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}
		request = urllib2.Request(url, headers = i_headers)

		try:
			response = urllib2.urlopen(request)
		except Exception, e:
			self.logger.error(str(e) + '\n')
			return None

		return response

	def get_home_page_data(self, url):
		response = self.get_response(url)
		if response == None:
			return None

		self.logger.info('Read source code')
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		return soup

	def get_statistics_data(self, url):
		soup = self.get_home_page_data(url)
		values = [datetime.date.today()]

		i = 0
		data_container = soup.find('div', {'class': 'wrap'})
		# get on sale and saled house data
		sale_data = data_container.find('div', {'class': 'box-l-t'}).find('div', {'class': 'qushi-2'}).findAll('a')
		for data in sale_data.strings:
			# i == 0: data = '在售房源78846套'
			if i == 0:
				values.append(re.sub("\D", "", data))
			# i == 1: data = '最近90天内成交房源35399套'
			elif i == 1:
				values.append(re.sub("\D", "", data)[2:])
			i = i + 1

		# get statistics data on yesterday
		i = 0
		statis_data = data_container.find('div', {'class': 'box-l-b'}).findAll('div', {'class': 'num'})
		for data in statis_data:
			if i > 0:
				values.append(data.find('span').string)
			i = i + 1

		# get daily new customer data and new house data
		url = 'http://bj.lianjia.com/fangjia/priceTrend//?analysis=1&duration=day'
		res_json = json.load(self.get_response(url))
		house_amount = res_json['houseAmount']
		customer_amount = res_json['customerAmount']

		values.append(house_amount[-1])
		values.append(customer_amount[-1])

		self.logger.debug("The statistics data got is: %s " % values )

		return values

	'''
	set the cell style
	'''
	def set_style(self, name,height,bold=False):
		# init style
		style = xlwt.XFStyle()

		# create font for style
		font = xlwt.Font()
		font.name = name # 'Times New Roman'
		#font.bold = bold
		font.color_index = 4
		font.height = height

		# borders= xlwt.Borders()
		# borders.left= 6
		# borders.right= 6
		# borders.top= 6
		# borders.bottom= 6

		style.font = font
		# style.borders = borders

		return style

	def write_to_excel(self, file_name, values):
		work_book = xlrd.open_workbook(file_name)
		row_num = work_book.sheet_by_index(0).nrows

		nwb = copy(work_book)
		sheet1 = nwb.get_sheet(0)

		for i in range(0,len(values)):
			sheet1.write(row_num, i, values[i], self.set_style('Arial',220,True))

		nwb.save(file_name)

	def create_excel(self, file_name, sheet_name):
		work_book = xlwt.Workbook(style_compression=2)
		sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)

		row0 = [u'记录时间', u'在售房源', u'90天成交房源', u'昨日成交', u'昨日带看', u'昨日新增房源', u'昨日新增房客' ]
		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		work_book.save(file_name)

	def record_into_db(self, conn, values):
		HistoryStatisticsDataHandler.insert_history_statistics_data(conn, values)

if __name__ == '__main__':
	hisStatisData = LianjiaHisStatisticsData()
	url = 'http://bj.lianjia.com/fangjia/'
	# get statistics data
	values = hisStatisData.get_statistics_data(url)

	# create excel
	# hisStatisData.create_excel('LianJiaHisStatisData.xls', 'sheet1')
	# write collected data into excel
	hisStatisData.write_to_excel('../docs/LianJiaHisStatisData.xls', values)

	'''
	Record data into db
	'''
	dbHandler = DBHandler()
	# create db connection
	conn = dbHandler.get_db_conn('house_data', 'root', 'passw0rd')
	# insert data into db
	hisStatisData.record_into_db(conn, values)
	# close db connection
	dbHandler.close_db_conn(conn)



