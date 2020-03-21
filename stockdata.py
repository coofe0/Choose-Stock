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
	
	
	#定义构造方法
	def __init__(self,code):
		self.code=code			
		self.price,self.name=self.getStockPrice()
		self.price=float(eval(self.price))
		self.name=eval(self.name)

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
		t=text[0].split(':')
		name=t[1]
		p=text[2].split(':')
		price=p[1]
	
		return price,name                                   #返回匹配后的字符串


	def calculatePEPB(self):
		'''计算PE、PB '''
		data=self.readsheet()
		
		earning=float(data.loc[1,0])
		book_value=float(data.loc[2,0])
		pe=self.price/earning
		pb=self.price/book_value
		print('PE:{:.2f}'.format(pe))
		print('PB:{:.2f}'.format(pb))
		return round(pe,2),round(pb,2)		




	def writesheet():
		pass

	def showsheet():
		pass


	def getFinanceList(self):
		''' 获取基本财务数据列表'''
		ls=[]
		finance_url='http://quotes.money.163.com/f10/zycwzb_'+self.code+'.html#01c01'		#财务数据网址
		finance_html=self.getHTMLText(finance_url)

		if finance_html !="Wrong":
			soup=BeautifulSoup(finance_html,'html.parser')		
			#-------------获得表格内容-------------#
			table=soup.find_all('table')[4]		#找到我要的表格，查网页上第四个数据表格
			tr=table.find('tr')

			for t in table.find_all('tr'):		#循环查找表格中找TR标签，T表示表格中的每排
				tds=t.find_all('td')		#tds表示每排中的一个单元格
				ts=[]				#定义临时空数据列表
				
				for i in range(len(tds)):	#依次查找每行的单元格
					ts.append(tds[i].string)#把单元格的字符串加到临时列表中
				ls.append(ts)			#（每行单元格添加结束后）每排依次添加到总列表中。

			ls0=[]					#定义空日期
			tr=table.find('tr')			#table中获得第一个tr
			ths=tr.find_all('th')			#tr 中找出所有th
			for k in range(len(ths)):		#
				ls0.append(ths[k].string)	#依次田间到ts0例表中

			ls[0]=ls0				#ls0作为一个元素写入到ls的第一个


#			print(ls)
			lsname=['日期','每股收益', '每股净资产', '每股现金流', '主营收入', '主营利润', '营业利润', '投资收益', '营业外收支', '利润总额', '净利润', '净利润(扣除非经常性损益后)', '经营活动产生的现金流量', '现金净增加额', '总资产', '流动资产', '总负债', '流动负债', '股东权益', '净资产收益率加权']
			return ls,lsname


	def getFinanceList2(self):
		'''-获得股票的每股净资产\每股现金流 '''
		finance_url2='https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/'+self.code+'.phtml'	#财务数据网址
		finance_html2=self.getHTMLText(finance_url2)
		if finance_html2 !="Wrong":
			datelist=[]							#定义空日期列表
			navlist=[]							#定义每股净资产列表
			cfpslist=[]							#定义每股现金流类列表
			soup=BeautifulSoup(finance_html2,'html.parser')		
			for n in soup.find_all(name='td',string='每股净资产-摊薄/期末股数'):		#循环每个td找出string	
				t=n.find_next_sibling().string						#找出下一个string
				navlist.append(t)							#添加到列表
			for n in soup.find_all(name='strong',string='截止日期'):
				t=n.find_parent().find_next_sibling().string
				datelist.append(t)
			for n in soup.find_all(name='td',string='每股现金流'):
				t=n.find_next_sibling().string
				cfpslist.append(t)

			for j in range(len(navlist)):						#删除每个元素中的元
				if navlist[j]:							#不为空
					try:
						navlist[j]=navlist[j].replace('元','')
					except:
						print('can not replace : 元')
				else:								#否则置0
					navlist[j]=0
			for j in range(len(cfpslist)):						#删除每个元素中的元
				if cfpslist[j]:
					try:
						cfpslist[j]=cfpslist[j].replace('元','')
					except:
						print('can not replace : 元')
				else:
					cfpslist[j]=0
#			print(datelist)
#			print(navlist)
#			print(cfpslist)
			return datelist,navlist,cfpslist


	def financeTable(self):
		ls,lsname=self.getFinanceList()
		datelist,navlist,cfpslist=self.getFinanceList2()
		dt=pd.DataFrame(ls,index=lsname)
		nav=pd.Series(navlist)
		cfps=pd.Series(cfpslist)
		if datelist[0]==dt.loc['日期',0]:
			dt.loc['每股净资产']=nav
			dt.loc['每股现金流']=cfps
		else:
			print('最新日期不同，不能合并')
		print(dt.head())
		
		return dt




