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
#print(soup.p) #查看TAG P
#print(soup.li.string) #查看TAG LI的内容
#print(soup.div.a) #查看DIV TAG下的A TAG
#print(soup.body.div.contents) #查看BODY 下DIV 的内容 包含换行符
# 用child方法查看子节点 返回为迭代器
'''
for i ,child in enumerate(soup,1):
    print(i,child)
'''
#用descendants 方法获取所有的子孙节点
'''
for i,child in enumerate(soup.body.div.descendants,1):
    print(i, child)
'''
#用next_siblings 获取后一个兄弟节点。 用previous_siblings获取前一个兄弟节点 
#返回是迭代器对象
'''
for i, item in enumerate(soup.body.div.next_siblings):
    print(i , item)
'''
#标准选择器
#find_all方法(name, attrs, recursive, text)
print(len(soup.find_all('li')))
li = soup.find_all('li')[20:30]
for i in li:
    print(i)