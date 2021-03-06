#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + '/../')

import urllib2
import datetime
import xlwt
import xlrd
from xlutils.copy import copy
from bs4 import BeautifulSoup
import json
import re

import db.mysql.VillageHisStatisDataHandler as VillageHisStatisDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class VillageHisStatisData:
	def __init__(self):
		self.logger = Logger(logname='/var/log/houseData.log', loglevel=1, logger='houseDataLogger').getLogger()

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

	def get_statistics_data(self, url, village_name):
		soup = self.get_home_page_data(url)
		values = [datetime.date.today()]
		values.append(village_name)	

		i = 0
		# get on sale and saled house data
		# /html/body/div[6]/div[2]/div[2]/ul/li[1]/span[2]
		# /html/body/div[6]/div[2]/div[2]/ul/li[3]/span[2]
		#statis_data = soup.select('div.wapper div.secondcon span.botline')

		data_container = soup.find('div', {'class': 'wrap'})
		qushi = data_container.find('div', {'class': 'box-l-t'}).find('div', {'class': 'qushi-2'})

		# get average unit price 
		unit_price = qushi.find('span', {'id': 'monthTrans'}).string
		values.append(unit_price)

		# get on sale and saled house data
		sale_data = qushi.findAll('a')
		for data in sale_data:
			# i == 0: data = '在售房源53套'
			if i == 0:
				values.append(re.sub("\D", "", data.string))
			# i == 1: data = '最近90天内成交房源13套'
			elif i == 1:
				values.append(re.sub("\D", "", data.string)[2:])
			i = i + 1

		# get chengjia in last 30 days and daikan in last 30 days
		i = 0
		statis_data = data_container.find('div', {'class': 'box-l-b'}).findAll('div', {'class': 'num'})
		for data in statis_data:
			if i > 0:
				values.append(data.find('span').string)
			i = i + 1

		self.logger.debug('The statistics data got for %s is: %s ' % (village_name, values) )
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

		for i in range(0, len(values)):
			for j in range(0,len(values[i])):
				sheet1.write(row_num + i, j, values[i][j], self.set_style('Times New Roman',220,True))

		nwb.save(file_name)

	def create_excel(self, file_name, sheet_name):
		work_book = xlwt.Workbook(style_compression=2)
		sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)

		row0 = [u'记录时间', u'小区名称', u'成交均价', u'在售房源', u'90天成交房源', u'30天成交房源', u'30天带看量' ]
		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		work_book.save(file_name)

	def record_into_db(self, conn, values):
		VillageHisStatisDataHandler.insert_village_his_statistics_data(conn, values)

if __name__ == '__main__':
	hisStatisData = VillageHisStatisData()

	common_url = 'http://bj.lianjia.com/fangjia/'
	village_infos = (
		('c1111027378224', 9, u'莱圳家园'), ('c1111027374195', 7, u'枫丹丽舍'), ('c1111027374615', 5, u'观景园'), ('c1111027374646', 7, u'观林园'), 
		('c1111027376795', 11, u'当代城市家园'), ('c1111046342806', 12, u'上地东里'), ('c1111027379186', 4, u'上地西里'), ('c1111027374308',10, u'蜂鸟家园'),
		('c1111027382146', 22, u'育新花园'), ('c1111027381078', 16, u'小南庄社区'), ('c1111027374543', 2, u'光大水墨'), ('c1111027374292', 9, u'富力桃园C区'), 
		('c1111027376008', 16, u'保利西山林语'), ('c1111027381913', 5, u'圆明园花园别墅'), ('c1111027376279', 5, u'博雅西园'), ('c1111027378785', 5, u'七彩华园'),
		('c1111027379551', 2,  u'山水蓝维'), ('c1111027380101', 10, u'太阳公元'), ('c1111027376127', 7, u'北纬40度二期'), ('c1111027376953', 15, u'慧忠里'), 
		('c1111027379077', 7, u'润泽悦溪'), ('c1111027382490', 18, u'珠江帝景'), ('c1111043464865', 2, u'国风美唐'), ('c1111027381003', 35, u'新龙城'), 
		('c1111027378138', 19, u'流星花园三区'), ('c1111027375871', 11, u'北京北'), ('c1111027378114', 3, u'龙腾苑五区'), ('c1111027380045', 10, u'天通苑本四区'), 
		('c1111027379515', 8, u'北街家园六区'), ('c1111043052734', 4, u'长阳半岛2号院'), ('c1111027375053', 3, u'宏汇园小区'), ('c1111027376697', 4, u'车站东街15号院'), 
		('c1111027373865', 5, u'德胜里一区'), ('c1111027382272', 18, u'裕中西里'), ('c1111027378023', 7, u'六铺炕二区'), ('c1111027378025', 5, u'六铺炕一区'))
	# village_infos = (('c1111027378224', 9, u'莱圳家园'), ('c1111027374195', 7, u'枫丹丽舍'))

	values = []
	for info in village_infos:
		# info = village_infos[0]
		url = common_url + info[0]
		value = hisStatisData.get_statistics_data(url, info[2])

		values.append(value)

	# hisStatisData.create_excel('VillageHisStatisData.xls', 'sheet1')
	# write data into excel
	hisStatisData.write_to_excel('../docs/VillageHisStatisData.xls', values)

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


