# -*- coding: utf-8 -*-

import pyodbc


cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.101;DATABASE=HTTPDB;UID=GDXGM_ADMIN;PWD=GDXGM_ADMIN2016')
cur = cnxn.cursor()
sql = "EXEC EOX.DBO.SP_ZH_AUTO_SC '%s' \
        \
        GO "
path = 'E:\\WORK\\autodata\\temp\\'
f = open(path + '1111.txt','r')
line = f.readlines()
for i in line:
    cur.execute(sql % i.strip())

cur.close()
cnxn.close()



