#!/usr/bin/python
# -*- coding=utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup

def get_response(url):
	# add header to avoid get 403 fobbiden message
	i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}
	request = urllib2.Request(url, headers = i_headers)

	try:
		sys.stdout.write('trying to fetch the page %s \n' % url)
		response = urllib2.urlopen(request)
	except Exception, e:
		sys.stderr.write('could not fetch webpage %s \n' % url)
		sys.stderr.write(str(e) + '\n')
		return None

	return response

def get_single_page_date(url):
	response = get_response(url)

	if (response != None):
		html = response.read()
		print html
		soup = BeautifulSoup(html)
		head = soup.head
		print head
		title = soup.title
		print title
		noveltext = soup.find('div')
		#print noveltext


url = "http://www.jjwxc.net/onebook.php?novelid=1857985&chapterid=1"
get_single_page_date(url)


