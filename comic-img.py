#!/usr/bin/env python
#encoding:utf-8

import re, urllib, urllib2, cookielib, ConfigParser, string

regex = re.compile(r"return p}.+\[(.+)\]")
regex2 = re.compile(r"\'([\w+\|]+)\'")
regex3 = re.compile(r"%\w")

conf = ConfigParser.ConfigParser()
conf.read("conf_comic")

section = "dmzj"
cfg = {}
for option in conf.options(section):
	cfg[option] = conf.get(section, option)

socket = urllib2.urlopen(cfg["test_url_img"])
content = socket.read()
socket.close()

rs = regex.findall(content)[0]
shortcut = rs[1]
urls = map(lambda x : x[2:-1], rs.replace("\\", "").split(","))

codes = regex2.findall(content)[1].split("|")

a = {}

index = string.digits + string.letters

for i, x in enumerate(index):
	try:
		a[x] = codes[i]
	except IndexError:
		pass
	except:
		print "error"


output = []
for x in urls:
	s = ""
	for i, c in enumerate(x):
		if c in index:
			if a[c] != "":
				s += a[c]
			else:
				s += c
		else:
			s += c
	
	output.append(s)


with open("img-analyse-output.txt", "w") as f:
	for x in output:
		f.write(cfg["root_img"]+ shortcut + x + "\n")
