# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#basic demo
import requests
import re
from requests.exceptions import RequestException
import json
from multiprocessing import Pool
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pymongo
from config import *
from hashlib import md5
import os 
from json.decoder import JSONDecodeError

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
            'offset': offset,
            'format': 'json',
            'keyword':keyword,
            'autoload': 'true',
            'count': '20',
            'cur_tab': 1
            }
    url = "https://www.toutiao.com/search_content/? " + urlencode(data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/66.0.3359.181 Safari/537.36',
               'Referer': 'https://www.toutiao.com/search/'
            }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None
    
def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                #print(item.get('article_url'))
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/66.0.3359.181 Safari/537.36',
               'Referer': 'https://www.toutiao.com/search/'
            }
        try:
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                #print(response.text)
                return response.text
            return None
        except RequestException as e:
            print('request website  missing:',url)
            return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)
    if soup:
        title = soup.select('title')[0].get_text()
        image_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),',re.S)
        result = re.search(image_pattern, html)

   
    if result:
        json_data = re.sub(r'\/','',result.group(1))

        json_data2 = json_data.replace(r'\"','"')
        
        json_data2 = json_data2.replace(r'\u','u')
        
        #data = eval(json_data2)
        data = json.loads(json_data2)
        

        if data and 'sub_images' in data.keys():

            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            #print(images)
            return {
                    'title':title,
                    'url':url,
                    'images':images,
                    }
def download_image(url):
    print('正在下载：', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
           AppleWebKit/537.36 (KHTML, like Gecko) \
           Chrome/66.0.3359.181 Safari/537.36',
           'Referer': 'https://www.toutiao.com/search/'
        }
    
    try:
        response = requests.get(url,headers=headers)
        
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException as e:
        print('请求图片出错:',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            
            f.write(content)
    



def save_to_mongo(result):     
    if db[MONGO_TABLE].insert(result):
        #print('存储到MONGODB成功',result)
        return True
    return False
    
def main(offset):
    html = get_page_index(offset,KEY_WORD)
    for url in parse_page_index(html):
        if url:
            print(url)
            html =get_page_detail(url)
            if html:
                print(html)
            result = parse_page_detail(html,url)
            if result:
                 #print(result)
                 save_to_mongo(result)
                 pass
if __name__ == "__main__":
    groups = [x*20 for x in range(GROUP_START,GROUP_END +1)]
    pool = Pool(5)
    pool.map(main,groups)    
      

























