#! /usr/bin/python3

import requests

#-------------获取网页----------------#
def getHTMLText(url):
	try:
		headers={'User-Agent':'Mozilla/5.0'}
		r=requests.get(url,timeout=20,headers=headers)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		print(r.status_code)
		return r.text
	except:
		print('Wrong')
		return "Wrong"








