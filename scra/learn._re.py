
import requests
import re
from bs4 import BeautifulSoup
url = 'http://quote.eastmoney.com/stocklist.html'
pattern = re.compile(r'<li.*?\((\d+)\).*?</li>')
html = requests.get(url).text
li = re.findall(pattern,html)
for i in range(20):
	print(li[i])
#soup = BeautifulSoup(html,'lxml')
#print(soup.prettify())