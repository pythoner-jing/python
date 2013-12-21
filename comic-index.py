#/usr/bin/env python
#coding:utf-8

'''
解析漫画主页
包括封面、章回、作者、连载状态、分类、漫画名、最新更新
'''

import urllib2, urllib, re

#过滤封面
regex = re.compile(r"<a\shref=\"[^\"]+\"><img\salt=\"[^\"]+\"\ssrc=\"([^\"]+)\"\sid=\"cover_pic\"/></a>")
#过滤作者
regex2 = re.compile(r"<td><a\shref=\'[^\']+\'>(.+)</a><br/></td>")
#过滤漫画名
regex3 = re.compile(r"g_comic_name\s=\s\"([^\"]+)\"")
#过滤连载状态
regex4 = re.compile(r"<td><a\shref=\"[^\"]+\"\salt=\"[^\"]+\">(.+)</a></td>")
#过滤分类
regex5 = re.compile(r"<td><a\stitle=\'[^\']+\'\shref=\'[^\']+\'>(.+)</a></td>")
#过滤新添章回
regex6 = re.compile(r"<li><a\stitle=\"[^\"]+\"\shref=\"([^\"]+)\"\s+class=\"color_red\">(.+)</a></li>")
#过滤章回
regex7 = re.compile(r"<li><a\stitle=\"[^\"]+\"\shref=\"([^\"]+)\"\s*>(.+)</a></li>")
#过滤最新章回
regex8 = re.compile(r"g_last_update\s=\s\"([^\"]+)\"")

url_test = "http://manhua.dmzj.com/meishidefulu/"

socket = urllib2.urlopen(url_test)
content = socket.read()
socket.close()

cover = regex.findall(content)[0]
author = regex2.findall(content)[0]
name = regex3.findall(content)[0]
status = regex4.findall(content)[1]
category = regex5.findall(content)[0]
update = regex6.findall(content)
lastupdate = regex8.findall(content)[0]
chapters0 = regex7.findall(content)

chapters = []
for x in chapters0:
	chapters.append((x[0], x[1]))

for x in update:
	chapters.append((x[0], x[1]))

with open("output.txt", "w") as f:
	f.write("封面 - " + cover + "\n")
	f.write("漫画名 - " + name + "\n")
	f.write("作者 - " + author + "\n")
	f.write("分类 - " + category + "\n")
	f.write("连载状态 - " + status + "\n")
	f.write("最新更新 - " + lastupdate + "\n")
	for x in chapters:
		f.write(" ".join((x[0], x[1])) + "\n")
