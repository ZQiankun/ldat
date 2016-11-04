#!/usr/bin/env python
#coding=utf-8
#Author : lenovo
#Date: 2015.04.13

#insert Library
__author__  = "LENOVO"
__version__ = "0.1"

from ldtp 	import * 
from ldtputils 	import *
from time	import *
from os 	import *
from logging 	import *
from unittest   import *
import xml.dom.minidom
import commands
import sys


global passwd
#path control
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath) #import file library
#print 'The current directory is: ' + sys.argv[0]
#insert logAPI
from logcase  import Logcase
#for XML parse
#******************************************
from caseobject import CaseObject
from ldtppub import LDTPPub
from screenshot import Screenshot
#******************************************
#global log instance
mylog=Logcase()  
Sshot=Screenshot()
Ldpub = LDTPPub()   
ReList0 = []
ReList1 = []
#*****************************************   
g_tag = '1.3.1.2-xrandr_resolution'
g_currentPath = sys.path[0]
#*****************************************
#Xmd="xrandr -q | sed -n '/[0-9]\{1,\}x[0-9]\{1,\}\s/p' | awk '{print $1}'"
kmd="xrandr -q | awk '{ if( $1 ~ /[0-9]{1,}x[0-9]{1,}/) {print $1}}'"

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


#creat PICS directory
#建立图像文件夹
def checkDir(dirName):
	try:
		if not os.path.exists(dirName):
			mylog.ilog(g_tag,'Beginning to create Pics Directory...' )
			if commands.getstatusoutput('echo %s | sudo -S mkdir ./resource' % passwd)[0] == 0:
				os.system('echo %s | sudo -S mkdir ./result ./screenshot ' % passwd )
				mylog.ilog(g_tag, 'Create ./resource successfully!')
			else:
				mylog.elog(g_tag, 'Create ./resource failed!')
				return
		else:
			if commands.getstatusoutput('echo %s | sudo -S rm -rf ./screenshot/*' % passwd)[0] == 0:
					mylog.ilog(g_tag,'Delete ./screenshot successfully!')
			mylog.ilog(g_tag,'./resouce has existed!' )
	except (NameError,Exception) as e:
		print e
	finally:
		return

def Genlists():
	tList=commands.getstatusoutput(kmd)[1].split('\n')
	tLen = len(tList)
	for i in range(tLen):
		tmpa = (tList[i].split('x'))[0]	
		tmpb = (tList[i].split('x'))[1]
		ReList0.append(tmpa)
		ReList1.append(tmpb)

	print 'Gen list0 is :', ReList0
	print 'Gen list1 is :', ReList1
		
				
	


def setResulotion0():
	for i in range(2):
                for m,n in zip(ReList0,ReList1):
                        Ldpub.setResolution('cos', m, n)
			sleep(5)
                        Sshot.scrprint(g_tag, '%sx%s_Normal '  % (m, n) , './screenshot/')
                        sleep(5)
                        print "Excute S3 automatic....."
			if os.environ['S3_ENABLE'] =='1':
                       		print "Excute S3 automatic....."
                        	os.system('echo %s | sudo -S rtcwake -m mem -s 120' % passwd)
                        	sleep(10)
			else:
				print 'S3 OP is canceled!'
				mylog.wlog(g_tag,'S3 OP is canceled!' )

                        sleep(5)
                        Sshot.scrprint(g_tag, '%sx%s_AfterS3 '  % (m, n) , './screenshot/')
                        sleep(5)
			if os.environ['S4_ENABLE'] =='1':
                       		print "Excute S4 automatic....."
                        	os.system('echo %s | sudo -S rtcwake -m disk -s 120' % passwd)
                        	sleep(10)
			else:
				print 'S4 OP is canceled!'
				mylog.wlog(g_tag,'S4 OP is canceled!' )
                        Sshot.scrprint(g_tag, '%sx%s_AfterS4 '  % (m, n) , './screenshot/')
                        sleep(5)
	return True
	

