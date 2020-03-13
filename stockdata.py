#! /usr/bin/python3

####类包含一个股票所有的数据#

import requests
import re
import os
from bs4 import BeautifulSoup
import bs4
import pandas as pd 
import matplotlib

class Stock():
	#定义基本属性
	code=''
	name=''
	
	#定义构造方法
	def __init__(self,code):
		self.code=code

	def readsheet(self):
		#'''读取财务数据 '''
		data=pd.read_excel('/home/coofe/ChooseStock/all_finance_sheet_done.xlsx',sheet_name=self.code)
		return data

	def getHTMLText(self,url):
		#"""  获取网页 """
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


	def getStockPrice(self):
	#	''' 获取当前价格 '''
		if self.code[0]=='6':	
			price_url = 'http://quotes.money.163.com/0'+self.code+'.html#01a01'             # #价格网址
		else:
			price_url = 'http://quotes.money.163.com/1'+self.code+'.html#01a01'
		print(price_url)
		phtml = self.getHTMLText(price_url)  

		sp=BeautifulSoup(phtml,'html.parser')
		a=sp.find_all(string=re.compile("window.stock_info"))               #找到含有window.stock_info字符串的标签
		a1=''.join(a)                                                       #把列表格式转成字符串格式
		#       print(a1)                       
		a1=re.sub('[,]|[ ]','',a1)                                          #把字符串中的空格和，替换成空
		text=re.split("[\r][\n]",a1)                                        #把字符串用换行符分割成列表格式
		text=text[2:-2]                                                     #把列表没用的前后去掉
		print("The text  is:",text)
		for i in range(len(text)):                                          
			p='price'                                                   
			if p in text[i]:                                            #依次判断列表中的元素是否含有price
				getprice=re.search(r'\d+[\.]\d+',text[i])                   #假如有则匹配数字，
				if getprice:
					print('price:',getprice.group(0))
					return getprice.group(0)                                                    #返回匹配后的字符串
				else:
					print('没有获取到当前价格')
					return 0


	def calculatePEPB(self):
		data=self.readsheet()
		price=float(self.getStockPrice())
		
		earning=float(data.loc[1,0])
		book_value=float(data.loc[2,0])
		pe=price/earning
		pb=price/book_value
		print('PE:{:.2f}'.format(pe))
		print('PB:{:.2f}'.format(pb))
		




	def writesheet():
		pass

	def showsheet():
		pass

