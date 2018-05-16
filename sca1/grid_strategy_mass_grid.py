from __future__ import division
import tushare as ts 
import pandas as pd 
import numpy as np 
import threading
pd.set_option('precision',6)


#print data['price'].quantile([0.1,0.9])
#print data
path = 'E:\\WORK\\stock\\'
grid_low  = 99.90
grid_high = 100.05
grid_step = 0.001

lows = int((grid_low+grid_step) * 1000)
highs = int((grid_high+grid_step) * 1000)
vec = pd.DataFrame({'buy':[],'sell':[]})


for low in range(lows,highs):
	vec_sell = range(low,highs)
	vec_temp = pd.DataFrame({'sell':vec_sell})
	vec_temp['sell'] = vec_temp['sell'] / 1000.0
	vec_temp['buy'] = low /1000 - grid_step
	vec = pd.concat([vec,vec_temp])
vec = vec.drop_duplicates()
vec.index = range(len(vec))

total_number = len(vec)
seqs = range(0,6)

class Thread_mass_grid(threading.Thread):
    def __init__(self,number):
        threading.Thread.__init__(self)
        self.number = number
    def run(self):
        if self.number < 5:
            for i in range(self.number*2000 + 2000):
                data = pd.read_hdf(path + 'tick.h5','511990')
                vec.ix[i,'number'] = signal(vec.ix[self.number*2000+i,:],data)
                vec['number'].fillna(0,inplace=True)
                print 'finished %s in %s' % (i, 2000)
        else:
            for i in range(self.number*2000 + 1326):
                data = pd.read_hdf(path + 'tick.h5','511990')
                vec.ix[i,'number'] = signal(vec.ix[self.number*2000+i,:],data)
                vec['number'].fillna(0,inplace=True)
                print 'finished %s in %s' % (i, 2000)
        
    

#print vec
# grid coloumns   price_buy  price_sell quantity

def signal(vec,df):
	df.ix[df['price'] < vec['buy'],'temp'] = 0 
	df.ix[df['price'] > vec['sell'],'temp'] = 1
	df['temp'].fillna(method='pad',inplace=True)
	df.ix[df['temp'] < df['temp'].shift(1),'change'] = 1
	df['change'].fillna(0,inplace=True)
	df['change'] = df['change'].cumsum()
	df.index = range(len(df))
	return int(df.ix[len(df)-1,'change'])




for i in range(len(vec)):
	data = pd.read_hdf(path + 'tick.h5','511990')
	vec.ix[i,'number']= signal(vec.ix[i,:],data)
	vec['number'].fillna(0,inplace=True)
	print 'finished %s in %s' % (i, len(vec))

vec.to_csv(path + 'mass_grid_data.csv')



