import requests
from bs4 import BeautifulSoup

def trade_spider(max_pages):
	page = 1
	while page <= max_pages:
		url = "https://developer.chrome.com/extensions"
		source_code = requests.get(url)
		# just get the code, no headers or anything
		plain_text = source_code.plain_text
		# BeautifulSoup objects can be sorted through easy
		soup = BeautifulSoup(plain_text)
		for link in soup.findAll(href=re.compile("extensions")):
			href = "https://developer.chrome.com" + link.get('href')
			title = link.string # just the text, not the HTML
			print(href)
			print(title)

		page += 1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    # if you want to gather information from that page
    for item_name in soup.findAll('div', {'class': 'toc'}):
        print(item_name.string)
    # if you want to gather links for a web crawler
    for link in soup.findAll('a'):
        href = "https://developer.chrome.com" + link.get('href')
        print(href)

# http://autoproxy.au.ibm.com/hk1.pac
