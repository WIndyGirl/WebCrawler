#!/usr/bin/python

import sys
import socket
import urllib2
import pacparser
from bs4 import BeautifulSoup

def is_proxy_alive(proxy):
	host_port = proxy.split(":")
	if len(host_port) != 2:
		sys.stderr.write('proxy host is not defined as host:port\n')
		return False
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(10)
	try:
		s.connect((host_port[0], int(host_port[1])))
	except Exception, e:
		sys.stderr.write('proxy %s is not accessible\n' % proxy)
		sys.stderr.write(str(e)+'\n')
		return False
	s.close()
	return True

def get_proxy_with_pac(url):
	proxy_str = None
	try:
		pacparser.init()
		pacparser.parse_pac('hk1.pac')
		proxy_str = pacparser.find_proxy(url)
	except:
		sys.stderr.write('could not find proxy for %s using this PAC file.\n' % url)
		return None

	# proxy_str = 'PROXY hkce01.hk.ibm.com:80; PROXY 9.181.193.210:80; DIRECT'
	proxy_list = proxy_str.split(';')
	proxies = {}
	for proxy in proxy_list:
		proxy = proxy.strip()
		if 'DIRECT' == proxy:
			continue
		if proxy[0:5].upper() == 'PROXY':
			proxy = proxy[6:].strip()
			if is_proxy_alive(proxy):
				proxies['http'] = proxy
				break
	sys.stdout.write('get proxy %s for %s\n' % (proxies, url)) 

	return proxies

def get_response(url):
	# browser proxy: http://autoproxy.au.ibm.com/hk1.pac
	proxy = get_proxy_with_pac(url)
	#proxy = {'http': '9.181.193.210:80'}
	if proxy == None:
		return None

	proxy_support = urllib2.ProxyHandler(proxy)
	opener = urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)

	# add header to avoid get 403 fobbiden message
	i_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}
	request = urllib2.Request(url, headers = i_headers)

	try:
		sys.stdout.write('trying to fetch the page %s using proxy %s\n' % (url, proxy))
		response = urllib2.urlopen(request)
	except Exception, e:
		sys.stderr.write('could not fetch webpage %s using proxy %s\n' % (url, proxy))
		sys.stderr.write(str(e) + '\n')
		return None

	return response

def trade_spider(max_pages):
	page = 1
	while page <= max_pages:
		url = "https://developer.chrome.com/extensions"
		response = get_response(url)
		# just get the code, no headers or anything
		html = response.read()
		# BeautifulSoup objects can be sorted through easy
		soup = BeautifulSoup(html)
		for link in soup.findAll(href=re.compile("extensions")):
			href = "https://developer.chrome.com" + link.get('href')
			title = link.string # just the text, not the HTML
			print(href)
			print(title)

		page += 1

def get_single_item_data(item_url):
	response = get_response(item_url)
	if response == None:
		return None

	print 'Read source code'
	html = response.read()
	soup = BeautifulSoup(html)
	# if you want to gather information from that page
	for item_name in soup.findAll('div', {'class': 'toc'}):
		print(item_name.string)
	# if you want to gather links for a web crawler
	for link in soup.findAll('a'):
		href = "https://developer.chrome.com" + link.get('href')
		print(href)

url = "https://developer.chrome.com/extensions"
get_single_item_data(url)
#url = 'https://apis.google.com'
#get_proxy_with_pac(url)
