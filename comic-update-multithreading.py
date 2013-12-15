#!/usr/bin/env python
#coding:utf-8

import re, ConfigParser, urllib2, threading, time

time_start = time.time()

regex = re.compile(r"img\s+src=\"([^\"]+)\"\s+alt=\"([^\"]+)")
regex2 = re.compile(r"span\s+class=\"gray12\">([^<]+)")
regex3 = re.compile(r"a\s+href=\"[^\"]+\"\s+target=\"[^\"]+\"\s+title=\"[^\"]+\"\s+class=\"[^\"]\"\s+>([^<]+)")
regex4 = re.compile(r"<li>([^<\+]+)")
regex5 = re.compile(r"a\s+target=\'[^\']+\'\s+title=\"([^(\")]+)\"\s+href=\"([^\"]+)\"s*>")
regex6 = re.compile(r"^\/([^\/]+/)")
regex7 = re.compile(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}")

conf = ConfigParser.ConfigParser()
conf.read("conf_comic")
section = "dmzj"

cfgDmjz = {}
for option in conf.options(section):
	cfgDmjz[option] = conf.get(section, option)

update_list = []
for i in xrange(1, 20):
	url = cfgDmjz["update"] + str(i) + ".shtml"
	#print url
	socket = urllib2.urlopen(url)
	if socket.geturl() != url:
		break
	update_list.append(url)

class FetchUpdateList(threading.Thread):
	def __init__(self, url, num):
		threading.Thread.__init__(self, name = num)
		self.url = url
		self.num = num
		self.running = True
		self.data = []
		self.maxsize = 0

	def run(self):
		time.sleep(1)
		print "开始采集第" + str(self.num) + "页更新列表"
		try:
			content = urllib2.urlopen(self.url).read()
		
			#封面图片地址，漫画名
			for x in regex.findall(content):
				self.data.append([x[0], x[1], "2", "3", "4", "5", "6", "7", "8"])

			self.maxsize = len(self.data)
			
			#作者
			for i, x in enumerate(regex2.findall(content)):
				self.data[i][2] = x
			
			#更新状态 漫画类型
			p = 0
			for i, x in enumerate(regex4.findall(content)):
				if( i > 1):
					if(i == 2):
						self.data[p][3] = x
					elif(i == 4):
						self.data[p][4] = x
						p += 1
					elif(i % 3 == 2):
						self.data[p][3] = x
					elif(i % 3 == 1):
						self.data[p][4] = x
						p += 1
	
				if p >= self.maxsize:
					break
				
			#更新卷
			for i, x in enumerate(regex5.findall(content)):
				self.data[i][5] = cfgDmjz["root"] + x[1]
				self.data[i][6] = x[0]
				self.data[i][7] = cfgDmjz["root"] + "/" + regex6.findall(x[1])[0]


			#更新时间
			for i, x in enumerate(regex7.findall(content)):
				self.data[i][8] = x

		except Exception, e:
			#pass
			print e

thread_pool = []
for i, x in enumerate(update_list):
	thread_pool.append(FetchUpdateList(x, i))
		
map(lambda x : x.start(),thread_pool)
map(lambda x : x.join(), thread_pool)

time_end = time.time()

f = open("update-list.txt", "w")

f.write("采集耗时: " + "%.3f" % (time_end - time_start) + "s" + "\n\n")
for i, thread in enumerate(thread_pool):
	f.write("---第 " + str(i + 1) + " 页更新列表---\n\n")
	for data in thread.data: 
		try:
			f.write("\n".join((data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])) + "\n\n")
		except:
			pass

f.close()
