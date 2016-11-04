#!/usr/bin/env python
#coding=utf-8
#general popuse thread class

import threading
from time import ctime

class MyThread(threading.Thread):
	#构造函数
	def __init__(self,func,args,name=''):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
		self.args = args
	#保存函数运行结果
	def getResult(self):
		return self.res	
	def run(self):
		#print 'starting', self.name, 'at:', \
			#ctime()
		self.res = apply(self.func, self.args)
		#print self.name, 'finished at:', \
			#ctime()
			
