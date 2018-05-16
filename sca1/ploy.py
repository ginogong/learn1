import numpy as np
import pyodbc
import matplotlib.pyplot as plt 

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.101;DATABASE=HTTPDB;UID=GDXGM_ADMIN;PWD=GDXGM_ADMIN2016')
cur = cnxn.cursor()
cur.execute("select RQ,KP,ZG,ZD,SP,CJL from T_GP_D1 WHERE GPDM='sz300013'and RQ >= '2016-01-01' and RQ <= '2016-05-01' order by RQ ")
df = cur.fetchall()
df = np.array(df)
df[:,1:6] = np.float64(df[:,1:6])
title = ['date','open', 'high','low','close','volume']
XNWL = np.vstack((title,df))
XNWL_CL = XNWL[1:,4]


cur.execute("select RQ,KP,ZG,ZD,SP,CJL from T_GP_D1 WHERE GPDM='sz002183'and RQ >= '2016-01-01' and RQ <= '2016-05-01' order by RQ ")
df = cur.fetchall()
df = np.array(df)
df[:,1:6] = np.float64(df[:,1:6])
title = ['date','open', 'high','low','close','volume']
YYT = np.vstack((title,df))
YYT_CL = YYT[1:,4]
cur.close()
cnxn.close()
t = np.arange(len(YYT_CL))
poly = np.polyfit(t,XNWL_CL - YYT_CL,3)
der = np.polyder(poly)
vals = np.polyval(poly,t)
plt.plot(t,XNWL_CL - YYT_CL )
plt.plot(t,vals)
plt.show()
print np.polyval(poly,t[-1] + 1)