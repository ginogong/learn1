import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tushare as ts 
import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine,Table,MetaData, Column, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mysql import DOUBLE,DATE
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:root@127.0.0.1/stock?charset=utf8")
Base = declarative_base()

class Stock_list(Base):
	__tablename__ = 'stock_list'
	uid = Column(Integer, primary_key=True)
	code = Column(String(20))

	def __repr__(self):
		return "<Stock_list(code='%s')>" % self.code

class Day_k(Base):
	__tablename__ = "day_k"
	_uid_ = Column(Integer, primary_key=True)
	date = Column(DATE)
	open_price = Column(DOUBLE())
	high_price = Column(DOUBLE())
	close_price = Column(DOUBLE())
	low_price = Column(DOUBLE())
	volume = Column(DOUBLE())
  	code = Column(String(20))

	def __repr__(self):
		return "<Day_k(code='%s'>" % self.code

def init_db():
	Base.metadata.create_all(engine)
def drop_db():
	Base.metadata.drop_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
init_db()
for instance in session.query(Stock_list):
	print 'proceeding %s' % instance.code
	print '\n'
	s1 = session.query(Day_k.volume).filter(Day_k.code==instance.code).filter(Day_k.date=='2016-10-31')
	if len(s1.all()) < 1:
		df = ts.get_k_data((str(instance.code)),start='2013-01-01', end='2016-10-31')
		if type(df) != type(None):
			df.columns = ['date', 'open_price', 'high_price', 'close_price', 'low_price', 'volume', 'code']
			df.to_sql('day_k',engine,if_exists='append')
			session.execute('''delete from day_k where uid in (select * from(select max(uid) from day_k group by date, code having count(date)>1) as b)''')
			session.flush()
			session.commit()
			print '\n'
			print '%s day data finishing!' % instance
			print '\n'

