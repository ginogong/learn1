import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tushare as ts 
import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine,Table,MetaData, Column, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mysql import DOUBLE,DATE,BIGINT, TEXT
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')
Base = declarative_base(bind=engine)
Session = sessionmaker()
session = Session()
year_list = [2013,2014,2015]
quarter_list = [1,2,3,4]
for year in year_list:
	print year
	print type(year)
	for quarter in quarter_list:
		print quarter
		print type(quarter)
		df = ts.get_report_data(year,quarter)
		df = df[['code','eps','eps_yoy','report_date']]
		df['date'] = '%s-%s' % (str(year),str(quarter))
		df.to_sql('report_table',engine,if_exists='append')
