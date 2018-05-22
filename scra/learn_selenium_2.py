# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#basic demo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url = 'http://quote.eastmoney.com/stocklist.html'
url_baidu = 'http://www.baidu.com'
url_taobao = "http://www.taobao.com"
#支持浏览器 声明对象
browser = webdriver.Chrome()
#browser = webdriver.Firefox()
#browser = webdriver.Edge()
#browser = webdriver.PhantomJS()
#browser = webdriver.Safari()

#获取网页对象
browser.get(url_taobao)
ps =browser.page_source
#查找元素
#单个元素
'''
input_first  = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third  = browser.find_element_by_xpath('//*[@id="q"]')
print(input_first)
print(input_second)
print(input_third)
#其他查找 by_name by_xpath  by_link_text  by_partial_link_text 
#by_tag_name  by_class_name       by_css_selector
input_first1 = browser.find_element(By.ID,'q')
'''
#多个元素查找  类似与单个元素查找  返回列表
lis = browser.find_elements_by_css_selector('.service-bd li')
#lis = browser.find_elements(By.CSS_SELECTOR,'.service-bd li')
print(lis)
browser.close()



