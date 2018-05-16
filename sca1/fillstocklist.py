import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import create_engine,Table,MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pyquery import PyQuery as pq
import re
import requests

url = 'http://quote.eastmoney.com/stocklist.html'
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }

engine = create_engine("mysql://root:root@127.0.0.1/stock?charset=utf8", echo=True)
Base = declarative_base() 
Session = sessionmaker(bind=engine)
session = Session()

class Stock_list(Base):
	__tablename__ = 'stock_list'
	uid = Column(Integer, primary_key=True)
	code = Column(String(20))

	def __repr__(self):
		return "<Stock_list(code='%s')>" % self.code

#Base.metadata.create_all(engine)
response = requests.get(url, headers=header_req)
response.encoding = 'gbk'
data = pq(response.text)
pattern = re.compile(u"\d{6}")
for item in data('#quotesearch ul a'):
	if pattern.findall(pq(item).text())[0][0:3] in ['600', '603', '601', '300', '002', '000']:
		sl = Stock_list()
		sl.code = pattern.findall(pq(item).text())[0]
		if sl.code != session.query(Stock_list).filter(Stock_list.code == sl.code):
			session.add(sl)
session.flush()
session.commit()

