#!/usr/bin/env python
#coding=utf-8

#S3_12 小时运行脚本
#素材文件夹:Load_Videos

import threading
import os
import sys
import commands
from difflib import ndiff
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
g_tag = '1.6.2-DiskPowerTest'
g_currentPath = sys.path[0]
#*****************************************
global passwd
global count

Lcmd = " who | head -1 | awk '{print $1}'"

#脚本框架
#调用当前目录下videoPress 目录下的脚本
#此脚本执行可变的时间参数

def setgrub():
	cmd = "echo " + passwd + " | sudo -S chmod a+w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S sed -i s/timeout=-1/timeout=1/g /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S chmod a-w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)

def resetgrub():
	cmd = "echo " + passwd + " | sudo -S chmod a+w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S sed -i s/timeout=1/timeout=-1/g /boot/grub/grub.cfg > /dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo chmod a-w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)

#构建目录结构
def ckDir(dirName):
	try:
		if not os.path.exists(dirName):
			mylog.ilog(g_tag,'Beginning to create Pics Directory...' )
			if commands.getstatusoutput('mkdir ./resource')[0] == 0:
				os.system('mkdir ./result ./screenshot ')
				mylog.ilog(g_tag, 'Create ./resource successfully!')
			else:
				mylog.elog(g_tag, 'Create ./resource failed!')
				return False
		else:
			os.system('echo %s | sudo -S rm -rf ./result/* ./screenshot/*' % passwd)
			mylog.ilog(g_tag,'./resouce has existed!' )
	except (NameError,Exception) as e:
		print e
	finally:
		return True


#执行S3/4 功能
def DisPowerTest(n):
	try:
		os.system('echo %s | sudo -S fdisk -l >> ./result/Disk_Nomal.log' % passwd)
		sleep(3)
		os.system('echo %s | sudo -S chmod 777 ./resource/*.sh' % passwd)
		Sshot.scrprint(g_tag, 'Before_S3_Test%d' % n, './screenshot/')
		sleep(5)

		if os.environ['S3_ENABLE'] =='1':
			os.system('echo %s | sudo -S ./resource/auto_s3.sh %d %s' % (passwd, count, passwd))
		else:
			mylog.wlog(g_tag,'os not s3' )

		Sshot.scrprint(g_tag, 'After_S3_Test%d' % n, './screenshot/')
		sleep(5)
		
		os.system('echo %s | sudo -S sh -c "fdisk -l >> ./result/Disk_AfterS3.log"' % passwd)
		sleep(3)

		Sshot.scrprint(g_tag, 'Before_S4_Test%d' % n, './screenshot/')
		sleep(5)

		if os.environ['S4_ENABLE'] =='1':
			os.system('echo %s | sudo -S ./resource/auto_s4.sh %d %s' % (passwd, count, passwd))
		else:
			print 'S4 OP is canceled!'
			mylog.wlog(g_tag,'os not s4' )

		Sshot.scrprint(g_tag, 'After_S4_Test%d' % n, './screenshot/')
		sleep(5)
		os.system('echo %s | sudo -S sh -c "fdisk -l >> ./result/Disk_AfterS4.log"' % passwd)
		sleep(3)
		
	except Exception as e:
		print e
	finally:
		return 

#磁盘信息对比
def diskCMP():
	try: 
		a = open('./result/Disk_Nomal.log','U').readlines()
		b = open('./result/Disk_AfterS3.log','U').readlines()
		c = open('./result/Disk_AfterS4.log','U').readlines()
		diff1 = ndiff(a, b)
		diff2 = ndiff(a, c)
		sleep(5)
		sys.stdout.writelines(diff1)
		sys.stdout.writelines(diff2)
	except IOError as e:
		print e
	finally:
		return
#主线程函数
def main():
	global passwd
	global count
	print 'resource path = ./resource'
	mylog.ilog(g_tag, 'resource path = ./resource'  )
	#************************************************************
	#for passwd
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	#调用getOSName 方法 脚本执行环境判断
	#if obj.getOSName() != 'cos':
		#print 'This OS is not cos!'
        #	mylog.wlog(g_tag, 'This OS is not cos')
        	#return	
	#获取循环次数
	doc = obj.getDocumentNode()  
    	common = obj.getXMLNode(doc, 'common',0)
  	cNode = obj.getXMLNode(common, 'count', 0)
    	count= obj.getXMLNodeValue(cNode, 0)
	print 'You need do times: ', count
	mylog.ilog(g_tag, 'You need do S3 and S4 %d times each' % count)
	#获取密码
	passwd = obj.getPasswd()
	print 'Your passwd is: ' + passwd
	os_type = obj.getOSName()
	if ((cmp(os_type, 'cos') ==0) or (cmp(os_type, 'isoft') ==0)):
		setgrub()
	Path = os.path.abspath(os.path.dirname(sys.argv[0]))
	os.chdir(Path) 
	os.system('echo %s | sudo -S touch ./result/Disk_Nomal.log' % passwd)
	os.system('echo %s | sudo -S touch ./result/Disk_AfterS3.log' % passwd)
	os.system('echo %s | sudo -S touch ./result/Disk_AfterS4.log' % passwd)
	res = ckDir('./resource/')
	if res == True:
		for i in range(count):
			DisPowerTest(i)
		#diskCMP()
	
	#获取登陆名
	logName = commands.getstatusoutput(Lcmd)[1]	
	os.system('echo %s | sudo -S chown -R %s ./result/*' % (passwd, logName))
	if ((cmp(os_type, 'cos') ==0) or (cmp(os_type, 'isoft') ==0)):
		resetgrub()
	#截屏操作
	sys.exit()	
	
if __name__ == '__main__':
	main()



