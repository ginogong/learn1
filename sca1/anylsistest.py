import numpy as np
import pyodbc
import matplotlib.pyplot as plt 

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.101;DATABASE=HTTPDB;UID=GDXGM_ADMIN;PWD=GDXGM_ADMIN2016')
cur = cnxn.cursor()
cur.execute("select RQ,KP,ZG,ZD,SP,CJL from T_GP_D1 WHERE GPDM='sz399300'and RQ >= '2015-01-01' and RQ <= '2016-01-01' order by RQ ")
df = cur.fetchall()
df = np.array(df)
df[:,1:6] = np.float64(df[:,1:6])
title = ['date','open', 'high','low','close','volume']
df = np.vstack((title,df))
high = df[1:,2]
low = df[1:,3]
closePr = df[1:,4]
pivots = (high + low + closePr) / 3

def fit_line(t,y):
	A = np.vstack([t,np.ones_like(t)]).T
	return np.linalg.lstsq(A,y) [0]

t = np.arange(len(closePr))
sa,sb = fit_line(t,pivots - (high - low))
ra,rb = fit_line(t,pivots + (high - low))
support = sa * t + sb 
resistance = ra * t + rb
condition = (closePr > support) & (closePr < resistance)
between_bands = np.where(condition)
between_bands = len(np.ravel(between_bands))
tomorrow_support = sa * (t[-1] + 1) + sb 
tomorrow_resistance = ra * (t[-1] + 1) + rb 
a1 = closePr[closePr > support]
a2 = closePr[closePr < resistance]
plt.plot(t,closePr)
plt.plot(t,support)
plt.plot(t,resistance)
plt.show()
 
cur.close()
cnxn.close()