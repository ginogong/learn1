# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:59:46 2018

@author: Gino
"""

from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import re
import pymongo
client = pymongo.MongoClient('localhost')
db = client['weixin']
base_url = 'http://weixin.sogou.com/weixin?'

headers = {
        'Cookie': 'CXID=955A9998149302D69A3FFC7B615321D0; SUID=AA93DDAB5B68860A5ABDF078000353A0; IPLOC=CN5101; SUV=00441786DA587C115ACC3F4C3596F068; sw_uuid=8846918407; cid=xm.click; ssuid=5593129501; dt_ssuid=7347698160; start_time=1526894139435; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ABTEST=0|1527047788|v1; SNUID=68BBF583292D45FFAD2A44ED2971CAF8; weixinIndexVisited=1; sct=1; JSESSIONID=aaax5wSEIyDynbodKLjnw; ppinf=5|1527051577|1528261177|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0Okdpbm98Y3J0OjEwOjE1MjcwNTE1Nzd8cmVmbmljazo0Okdpbm98dXNlcmlkOjQ0Om85dDJsdVBudVlwSDRNeS02aTIyRGZMRzU1TFFAd2VpeGluLnNvaHUuY29tfA; pprdig=VjPRWZX576mf4fVRbTWKw1jFp2728Ddpfzob_A9w27GpdHEjnqb3gH1Ma1TRIpU0mOYjiTLo1UQEKf_90FBZjjFSAwRQL_IW8nWxW4Cz3ojHgsIJSMCsblSItIP1AMsZ8qUd-BwlV967q2XwmTDAY0fLaZ-CAeNNXjfKgZiLokU; sgid=28-35201141-AVsE9TkicvHtFYoiatCNd2N3c; ppmdig=15270515780000001bc6545a30473754e729ef0fbc708e80',
        'Host': 'weixin.sogou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        
        }


keyword = "美女"
proxy_pool_url = 'http://127.0.0.1:5555/random'

proxy = None
max_count = 5



def get_html(url,count=1):
    print('crawling',url)
    print('Trying count:', count)
    global proxy
    if count >= max_count:
        print('Tried too many counts')
        return None
        
    try:
        if proxy:
            proxies = {
                    'http':'http://' + proxy
                    
                    }
            response = requests.get(url,allow_redirects=False, headers = headers,proxies=proxies)
        else:
            response = requests.get(url,allow_redirects=False, headers = headers)
        if response.status_code == 200:
            return response.text
        if response.status_code ==302:
            #Need Proxy
            print('302 is coming')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
    
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occured', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url,count)


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code ==200:
            return response.text
        return None
    except ConnectionError:
        return None



def get_index(keyword,page):
    data = {
            'query':keyword,
            'type':2,
            'page':page
            
            }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return(html)
    
    
def parse_index(html):
    doc = pq(html)
    #items = doc('.news-box .news-list li . txt-box h3 a ').items()
    items = doc('.news-box .news-list li .txt-box h3 a ').items()

    for item in items:
        yield item.attr('href')
        
def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def save_to_mango(data):
    if db['articles'].update({'title':data['title']},{'$set':data}, True):
        print('Save to Mongo ',data['title'])
    else:
        print('Saved to Mongo failed', data['title'])



def parse_detail(html):
    #print('Parsing')
    try:
        pattern = re.compile('var publish_time = "(.*?)".*?;')
        pattern_title = re.compile("_ios'>(.*?)</span>")
        doc     = pq(html)
        title   = doc('#img-content h2').text()
        
        title_content = pattern_title.findall(title)[0]

        content = doc('.rich_media_content ').text()
        date    = pattern.findall(doc.text())[0]
        nickname   = doc('.profile_container .profile_nickname ').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return  {
                'title':title_content,            
                'date':date,
                'nickname':nickname,
                'wechat':wechat,
                'content':content,
                }
    except Exception:
        return None
      
                

def main():
    for page in range(1,2):
        html = get_index(keyword, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    #print(html)
                    article_data = parse_detail(article_html)
                    #print()
                    if article_data:
                        save_to_mango(article_data)
             

    


if __name__ =='__main__':
    main()