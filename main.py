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
	

def main():
#	getStockList()
	stock = Stock('600052')
#	stock.getStockPrice()
	stock.calculatePEPB()

###################---main()---###################
if __name__=="__main__":
	main()
