#!/usr/bin/env python
#coding:utf-8

import re, ConfigParser, urllib2

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

f = open("input.txt")
content = f.read()
f.close()

data = []

#封面图片地址，漫画名
for i, x in enumerate(regex.findall(content)):
	data.append([x[0], x[1], "2", "3", "4", "5", "6", "7", "8"])

maxsize = len(data)

#作者
for i, x in enumerate(regex2.findall(content)):
	data[i][2] = x

#更新状态 漫画类型
p = 0
for i, x in enumerate(regex4.findall(content)):
	if( i > 1):
		if(i == 2):
			data[p][3] = x
		elif(i == 4):
			data[p][4] = x
			p += 1
		elif(i % 3 == 2):
			data[p][3] = x
		elif(i % 3 == 1):
			data[p][4] = x
			p += 1
	
	if p >= maxsize:
		break

#更新卷
for i, x in enumerate(regex5.findall(content)):
	#链接
	data[i][5] = cfgDmjz["root"] + x[1]
	#状态
	data[i][6] = x[0]
	#主页
	data[i][7] = cfgDmjz["root"] + "/" + regex6.findall(x[1])[0]

#更新时间
for i, x in enumerate(regex7.findall(content)):
	data[i][8] = x

f = open("update-output.txt", "w")

for i, x in enumerate(data):
	#if i > 5:
	#	break;
       	f.write("\n".join((x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])) + "\n\n")
	#print(" ".join((x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])) + "\n\n")

f.close()
