#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + "/../")
import datetime

import re
import urllib2
import xlwt
import xlrd
from xlutils.copy import copy
from bs4 import BeautifulSoup

import db.mysql.JianWeiDealDataHandler as JianWeiDealDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class JianWeiDealData:
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

	def get_response(self, url):
		# add header to avoid get 403 fobbiden message
		i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}
		request = urllib2.Request(url, headers = i_headers)

		try:
			response = urllib2.urlopen(request)
		except Exception, e:
			sys.stderr.write(str(e) + '\n')
			return None

		return response

	def get_page_html(self, item_url):
		response = self.get_response(item_url)
		if response == None:
			return None

		self.logger.info('Read HTML source code')
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		return soup

	def get_data(self, url):
		soup = self.get_page_html(url)
		day = datetime.date.today() - datetime.timedelta(days=1)
		values = [day]

		tables = soup.findAll('table', {'class': 'tjInfo'})
		
		i = 0
		for table in tables:
			if (i == 1):
				i = i + 1
				continue

			tds = table.findAll('td')
			for td in tds:
				values.append(td.string)	
			i = i + 1	

		self.logger.debug('JianWei Deal data at %s is: %s ' % (day, values) )
		return values		

	def write_to_excel(self, file_name, values):
		work_book = xlrd.open_workbook(file_name)
		row_num = work_book.sheet_by_index(0).nrows

		nwb = copy(work_book)
		sheet1 = nwb.get_sheet(0)

		for i in range(0, len(values)):
			sheet1.write(row_num, i, values[i], self.set_style('Times New Roman',220,True))

		nwb.save(file_name)

	def create_excel(self, file_name, sheet_name):
		work_book = xlwt.Workbook(style_compression=2)
		sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)

		row0 = [u'记录时间', u'核验房源', u'核验房源面积(m2)', u'核验住宅', u'核验住宅面积(m2)', u'网上签约', u'网上签约面积(m2)', u'住宅签约', u'住宅签约面积(m2)']

		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		work_book.save(file_name)

	def record_into_db(self, values, conn):
		JianWeiDealDataHandler.insert_jianwei_deal_data(conn, values)

if __name__ == '__main__':
	JWDealData = JianWeiDealData()

	url = "http://210.75.213.188/shh/portal/bjjs/index.aspx"
	# get data
	values = JWDealData.get_data(url)

	'''
	Write to Excel
	'''
	# create workbook
	work_book = xlwt.Workbook(style_compression=2)

	# create excel file
	# JWDealData.create_excel('../docs/JianWeiDealData.xls', 'sheet1')
	# # write data into excel
	# JWDealData.write_to_excel('../docs/JianWeiDealData.xls', values)

	'''
	Record in db
	'''
	dbHandler = DBHandler()
	# create db connection
	conn = dbHandler.get_db_conn('house_data', 'root', 'passw0rd')
	# get data and insert into db	
	JWDealData.record_into_db(values, conn)

	dbHandler.close_db_conn(conn)





