#! /usr/bin/python3

###目的：爬取符合我投资要求的上市公司的股票名称。学习python###
###筛选出优质公司：每股净利润高，负债率低###
###筛选出便宜的股票：pe,pb评估，行业对比评估###

import requests
import re
import os
from bs4 import BeautifulSoup
import bs4
import pandas as pd 
import os
import matplotlib
from stockdata import Stock

def getStockList():
	with open('RoeRolStockList2.txt','r',encoding='utf-8') as f:
		t=f.readlines()
		for i in range(len(t)):
			t[i]=t[i][:6]
		print(t)
		return t	
def getGreatCL():
	with open('GreatCompany.txt','r',encoding='utf-8') as f:
		t=f.read()
		pattern=re.compile(r'\d{6}')
		ls=pattern.findall(t)
		print(ls)
		return ls

def getCheapC():
	''' 选出便宜的公司 price\PE\PB  '''
	t=getStockList()
	ls=[]
	for i in range(len(t)):
		stock = Stock(t[i])
		PE,PB=stock.calculatePEPB()
		l=[stock.name,stock.code,stock.price,PE,PB]
		s=pd.Series(l)
		ls.append(s)
		print(l)
	df=pd.DataFrame(ls)
	df.columns=['name','stock','price','PE','PB']
	
	print(df)
#	df.to_excel('choosedata.xlsx')

	return df


	#-----------------基本面指标计算-------------------#
#	ROE:综合评价一家公司盈利能力的最佳指标。ROE越高越好，最低标准得15%以上
#	负债率：负债率代表一家公司承受打击的能力，负债率越低越好，低于50%是最好的。
#	分红率：分红代表一家公司的诚信.每年股息率能大于一年定期收益是最好的.
#	毛利率：毛利率往往代表着一家公司的护城河宽度及垄断能力，毛利率越高越好，大于50%是最好的。
def getGreatC():
	'''选出优质的公司，三年roe>15，rol<50%,现金流>0
	2020年3月21日，符合的公司有：'''

	slist=getStockList()
	lst=[]						#空的最终清单
	count=0
	for i in range(len(slist)):
		stock=Stock(slist[i])
		data=stock.financeTable()		
		roe=data.loc['净资产收益率']	
		rol=int(re.sub(',','',data.loc['总负债',0]))/int(re.sub(',','',data.loc['总资产',0]))
		try:	
			yroe=0
			flag=0
			for k in range(12):
				yroe+=float(roe[k])
#				print('yroe:',yroe,'     reo:',roe[k])
				if (k+1)%4==0:
					if yroe/4>15:
						flag=1
						print('年净资产收益率yroe:',yroe/4)
						yroe=0
					else:
						flag=0
						print('年净资产收益率yroe:',yroe/4)
						yroe=0
			if flag :
				if rol<50:
					if float(data.loc['每股现金流',0])>0:
						lst.append(slist[i])
						count+=1
						print('已经找到：',count)
						print('Get great company:',slist[i])
					else:
						print('每股现金流没达标准：',data.loc['每股现金流',0])
				else:
					print('负债率没达到标准：',round(rol,2))
			else:
				print('净资产收益率没达到标准：')
		except Exception as e:
			print('数据不完整:',e)
	print(lst)
	with open('GreatCompany.txt','w',encoding='utf-8') as fl:
		fl.write(str(lst))
	return lst

def main():
	getGreatCL()
	
#	dt=pd.read_excel('choosedata.xlsx')
#	ds=dt.sort_values(by='PE',ascending='True')
#	print(ds.head(50))
#	print(dt.describe())

###################---main()---###################
if __name__=="__main__":
	main()
