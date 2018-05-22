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


url = "http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
#支持浏览器 声明对象
browser = webdriver.Chrome()
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
 #交互动作                                       
target = browser.find_element_by_css_selector('#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(source,target)
actions.perform()
#元素交互动作  模拟输入
'''
input1 = browser.find_element(By.ID,'q')
input1.send_keys('TV')
time.sleep(1)
input1.clear()
input1.send_keys('MI')
button = browser.find_element_by_class_name('btn-search')
button.click()
'''


#browser.close()


























