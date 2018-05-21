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
html = requests.get(url).text

doc = pq(html)

#东方财富用gbk来进行中文的解码
#通过pq直接请求方式  不容易解码
#doc = pq(url=url)

#print(doc('li'))
#print(type(doc))

#文件初始化 file=filename
#基本CSS 选择器  # . tag 不一定是父子关系， 只要是层级关系就可以
#doc(.class_ #id  li)

#查找元素
ul = doc('ul')
lists = ul.find('li a ')
print(len(lists))




