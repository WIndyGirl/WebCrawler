#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + "/../")

import re
import urllib2
import xlwt
import xlrd
from bs4 import BeautifulSoup

import db.mysql.DealDataHandler as DealDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class LianjiaDealData:
	def __init__(self):
		self.logger = Logger(logname='/var/log/houseData.log', loglevel=1, logger="houseDataLogger").getLogger()

	'''
	set the cell style
	'''
	def set_style(self, name,height,bold=False):
		# init style
		style = xlwt.XFStyle()

		# create font for style
		font = xlwt.Font()
		font.name = name # 'Times New Roman'
		font.size = 10
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

	def get_deal_data(self, soup):
		# row index
		n = 0
		# tunple for values to insert db
		values = []

		for item_name in soup.findAll('div', {'class': 'info-panel'}):
			self.logger.info('Collecting %s row' % n)
			# str index
			j = 0
			# cloumn index
			m = 0
			# flag for data from other agent
			f = False
			# array to get the column value
			arr = (2, 8, 11)
			# len of item_name.strings
			k = 0
			for str in item_name.strings:
				k = k + 1

			if k < 14:
				arr = (k-6, k-3)

			value = []
			for str in item_name.strings:
				if j == 0:
					tmp = str.split(' ')
					l = 0;
					while l < len(tmp):
						# 71平米 --> 71
						if l == 2:
							value.append(re.sub('\D', '', tmp[l]))
						else:
							value.append(tmp[l])
						# update column index to next column
						m = m + 1
						l = l + 1
				elif j == 1 and str == u'历史成交，暂无详情页':
					f = True
					arr = (k-6, k-3)
				elif j == 1 or (j == 2 and f):
					tmp = str.split('/')
					l = 0;
					while l < len(tmp) - 1:
						value.append(tmp[l])
						# update column index to next column
						m = m + 1
						l = l + 1
					if f:
						value.append('')
						m = m + 1
				elif j == 2 and k < 14:
					value.append('')
					m = m + 1
				elif j == k - 8:
					if len(str) == 7:
						str = str + '.01'

					value.append(str)
					m = m + 1
				elif j in arr:
					value.append(str)
					# update column index to next column
					m = m + 1
				# update str index to next column
				j = j + 1
			if len(value) == 9:
				values.append(value)
			# update row index to the next row
			n = n + 1
		self.logger.info('%s rows data has been collected; the length of list stores the collected data is %s' % (n, len(values)))
		self.logger.info('the collected data is: %s' % values)

		return values

	def get_response(self, url):
		# add header to avoid get 403 fobbiden message
		i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
					'Cookie': 'lianjia_uuid=2ebbfb89-6086-41ba-8c8b-06299a4ef5c8; lianjia_token=1.0092e5f86f1e8105f63d6d6fd4d79d9738'}
		request = urllib2.Request(url, headers = i_headers)

		try:
			response = urllib2.urlopen(request)
		except Exception, e:
			sys.stderr.write(str(e) + '\n')
			return None

		return response

	def get_single_page_html(self, item_url):
		response = self.get_response(item_url)
		if response == None:
			return None

		self.logger.info('Read HTML source code')
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		return soup

	def get_all_data(self, url_suffix, page_count):
		url_common_part = "http://bj.lianjia.com/chengjiao/"
		values = []

		i = 1
		while i <= page_count:
			url = url_common_part + "pg" + str(i) + url_suffix
			soup = self.get_single_page_html(url)
			values = values + self.get_deal_data(soup)

			i = i + 1

		return values

	def record_data_excel(self, values, work_book, sheet_name):
		if sheet_name == "":
			self.logger.error('Invalid sheet name')
			return None

		if values == [] or values == None:
			self.logger.error('No data provided to record')
			return None

		# create sheet
		sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
		# set row title
		row0 = [u'小区名',u'户型',u'面积(平米)',u'朝向',u'楼层',u'是否满五唯一',u'成交日期',u'单价(元/平)', u'总价(万)']

		default = self.set_style('Times New Roman',220,True)
		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0, i, row0[i], default)
		
		for i in range(1, len(values)):
			for j in range(0, len(values[i])):
				sheet1.write(i, j, values[i][j], default)

	def record_data_db(self, values, conn):
		DealDataHandler.insert_deal_data(conn, values)

if __name__ == '__main__':
	ljDealData = LianjiaDealData()

	# village_infos = (('c1111027378224', 1, u'莱圳家园'), ('c1111027374195', 1, u'枫丹丽舍'))

	village_infos = (
		('c1111027378224', 9, u'莱圳家园'), ('c1111027374195', 7, u'枫丹丽舍'), ('c1111027374615', 5, u'观景园'), ('c1111027374646', 7, u'观林园'), 
		('c1111027376795', 11, u'当代城市家园'), ('c1111046342806', 12, u'上地东里'), ('c1111027379186', 4, u'上地西里'), ('c1111027374308',10, u'蜂鸟家园'),
		('c1111027382146', 22, u'育新花园'), ('c1111027381078', 16, u'小南庄社区'), ('c1111027374543', 2, u'光大水墨'), ('c1111027374292', 9, u'富力桃园C区'), 
		('c1111027376008', 16, u'保利西山林语'), ('c1111027379551', 2,  u'山水蓝维'), ('c1111027380101', 10, u'太阳公元'), ('c1111027376127', 7, u'北纬40度二期'), 
		('c1111027376953', 15, u'慧忠里'), ('c1111027379077', 7, u'润泽悦溪'), ('c1111027382490', 18, u'珠江帝景'), ('c1111043464865', 2, u'国风美唐'),
		('c1111027381003', 35, u'新龙城'), ('c1111027378138', 19, u'流星花园三区'), ('c1111027375871', 11, u'北京北'), ('c1111027378114', 3, u'龙腾苑五区'),
		('c1111027380045', 10, u'天通苑本四区'), ('c1111027379515', 8, u'北街家园六区'), ('c1111043052734', 4, u'长阳半岛2号院'), 
		('c1111027375053', 3, u'宏汇园小区'), ('c1111027376697', 4, u'车站东街15号院'), ('c1111027373865', 5, u'德胜里一区'), ('c1111027382272', 18, u'裕中西里'),
		('c1111027378023', 7, u'六铺炕二区'), ('c1111027378025', 5, u'六铺炕一区'))

	'''
	Write to Excel
	'''
	# create workbook
	# work_book = xlwt.Workbook(style_compression=2)
	# # get data and record in excel
	# for info in village_infos:		
	# 	values = ljDealData.get_all_data(info[0], info[1])
	# 	ljDealData.record_data_excel(values, work_book, info[2])

	# # save the recorded data
	# work_book.save('LianjiaDealData.xls')

	'''
	Record in db
	'''
	dbHandler = DBHandler()
	# create db connection
	conn = dbHandler.get_db_conn('house_data', 'root', 'passw0rd')
	# get data and insert into db
	for info in village_infos:
		values = ljDealData.get_all_data(info[0], info[1])	
		ljDealData.record_data_db(values, conn)

	dbHandler.close_db_conn(conn)

	# 0 莱圳家园 1室2厅 71平米
	# 1 南 / 高楼层(共18层) / 2012板塔结合
	# 2 房本满两年
	# 3 永泰小学
	# 4 距8号线西小口372米
	# 5 查看同户型成交记录z
	# 6 2015.10.18
	# 7 链家网签约
	# 8 43661
	# 9 元/平
	# 10 签约单价
	# 11 310
	# 12 万
	# 13 签约总价





