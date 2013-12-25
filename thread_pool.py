#!/usr/bin/env python
#encoding:utf-8

import Queue, threading, time, random

NUM_WORKERS = 3
thread_pool = []

class MyThread(threading.Thread):
	def __init__(self, queue, thread_no, processer):
		self.queue = queue
		self.thread_no = thread_no
		self.processer = processer
		threading.Thread.__init__(self, name = thread_no)

	def run(self):
		while self.queue.qsize() > 0:
			self.processer(self.queue.get(), self.thread_no)

def doTask(task, thread_no):
	time.sleep(random.random() * 3)
	print "doing", task, "thread_no", thread_no 

if __name__ == "__main__":
	print "begin..."
	q = Queue.Queue(0)

	map(lambda x : q.put(x), range(NUM_WORKERS * 2))
	print "job qsize:", q.qsize()
	map(lambda x : thread_pool.append(MyThread(q, x, doTask)), range(NUM_WORKERS))
	map(lambda x : x.setDaemon(True), thread_pool)
	map(lambda x : x.start(), thread_pool)
	map(lambda x : x.join(), thread_pool)
		
	print "done"
