#!/usr/bin/env python
#coding:utf-8

def create(pos = [0, 0]):
	def move(direction, step):
		pos[0] = pos[0] + direction[0] * step
		pos[1] = pos[1] + direction[1] * step
		return pos
	return move

s = create()
print s([1, 0], 10)
print s([1, 0], 10)
