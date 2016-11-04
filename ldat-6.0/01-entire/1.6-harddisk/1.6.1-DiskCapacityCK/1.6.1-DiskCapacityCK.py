#!/usr/bin/env python
#coding=utf-8

#S3_12 小时运行脚本
#素材文件夹:Load_Videos

import threading
import os
import sys
import commands
import xml.dom.minidom
from ldtp      import *
from ldtputils import *
from time import sleep
#path control
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath) 

#导入日志类
from logcase  import Logcase
from caseobject import CaseObject
from screenshot import Screenshot
#global log instance
mylog=Logcase()   
#global screenshot  
Sshot=Screenshot()
#*****************************************   
g_tag = '1.6.1-DiskCapacityCK'
g_currentPath = sys.path[0]
#*****************************************
global passwd
#脚本框架
#调用当前目录下videoPress 目录下的脚本
#此脚本执行可变的时间参数

#检测目录存在函数
def ckDir(dirName):
	try:
		if not os.path.exists(dirName):
			mylog.ilog(g_tag, 'Beginning to creat videoPress DIR!')
			#同时创建两个文件夹
			if commands.getstatusoutput('echo %s | sudo -S mkdir -p ./resource/ ./screenshot/ ./result/ ' % passwd )[0] ==0:
				os.system('echo %s | sudo -S touch ./result/disk.log' % passwd)
				mylog.ilog(g_tag, 'Creating videoPress Successfully!')
			else:
				mylog.ilog(g_tag, 'Creating videoPress Failed!')
				return False
		else:
			mylog.ilog(g_tag, 'dir Name has existed......')
	except (NameError,Exception) as e:
		print e
	finally:
		return True

#调用df 命令显示磁盘容量
def dfDiskCK():
	try:
		mylog.ilog(g_tag, 'call df command to Display The capacity')
		res = commands.getstatusoutput('echo %s | sudo -S df -Th | grep /dev/ > ./result/disk.log' % passwd )[0]
		if res == 0:
			print 'Output the disk capacity information to terminal'
			os.system('echo %s | sudo -S cat ./result/disk.log' % passwd)
			return True
		else:
			return False
	except (NameError,Exception) as e:
		print e
	finally:
		return True


#从控制面板磁盘容量信息
#打开DDC显示窗口
def DiskInfo():
	try:
		os.system('/usr/bin/python /usr/lib/cinnamon-settings/cinnamon-settings.py &')
		sleep(3)
		activatewindow(u'frm系统设置面板')
		if guiexist(u'frm系统设置面板') ==1:
			mousemove(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f', u'btn\u67e5\u770b\u8bbe\u5907')
			click(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f', u'btn\u67e5\u770b\u8bbe\u5907')
			sleep(2)
			if guiexist(u'frm\u8bbe\u5907\u7ba1\u7406\u5668','btn7') ==1:
				mousemove(u'frm\u8bbe\u5907\u7ba1\u7406\u5668','btn7')
				click(u'frm\u8bbe\u5907\u7ba1\u7406\u5668','btn7')
				sleep(2)
				Sshot.scrprint(g_tag, 'Disk_capacity_info01', './screenshot/')	
				sleep(5)
		activatewindow(u'frm\u8bbe\u5907\u7ba1\u7406\u5668')
		if waittillguiexist(u'frm\u8bbe\u5907\u7ba1\u7406\u5668') ==1:
			keypress('<alt>')
			keypress('<f4>')
			keyrelease('<alt>')
			keyrelease('<f4>')
			sleep(2)
		
		activatewindow(u'frm系统设置面板')
		if waittillguiexist(u'frm系统设置面板') ==1:
			keypress('<alt>')
			keypress('<f4>')
			keyrelease('<alt>')
			keyrelease('<f4>')
			sleep(2)

	except Exception as e:
		print e
	finally:
		return True		

	
#主线程函数
def main():
	global passwd
	global time
	print 'resource path = ./resource'
	mylog.ilog(g_tag, 'resource path = ./resource'  )
	#************************************************************
	#for passwd
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	#调用getOSName 方法 脚本执行环境判断
	#if obj.getOSName() != 'cos':
	#	print 'This OS is not cos!'
        #	mylog.wlog(g_tag, 'This OS is not cos')
        #	return	
	#获取密码
	passwd = obj.getPasswd()
	print 'Your passwd is' + passwd
	Path = os.path.abspath(os.path.dirname(sys.argv[0]))
	os.chdir(Path) 
	res = ckDir('./resource/')
	if res == True:
		dfDiskCK()
		#DiskInfo()
	#截屏操作
	sys.exit()	
	
if __name__ == '__main__':
	main()



