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
browser = webdriver.Chrome()
try:
    browser.get(url_baidu)
    inpu = browser.find_element_by_id('kw')
    inpu.send_keys('Python')
    inpu.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    #print(browser.page_source)
finally:
    browser.close()





