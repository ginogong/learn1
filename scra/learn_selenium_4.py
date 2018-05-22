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
import time
from selenium.webdriver import ActionChains


url = "https://www.taobao.com/"

browser = webdriver.Chrome()

#执行JAVASCRIPT
'''
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
'''
#获取元素信息
#获取属性
#logo = browser.find_element_by_id('zh-top-link-logo')
#print(logo)
#print(logo.get_attribute('class'))
#获取文本 ID 位置 标签名 大小
'''
text1 = browser.find_element_by_class_name('zu-top-add-question')
print(text1.id)
print(text1.location)
print(text1.tag_name)
print(text1.size)
print(text1.text)
'''
#隐式等待
'''
browser.implicitly_wait(10)
browser.get(url)   
input1 = browser.find_element_by_class_name('zu-top-add-question')
print(input1)   
'''
#显式等待
'''
browser.get(url) 
wait = WebDriverWait(browser,10)
input1 = wait.until(EC.presence_of_element_located((By.ID,'q')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'btn-search')))
print(input1, button)
'''
#Cookie操作

url_zh = "https://www.zhihu.com/explore"
browser.get(url_zh)
browser.add_cookie({'name':'name','domain':'www.zhihu.com','value':'gino'})
print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())


      
      
      
      
      
      
      
#browser.close()


























