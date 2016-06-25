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

import db.mysql.HotRegionHisStatisDataHandler as HotRegionHisStatisDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class HotRegionHisStatisData:
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

	def get_statistics_data(self, url, region_name):
		soup = self.get_home_page_data(url)
		values = [datetime.date.today()]
		values.append(region_name)	

		i = 0
		# get on sale and saled house data
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

		# get chengjia and daikan in last 7 days
		statis_data = data_container.find('div', {'class': 'box-l-b'}).findAll('div', {'class': 'num'})
		for data in statis_data:
			values.append(data.find('span').string)

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

		# values.append(round(float(values[-1])*100/float(values[-4]),2))

		self.logger.debug('The statistics data got for %s is: %s ' % (region_name, values) )
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

		row0 = [u'记录时间', u'区域名称', u'成交均价', u'在售房源', u'90天成交房源', u'近7日成交', u'近7日带看量', u'上月成交量', u'成交量环比上月(%)', u'成交量同比上年(%)', u'带看量比例' ]
		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		work_book.save(file_name)

	def record_into_db(self, conn, values):
		HotRegionHisStatisDataHandler.insert_hot_region_his_statistics_data(conn, values)

if __name__ == '__main__':
	hisStatisData = HotRegionHisStatisData()

	common_url = 'http://bj.lianjia.com/fangjia/'
	region_infos = (
		('wanliu', u'万柳'), ('shangdi1', u'上地'), ('xierqi1', u'西二旗'),('wudaokou', u'五道口'), ('anningzhuang1', u'安宁庄'),
		('xisanqi1', u'西三旗'), ('qinghe11', u'清河'), ('xibeiwang', u'西北旺'), ('malianwa', u'马连洼'), ('erlizhuang', u'二里庄'),
		('zhichunlu', u'知春路'), ('suzhouqiao', u'苏州桥'), ('shijicheng', u'世纪城'), ('zaojunmiao', u'皂君庙'), ('xiaoxitian1', u'小西天'), 
		('baishiqiao1', u'白石桥'), ('lugu1', u'鲁谷'), ('dinghuisi', u'定慧寺'), ('zhongguancun', u'中关村'), ('aolinpikegongyuan11', u'奥林匹克公园'),
		('yayuncun', u'亚运村'), ('wangjing', u'望京'), ('madian1', u'马甸'), ('anzhen1', u'安贞'), ('shaoyaoju', u'芍药居'), ('chaoqing', u'朝青'),
		('taiyanggong', u'太阳宫'), ('xibahe', u'西坝河'), ('hepingli', u'和平里'), ('jiuxianqiao', u'酒仙桥'), ('dongba', u'东坝'),
		('chaoyanggongyuan', u'朝阳公园'), ('shifoying', u'石佛营'), ('cbd', 'CBD'), ('shuangjing', u'双井'), ('dawanglu', u'大望路'),
		('beiyuan2', u'北苑'), ('guanzhuang', u'管庄'), ('liupukang', u'六铺炕'), ('deshengmen', u'德胜门'), ('jinrongjie', u'金融街'), 
		('yuetan', u'月坛'), ('changchunjie', u'长椿街'), ('tianningsi1', u'天宁寺'), ('guanganmen', u'广安门'), ('caoqiao', u'草桥'), 
		('jiugong1', u'旧宫'), ('lize', u'丽泽'), ('liuliqiao1', u'六里桥'), ('kejiyuanqu', u'科技园区'), ('huilongguan2', u'回龙观'), 
		('longze1', u'龙泽'), ('tiantongyuan1', u'天通苑'), ('changyang1', u'长阳'), ('liyuan', u'梨园'))
	
	#district_infos = (('shunyi', u'顺义'), ('daxing', u'大兴'))

	values = []
	for info in region_infos:
		# info = village_infos[0]
		url = common_url + info[0]
		value = hisStatisData.get_statistics_data(url, info[1])

		values.append(value)

	# hisStatisData.create_excel('../docs/HotRegionHisStatisData.xls', 'sheet1')
	# write data into excel
	hisStatisData.write_to_excel('../docs/HotRegionHisStatisData.xls', values)

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


