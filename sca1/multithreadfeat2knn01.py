#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
from sklearn import neighbors
import threading
import time
#----setting------
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)
#-----------------

#get data
data = pd.read_hdf('ml.h5','feature')
data.pop('change')
data.pop('all_a')
col_data = list(data.columns)
label = pd.read_hdf('ml.h5','label')
label.pop('change')
label.pop('all_a')

col_label = list(label.columns)
feat_all = col_data[:2]
feat_sma_change = col_data[2:8]
feat_prd_change = col_data[8:11]
feat_prd_amp = col_data[11:15]
feat_vol_change = col_data[15:19]

#feature classify
#1 all_a  -  hs300    change    and  all_a - zz1000 change      2
#2 hs300 sma period change  - zz1000 sma period change          6
#3 hs300 period change - zz1000 period change					3
#4 hs300 period amplitude - zz1000 period amplitude				4
#5 hs300 sma period change - zz1000 sma period change			4
#---- split data set
def split_data(df,start='2010-01-04',end='2014-12-30'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df
def auto_norm(df):
	df1 = df.copy()
	for i in  list(df.columns):
		df1[i] = (df[i] - df[i].min()) / (df[i].max() - df[i].min())
	return df1


class Thread_knn(threading.Thread):
	def __init__(self,index,create_time):
		threading.Thread.__init__(self)
		self.index = index
		self.create_time = create_time
	def run(self):
		k = range(5,30)
		num = 200
		for i in k:
			for j in col_label:
				for item2 in feat_prd_change:
					for item3 in feat_prd_amp:
						for item4 in feat_vol_change:
							print '\n the %s thread is processing' % self.index
							flag = []
							training_label = split_data(label)
							training = training_data[[feat_all[0],feat_all[1],self.index,item2,item3,item4]]
							classify = classify_data[[feat_all[0],feat_all[1],self.index,item2,item3,item4]]
							times = int(round(len(classify) / num)) + 1
							clf = neighbors.KNeighborsClassifier(i,weights='uniform')
							#clf.fit(training,training_label[j])
							for it in range(times):
								srt_num = it * num
								end_num = (it + 1) * num 
								classify_temp = classify[srt_num:end_num]
								classify_label_temp = classify_label[srt_num:end_num] 
								if len(classify_temp) > 0 :

									clf.fit(training,training_label[j])
									z = clf.predict(classify_temp)
									flag.extend(z)
									training = pd.concat([training,classify_temp])
									training_label = pd.concat([training_label,classify_label_temp])
								

							classify_label['z'] = flag
							num_right = len(classify_label[classify_label[j] == classify_label['z']])
							num_total = len(classify_label)
							ratio = num_right / num_total
							win_rate.append(ratio)
							feat_sma_change_list.append(self.index)
							feat_prd_change_list.append(item2)
							feat_prd_amp_list.append(item3)
							feat_vol_change_list.append(item4)
							k_list.append(i)
							label_list.append(j)
							print '\n the %s thread is finishing' % self.index,time.time() - self.create_time
							self.create_time = time.time()


data1 = auto_norm(data)
training_data = split_data(data1)
#training_label = split_data(label)

classify_start = '2015-01-01'
classify_end = '2017-02-10'
classify_data = split_data(data1,start=classify_start,end=classify_end)
classify_label = split_data(label,start=classify_start,end=classify_end)

#neighbors calcalute

feat_all_list = []
feat_sma_change_list = []
feat_prd_change_list = []
feat_prd_amp_list = []
feat_vol_change_list = []
k_list = []
win_rate = []
label_list = []
number_list = []
run_time = 1
		
threads = []
for item in feat_sma_change:
	thread = Thread_knn(item,time.time())
	thread.start()
	threads.append(thread)

for t in threads:
	t.join()

print len(k_list)
print k_list 
df = pd.DataFrame({'k':k_list,'label':label_list,'sma_change':feat_sma_change_list,\
					'prd_change':feat_prd_change_list,'prd_amp':feat_prd_amp_list,\
					'vol_change':feat_vol_change_list,'win_rate':win_rate})
df.to_csv('feature011.csv')






