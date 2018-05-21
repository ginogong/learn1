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

#标准选择器 
#attrs 按照tag的属性进行查找
'''
print(soup.find_all(attrs={'name':'sh'}))
print(soup.find_all(class_='sltit'))
print(type(soup.find_all(attrs={'name':'sh'})))
'''
#text 查找
print(soup.find_all(text='R003(201000)'))
print(type(soup.find_all(text='R003(201000)')))


#find 方法跟find_all类似 只是返回第一个元素 找不到返回None
#find_parent, find_parents, find_previous_siblings 用法完全类似


