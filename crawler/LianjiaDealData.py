#!/usr/bin/python
# -*- coding:utf-8 -*-  

import sys
import socket
import urllib2
import pacparser
import xlwt
import xlrd
from bs4 import BeautifulSoup

'''
set the cell style
''' 
def set_style(name,height,bold=False):
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

def get_response(url):
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

def get_single_page_data(item_url, sheet, row_num):
	response = get_response(item_url)
	if response == None:
		return None

	print 'Read source code'
	html = response.read()
	soup = BeautifulSoup(html)
	write_to_excel(soup, sheet, row_num)
	
	
def write_to_excel(soup, sheet, row_num):
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

		default = set_style('Times New Roman',220,True)
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

def get_all_data(url_suffix, page_count, sheet):
	url_common_part = "http://bj.lianjia.com/chengjiao/"
	url = None
	i = 1
	while i <= page_count:
		url = url_common_part + "pg" + str(i) + url_suffix
		get_single_page_data(url, sheet, (i - 1) * 30 + 1) 
		i = i + 1

def record_data_excel(url_suffix, page_count, work_book, sheet_name):
	if sheet_name == "":
		print 'Invalid sheet name'
		return None
	# create sheet 
	sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True) 
	# set row title
	row0 = [u'小区名',u'户型',u'面积',u'朝向',u'楼层',u'是否满五唯一',u'成交日期',u'单价(元/平)', u'总价(万)']

	# write the first row
	for i in range(0,len(row0)):
		sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

	get_all_data(url_suffix, page_count, sheet1)
	
# create workbook
work_book = xlwt.Workbook(style_compression=2)

'''
get data for '莱圳家园'
'''
url_suffix = "c1111027378224/"
page_count = 9 
sheet_name = u'莱圳家园'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

'''
get data for '枫丹丽舍'
'''
url_suffix = "c1111027374195"
page_count = 7
sheet_name = u'枫丹丽舍'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

work_book.save('LianjiaDealData.xls')

# 观景园
url_suffix = "c1111027374615/"
page_count = 5
sheet_name = u'观景园'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# 观林园
url_suffix = "c1111027374646/"
page_count = 7
sheet_name = u'观林园'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# 山水蓝维
url_suffix = "c1111027379551"
page_count = 2
sheet_name = u'山水蓝维'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# 国风美唐 
url_suffix = "c1111043464865"
page_count = 2 
sheet_name = u'国风美唐'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

work_book.save('LianjiaDealData.xls')

# 新龙城
url_suffix = "c1111027381003"
page_count = 35
sheet_name = u'新龙城'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# 流星花园三区
url_suffix = "c1111027378138"
page_count = 19
sheet_name = u'流星花园三区'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

work_book.save('LianjiaDealData.xls')

# 当代城市家园
url_suffix = "c1111027376795"
page_count = 11
sheet_name = u'当代城市家园'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# 上地东里
url_suffix = "c1111046342806"
page_count = 12
sheet_name = u'上地东里'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# 上地西里
url_suffix = "c1111027379186"
page_count = 4
sheet_name = u'上地西里'
# get and record data
record_data_excel(url_suffix, page_count, work_book, sheet_name)

# save the recorded data
work_book.save('LianjiaDealData.xls')

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





