#encoding=utf-8
from urllib import urlopen
'''
def reporthook(block_count, block_size, file_size):
	if file_size == -1:
		print "retrieved data", block_count*block_size
	else:
		percentage = int((block_count*block_size*100.0)/file_size)
		if percentage > 100:
			print '100%'
		else:
			print '%d%%' % percentage

		

url = urlretrieve('http://www.python.org', filename='', reporthook=reporthook)
'''
'''
r = urlopen("http://www.baidu.com")
#print type(r)
#print r.geturl()
#print r.url
#m = r.info()
'''
'''
for k,v in m.items():
	print k,'=', v
'''
import httplib
print help(httplib)