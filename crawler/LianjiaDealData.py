#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + "/../")

import urllib2
import xlwt
import xlrd
from bs4 import BeautifulSoup

import db.mysql.DealDataHandler as DealDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class LianjiaDealData:
	# def __init__(self):
	# 	self.logger = Logger(logname='/var/log/houseData.log', loglevel=1, logger="houseDataLogger").getLogger()

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

	def insert_into_db(self, soup, conn):
		# row index
		n = row_num
		# tunple for values to insert db
		values = None

		for item_name in soup.findAll('div', {'class': 'info-panel'}):
			print 'Writing %s row' % n
			# str index
			j = 0
			# cloumn index
			m = 0
			# flag for data from other agent
			f = False
			# array to get the column value
			arr = (2, 6, 8, 11)
			# len of item_name.strings
			k = 0
			for str in item_name.strings:
				k = k + 1

			if k < 14:
				arr = (k-8, k-6, k-3)

			value = []
			for str in item_name.strings:
				if j == 0:
					tmp = str.split(' ')
					l = 0;
					while l < len(tmp):
						value[m] = tmp[l]
						# update column index to next column
						m = m + 1
						l = l + 1
				elif j == 1 and str == u'历史成交，暂无详情页':
					f = True
					arr = (k-8, k-6, k-3)
				elif j == 1 or (j == 2 and f):
					tmp = str.split('/')
					l = 0;
					while l < len(tmp) - 1:
						value[m] = tmp[l]
						# update column index to next column
						m = m + 1
						l = l + 1
					if f:
						values[m] = ''
						m = m + 1
				elif j == 2 and k < 14:
					values[m] = ''
					m = m + 1
				elif j in arr:
					value[m] = str
					# update column index to next column
					m = m + 1
				# update str index to next column
				j = j + 1
			# update row index to the nexe row
			n = n + 1
			values[n] = value

		DealDataHandler.insert_deal_data(conn, values)


	def write_to_excel(self, soup, sheet, row_num):
		# row index
		n = row_num
		for item_name in soup.findAll('div', {'class': 'info-panel'}):
			print 'Writing %s row' % n
			# str index
			j = 0
			# cloumn index
			m = 0
			# flag for data from other agent
			f = False
			# array to get the column value
			arr = (2, 6, 8, 11)
			# len of item_name.strings
			k = 0
			for str in item_name.strings:
				k = k + 1

			if k < 14:
				arr = (k-8, k-6, k-3)

			default = self.set_style('Times New Roman',220,True)
			for str in item_name.strings:
				if j == 0:
					tmp = str.split(' ')
					l = 0;
					while l < len(tmp):
						sheet.write(n, m, tmp[l], default)
						# update column index to next column
						m = m + 1
						l = l + 1
				elif j == 1 and str == u'历史成交，暂无详情页':
					f = True
					arr = (k-8, k-6, k-3)
				elif j == 1 or (j == 2 and f):
					tmp = str.split('/')
					l = 0;
					while l < len(tmp) - 1:
						sheet.write(n, m, tmp[l], default)
						# update column index to next column
						m = m + 1
						l = l + 1
					if f:
						m = m + 1
				elif j == 2 and k < 14:
					m = m + 1
				elif j in arr:
					sheet.write(n, m, str, default)
					# update column index to next column
					m = m + 1
				# update str index to next column
				j = j + 1
			# update row index to the nexe row
			n = n + 1

	def get_response(self, url):
		# add header to avoid get 403 fobbiden message
		i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
					'Cookie': 'lianjia_uuid=13b925fd-319a-427e-9194-926b8b62f449;lianjia_token=1.0098cd0327081814a8a234148c290c4ac6'}
		request = urllib2.Request(url, headers = i_headers)

		try:
			response = urllib2.urlopen(request)
		except Exception, e:
			sys.stderr.write(str(e) + '\n')
			return None

		return response

	def get_single_page_data(self, item_url):
		response = self.get_response(item_url)
		if response == None:
			return None

		print 'Read source code'
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		return soup

	def get_all_data(self, url_suffix, page_count, dest, db_excel):
		url_common_part = "http://bj.lianjia.com/chengjiao/"
		url = None
		i = 1
		while i <= page_count:
			url = url_common_part + "pg" + str(i) + url_suffix
			soup = self.get_single_page_data(url)

			if db_excel == 'db':
				self.insert_into_db(soup, dest)
			elif db_excel == 'excel':
				self.write_to_excel(soup, dest, (i - 1) * 30 + 1)

			i = i + 1

	def record_data_excel(self, url_suffix, page_count, work_book, sheet_name):
		if sheet_name == "":
			print 'Invalid sheet name'
			return None
		# create sheet
		sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
		# set row title
		row0 = [u'小区名',u'户型',u'面积(平米)',u'朝向',u'楼层',u'是否满五唯一',u'成交日期',u'单价(元/平)', u'总价(万)']

		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		self.get_all_data(url_suffix, page_count, sheet1, 'excel')

	def record_data_db(self, url_suffix, page_count, conn):
		if sheet_name == "":
			print 'Invalid sheet name'
			return None

		self.get_all_data(url_suffix, page_count, conn, 'db')

if __name__ == '__main__':
	ljDealData = LianjiaDealData()

	village_infos = (("c1111027378224", 9, u'莱圳家园'))

	# village_infos = (("c1111027378224", 9, u'莱圳家园'), ("c1111027374195", 7, u'枫丹丽舍'), ("c1111027374615", 5, u'观景园'),
	# 	("c1111027374646", 7, u'观林园'), ("c1111027379551", 2,  u'山水蓝维'), ("c1111043464865", 2, u'国风美唐'),
	# 	("c1111027381003", 35, u'新龙城'), ("c1111027378138", 19, u'流星花园三区'), ("c1111027376795", 11, u'当代城市家园'),
	# 	("c1111046342806", 12, u'上地东里'), ("c1111027379186", 4, u'上地西里'))

	'''
	Write to Excel
	'''
	# create workbook
	work_book = xlwt.Workbook(style_compression=2)
	for info in village_infos:
		# get and record data
		ljDealData.record_data_excel(info[0], info[1], work_book, info[2])
	# save the recorded data
	work_book.save('LianjiaDealData.xls')

	# '''
	# Record in db
	# '''
	# dbHandler = new DBhandler()
	# # create db connection
	# conn = dbHandler.get_db_conn('house_data', 'root', 'passw0rd')
	# for info in village_infos:
	# 	ljDealData.record_data_db(info[0], info[1], conn)

	# dbHandler.close_db_conn(conn)

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





