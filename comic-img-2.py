#!/usr/bin/env python
#encoding:utf-8
'''
完成一个章回的图片多线程下载

依赖spidermonkey库
'''

import threading, re, urllib, urllib2, ConfigParser, string, os, time
from spidermonkey import Runtime

#过滤图片URL列表
regex = re.compile(r"eval(.+)")
#过滤漫画名
regex2 = re.compile(r"g_comic_name\s=\s\"([^\"]+)\"")
#过滤章回
regex3 = re.compile(r"g_chapter_name\s=\s\"([^\"]+)\"")
#过滤图片类型
regex4 = re.compile(r"(\w+)")

cfg = {}
conf = ConfigParser.ConfigParser()
conf.read("conf_comic")
section = "dmzj"
for option in conf.options(section):
	cfg[option] = conf.get(section, option)	


socket = urllib2.urlopen(cfg["test_url_img"])
content = socket.read()
socket.close()

rt = Runtime()
cx = rt.new_context()
rs = regex.findall(content)[0]

urls_img = list(cx.eval_script("eval(" + rs + ");eval(pages);"))
urls_img = map(lambda x : cfg["root_img"] + x, urls_img)
name_comic = regex2.findall(content)[0]
name_chapter = regex3.findall(content)[0]


class ComicDownload(threading.Thread):
	def __init__(self, url, localfile):
		threading.Thread.__init__(self, name = url)
		self.url = url
		self.localfile = localfile
	
	def run(self):
		try:
			time.sleep(5)
			urllib.urlretrieve(self.url, self.localfile)
		except Exception, e:
			print e

thread_pool = []
try:
	os.mkdir(name_comic)
	path = "/".join((name_comic, name_chapter))
	os.mkdir(path)

	for i, x in enumerate(urls_img):
		type_img = regex4.findall(x)[-1]
		filename = ".".join((str(i + 1), type_img))
		thread_pool.append(ComicDownload(x, "/".join((path, filename))))
		
	map(lambda t : t.start(), thread_pool)
	map(lambda t : t.join(), thread_pool)

except Exception, e:
	print e
