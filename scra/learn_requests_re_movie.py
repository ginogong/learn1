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

def get_one_page(url):
    headers = {'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36''',\
           'Referer': 'http://maoyan.com/board/4',
          }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None
def parse_one_page(html):
    pattern1 = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?img data-src="(.*?)".*?'
                         + 'name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)

    pattern2 = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?img data-src="(.*?)".*?'
                          +'name"><a.*?>(.*?)</a>.*?</dd>',re.S)    
    items = re.findall(pattern1, html)
    for item in items:
        yield{
                'index':item[0],
                'image':item[1],
                'title':item[2],
                'stars':item[3].strip()[3:],
                'time':item[4].strip()[5:],
                'score':item[5]+item[6]
                }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + "\n")
   
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        write_to_file(item)
    
if __name__=='__main__':
    
    pool = Pool(10)
    pool.map(main,[i*10 for i in range(10)])


      
      

























