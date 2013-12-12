#!/usr/bin/env python
#coding:utf-8

import threading
import time
import thread

p = 0
lst = [1, 2, 3, 4, 5]

lock = threading.RLock()

def foo(threadname):
	global p
	print threadname, lst[p]
	p += 1

class MyThread(threading.Thread):
	def __init__(self, threadname):
		threading.Thread.__init__(self, name = threadname)
		self.running = True
	
	def run(self):
		while self.running:
			lock.acquire()
			if p < len(lst):
				foo(self.getName())
			else:
				self.running = False
			lock.release()
			time.sleep(1)
			
if __name__ == "__main__":
	thread1 = MyThread("thread 1")
	thread2 = MyThread("thread 2")
	thread1.start()
	thread2.start()
