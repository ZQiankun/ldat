#!/usr/bin/env python
#coding=utf-8
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
import sys
import commands
#path control
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath) #import file library

#insert logAPI
from logcase  import Logcase
from screenshot import Screenshot
#for XML parse
global passwd
#******************************************
from caseobject import CaseObject
#******************************************
#global log instance
mylog=Logcase()   
Sshot=Screenshot()
#*****************************************   
g_tag = '1.3.1.3-xrandr_resolution'
g_currentPath = sys.path[0]
#***************************************** 

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


#建立图像文件夹
def ckDir(dirName):
	try:
		if not os.path.exists(dirName):
			mylog.ilog(g_tag,'Beginning to create Pics Directory...' )
			if commands.getstatusoutput('echo %s | sudo -S mkdir ./resource' % passwd)[0] == 0:
				os.system('echo %s | sudo -S mkdir ./result ./screenshot ' % passwd)
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

def main():
	try:
		global passwd
		#xml parse for passwd
		#************************************************************
		obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	
		passwd = obj.getPasswd()
		os_type = obj.getOSName()
	
		if ((cmp(os_type, 'cos') ==0) or (cmp(os_type, 'isoft') ==0)):
			setgrub()

		path = os.path.abspath(os.path.dirname(sys.argv[0]))
		chdir(path) 

		mylog.ilog(g_tag,'Beginning call resolution_rotate.sh....')
		Sshot.scrprint(g_tag, 'BeforeScreen_sh', './screenshot/')	
		sleep(5)
		system('chmod 777 ./resource/*.sh')
		system('./resource/resolution_rotate.sh')
		Sshot.scrprint(g_tag, 'AfterScreen_sh', './screenshot/')
		mylog.ilog(g_tag,'ending call resolution_rotate.sh....')	
		sleep(5)	

		if os.environ['S3_ENABLE'] == '1': # resolution_s3.sh include rtcwake for S3
			mylog.ilog(g_tag,'Beginning call resolution.sh....')
			Sshot.scrprint(g_tag, 'BeforeResolution-selep_sh', './screenshot/')
			sleep(5)	
			system('echo %s | sudo -S ./resource/resolution_s3.sh' % passwd)
			Sshot.scrprint(g_tag, 'AfterResolution-selep_sh', './screenshot/')
			mylog.ilog(g_tag,'ending call resolution.sh....')
			sleep(5)
		else:
			mylog.wlog(g_tag, 'S3 Unable')
			
		if ((cmp(os_type, 'cos') ==0) or (cmp(os_type, 'isoft') ==0)):
			resetgrub()

	except (NameError,Exception) as e:
		print e
		mylog.elog(g_tag,'An exception occured.....')
	finally:
		#main exit()
		mylog.ilog(g_tag,'xrandr_resolution.py exit Successfully!')
		exit()

	

if __name__ == '__main__':
	main()




