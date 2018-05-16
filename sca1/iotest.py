import tushare as ts 
import numpy as np 
import pandas as pd 


hs300 = ts.get_hist_data('hs300')
hs300 = hs300.sort_text()
print hs300.tail()