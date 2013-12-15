#!/usr/bin/env python
#coding:utf-8

import re, ConfigParser

regex = re.compile("img\s+src=([^\s]+)\s+alt=([^\/]+)")
regex2 = re.compile("span\s+class=\"gray12\">([^<]+)")
regex3 = re.compile("a\s+href=[^\s]+\s+target=[^\s]+\s+title=[^\s]+\s+class=[^>]+>([^<]+)")
regex4 = re.compile("<li>([^<]+)")
regex5 = re.compile("a\s+target=[^s]+\s+title=[^\s]+\s+href=([^>]+)>([^<]+)")
regex6 = re.compile("^\/([^\/]+/)")
regex7 = re.compile("\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}")

conf = ConfigParser.ConfigParser()
conf.read("conf_comic")
section = "dmzj"

cfgDmjz = {}
for option in conf.options(section):
	cfgDmjz[option] = conf.get(section, option)

f = open("content-dmzj.txt")
content = f.read()
f.close()

data = []

#封面图片地址，漫画名
for x in regex.findall(content):
	data.append([x[0].replace("\"", ""), x[1].replace("\"", ""), 2, 3, 4, 5, 6, 7, 8])

maxsize = len(data)

#作者
for i, x in enumerate(regex2.findall(content)):
	data[i][2] = x

#更新状态 漫画类型
p = 0
for i, x in enumerate(regex4.findall(content)):
	if(i % 3 == 1):
		data[p][3] = x
	elif(i % 3 == 2):
		data[p][4] = x
		p += 1
	
	if p >= maxsize:
		break

#更新卷
for i, x in enumerate(regex5.findall(content)):
	data[i][5] = cfgDmjz["url"] + x[0].replace("\"", "")
	data[i][6] = x[1]
	data[i][7] = cfgDmjz["url"] + "/" + regex6.findall(x[0].replace("\"", ""))[0]

#更新时间
for i, x in enumerate(regex7.findall(content)):
	data[i][8] = x

f = open("update-output.txt", "w")

for x in data:
	f.write("\n".join((x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])) + "\n\n")

f.close()
