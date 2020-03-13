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
from stockdata import Stock

def getStockList():
	with open('RoeRolStockList2.txt','r',encoding='utf-8') as f:
		t=f.readlines()
		for i in range(len(t)):
			t[i]=t[i][:6]
		print(t)
		return t	

def getdata():
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
	df.to_excel('choosedata.xlsx')

def main():
	dt=pd.read_excel('choosedata.xlsx')
	print(dt)
	print(dt.describe())
	dt.plot()

###################---main()---###################
if __name__=="__main__":
	main()
