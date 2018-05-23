# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:12:25 2018

@author: Gino
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
from pyquery import PyQuery as pq
import pymongo
from congfig_taobao import *
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]



browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser,10)

#browser.set_window_size(1400,900)


def search():
    print('正在收索')
    try:
        browser.get('https://www.taobao.com')
        input1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input1.send_keys(KEY_WORD)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        time.sleep(5)
        return search()     

def next_page(page_number):
    print('当前正在翻页到：%s'% page_number)
    try:
        input1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,' #mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input1.clear()
        input1.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        time.sleep(5)
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
                'image':item.find('.pic .img').attr('src'),
                'price':item.find('.price').text().strip(),
                'deal':item.find('.deal-cnt').text()[0:-3],
                'title':item.find('.title').text(),
                'shop':item.find('.shop').text(),
                'location':item.find('.location').text()
                
                }
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存到MONGODB成功', result)
    except Exception:
        print('保存到MONGODB失败')
 


     
def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total+1):
            next_page(i)
    except Exception:
        print('出错了')
    finally:
        browser.close()
    
    
if __name__=='__main__':
    main()