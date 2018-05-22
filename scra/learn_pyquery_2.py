# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
url = 'http://quote.eastmoney.com/stocklist.html'

#通过requests请求方式

#html = requests.get(url).content.decode('gbk')
html = requests.get(url).content.decode('gbk')

doc = pq(html)

#东方财富用gbk来进行中文的解码
#遍历 .items()
'''
ul = doc('ul').items()
print(type(ul))
for item in ul:
    print(item)
'''
#获取信息
#获取属性
'''
ul = doc('ul')
lists = ul.find('li a ').items()
for li in lists:
    print(li.attr.href)
'''
#获取文本 .text()
'''
ul = doc('ul')
lists = ul.find('li a ').items()
for li in lists:
    print(li.text())
'''
#获取HTML
ul = doc('ul')
lists = ul.find('li').items()
for li in lists:
    print(li.html())
    