def setResulotion1():
	for i in range(2):
                for m,n in zip(ReList0,ReList1):
                        Ldpub.setResolution('isoft', m, n)
			sleep(5)
                        Sshot.scrprint(g_tag, '%sx%s_Normal '  % (m, n) , './screenshot/')
			if os.environ['S3_ENABLE'] == '1':
                        	sleep(5)
                        	print "Excute S3 automatic....."
                        	os.system('echo %s | sudo -S rtcwake -m mem -s 120' % passwd)
                        	sleep(5)
                        	Sshot.scrprint(g_tag, '%sx%s_AfterS3 '  % (m, n) , './screenshot/')
                        	sleep(5)
			else:
				mylog.wlog(g_tag, 'S3 Unable')
				print 'S3 operation is cancelled!'
			if os.environ['S4_ENABLE'] =='1':
                       		print "Excute S4 automatic....."
                        	os.system('echo %s | sudo -S rtcwake -m disk -s 120' % passwd)
                        	sleep(10)
			else:
				mylog.wlog(g_tag, 'S4 Unable')
				print 'S4 OP is canceled!'
                        Sshot.scrprint(g_tag, '%sx%s_AfterS4 '  % (m, n) , './screenshot/')
                        sleep(5)
	return True
	

def setResulotion2():
	for i in range(2):
                for m,n in zip(ReList0,ReList1):
                        Ldpub.setResolution('kylin', m, n)
			sleep(5)
                        Sshot.scrprint(g_tag, '%sx%s_Normal '  % (m, n) , './screenshot/')
                        sleep(5)
			if os.environ['S3_ENABLE'] == '1':
                        	print "Excute S3 automatic....."
                        	os.system('echo %s | sudo -S rtcwake -m mem -s 120' % passwd)
                        	sleep(5)
                        	Sshot.scrprint(g_tag, '%sx%s_AfterS3 '  % (m, n) , './screenshot/')
                        	sleep(5)
			else:
				mylog.wlog(g_tag, 'S3 Unable')
				print 'S3 operation is canceled!'
			if os.environ['S4_ENABLE'] =='1':
                       		print "Excute S4 automatic....."
                        	os.system('echo %s | sudo -S rtcwake -m disk -s 120' % passwd)
                        	sleep(10)
			else:
				mylog.wlog(g_tag, 'S3 Unable')
				print 'S4 OP is canceled!'
				
                        Sshot.scrprint(g_tag, '%sx%s_AfterS4 '  % (m, n) , './screenshot/')
                        sleep(5)
	return True
	
	
def main():
	try:
		global passwd
		#************************************************************
		obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
		#调用getOSName 方法 脚本执行环境判断
		#if obj.getOSName() != 'cos':
		#	print 'This OS is not cos!'
        	#	mylog.wlog(g_tag, 'This OS is not cos')
        	#	return
    
		passwd = obj.getPasswd()
		
		#************************************************************
		print 'Your passwd is : ' , passwd
		path = os.path.abspath(os.path.dirname(sys.argv[0]))
		chdir(path) 
		checkDir('./resource/')
		#mylog.ilog(g_tag,'Beginning call vans.sh
		Genlists()
		os_type = obj.getOSName()
		print 'OS type is:', os_type
		if cmp(os_type, 'cos') ==0:
			setgrub()
			setResulotion0()
		elif cmp(os_type, 'isoft') ==0:
			setgrub()
			setResulotion1()
		elif cmp(os_type, 'kylin') ==0:
			setResulotion2()
		else:
			print 'Invilid OS type!'
			sys.exit()
			
		sleep(3)


		print '恢复默认分辨率....'
		os.system('chmod a+x ./resource/set_resolution.sh')
		os.system('sh ./resource/set_resolution.sh')
		#mylog.ilog(g_tag,'Beginning call screen.sh....')
		if ((cmp(os_type, 'cos') ==0) or (cmp(os_type, 'isoft') ==0)):
			resetgrub()


	except (NameError,Exception) as e:
		print e
		#imagecapture(u'frm\u684c\u9762','./screenshot/exception.png')
		mylog.elog(g_tag,'An exception occured.....')
	finally:

		#main exit()
		mylog.ilog(g_tag,'xrandr_resolution.py exit Successfully!')
		exit()

	

if __name__ == '__main__':
	main()




