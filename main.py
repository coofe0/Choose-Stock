#! /usr/bin/python3

###目的：爬取符合我投资要求的上市公司的股票名称。学习python###
###路线：网易个股行情网页爬取股票信息，分析财务数据###
###      扩展到整个国内的上实公司，筛选符合我要求的公司###

import requests
import re
import os
from bs4 import BeautifulSoup
import bs4
import pandas as pd 

def readsheet():
	data=pd.read_excel('/home/coofe/ChooseStock/all_finance_sheet_done.xlsx',sheet_name='300789')
	print(data)
	print(data.iloc[2])

def getStockPrice():
	pass

def calculatePEPB():
	pass

def writesheet():
	pass

def showsheet():
	pass


def main():
	readsheet()


###################---main()---###################
if __name__=="__main__":
	main()
