# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sqlalchemy as sa 
import pandas as pd 
from sqlalchemy import create_engine 
import pyodbc

#engine = create_engine('mssql+pymssql://GDXGM_GW:GDXGM2017@192.168.1.101/HTTPDB')
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.101;DATABASE=HTTPDB;UID=GDXMG_GW;PWD=GDXGM2017')
sql = "select * from T_GP_RNLZZB;"	
cur = cnxn.cursor()
cur.execute(sql)
df = cur.fetchall()
df = pd.DataFrame(df)
#df = pd.read_sql(sa.text('select RQ from T_GP_RNLZZB'),cnxn,chunksize=10000)

print df[0:10]
