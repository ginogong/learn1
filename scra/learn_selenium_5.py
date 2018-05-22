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
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException


#选项卡管理
'''
url1 = "https://www.taobao.com/"
url2 = "https://www.baidu.com/"
url3 = "https://www.python.org/"
browser = webdriver.Chrome()
browser.get(url1)
browser.execute_script('window.open()')
time.sleep(1)
browser.switch_to_window(browser.window_handles[1])
browser.get(url2)
time.sleep(2)
browser.switch_to_window(browser.window_handles[0])
browser.get(url3)  
'''
#异常处理
browser = webdriver.Chrome()
try:
    browser.get('http://www.baidu.com')
except TimeoutException:
    print('Time out')
try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()
      
      
      
      
      
      
      
#browser.close()


























