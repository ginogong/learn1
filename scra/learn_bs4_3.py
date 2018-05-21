# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import re
from bs4 import BeautifulSoup
url = 'http://quote.eastmoney.com/stocklist.html'
html = requests.get(url).text
soup = BeautifulSoup(html,'lxml')

#CSS选择器 通过select()直接传入CSS选择器完成选择
#.代表Class  #代表id
#print(soup.select('.quotebody #quotesearch'))
'''
print(len(soup.select('ul li')))

print(soup.select('ul li')[20:30])
'''
#select 嵌套
'''
ul = soup.select('ul')
for li in ul:
    print(li.select('li'))
'''
#获取属性
ul = soup.select('ul')
for li in ul:
    print(li.get_text())

