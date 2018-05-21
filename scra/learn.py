
import requests
import re
from bs4 import BeautifulSoup
url = 'http://quote.eastmoney.com/stocklist.html'
html = requests.get(url).text
soup = BeautifulSoup(html,'lxml')
print(soup.prettify())