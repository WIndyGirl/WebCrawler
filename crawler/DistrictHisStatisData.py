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

import db.mysql.DistrictHisStatisDataHandler as DistrictHisStatisDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class DistrictHisStatisData:
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

	def get_statistics_data(self, url, district_name):
		soup = self.get_home_page_data(url)
		values = [datetime.date.today()]
		values.append(district_name)	

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

		# get deal in last month
		trend = soup.find('div', {'class': 'm-chart echarts-trend'}).find('div', {'class': 'trend'}).find('div', {'class': 'txt hide'}).string
		# trend example: 5月挂牌均价：85900.24元/平米，环比上月下跌0.84%，同比去年上涨38.78%。  
		# 5月成交均价：79510元/平米，环比上月上涨1.39%，同比去年上涨35.18%。  
		# 5月成交量：860套，环比上月下跌18.02%，同比去年下跌12.78%。  （数据来源：链家成交系统统计，更新日期：2016年5月）
		deal_amount_strs = (trend.split( u'。')[2]).split(u'，')

		# get deal in last month
		deal = 0
		if (datetime.date.today().month < 10):
			deal = re.sub("\D", "", deal_amount_strs[0])[1:]
		else:
			deal = re.sub("\D", "", deal_amount_strs[0])[2:]
		values.append(deal)

		# get deal compare data
		compare_last_month = deal_amount_strs[1][6:-1]
		compare_last_year = deal_amount_strs[2][6:-1]

		if (deal_amount_strs[1][4:6] == u'下跌'):
			compare_last_month = float('-%s' % compare_last_month)
		if (deal_amount_strs[2][4:6] == u'下跌'):
			compare_last_year = float('-%s' % compare_last_year)

		values.append(compare_last_month)
		values.append(compare_last_year)		

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

		# get chengjia and daikan in yesterday
		statis_data = data_container.find('div', {'class': 'box-l-b'}).findAll('div', {'class': 'num'})
		for data in statis_data:
			values.append(data.find('span').string)

		# values.append(round(float(values[-1])*100/float(values[-4]),2))

		self.logger.debug('The statistics data got for %s is: %s ' % (district_name, values) )
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

		row0 = [u'记录时间', u'区名称', u'成交均价', u'上月成交量', u'成交量环比上月(%)', u'成交量同比上年(%)', u'在售房源', u'90天成交房源', u'昨日成交', u'昨日带看量', u'带看量比例' ]
		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		work_book.save(file_name)

	def record_into_db(self, conn, values):
		DistrictHisStatisDataHandler.insert_district_his_statistics_data(conn, values)

if __name__ == '__main__':
	hisStatisData = DistrictHisStatisData()

	common_url = 'http://bj.lianjia.com/fangjia/'
	district_infos = (
		('xicheng', u'西城'), ('dongcheng', u'东城'), ('haidian', u'海淀'),('chaoyang', u'朝阳'), ('tongzhou', u'通州'),
		('fengtai', u'丰台'), ('changping', u'昌平'), ('shijingshan', u'石景山'), ('fangshan', u'房山'), ('mentougou', u'门头沟'),
		('shunyi', u'顺义'), ('daxing', u'大兴'), ('yizhuangkaifaqu', u'亦庄开发区'))
	# ('yanjiao', u'燕郊'),
	#district_infos = (('shunyi', u'顺义'), ('daxing', u'大兴'))

	values = []
	for info in district_infos:
		# info = village_infos[0]
		url = common_url + info[0]
		value = hisStatisData.get_statistics_data(url, info[1])

		values.append(value)

	# hisStatisData.create_excel('../docs/DistrictHisStatisData.xls', 'sheet1')
	# write data into excel
	hisStatisData.write_to_excel('../docs/DistrictHisStatisData.xls', values)

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


