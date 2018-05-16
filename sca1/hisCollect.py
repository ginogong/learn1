import tushare as ts 
import pandas as pd 
import numpy as np 
import datetime

'''
start = '2008-01-01'
end = str(datetime.datetime.date(datetime.datetime.now()))
stock = '002183'
path = "d:/datadownload/data/"

def hisCollector(stock=stock,start=start,end=end):
	data = ts.get_hist_data(stock,start,end)
	data = data.sort_index()
	data.to_excel(path + stock + '_' + end + '.xlsx')

	return 'History data has downloaded!'

hisCollector()
'''
print help(pd.DataFrame.str)