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
#DOM操作
#addClass removeClass

#li.addClass('active')

#attr css
#li.attr('name','link')
#li.css('font-size','14px')
#remove
'''
li = doc('ul')
lists = li.find('li')
lists.find('a').remove()
for item in lists.items():
    print(item.text())
'''
#伪类选择器
#li:first-child  last-child   nth-child(2)  li:gt(2)  li:contains(str)
li = doc('li')
print((li('li:gt(2)')))




