#!/usr/bin/env python
#coding:utf-8

import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("conf")

#获取所有区域
conf.sections()

#获取每个区域的属性
for sn in conf.sections():
	print conf.options(sn)

#获取每个区域的属性值
for sn in conf.sections():
	for attr in conf.options(sn):
		print attr, "=", conf.get(sn, attr)
	
f = open("conf2", "w")
conf = ConfigParser.ConfigParser()
#添加区域
conf.add_section("test")
conf.set("test", "run", "false")
conf.set("test", "set", 1)
conf.write(f)
f.close()
