
import tushare as ts
import numpy as np
import time

path = 'E:\\WORK\\autodata\\data\\'
grid = 0.003
volume_num = 500
pluse_num = 0
chance_num = 0


def vwap(num,volume):
	if volume  > (num + 1) * volume_num :
		num += 1
		return True
	else:
		return False
	time.sleep(3)

def trade_strategy(chance,price,weightp,weightp15,relative,vol_a,vol_cur):
	#'normal type'
	if (price <= weightp * (1 + 5 * grid) and price >= weightp * (1 + 1 *grid) ):   
		' limit order sell 1lot'
		'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
		chance += 1
	elif (price <= weightp * (1 - 1 * grid) and price >= weightp * (1 -5 *grid) ):
		'limit order buy 1lot'
		'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
		chance += 1
	elif (price > weightp * (1 - 1 * grid) and price < weightp * (1 + 1 *grid)):
		'no trading chance'
		pass 
		#'trending'
	else:
		if (abs(0.5 - relative) < 0.1 and vol_cur > 3 * vol_a) :
			if relative > 0.5:
				'buy at sell1 , 5 lot;sell at sell1 + grid , 5lot'
				chance += 1
			if relative < 0.5:
				'sell at buy1 , 5 lot; buy at buy1 - grid, 5lot'
				chance += 1
		else:
			if (price <= weightp15 * (1 + 5 * grid) and price >=  weightp15 * (1 + 1 *grid) ):
				' limit order sell 1lot'
				'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
				chance += 1
			elif (price <= weightp15 * (1 - 1 * grid) and price >=  weightp15 * (1 -5 *grid) ):
				'limit order buy 1lot'
				'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
				chance += 1
			else:
				'no trading chance'
				pass
	return chance

if __name__ == '__main__':
	while True:
		df = ts.get_tick_data('300017',date='2016-07-29')
		df1 = df[['time','price','volume']]
		now_price = df1['price'][0]
		num = len(df1)
		index2 = np.arange(num-1,-1,-1)
		df2 = df1
		df2.index = index2
		df2 = df2.sort_index()
		weight_price = np.sum(df2['price'] * df2['volume']) / np.sum(df2['volume'])
		volume_total = np.sum(df2['volume'])
		high = np.max(df2['price'])
		low = np.min(df2['price'])
		relative_position = (now_price - low ) / (high - low)
		volume_avg = np.mean(df['volume'])
		volume_cur = np.mean(df['volume'].head(30))
		weight_price100 = np.sum(df['price'].head(100) * df['volume'].head(100)) / np.sum(df['volume'].head(100))

		sig = vwap(pluse_num,volume_total)
		if sig:
			chance_num = trade_strategy(chance_num,now_price,weight_price,weight_price100,relative_position,volume_avg,volume_cur)
			print chance_num 


