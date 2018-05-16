import time ,threading
'''
balance = 0 
lock = threading.Lock()

def change_it(n):

	global balance
	balance = balance + n 
	balance = balance - n 

def run_thread(n):

	for i in range(1000):
		lock.acquire()
		try:
			change_it(n)
		finally:
			lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print balance
'''

local_school = threading.local()

def process_student():
	print 'hello, %s(in %s)' % (local_school.student, threading.current_thread().name)

def process_thread(name):
	local_school.student = name 
	process_student()


t1 = threading.Thread(target = process_thread, args =( 'Alice',), name='Thread-A')
t2 = threading.Thread(target = process_thread, args =('Bob',) , name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()




















