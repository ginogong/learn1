#-*- coding:utf-8 -*-
import thread
import time
def foo():
	print 'foo'
	time.sleep(5)
	print 'done'

def boo():
	print 'boo'
	time.sleep(3)
	print 'boo done'

def main():
	thread.start_new_thread(foo,())
	thread.start_new_thread(boo,())
	time.sleep(10)
	print 'all done'

if __name__ == '__main__':
	main()
