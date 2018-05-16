#coding=utf-8 
import pyodbc
import sys
import tushare as ts
import numpy as np
import pandas as pd


reload(sys)
sys.setdefaultencoding('utf8')

df = ts.get_report_data(2015,4)
df =df[['code','eps']]

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SIGMA-DT-01;DATABASE=STOCKDB;UID=sa;PWD=tomeko123')
cursor = cnxn.cursor()

for i in range(len(df)):
	STR1 = df['code'].iloc[i]
	if df['eps'].iloc[i] == df['eps'].iloc[i]:
		query = "IF NOT EXISTS(SELECT 1 FROM T_GP_MGSY WHERE GPDM='%s' AND RQ='%s')" % (STR1,'2015-12-31')
		query += "INSERT INTO T_GP_MGSY(GPDM,RQ,MGSY)  VALUES('%s','%s',%f)" % (STR1, '2015-12-31', df['eps'].iloc[i])
		cursor.execute(query)
	if df['eps'].iloc[i] == df['eps'].iloc[i]:
		query += "INSERT INTO T_GP_MGSY(GPDM,RQ,MGSY)  VALUES('%s','%s',%f)" % (STR1, '2015-12-31', df['eps'].iloc[i])
		cursor.execute(query)


#cursor.close()
cnxn.commit()
cnxn.close()
