#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
file_path = (os.path.abspath(__file__))
sys.path.append(os.path.dirname(file_path) + "/../")

import urllib2
import datetime
import xlwt
import xlrd
from xlutils.copy import copy
from bs4 import BeautifulSoup

import db.mysql.DealDataHandler as DealDataHandler
from db.mysql.DBHandler import DBHandler
from lib.Logger import Logger

class VillageHisStatisData:
	#def __init__(self):
		# self.logger = Logger(logname='/var/log/houseData.log', loglevel=1, logger="houseDataLogger").getLogger()

	def get_response(self, url):
		# add header to avoid get 403 fobbiden message
		i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}
		request = urllib2.Request(url, headers = i_headers)

		try:
			response = urllib2.urlopen(request)
		except Exception, e:
			sys.stderr.write(str(e) + '\n')
			return None

		return response

	def get_home_page_data(self, url):
		response = self.get_response(url)
		if response == None:
			return None

		print 'Read source code'
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		return soup

	def get_statistics_data(self, url, village_name):
		soup = self.get_home_page_data(url)
		values = [datetime.date.today()]

		i = 0
		# get on sale and saled house data
		# /html/body/div[6]/div[2]/div[2]/ul/li[1]/span[2]
		# /html/body/div[6]/div[2]/div[2]/ul/li[3]/span[2]
		#statis_data = soup.select('div.wapper div.secondcon span.botline')
		values.append(village_name)

		# get statistic data
		statis_data = soup.find('div', {'class': 'secondcon fl'}).findAll('span', {'class': 'botline'})
		for data in statis_data:
			if i == 3:
				values.append(data.find('strong').string)
				break
			for item in data.find('a'):
				values.append(item)

			i = i + 1

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

		row0 = [u'记录时间', u'小区名称', u'成交均价', u'在售房源', u'90天成交房源', u'30天带看量' ]
		# write the first row
		for i in range(0,len(row0)):
			sheet1.write(0,i,row0[i],self.set_style('Times New Roman',220,True))

		work_book.save(file_name)

if __name__ == '__main__':
	hisStatisData = VillageHisStatisData()

	common_url = 'http://bj.lianjia.com/ershoufang/'
	village_infos = (("c1111027378224", 9, u'莱圳家园'), ("c1111027374195", 7, u'枫丹丽舍'), ("c1111027374615", 5, u'观景园'),
		("c1111027374646", 7, u'观林园'), ("c1111027379551", 2,  u'山水蓝维'), ("c1111043464865", 2, u'国风美唐'),
		("c1111027381003", 35, u'新龙城'), ("c1111027378138", 19, u'流星花园三区'), ("c1111027376795", 11, u'当代城市家园'),
		("c1111046342806", 12, u'上地东里'), ("c1111027379186", 4, u'上地西里'))
	# village_infos = (("c1111027378224", 9, u'莱圳家园'), ("c1111027374195", 7, u'枫丹丽舍'))

	values = []
	for info in village_infos:
		# info = village_infos[0]
		url = common_url + info[0]
		value = hisStatisData.get_statistics_data(url, info[2])

		values.append(value)
	print values

	# hisStatisData.create_excel('VillageHisStatisData.xls', 'sheet1')

	hisStatisData.write_to_excel('../docs/VillageHisStatisData.xls', values)


