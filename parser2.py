#!/usr/bin/env python
#encoding:utf-8

#div > p id = "da" > a text #div > p id = "da" > html 
from sgmllib import SGMLParser 
import urllib2, re

#抓取封面
#div 1 
#div class = "boxdiv1" > img src

#抓取漫画名
#div 2 li 1 a 1
#div class = "boxdiv1" > div class = "pictext" > ul > li > a text

#抓取作者
#div 2 li 2 span 1 
#div class = "boxdiv1" > div class = "pictext" > ul > li > span text

#抓取分类
#div 2 li 3
#div class = "boxdiv1" > div class = "pictext" > ul > li text

#抓取更新
#div 2 li 4 a 2
#div class = "boxdiv1" > div class = "pictext" > ul > li > a text 

#抓取状态
#div 2 li 5
#div class = "boxdiv1" > div class = "pictext" > ul > li > text 

#抓取时间
#div 2 li 6 span 2 
#div class = "boxdiv1" > div class = "pictext" > ul > li > span text 

class Parser(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)

		self.test_div = 0 
		self.test_li = 0
		self.test_a = 0
		self.test_span = 0

		self.test_end_div = 0 

		self.img = "" 
		self.name = "" 
		self.author = ""
		self.category = ""
		self.update = ""
		self.status = ""
		self.time = ""

		self.info = []

	def start_div(self, attrs):
		for k, v in attrs:
			if k == "class":
				if v == "boxdiv1":
					self.test_div = 1
				elif v == "pictext" and self.test_div == 1:
					self.test_div = 2
				
	def end_div(self):
		if self.test_div > 0:
			self.test_end_div += 1

		if self.test_end_div == 3:
			self.test_end_div = 0
			self.info.append((self.img, self.name, self.author, self.category, self.update, self.status, self.time))

	def start_img(self, attrs):
		if self.test_div == 1:
			for k, v in attrs:
				if k == "src":
					self.img = v
					
	def start_li(self, attrs):
		if self.test_div == 2:
			self.test_li += 1

	def end_li(self):
		if self.test_div == 2 and self.test_li == 6:
			self.test_li = 0

	def start_a(self, attrs):
		if self.test_li == 1:
			self.test_a = 1
		elif self.test_li == 4:
			self.test_a = 2

	def end_a(self):
		if self.test_a > 0:
			self.test_a = 0
	
	def handle_data(self, data):
		if len(data.strip()):
			if self.test_a == 1:
				self.name = data

			elif self.test_span == 1:
				self.author = data

			elif self.test_li == 3:
				self.category = data

			elif self.test_li == 5:
				self.status = data

			elif self.test_a == 2:
				self.update = data

			elif self.test_span == 2:
				self.time = data

	def start_span(self, attrs):
		if self.test_li == 2:
			self.test_span = 1
		elif self.test_li == 6:
			self.test_span = 2

	def end_span(self):
		if self.test_span > 0:
			self.test_span = 0

with open("input.txt") as f:
	content = f.read()

parser = Parser()
parser.feed(content)

with open("output.txt", "w") as f:
	for x in parser.info:
		for y in x:
			f.write(y + "\n")
		f.write("\n")
