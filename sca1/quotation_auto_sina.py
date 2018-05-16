# -*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np
import warnings 
import tushare as ts
from pyquery import PyQuery as pq
import re
import requests
import datetime
from rollingmaxdd import max_dd
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)

now_time = datetime.datetime.now()
now = now_time.strftime('%Y-%m-%d')
index_list = ['sz399300','sh000852']

def find_lastday(dataframe):
	last_day = dataframe['date'].sort_values(ascending=False).unique()[0]
	return last_day

def get_dayk(code,start,end):
	df = ts.get_k_data(code,start=start,end=end)
	return df

def add_prefix(code):
	code = str(code)
	if code.startswith('6'):
		code = 'sh'+ code
	else:
		code = 'sz' + code
	return code

def get_data(code,head):
	url = 'http://hq.sinajs.cn/list='
	response = requests.get(url + code, headers=head)
	l1 = response.text.split(',')
	if len(l1) >= 5:
		if float(l1[1]) != 0.0 and float(l1[8]) > 0:
		    now = datetime.datetime.now().strftime('%Y-%m-%d')
		    date_list.append(l1[30])
		    open_price_list.append(float(l1[1]))
		    close_price_list.append(float(l1[3]))
		    high_price_list.append(float(l1[4]))
		    low_price_list.append(float(l1[5]))
		    volume_list.append(int(l1[8])/100)
		    code_list.append(code[2:])

		    print '%s has finished!' % code

#get new stock list
url = 'http://quote.eastmoney.com/stocklist.html'
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }

response = requests.get(url, headers=header_req)
response.encoding = 'gbk'
data = pq(response.text)
pattern = re.compile(u"\d{6}")
temp_list = []
with open('stocklist.txt', 'w') as sl:
	for item in data('#quotesearch ul a'):
		if pattern.findall(pq(item).text())[0][0:3] in ['600', '603', '601', '300', '002', '000','001']:
			sl.write(pattern.findall(pq(item).text())[0] + '\n')
			temp_list.append(pattern.findall(pq(item).text())[0])
			#print pattern.findall(pq(item).text())[0]
			#num += 1
df_stlist = pd.DataFrame(temp_list,columns=['stocklist'])
df_hist = pd.read_hdf('stocklist.h5','stocklist')
df_hist = pd.concat([df_hist,df_stlist])
df_hist = df_hist.drop_duplicates()
df_hist = df_hist.sort_values('stocklist')
df_hist.index = np.arange(len(df_hist))
df_hist.to_hdf('stocklist.h5','stocklist')
print 'stock list number= %d updating finished ' % len(df_stlist)
#read history data decision

date_list = []
open_price_list = []
close_price_list = []
high_price_list = []
low_price_list = []
volume_list = []
code_list = []
columns = ['date','open','close','high','low','volume','code']
stock_list = pd.read_hdf('stocklist.h5','stocklist')

for i in range(len(stock_list)):	
	code = stock_list.ix[i,'stocklist']
	code_temp = add_prefix(code)
	get_data(code_temp,header_req)

df = pd.DataFrame({'date':date_list,'open':open_price_list,'close':close_price_list,\
					'high':high_price_list,'low':low_price_list,'volume':volume_list,\
					'code':code_list})
df = df[columns]

df_hist = pd.read_hdf('dayk_17.h5','dayk_17')
df_hist = pd.concat([df_hist,df])
df_hist = df_hist.drop_duplicates()
df_hist.to_hdf('dayk_17.h5','dayk_17')
print '%d stock day k data updating finished' % len(df)



hs_date_list = []
hs_open_list = []
hs_close_list = []
hs_high_list = []
hs_low_list = []
hs_volume_list = []
url1 = 'http://hq.sinajs.cn/list='
df_hs = pd.read_hdf('all_index.h5','hs300')
response_hs = requests.get(url1 + index_list[0], headers=header_req)
hs_res = response_hs.text.split(',')
if len(hs_res) >= 5:
	if float(hs_res[1]) != 0.0 and float(hs_res[8] > 0):	   
	    hs_date_list.append(hs_res[30])
	    hs_open_list.append(round(float(hs_res[1]),2))
	    hs_close_list.append(round(float(hs_res[3]),2))
	    hs_high_list.append(round(float(hs_res[4]),2))
	    hs_low_list.append(round(float(hs_res[5]),2))
	    hs_volume_list.append(int(hs_res[8])/100)
hs_temp = pd.DataFrame({'date':hs_date_list,'open':hs_open_list,'close':hs_close_list,\
						'high':hs_high_list,'low':hs_low_list,'volume':hs_volume_list})
hs_temp = hs_temp.set_index('date')
hs_temp.index = pd.to_datetime(hs_temp.index)
hs_temp = hs_temp[['open','close','high','low','volume']]
df_hs = pd.concat([df_hs,hs_temp])
df_hs = df_hs.drop_duplicates()
df_hs.to_hdf('all_index.h5','hs300')
print 'hs300 updating finished'

url1 = 'http://hq.sinajs.cn/list='
zz_date_list = []
zz_open_list = []
zz_close_list = []
zz_high_list = []
zz_low_list = []
zz_volume_list = []
df_zz = pd.read_hdf('all_index.h5','zz1000')
response_zz = requests.get(url1 + index_list[1], headers=header_req)
zz_res = response_zz.text.split(',')

if len(zz_res) >= 5:
	if float(zz_res[1]) != 0.0 and float(zz_res[8] > 0):	   
	    zz_date_list.append(zz_res[30])
	    zz_open_list.append(round(float(zz_res[1]),2))
	    zz_close_list.append(round(float(zz_res[3]),2))
	    zz_high_list.append(round(float(zz_res[4]),2))
	    zz_low_list.append(round(float(zz_res[5]),2))
	    zz_volume_list.append(int(zz_res[8]))
zz_temp = pd.DataFrame({'date':zz_date_list,'open':zz_open_list,'close':zz_close_list,\
						'high':zz_high_list,'low':zz_low_list,'volume':zz_volume_list})
zz_temp = zz_temp.set_index('date')
zz_temp.index = pd.to_datetime(zz_temp.index)
zz_temp = zz_temp[['open','close','high','low','volume']]
df_zz = pd.concat([df_zz,zz_temp])
df_zz = df_zz.drop_duplicates()
df_zz.to_hdf('all_index.h5','zz1000')
print 'zz1000 updating finished'









